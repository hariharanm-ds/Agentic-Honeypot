"""
API Interface - Complete Production-Ready Honeypot API
Handles scam detection, agent engagement, intelligence extraction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
import logging
import time
import json
from functools import wraps
import traceback

from src.scam_detector import ScamDetectionEngine, ScamType
from src.agent_controller import AgentController, StrategyPhase
from src.persona import get_persona
from src.conversation_engine import ConversationEngine
from src.memory_store import MemoryManager, MemoryStore
from src.intelligence_extractor import IntelligenceExtractor
from configs.config import get_config

# Initialize Flask app
app = Flask(__name__)
CORS(app)
config = get_config()

# Initialize logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
scam_detector = ScamDetectionEngine()
memory_manager = MemoryManager()
intelligence_extractor = IntelligenceExtractor()
agent_controllers = {}  # conversation_id -> AgentController

# ============================================================================
# MIDDLEWARE & DECORATORS
# ============================================================================

def require_api_key(f):
    """Decorator to verify API key"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key not in config.API_KEYS:
            return jsonify({
                "success": False,
                "error": "Unauthorized",
                "error_code": "AUTH_001",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }), 401
        
        return f(*args, **kwargs)
    return decorated

def get_or_create_agent(conversation_id: str) -> AgentController:
    """Get or create agent for conversation"""
    if conversation_id not in agent_controllers:
        memory_store = memory_manager.get_or_create(conversation_id)
        agent_controllers[conversation_id] = AgentController(memory_store)
    return agent_controllers[conversation_id]

# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            "success": True,
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "agentic-honeypot",
            "version": "1.0.0",
            "active_conversations": memory_manager.get_active_count()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/api/v1/status', methods=['GET'])
@require_api_key
def get_status():
    """Get system status"""
    return jsonify({
        "success": True,
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metrics": {
            "active_conversations": memory_manager.get_active_count(),
            "scam_detections_today": memory_manager.get_scam_count_today(),
            "total_intelligence_extracted": memory_manager.get_total_intelligence_count()
        }
    }), 200

# ============================================================================
# MAIN ENGAGEMENT ENDPOINT
# ============================================================================

@app.route('/api/v1/engage-scammer', methods=['POST'])
@require_api_key
def engage_scammer():
    """
    Main honeypot engagement endpoint.
    
    Detects scam, engages agent, extracts intelligence.
    
    Request JSON:
    {
        "conversation_id": "string",
        "message": "string",
        "sender_role": "scammer|victim",
        "timestamp": "ISO8601 (optional)",
        "metadata": {object (optional)}
    }
    
    Response: Strict JSON with scam detection, agent response, and intelligence
    """
    request_start_time = time.time()
    
    try:
        # ===== STEP 1: VALIDATE INPUT =====
        data = request.get_json()
        
        if not data:
            return make_error_response(
                "Invalid JSON in request body",
                "PARSE_001",
                400
            )
        
        # Validate required fields
        if 'message' not in data:
            return make_error_response(
                "Missing required field: message",
                "VALIDATION_001",
                400
            )
        
        if 'conversation_id' not in data:
            return make_error_response(
                "Missing required field: conversation_id",
                "VALIDATION_002",
                400
            )
        
        message = str(data['message']).strip()
        conversation_id = str(data['conversation_id']).strip()
        sender_role = str(data.get('sender_role', 'scammer')).strip()
        
        # Validate message length
        if not message or len(message) > 5000:
            return make_error_response(
                "Message must be 1-5000 characters",
                "VALIDATION_003",
                400
            )
        
        if not conversation_id or len(conversation_id) > 100:
            return make_error_response(
                "Conversation ID must be 1-100 characters",
                "VALIDATION_004",
                400
            )
        
        # ===== STEP 2: GET OR CREATE CONVERSATION =====
        conv_memory = memory_manager.get_or_create(conversation_id)
        
        # ===== STEP 3: DETECT SCAM (FAST PATH) =====
        detection_result = scam_detector.detect(message)
        
        # Update memory with detection
        conv_memory.current_state.scam_detected = detection_result.is_scam
        if detection_result.is_scam:
            conv_memory.current_state.scam_type = detection_result.scam_type.value
        
        # ===== STEP 4: EXTRACT INTELLIGENCE =====
        extracted_entities = intelligence_extractor.extract(
            message,
            [m.content for m in conv_memory.message_history]
        )
        
        # ===== STEP 5: GENERATE AGENT RESPONSE =====
        if not detection_result.is_scam:
            # Non-scam: generic response
            agent_response = "I don't think that applies to me."
            strategy_phase = "identification"
        else:
            # Get agent and generate response
            agent = get_or_create_agent(conversation_id)
            
            agent_response = agent.generate_response(
                message=message,
                detection_confidence=detection_result.confidence,
                conversation_history=conv_memory.message_history,
                strategy_phase=agent.get_current_phase(len(conv_memory.message_history))
            )
            
            strategy_phase = agent.get_current_phase(len(conv_memory.message_history)).value
            conv_memory.current_state.current_strategy = strategy_phase
        
        # ===== STEP 6: UPDATE MEMORY =====
        conv_memory.add_message(
            role='scammer',
            content=message,
            scam_indicators=detection_result.extracted_keywords,
            extracted_entities={
                k.value: [e.to_dict() for e in v] 
                for k, v in extracted_entities.items()
            }
        )
        
        conv_memory.add_message(
            role='victim',
            content=agent_response
        )
        
        # ===== STEP 7: CHECK TERMINATION CRITERIA =====
        should_terminate, termination_reason = should_terminate_conversation(conv_memory)
        
        # ===== STEP 8: CALCULATE METRICS =====
        turn_count = len(conv_memory.message_history) // 2
        elapsed_seconds = time.time() - conv_memory.created_at.timestamp()
        engagement_score = calculate_engagement_score(conv_memory)
        
        # ===== STEP 9: BUILD RESPONSE =====
        response = {
            "success": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "conversation_id": conversation_id,
            "scam_detection": {
                "is_scam": detection_result.is_scam,
                "scam_type": detection_result.scam_type.value,
                "confidence": round(detection_result.confidence, 3),
                "detection_method": detection_result.detection_method
            },
            "engagement": {
                "strategy_phase": strategy_phase,
                "turn_number": turn_count,
                "engagement_score": round(engagement_score, 3),
                "should_terminate": should_terminate,
                "termination_reason": termination_reason
            },
            "agent_response": agent_response,
            "extracted_intelligence": {
                "upi_ids": [e.to_dict() for e in extracted_entities.get("upi_ids", [])],
                "phone_numbers": [e.to_dict() for e in extracted_entities.get("phone_numbers", [])],
                "bank_accounts": [e.to_dict() for e in extracted_entities.get("bank_accounts", [])],
                "phishing_links": [e.to_dict() for e in extracted_entities.get("phishing_links", [])],
                "email_addresses": [e.to_dict() for e in extracted_entities.get("email_addresses", [])]
            },
            "conversation_metrics": {
                "total_turns": turn_count,
                "elapsed_seconds": round(elapsed_seconds, 3),
                "honeypot_exposure_risk": round(conv_memory.current_state.honeypot_exposure_risk, 3)
            },
            "performance": {
                "response_time_ms": round((time.time() - request_start_time) * 1000, 2)
            }
        }
        
        # ===== STEP 10: LOG ENGAGEMENT =====
        logger.info(f"Engagement complete: {conversation_id} | "
                   f"Scam: {detection_result.is_scam} | "
                   f"Turns: {turn_count} | "
                   f"Confidence: {detection_result.confidence:.2f} | "
                   f"ResponseTime: {response['performance']['response_time_ms']}ms")
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in engage_scammer: {str(e)}\n{traceback.format_exc()}")
        return make_error_response(
            "Internal server error",
            "SERVER_001",
            500
        )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def make_error_response(message: str, error_code: str, status_code: int) -> tuple:
    """Create standardized error response"""
    return jsonify({
        "success": False,
        "error": message,
        "error_code": error_code,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), status_code

def should_terminate_conversation(conv_memory: MemoryStore) -> tuple:
    """
    Determine if conversation should terminate.
    
    Returns:
        (should_terminate: bool, reason: str or None)
    """
    turn_count = len(conv_memory.message_history) // 2
    
    # Check max turns
    if turn_count >= config.MAX_CONVERSATION_TURNS:
        return True, f"Maximum conversation turns ({config.MAX_CONVERSATION_TURNS}) reached"
    
    # Check timeout
    elapsed_minutes = (datetime.now() - conv_memory.created_at).total_seconds() / 60
    if elapsed_minutes >= config.CONVERSATION_TIMEOUT_MINUTES:
        return True, f"Conversation timeout ({config.CONVERSATION_TIMEOUT_MINUTES} minutes)"
    
    # Check honeypot exposure risk
    if conv_memory.current_state.honeypot_exposure_risk > config.HONEYPOT_EXPOSURE_THRESHOLD:
        return True, "Honeypot exposure risk too high"
    
    return False, None

def calculate_engagement_score(conv_memory: MemoryStore) -> float:
    """
    Calculate engagement score based on conversation depth.
    
    Scoring:
    - Turn count (0-50): 40%
    - Strategy phase reached: 30%
    - Intelligence extracted: 20%
    - Conversation coherence: 10%
    
    Returns: float 0-1
    """
    turn_count = len(conv_memory.message_history) // 2
    
    # Turn count score (0-1)
    turn_score = min(turn_count / 50.0, 1.0) * 0.4
    
    # Phase score (0-1)
    phase_values = {
        "identification": 0.2,
        "build_trust": 0.5,
        "extract_intelligence": 0.75,
        "delay_probe": 0.9,
        "safe_exit": 1.0
    }
    current_phase = conv_memory.current_state.current_strategy
    phase_score = phase_values.get(current_phase, 0.0) * 0.3
    
    # Intelligence score (0-1)
    total_extracted = sum(len(v) for v in conv_memory.extracted_intelligence.values())
    intelligence_score = min(total_extracted / 5.0, 1.0) * 0.2
    
    # Coherence score (assume high if not terminated early)
    coherence_score = 0.1
    
    total_score = turn_score + phase_score + intelligence_score + coherence_score
    return min(total_score, 1.0)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "error_code": "NOT_FOUND",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500"""
    logger.error(f"Unhandled server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "error_code": "SERVER_ERROR",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 500

# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.before_request
def before_request():
    """Before each request"""
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """After each request"""
    if hasattr(request, 'start_time'):
        elapsed = time.time() - request.start_time
        response.headers['X-Response-Time'] = f"{elapsed:.3f}s"
    return response

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    logger.info(f"Starting Agentic Honeypot API")
    logger.info(f"Host: {config.API_HOST}, Port: {config.API_PORT}, Debug: {config.DEBUG}")
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG,
        use_reloader=config.USE_RELOADER
    )
