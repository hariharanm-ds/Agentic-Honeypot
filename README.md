# 🍯 Agentic AI Honeypot System - Complete Implementation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Flask

### Installation

```bash
# Clone/setup project
cd "e:\Agentic Honeypot"

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (first time only)
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

### Running the API

```bash
# Development mode
python -m src.api

# Production mode
gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
```

The API will be available at `http://localhost:5000`

---

## 📋 Project Structure

```
Agentic Honeypot/
├── ARCHITECTURE.md          # Complete system design documentation
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
│
├── src/
│   ├── __init__.py
│   ├── api.py              # Flask REST API
│   ├── scam_detector.py    # Scam detection engine
│   ├── persona.py          # Persona engine
│   ├── conversation_engine.py  # Multi-turn conversations
│   ├── agent_controller.py # Autonomous decision-making
│   ├── memory_store.py     # Conversation memory
│   └── intelligence_extractor.py  # Entity extraction
│
├── configs/
│   └── config.py           # Configuration management
│
├── tests/
│   ├── test_scam_detector.py
│   ├── test_persona.py
│   ├── test_agent.py
│   └── test_api.py
│
├── data/
│   └── sample_conversations/  # Test conversations
│
└── docs/
    ├── API_REFERENCE.md    # API documentation
    └── DEPLOYMENT.md       # Deployment guide
```

---

## 🔌 API Usage

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Create Conversation
```bash
curl -X POST http://localhost:5000/api/v1/conversation \
  -H "X-API-Key: test_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "persona_name": "rajesh_kumar"
  }'
```

Response:
```json
{
  "conversation_id": "abc-def-123",
  "persona": {
    "name": "Rajesh Kumar",
    "age": 58,
    "location": "Bangalore",
    "technical_level": "very_low",
    "vulnerability_factors": ["isolation", "trusts_authority"]
  },
  "timestamp": "2026-02-03T10:30:00Z"
}
```

### 3. Process Scammer Message
```bash
curl -X POST http://localhost:5000/api/v1/conversation/abc-def-123/message \
  -H "X-API-Key: test_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, this is Bank Security. Your account is compromised. Verify your UPI immediately.",
    "sender_role": "scammer"
  }'
```

Response:
```json
{
  "conversation_id": "abc-def-123",
  "timestamp": "2026-02-03T10:32:00Z",
  "scam_detection": {
    "is_scam": true,
    "scam_type": "phishing_upi",
    "confidence": 0.94,
    "detection_method": "pattern_matching + nlp",
    "extracted_keywords": ["verify", "urgent", "account"],
    "explanation": "UPI verification request with urgency markers"
  },
  "agent_response": {
    "reply": "Oh God! Really sir? Which bank you are from? I have 4 bank accounts.",
    "strategy_phase": "identification",
    "confidence": 0.85,
    "reasoning": "Need to confirm scam script consistency",
    "behavioral_cues": {
      "response_delay_ms": 3500,
      "emotional_tone": "fearful_confused",
      "typing_indicators": true
    }
  },
  "intelligence_extracted": {
    "upi_ids": [],
    "phone_numbers": [],
    "bank_accounts": [],
    "phishing_links": [],
    "email_addresses": []
  },
  "memory_state": {
    "conversation_turn": 1,
    "message_count": 1,
    "entities_tracked": {},
    "strategy_progression": ["identification"]
  }
}
```

### 4. Get Conversation Details
```bash
curl http://localhost:5000/api/v1/conversation/abc-def-123 \
  -H "X-API-Key: test_key_12345"
```

### 5. Export Full Conversation
```bash
curl http://localhost:5000/api/v1/conversation/abc-def-123/export \
  -H "X-API-Key: test_key_12345" > conversation.json
```

---

## 🧠 System Components

### 1. **Scam Detection Engine** (`scam_detector.py`)
- Pattern-based detection (regex patterns)
- NLP-based classification (sentiment analysis)
- Keyword-weighted scoring
- Confidence calibration

**Key Methods:**
- `detect(message)` - Detect if message is scam
- `_calculate_pattern_score()` - Pattern matching
- `_calculate_nlp_score()` - NLP analysis
- `_classify_scam_type()` - Classify scam type

### 2. **Persona Engine** (`persona.py`)
- Realistic human persona simulation
- Language style injection (Hindi-English mix, broken English, etc.)
- Emotional state management
- Behavioral quirks and mistakes

**Pre-defined Personas:**
- **Rajesh Kumar** (58, retired bank manager, very low tech)
- **Priya Sharma** (32, homemaker, low tech)
- **Arjun Nair** (45, business owner, low tech)

**Key Methods:**
- `inject_language_style(text)` - Apply persona language
- `inject_mistakes(text)` - Add typos/errors
- `calculate_response_delay()` - Realistic delays
- `update_emotional_state()` - Update emotions based on interaction

### 3. **Agent Controller** (`agent_controller.py`)
- Autonomous decision-making on strategy
- Phase progression logic
- Safety threshold monitoring
- Response guidance

**Strategy Phases:**
1. **IDENTIFICATION** - Confirm scam and gather initial info
2. **BUILD_TRUST** - Create false victim credibility
3. **EXTRACT_INTELLIGENCE** - Deep probing for details
4. **DELAY_PROBE** - Introduce obstacles; validate consistency
5. **SAFE_EXIT** - Gracefully disengage

**Key Methods:**
- `decide_strategy()` - Make strategy decision
- `_confirm_scam_script()` - Validate scam patterns
- `_check_safety_threshold()` - Ensure safety boundaries
- `get_response_guidance()` - Get tone/approach for phase

### 4. **Conversation Engine** (`conversation_engine.py`)
- Multi-turn conversation management
- Context-aware response generation
- Template-based replies with persona injection
- Conversation coherence maintenance

**Key Methods:**
- `generate_response()` - Generate adaptive reply
- `_generate_identification_response()` - ID phase response
- `_generate_extraction_response()` - Extraction phase response
- `should_ask_followup()` - Determine probing strategy

### 5. **Memory & Context Store** (`memory_store.py`)
- Short-term conversation history (last 20 turns)
- Long-term intelligence repository
- Entity tracking and pattern learning
- Conversation state management

**Key Methods:**
- `add_message()` - Add to conversation history
- `get_recent_messages()` - Retrieve context
- `add_extracted_intelligence()` - Store entities
- `calculate_extraction_score()` - Score extraction quality
- `get_memory_summary()` - Summarize conversation state

### 6. **Intelligence Extractor** (`intelligence_extractor.py`)
- Regex-based entity extraction (UPI, phone, accounts, links)
- Validation and confidence scoring
- Cross-validation against conversation history
- Phishing risk analysis

**Extracted Entities:**
- UPI IDs (`identifier@bank`)
- Phone numbers (10-digit Indian mobile)
- Bank accounts (9-18 digit numbers)
- Phishing links (HTTP/HTTPS URLs)
- Email addresses

**Key Methods:**
- `extract()` - Extract all entities from message
- `_validate_upi()` - UPI validation
- `_validate_phone()` - Phone validation
- `analyze_phishing_risk()` - Assess link risk
- `extract_and_grade()` - Extract with confidence scores

### 7. **REST API** (`api.py`)
- Flask-based HTTP API
- API key authentication
- IP whitelist enforcement
- Comprehensive error handling
- Audit logging

**Endpoints:**
- `GET /health` - Health check
- `POST /api/v1/detect-scam` - Detect single message
- `POST /api/v1/conversation` - Create conversation
- `POST /api/v1/conversation/<id>/message` - Process message
- `GET /api/v1/conversation/<id>` - Get conversation
- `GET /api/v1/conversation/<id>/export` - Export conversation
- `DELETE /api/v1/conversation/<id>` - Delete conversation
- `GET /api/v1/statistics` - System statistics

---

## 🔐 Configuration

Create `.env` file in project root:

```bash
# API Configuration
FLASK_ENV=development
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False

# Security
AUTHORIZED_IPS=127.0.0.1,192.168.1.100
API_KEYS=test_key_12345,production_key_xyz

# Database
DATABASE_URL=sqlite:///honeypot.db

# Redis (optional, for scaling)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Agent Configuration
MAX_CONVERSATION_TURNS=50
CONVERSATION_TIMEOUT_MINUTES=60

# Intelligence Extraction
MIN_ENTITY_CONFIDENCE=0.75
ENABLE_REGEX_EXTRACTION=true
ENABLE_NLP_EXTRACTION=true

# Safety
HONEYPOT_EXPOSURE_THRESHOLD=0.7
ENABLE_SAFETY_CHECKS=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/honeypot.log
```

---

## 🎯 Hackathon Evaluation Criteria

### ✅ What Judges Will Look For

#### 1. **Technical Excellence (40%)**
- [ ] Clean, modular code architecture
- [ ] Well-documented components
- [ ] Robust error handling
- [ ] Efficient resource usage
- [ ] API follows REST standards

#### 2. **Intelligence Extraction (30%)**
- [ ] Accurately identifies UPI IDs (>90% accuracy)
- [ ] Extracts phone numbers with validation
- [ ] Detects phishing links
- [ ] Confidence scores are calibrated (<0.1 error margin)
- [ ] False positive rate < 5%

#### 3. **Agent Sophistication (15%)**
- [ ] Multi-phase conversation strategy
- [ ] Adaptive behavior based on scammer response
- [ ] Realistic persona maintained throughout
- [ ] Memory-driven decision-making
- [ ] Safe exit mechanisms

#### 4. **Real-World Value (10%)**
- [ ] Clear deployment path
- [ ] Actionable intelligence outputs
- [ ] Measurable impact metrics
- [ ] Ethical safeguards documented
- [ ] Law enforcement ready

#### 5. **Presentation (5%)**
- [ ] Clear architecture diagrams
- [ ] Live demo or simulation
- [ ] Vision for future extensions
- [ ] Cost/scalability analysis

### 📊 Success Metrics

**Extraction Quality:**
```
Extraction_Rate = Unique_Entities / Total_Possible × 100%
False_Positive_Rate = Invalid_Entities / All_Extracted × 100%
Confidence_Accuracy = |Predicted_Confidence - Actual| ≤ 0.1
```

**Engagement Quality:**
```
Average_Engagement_Duration > 5 minutes
Trust_Level_Progression: Exponential growth
Strategy_Adaptation_Rate: 3-5 changes per conversation
```

**System Performance:**
```
Response_Latency: 1-5 seconds (realistic)
API_Availability: > 99%
Intelligence_Delivery: < 5 minutes
```

---

## 🚀 Example Test Scenario

```python
# Simulated conversation
scammer: "Hi, your bank account is compromised. Verify your UPI immediately."
agent: "Oh God! Really sir? Which bank you are from? I have 4 bank accounts."

scammer: "HDFC Bank Security. Download this app to verify: https://hdfc-secure.online/verify"
agent: "Ok sir... but I'm in office. Can you explain how my account got hacked?"

scammer: "Send 100 rupees to scammer@paybank to verify your account."
agent: "Sir please explain why I need to send money? Will it be safe?"

[After several turns, system extracts: UPI ID, phishing link, phone number]
[Confidence scores > 0.85 for all entities]
[Agent safely exits maintaining victim persona]
```

---

## 🔧 Development & Testing

### Run Unit Tests
```bash
python -m pytest tests/ -v
```

### Test Individual Components
```python
# Test scam detector
from src.scam_detector import ScamDetectionEngine
detector = ScamDetectionEngine()
result = detector.detect("Verify your UPI urgently")
print(result)

# Test persona
from src.persona import get_persona
persona = get_persona("rajesh_kumar")
response = persona.inject_language_style("I will do it")
print(response)

# Test API
curl -X POST http://localhost:5000/api/v1/detect-scam \
  -H "X-API-Key: test_key_12345" \
  -d '{"message": "verify account urgently"}'
```

---

## 📈 Scaling & Deployment

### For Small Scale (< 100 concurrent conversations)
- Single Flask server
- SQLite database
- Local memory store

### For Medium Scale (100-1000 conversations)
- Load balancer (nginx)
- Multiple Flask workers (4-8)
- PostgreSQL database
- Redis cache layer

### For Production (1000+ conversations)
- Kubernetes cluster
- Message queue (RabbitMQ/Kafka)
- PostgreSQL with replication
- Redis cluster
- SIEM integration
- Log aggregation (ELK stack)

---

## 🛡️ Ethical Safeguards

### This System:
✅ Only interacts with Mock Scammer API (simulation)  
✅ Never executes real transactions  
✅ Never harms real individuals  
✅ Requires explicit API key authentication  
✅ Logs all operations for audit  
✅ Limits deployment to authorized entities only  
✅ Clear licensing restricting misuse  

### What It Cannot Do:
❌ Be used on real users without consent  
❌ Execute any financial transactions  
❌ Collect real personal data  
❌ Contact real individuals  
❌ Be used for profit without authorization  

---

## 📚 Additional Resources

- [Complete Architecture](ARCHITECTURE.md) - System design details
- [API Reference](docs/API_REFERENCE.md) - Full API documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Research Papers](docs/RESEARCH.md) - Academic references

---

## 👥 Team & Credits

Built for the GUVI Hackathon 2026 (HCL Association)  
Theme: **AI for Fraud Detection & User Safety**

---

## 📞 Support

For issues or questions:
1. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system details
2. Review [docs/API_REFERENCE.md](docs/API_REFERENCE.md) for API help
3. See error logs in `logs/honeypot.log`

---

## 📜 License

This project is provided for hackathon evaluation and educational purposes only. Unauthorized use for fraud, deception of real users, or any illegal purpose is strictly prohibited.

---

**Last Updated:** February 3, 2026  
**Version:** 1.0.0  
**Status:** Production Ready for Hackathon Submission
