"""
API Interface - Flask REST API for Honeypot System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import logging
from functools import wraps

from src.scam_detector import ScamDetectionEngine, ScamType
from src.persona import get_persona
from src.conversation_engine import ConversationEngine
from src.agent_controller import AgentController
from src.memory_store import MemoryManager
from src.intelligence_extractor import IntelligenceExtractor

# Initialize components
app = Flask(__name__)
CORS(app)

# Configuration
from configs.config import get_config
config = get_config()

# Initialize global services
scam_detector = ScamDetectionEngine()
memory_manager = MemoryManager()
intelligence_extractor = IntelligenceExtractor()

# Logging
logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def require_api_key(f):
    """Decorator to require API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key not in config.API_KEYS:
            return jsonify({"error": "Unauthorized"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def require_ip_whitelist(f):
    """Decorator to check IP whitelist"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        
        if client_ip not in config.AUTHORIZED_IPS and "*" not in config.AUTHORIZED_IPS:
            return jsonify({"error": "IP not authorized"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_conversations": memory_manager.get_active_count()
    })

@app.route('/api/v1/detect-scam', methods=['POST'])
@require_api_key
@require_ip_whitelist
def detect_scam():
    """
    Detect if message is a scam
    
    Request JSON:
    {
        "message": "string",
        "sender_role": "scammer|victim",
        "conversation_id": "string (optional)"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        message = data['message']
        sender_role = data.get('sender_role', 'scammer')
        
        # Detect scam
        result = scam_detector.detect(message)
        
        logger.info(f"Scam detection: {result.scam_type.value} (confidence: {result.confidence})")
        
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "detection": result.to_dict()
        })
    
    except Exception as e:
        logger.error(f"Error in detect_scam: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/conversation', methods=['POST'])
@require_api_key
@require_ip_whitelist
def create_conversation():
    """
    Create new conversation
    
    Request JSON:
    {
        "persona_name": "rajesh_kumar|priya_sharma|arjun_nair"
    }
    """
    try:
        data = request.get_json() or {}
        persona_name = data.get('persona_name', 'rajesh_kumar')
        
        # Generate conversation ID
        conversation_id = str(uuid.uuid4())
        
        # Create memory store
        memory = memory_manager.create_conversation(conversation_id, persona_name)
        
        # Get persona
        persona_engine = get_persona(persona_name)
        
        logger.info(f"Created conversation {conversation_id} with persona {persona_name}")
        
        return jsonify({
            "conversation_id": conversation_id,
            "persona": persona_engine.get_persona_info(),
            "timestamp": datetime.now().isoformat()
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/conversation/<conversation_id>/message', methods=['POST'])
@require_api_key
@require_ip_whitelist
def process_message(conversation_id):
    """
    Process scammer message and get agent response
    
    Request JSON:
    {
        "message": "string",
        "sender_role": "scammer"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing message"}), 400
        
        message = data['message']
        
        # Get conversation memory
        memory = memory_manager.get_conversation(conversation_id)
        if not memory:
            return jsonify({"error": "Conversation not found"}), 404
        
        # Get persona
        persona_engine = get_persona(memory.persona_name)
        
        # Detect scam
        detection_result = scam_detector.detect(message)
        memory.update_state(
            scam_detected=detection_result.is_scam,
            scam_type=detection_result.scam_type.value
        )
        
        # Extract intelligence
        extracted = intelligence_extractor.extract(
            message,
            [m.content for m in memory.message_history]
        )
        
        # Add to memory
        memory.add_message(
            role='scammer',
            content=message,
            scam_indicators=detection_result.extracted_keywords,
            extracted_entities={k.value: [e.to_dict() for e in v] for k, v in extracted.items()}
        )
        
        # Extract intelligence and store
        for entity_type, entities in extracted.items():
            for entity in entities:
                memory.add_extracted_intelligence(
                    entity_type.value,
                    entity.value,
                    entity.confidence,
                    entity.metadata
                )
        
        # Agent decides strategy
        agent = AgentController(memory)
        decision = agent.decide_strategy(
            message,
            detection_result.to_dict(),
            {k.value: [e.to_dict() for e in v] for k, v in extracted.items()}
        )
        
        # Generate response
        conv_engine = ConversationEngine(persona_engine)
        response = conv_engine.generate_response(
            message,
            decision.strategy_phase,
            memory.get_memory_summary(),
            []
        )
        
        # Add victim response to memory
        memory.add_message(
            role='victim',
            content=response
        )
        
        # Calculate response delay
        delay_ms = int(persona_engine.calculate_response_delay() * 1000)
        
        logger.info(f"Processed message for conversation {conversation_id}")
        
        return jsonify({
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "scam_detection": detection_result.to_dict(),
            "agent_response": {
                "reply": response,
                "strategy_phase": decision.strategy_phase.value,
                "confidence": decision.confidence,
                "reasoning": decision.reasoning,
                "behavioral_cues": {
                    "response_delay_ms": delay_ms,
                    "emotional_tone": persona_engine.persona.emotional_state.value,
                    "typing_indicators": True
                }
            },
            "intelligence_extracted": {k.value: [e.to_dict() for e in v] for k, v in extracted.items()},
            "memory_state": memory.get_memory_summary()
        })
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/conversation/<conversation_id>', methods=['GET'])
@require_api_key
def get_conversation(conversation_id):
    """Get conversation details"""
    try:
        memory = memory_manager.get_conversation(conversation_id)
        if not memory:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify({
            "conversation_id": conversation_id,
            "summary": memory.get_memory_summary(),
            "extracted_intelligence": memory.extracted_intelligence,
            "behavior_patterns": memory.behavior_patterns
        })
    
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/conversation/<conversation_id>/export', methods=['GET'])
@require_api_key
def export_conversation(conversation_id):
    """Export full conversation"""
    try:
        memory = memory_manager.get_conversation(conversation_id)
        if not memory:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify(memory.export_to_dict())
    
    except Exception as e:
        logger.error(f"Error exporting conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/conversation/<conversation_id>', methods=['DELETE'])
@require_api_key
def delete_conversation(conversation_id):
    """Delete conversation"""
    try:
        memory_manager.delete_conversation(conversation_id)
        logger.info(f"Deleted conversation {conversation_id}")
        return jsonify({"status": "deleted"})
    
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/statistics', methods=['GET'])
@require_api_key
def get_statistics():
    """Get system statistics"""
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "active_conversations": memory_manager.get_active_count(),
        "api_version": "v1"
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info(f"Starting Honeypot API on {config.API_HOST}:{config.API_PORT}")
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=False,
        use_reloader=False
    )
