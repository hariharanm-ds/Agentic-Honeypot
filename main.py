"""
Agentic Honeypot - Complete Production API
A sophisticated scam detection and engagement system using autonomous agents
"""

from flask import Flask, request, jsonify, Request
from flask_cors import CORS
from datetime import datetime
import uuid
import logging
import re
import random
import threading
import json
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from werkzeug.exceptions import BadRequest, HTTPException
from werkzeug.datastructures import Headers

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = False  # Important: don't propagate, handle gracefully
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================
API_KEY = "test_key_12345"  # Use this for X-API-Key header
MAX_CONVERSATIONS = 1000
CONVERSATION_TIMEOUT_MINUTES = 120

# ============================================================================
# CUSTOM REQUEST HANDLING - Parse JSON safely
# ============================================================================
class SafeRequest(Request):
    """Custom Request class that never throws JSON parsing errors"""
    
    @property
    def json(self):
        """Override to safely get JSON without throwing errors"""
        try:
            if self.is_json:
                return self.get_json(force=False, silent=True)
        except Exception as e:
            logger.warning(f"JSON parse error: {str(e)}")
        return None
    
    def get_json(self, force=False, silent=False, cache=True):
        """Override to never raise BadRequest"""
        try:
            return super().get_json(force=force, silent=True, cache=cache)
        except Exception as e:
            logger.warning(f"JSON parse error in get_json: {str(e)}")
            return None

# Use custom request class
app.request_class = SafeRequest

# ============================================================================
# SCAM DETECTION ENGINE
# ============================================================================
class ScamType(Enum):
    PHISHING_UPI = "phishing_upi"
    PHISHING_BANKING = "phishing_banking"
    LOTTERY_SCAM = "lottery_scam"
    ROMANCE_SCAM = "romance_scam"
    INVESTMENT_FRAUD = "investment_fraud"
    TECH_SUPPORT = "tech_support"
    FAKE_JOB_OFFER = "fake_job_offer"
    PACKAGE_DELIVERY = "package_delivery"
    TAX_GOVERNMENT = "tax_government"
    CRYPTOCURRENCY = "cryptocurrency"
    SOCIAL_ENGINEERING = "social_engineering"
    PRIZE_REWARD = "prize_reward"
    IMPERSONATION = "impersonation"
    BLACKMAIL_EXTORTION = "blackmail_extortion"
    INHERITANCE_MONEY = "inheritance_money"
    UNKNOWN = "unknown"

@dataclass
class ScamDetectionResult:
    is_scam: bool
    scam_type: ScamType
    confidence: float
    detection_method: str
    extracted_keywords: List[str]
    explanation: str
    
    def to_dict(self) -> dict:
        return {
            "is_scam": self.is_scam,
            "scam_type": self.scam_type.value,
            "confidence": round(self.confidence, 3),
            "detection_method": self.detection_method,
            "extracted_keywords": self.extracted_keywords,
            "explanation": self.explanation
        }

class ScamDetectionEngine:
    def __init__(self):
        self.phishing_patterns = [
            # Phishing & Banking
            (r"verify.*upi|upi.*verify|confirm.*upi", "UPI Verification", 0.95),
            (r"verify.*account|confirm.*account|update.*account|verify.*immediately", "Account Compromise", 0.85),
            (r"account.*block|account.*suspended|account.*will.*block|block.*account", "Account Blocked", 0.90),
            (r"urgent.*atm|atm.*card.*block|card.*block.*urgent", "Card Block", 0.90),
            
            # Lottery & Reward
            (r"won.*lottery|congratulations.*won", "Lottery Scam", 0.88),
            (r"won.*prize|claim.*gift|free.*voucher|free.*reward", "Prize/Reward Scam", 0.82),
            
            # Investment & Financial
            (r"double.*money|quick.*profit|guaranteed.*return", "Investment Fraud", 0.85),
            
            # Romance
            (r"meet.*soon|love.*you|feeling.*close", "Romance Scam", 0.80),
            
            # Tech Support
            (r"virus|malware|computer.*infected|click.*fix|detect.*malware", "Tech Support", 0.83),
            (r"microsoft|windows.*update|system.*detected", "Tech Support", 0.80),
            
            # Job Scams
            (r"processing fee|job.*application|hiring.*bonus|high.*paying.*job", "Fake Job Offer", 0.82),
            (r"congratulations.*selected|job.*offer.*confirm", "Fake Job Offer", 0.80),
            
            # Package Delivery
            (r"delivery.*failed|update.*payment|reschedule.*delivery|package.*claim", "Package Delivery", 0.85),
            (r"failed.*delivery|shipping.*info|confirm.*address", "Package Delivery", 0.82),
            
            # Tax & Government
            (r"irs|tax.*return|legal.*action|avoid.*fine", "Tax/Government", 0.87),
            (r"government.*agency|official.*notice|audit", "Tax/Government", 0.84),
            
            # Cryptocurrency
            (r"bitcoin|ethereum|crypto|blockchain|nft.*million|wallet.*address", "Cryptocurrency", 0.84),
            (r"invest.*crypto|get.*free.*nft|limited.*time.*offer", "Cryptocurrency", 0.82),
            
            # Social Engineering
            (r"confirm.*password|verify.*password|security.*verification", "Social Engineering", 0.86),
            (r"calling.*from.*bank|represent.*company", "Social Engineering", 0.80),
            
            # Impersonation
            (r"calling.*on.*behalf|represent|authorized.*agent", "Impersonation", 0.83),
            
            # Blackmail & Extortion
            (r"compromising.*picture|send.*money|i.*have.*photo|post.*everywhere", "Blackmail/Extortion", 0.90),
            (r"unless.*pay|ransom.*demand", "Blackmail/Extortion", 0.88),
            
            # Inheritance & Money Transfer
            (r"inherited.*million|relative.*passed|legacy.*fund", "Inheritance/Money", 0.86),
            (r"bank.*detail|transfer.*money|claim.*inheritance", "Inheritance/Money", 0.82),
        ]
    
    def detect(self, message: str) -> ScamDetectionResult:
        message_lower = message.lower()
        keywords = re.findall(r'\b\w+\b', message_lower)
        max_confidence = 0.0
        detected_type = ScamType.UNKNOWN
        matched_pattern = ""
        
        for pattern, scam_name, confidence in self.phishing_patterns:
            if re.search(pattern, message_lower):
                if confidence > max_confidence:
                    max_confidence = confidence
                    matched_pattern = scam_name
                    
                    # Map scam names to ScamType enum
                    if scam_name == "UPI Verification":
                        detected_type = ScamType.PHISHING_UPI
                    elif scam_name == "Account Compromise":
                        detected_type = ScamType.PHISHING_BANKING
                    elif scam_name == "Account Blocked":
                        detected_type = ScamType.PHISHING_BANKING
                    elif scam_name == "Card Block":
                        detected_type = ScamType.PHISHING_BANKING
                    elif scam_name == "Lottery Scam":
                        detected_type = ScamType.LOTTERY_SCAM
                    elif scam_name == "Prize/Reward Scam":
                        detected_type = ScamType.PRIZE_REWARD
                    elif scam_name == "Investment Fraud":
                        detected_type = ScamType.INVESTMENT_FRAUD
                    elif scam_name == "Romance Scam":
                        detected_type = ScamType.ROMANCE_SCAM
                    elif scam_name == "Tech Support":
                        detected_type = ScamType.TECH_SUPPORT
                    elif scam_name == "Fake Job Offer":
                        detected_type = ScamType.FAKE_JOB_OFFER
                    elif scam_name == "Package Delivery":
                        detected_type = ScamType.PACKAGE_DELIVERY
                    elif scam_name == "Tax/Government":
                        detected_type = ScamType.TAX_GOVERNMENT
                    elif scam_name == "Cryptocurrency":
                        detected_type = ScamType.CRYPTOCURRENCY
                    elif scam_name == "Social Engineering":
                        detected_type = ScamType.SOCIAL_ENGINEERING
                    elif scam_name == "Impersonation":
                        detected_type = ScamType.IMPERSONATION
                    elif scam_name == "Blackmail/Extortion":
                        detected_type = ScamType.BLACKMAIL_EXTORTION
                    elif scam_name == "Inheritance/Money":
                        detected_type = ScamType.INHERITANCE_MONEY
        
        is_scam = max_confidence > 0.5
        
        return ScamDetectionResult(
            is_scam=is_scam,
            scam_type=detected_type,
            confidence=max_confidence,
            detection_method="pattern_matching",
            extracted_keywords=keywords[:5],
            explanation=f"Matched {matched_pattern}" if matched_pattern else "No specific pattern matched"
        )

# ============================================================================
# CONVERSATION ENGINE
# ============================================================================
class StrategyPhase(Enum):
    IDENTIFICATION = "identification"
    BUILD_TRUST = "build_trust"
    EXTRACT_INTELLIGENCE = "extract_intelligence"
    DELAY_PROBE = "delay_probe"
    SAFE_EXIT = "safe_exit"

class ConversationEngine:
    def __init__(self):
        self.templates = {
            StrategyPhase.IDENTIFICATION: [
                "Which bank are you calling from sir?",
                "How did you get my number?",
                "What is your employee ID sir?",
                "I'm worried... is this a scam?",
                "Can you verify your identity please?",
            ],
            StrategyPhase.BUILD_TRUST: [
                "Ok sir, I'll do whatever you say.",
                "Yes sir, I trust you. What should I do?",
                "I'm listening sir, tell me the steps.",
                "But sir, will my money be safe?",
                "Is this risky sir?",
            ],
            StrategyPhase.EXTRACT_INTELLIGENCE: [
                "Which account should I transfer from?",
                "How much money should I send?",
                "What's your account number sir?",
                "Where should I meet you?",
                "Can you give me your phone number?",
            ],
            StrategyPhase.DELAY_PROBE: [
                "Wait sir, let me think about this...",
                "I need to check something first.",
                "Can you hold on for a moment?",
                "My wife is asking questions...",
                "Let me confirm the details once more.",
            ],
            StrategyPhase.SAFE_EXIT: [
                "Thank you for your help sir, I understand now.",
                "I'll proceed with this cautiously.",
                "I appreciate your time sir.",
                "I'll contact my bank as you suggested.",
                "Thank you for the guidance.",
            ]
        }
    
    def generate_response(self, phase: StrategyPhase) -> str:
        templates = self.templates.get(phase, self.templates[StrategyPhase.IDENTIFICATION])
        response = random.choice(templates)
        # Add human-like typos (10% chance per response)
        if random.random() < 0.1:
            words = response.split()
            if words:
                idx = random.randint(0, len(words) - 1)
                words[idx] = words[idx][:-1] if len(words[idx]) > 1 else words[idx]
                response = " ".join(words)
        return response

# ============================================================================
# INTELLIGENCE EXTRACTOR
# ============================================================================
class EntityType(Enum):
    UPI_ID = "upi_ids"
    PHONE_NUMBER = "phone_numbers"
    BANK_ACCOUNT = "bank_accounts"
    PHISHING_LINK = "phishing_links"
    EMAIL_ADDRESS = "email_addresses"

@dataclass
class ExtractedEntity:
    value: str
    type: EntityType
    confidence: float
    context: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "type": self.type.value,
            "confidence": round(self.confidence, 3),
            "context": self.context
        }

class IntelligenceExtractor:
    def __init__(self):
        self.patterns = {
            EntityType.UPI_ID: r'[\w.-]+@[\w.-]+',
            EntityType.PHONE_NUMBER: r'(?:^|\D)([6-9]\d{9})(?:\D|$)',
            EntityType.BANK_ACCOUNT: r'\b(?:\d{4}[\s-]?)?\d{10,14}\b',
            EntityType.PHISHING_LINK: r'https?://[^\s)]+',
            EntityType.EMAIL_ADDRESS: r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        }
    
    def extract(self, message: str) -> Dict[EntityType, List[ExtractedEntity]]:
        results = {entity_type: [] for entity_type in EntityType}
        
        for entity_type, pattern in self.patterns.items():
            matches = re.findall(pattern, message)
            for match in matches:
                results[entity_type].append(
                    ExtractedEntity(
                        value=match,
                        type=entity_type,
                        confidence=0.85,
                        context=message[:100]
                    )
                )
        
        return results

# ============================================================================
# MEMORY STORE
# ============================================================================
@dataclass
class Message:
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    scam_indicators: List[str] = field(default_factory=list)
    extracted_entities: Dict = field(default_factory=dict)

@dataclass
class ConversationState:
    conversation_id: str
    persona_name: str
    scam_detected: bool = False
    scam_type: Optional[str] = None
    current_phase: str = "identification"
    trust_level: float = 0.0

class MemoryStore:
    def __init__(self, conversation_id: str, persona_name: str):
        self.conversation_id = conversation_id
        self.persona_name = persona_name
        self.created_at = datetime.now()
        self.message_history: List[Message] = []
        self.state = ConversationState(
            conversation_id=conversation_id,
            persona_name=persona_name
        )
        self.extracted_intelligence = defaultdict(list)
    
    def add_message(self, role: str, content: str, scam_indicators=None, extracted_entities=None):
        msg = Message(
            role=role,
            content=content,
            scam_indicators=scam_indicators or [],
            extracted_entities=extracted_entities or {}
        )
        self.message_history.append(msg)
    
    def update_phase(self, phase: str):
        self.state.current_phase = phase
    
    def add_intelligence(self, entity_type: str, value: str, confidence: float):
        self.extracted_intelligence[entity_type].append({
            "value": value,
            "confidence": confidence
        })
    
    def get_summary(self) -> dict:
        return {
            "conversation_id": self.conversation_id,
            "persona_name": self.persona_name,
            "message_count": len(self.message_history),
            "scam_detected": self.state.scam_detected,
            "scam_type": self.state.scam_type,
            "current_phase": self.state.current_phase,
            "trust_level": round(self.state.trust_level, 2),
            "intelligence_extracted": dict(self.extracted_intelligence),
            "created_at": self.created_at.isoformat()
        }

class MemoryManager:
    def __init__(self):
        self.conversations = {}
        self.lock = threading.Lock()
    
    def create_conversation(self, conversation_id: str, persona_name: str) -> MemoryStore:
        with self.lock:
            if conversation_id in self.conversations:
                return self.conversations[conversation_id]
            
            store = MemoryStore(conversation_id, persona_name)
            self.conversations[conversation_id] = store
            return store
    
    def get_conversation(self, conversation_id: str) -> Optional[MemoryStore]:
        with self.lock:
            return self.conversations.get(conversation_id)
    
    def get_active_count(self) -> int:
        with self.lock:
            return len(self.conversations)

# ============================================================================
# AGENT CONTROLLER
# ============================================================================
@dataclass
class AgentDecision:
    strategy_phase: StrategyPhase
    action_type: str
    confidence: float
    reasoning: str

class AgentController:
    def __init__(self, memory: MemoryStore):
        self.memory = memory
    
    def decide_phase(self, turn_count: int, scam_confidence: float) -> StrategyPhase:
        # Phase transitions based on turn count
        if turn_count <= 3:
            return StrategyPhase.IDENTIFICATION
        elif turn_count <= 8:
            return StrategyPhase.BUILD_TRUST
        elif turn_count <= 15:
            return StrategyPhase.EXTRACT_INTELLIGENCE
        elif turn_count <= 25:
            return StrategyPhase.DELAY_PROBE
        else:
            return StrategyPhase.SAFE_EXIT
    
    def decide_strategy(self, message: str, scam_confidence: float) -> AgentDecision:
        turn_count = len(self.memory.message_history)
        phase = self.decide_phase(turn_count, scam_confidence)
        
        return AgentDecision(
            strategy_phase=phase,
            action_type="respond",
            confidence=0.85,
            reasoning=f"Turn {turn_count}, scam confidence: {scam_confidence:.2f}"
        )

# ============================================================================
# INITIALIZATION
# ============================================================================
scam_detector = ScamDetectionEngine()
conversation_engine = ConversationEngine()
intelligence_extractor = IntelligenceExtractor()
memory_manager = MemoryManager()

# ============================================================================
# REQUEST HANDLERS - MUST BE BEFORE ROUTES
# ============================================================================

@app.before_request
def handle_preflight():
    """Handle CORS preflight only"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,HEAD,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-API-Key,Authorization'
        }

def require_api_key(f):
    """Decorator to require API key"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Unauthorized", "message": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# API ENDPOINTS
# ============================================================================
# SCAM DETECTION ENDPOINT - Matches Tester Format
# ============================================================================

@app.route('/api/v1/scam-detection', methods=['POST'])
@require_api_key
def scam_detection():
    """
    Scam detection endpoint - matches tester request format
    
    Expected request:
    {
        "sessionId": "string",
        "message": {
            "sender": "string",
            "text": "string",
            "timestamp": number
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "string",
            "language": "string",
            "locale": "string"
        }
    }
    """
    try:
        data = request.get_json(force=False, silent=True)
        
        if not data:
            return jsonify({
                "status": "error",
                "reply": "No request data provided"
            }), 400
        
        # Extract message text
        message_obj = data.get('message', {})
        if isinstance(message_obj, dict):
            message_text = message_obj.get('text', '')
        else:
            message_text = str(message_obj)
        
        if not message_text:
            return jsonify({
                "status": "error", 
                "reply": "No message text provided"
            }), 400
        
        # Detect scam
        detection_result = scam_detector.detect(message_text)
        
        # Generate appropriate reply
        if detection_result.is_scam:
            # For scams, generate a response that appears to be from the victim
            reply = generate_victim_response(message_text, detection_result.scam_type)
        else:
            reply = "I need more information to help you."
        
        return jsonify({
            "status": "success",
            "reply": reply
        }), 200
    
    except Exception as e:
        logger.error(f"Error in scam_detection: {str(e)}")
        return jsonify({
            "status": "error",
            "reply": f"Internal server error"
        }), 500

def generate_victim_response(message: str, scam_type) -> str:
    """Generate a victim response to the scammer's message"""
    # Map scam types to realistic victim responses
    responses = {
        "phishing_upi": "Why is my account being suspended?",
        "phishing_banking": "Why is my account being suspended?",
        "phishing_credentials": "What do you mean verify my account?",
        "lottery_scam": "I never entered any lottery.",
        "romance_scam": "When can I meet you?",
        "investment_fraud": "Can you explain this investment opportunity more clearly?",
        "tax_fraud": "I don't owe any taxes.",
        "tech_support_scam": "How did you get my number?",
        "unknown": "I'm confused. Can you explain?"
    }
    
    # Get the scam type value
    scam_name = scam_type.value if hasattr(scam_type, 'value') else str(scam_type)
    return responses.get(scam_name, "Why is my account being suspended?")

# ============================================================================

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def root():
    """Root health check - accepts GET, POST, HEAD - returns 200 OK with JSON"""
    return jsonify({
        "status": "ok",
        "service": "agentic-honeypot",
        "version": "1.0"
    }), 200

# ============================================================================
# ERROR HANDLERS - Catch ALL errors and return valid JSON
# ============================================================================

@app.errorhandler(400)
def handle_400(e):
    """Handle 400 Bad Request"""
    return jsonify({
        "error": "Bad Request",
        "message": "The request could not be processed"
    }), 400

@app.errorhandler(401)
def handle_401(e):
    """Handle 401 Unauthorized"""
    return jsonify({
        "error": "Unauthorized",
        "message": "Invalid or missing authentication"
    }), 401

@app.errorhandler(404)
def handle_404(e):
    """Handle 404 Not Found"""
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(405)
def handle_405(e):
    """Handle 405 Method Not Allowed - convert to 200 for root endpoint"""
    if request.path == '/':
        return jsonify({
            "status": "ok",
            "service": "agentic-honeypot",
            "version": "1.0"
        }), 200
    return jsonify({
        "error": "Method Not Allowed",
        "message": f"The {request.method} method is not allowed for this endpoint"
    }), 405

@app.errorhandler(500)
def handle_500(e):
    """Handle 500 Internal Server Error"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Catch ALL unhandled exceptions and return valid JSON"""
    logger.error(f"Unhandled exception: {type(e).__name__}: {str(e)}")
    
    # If it's an HTTP exception, use its status code
    if isinstance(e, HTTPException):
        return jsonify({
            "error": e.name,
            "message": e.description
        }), e.code
    
    # For all other exceptions, return 500
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_conversations": memory_manager.get_active_count(),
        "api_version": "1.0"
    })

@app.route('/api/v1/detect-scam', methods=['POST'])
@require_api_key
def detect_scam():
    """Detect if message is a scam"""
    try:
        data = request.get_json(force=False, silent=True)
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing required field: message"}), 400
        
        message = data['message']
        result = scam_detector.detect(message)
        
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "detection": result.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"Error in detect_scam: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/conversation', methods=['POST'])
@require_api_key
def create_conversation():
    """Create new conversation"""
    try:
        data = request.get_json(force=False, silent=True) or {}
        persona_name = data.get('persona_name', 'victim_001')
        
        conversation_id = str(uuid.uuid4())
        memory = memory_manager.create_conversation(conversation_id, persona_name)
        
        return jsonify({
            "conversation_id": conversation_id,
            "persona_name": persona_name,
            "timestamp": datetime.now().isoformat()
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/conversation/<conversation_id>/message', methods=['POST'])
@require_api_key
def process_message(conversation_id):
    """Process scammer message and get agent response"""
    try:
        data = request.get_json(force=False, silent=True)

        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing required field: message"}), 400
        
        message = data['message']
        memory = memory_manager.get_conversation(conversation_id)
        
        if not memory:
            return jsonify({"error": "Conversation not found"}), 404
        
        # Detect scam
        detection_result = scam_detector.detect(message)
        memory.state.scam_detected = detection_result.is_scam
        memory.state.scam_type = detection_result.scam_type.value
        
        # Extract intelligence
        extracted = intelligence_extractor.extract(message)
        
        # Add message to memory
        memory.add_message(
            role='scammer',
            content=message,
            scam_indicators=detection_result.extracted_keywords,
            extracted_entities={k.value: [e.to_dict() for e in v] for k, v in extracted.items()}
        )
        
        # Store extracted intelligence
        for entity_type, entities in extracted.items():
            for entity in entities:
                memory.add_intelligence(entity_type.value, entity.value, entity.confidence)
        
        # Agent decides strategy
        agent = AgentController(memory)
        decision = agent.decide_strategy(message, detection_result.confidence)
        memory.update_phase(decision.strategy_phase.value)
        
        # Generate response
        response = conversation_engine.generate_response(decision.strategy_phase)
        memory.add_message(role='victim', content=response)
        
        # Calculate response delay (random between 1-5 seconds)
        delay_ms = random.randint(1000, 5000)
        
        return jsonify({
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "scam_detection": detection_result.to_dict(),
            "agent_response": {
                "reply": response,
                "strategy_phase": decision.strategy_phase.value,
                "confidence": round(decision.confidence, 2),
                "reasoning": decision.reasoning,
                "behavioral_cues": {
                    "response_delay_ms": delay_ms,
                    "typing_indicators": True
                }
            },
            "intelligence_extracted": {k.value: [e.to_dict() for e in v] for k, v in extracted.items()},
            "memory_state": memory.get_summary()
        }), 200
    
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/conversation/<conversation_id>', methods=['GET'])
@require_api_key
def get_conversation(conversation_id):
    """Get conversation state"""
    try:
        memory = memory_manager.get_conversation(conversation_id)
        
        if not memory:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify(memory.get_summary()), 200
    
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
