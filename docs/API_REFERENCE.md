# API Reference - Agentic AI Honeypot System

## Base URL
```
http://localhost:5000
```

## Authentication
All endpoints (except `/health`) require:
- Header: `X-API-Key: <your_api_key>`
- Header: `Content-Type: application/json`

## Endpoints

### 1. Health Check
**Endpoint:** `GET /health`  
**Authentication:** Not required  
**Description:** Check if API is running

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-03T10:30:00Z",
  "active_conversations": 5
}
```

---

### 2. Detect Scam (Single Message)
**Endpoint:** `POST /api/v1/detect-scam`  
**Authentication:** Required  
**Description:** Detect if a single message is a scam

**Request Body:**
```json
{
  "message": "Hi, your bank account is compromised. Verify your UPI immediately.",
  "sender_role": "scammer"
}
```

**Response (200 OK):**
```json
{
  "timestamp": "2026-02-03T10:30:00Z",
  "detection": {
    "is_scam": true,
    "scam_type": "phishing_upi",
    "confidence": 0.94,
    "detection_method": "pattern_matching + nlp + keywords",
    "extracted_keywords": ["verify", "urgent", "account", "compromised"],
    "explanation": "UPI verification request with urgency markers and account compromise language"
  }
}
```

**Scam Types:**
- `phishing_upi` - UPI/payment verification phishing
- `phishing_banking` - Banking credential phishing
- `phishing_credentials` - Generic credential theft
- `lottery_scam` - Lottery/prize winning scam
- `romance_scam` - Relationship/romance scam
- `investment_fraud` - Investment opportunity fraud
- `tax_fraud` - Tax/government fraud
- `tech_support_scam` - Technical support fraud
- `unknown` - Unclassified

---

### 3. Create Conversation
**Endpoint:** `POST /api/v1/conversation`  
**Authentication:** Required  
**Description:** Start a new honeypot conversation

**Request Body:**
```json
{
  "persona_name": "rajesh_kumar"
}
```

**Available Personas:**
- `rajesh_kumar` - Retired bank manager, 58, very low tech
- `priya_sharma` - Homemaker, 32, low tech
- `arjun_nair` - Business owner, 45, low tech

**Response (201 Created):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "persona": {
    "name": "Rajesh Kumar",
    "age": 58,
    "location": "Bangalore",
    "occupation": "Retired Bank Manager",
    "language_style": "semi_formal_hindi_mix",
    "technical_level": "very_low",
    "vulnerability_factors": ["isolation", "trusts_authority", "money_conscious", "recent_retirement"],
    "emotional_state": "neutral",
    "fatigue_level": 0.0,
    "trust_level": 0.0,
    "message_count": 0
  },
  "timestamp": "2026-02-03T10:30:00Z"
}
```

---

### 4. Process Scammer Message
**Endpoint:** `POST /api/v1/conversation/<conversation_id>/message`  
**Authentication:** Required  
**Description:** Send scammer message and get agent response

**Request Body:**
```json
{
  "message": "Hi, this is Bank Security. Your account is compromised. Verify your UPI immediately.",
  "sender_role": "scammer"
}
```

**Response (200 OK):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-03T10:35:00Z",
  
  "scam_detection": {
    "is_scam": true,
    "scam_type": "phishing_upi",
    "confidence": 0.94,
    "detection_method": "pattern_matching + nlp",
    "extracted_keywords": ["verify", "urgent", "account", "compromised"],
    "explanation": "UPI verification request with urgency markers"
  },
  
  "agent_response": {
    "reply": "Oh God! Really sir? Which bank you are from? I have account in 4 banks. Should I change my password sir?",
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
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "persona": "rajesh_kumar",
    "duration_minutes": 0.1,
    "message_count": 1,
    "scammer_messages": 1,
    "victim_messages": 1,
    "current_state": {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "persona_name": "rajesh_kumar",
      "scam_detected": true,
      "scam_type": "phishing_upi",
      "current_strategy": "identification",
      "emotional_state": "fearful",
      "trust_level": 0.1,
      "honeypot_exposure_risk": 0.05
    },
    "unique_entities_count": 0,
    "high_confidence_entities": 0,
    "extraction_score": 0.0
  }
}
```

**Strategy Phases:**
- `identification` - Initial scam confirmation
- `build_trust` - Creating victim credibility
- `extract_intelligence` - Deep probing for details
- `delay_probe` - Introducing obstacles and validating
- `safe_exit` - Gracefully disengaging

---

### 5. Get Conversation Summary
**Endpoint:** `GET /api/v1/conversation/<conversation_id>`  
**Authentication:** Required  
**Description:** Get summary of conversation and extracted intelligence

**Response (200 OK):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "summary": {
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "persona": "rajesh_kumar",
    "duration_minutes": 12.5,
    "message_count": 8,
    "scammer_messages": 4,
    "victim_messages": 4,
    "current_state": {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "persona_name": "rajesh_kumar",
      "scam_detected": true,
      "scam_type": "phishing_upi",
      "current_strategy": "extract_intelligence",
      "emotional_state": "confused",
      "trust_level": 0.6,
      "honeypot_exposure_risk": 0.3
    },
    "unique_entities_count": 3,
    "high_confidence_entities": 3,
    "extraction_score": 0.65,
    "mentioned_entity_types": {
      "upi_ids": 1,
      "phone_numbers": 2,
      "phishing_links": 1
    }
  },
  "extracted_intelligence": {
    "upi_ids": [
      {
        "value": "scammer@paybank",
        "confidence": 0.92,
        "first_appeared": "2026-02-03T10:35:00Z",
        "appearance_count": 2
      }
    ],
    "phone_numbers": [
      {
        "value": "9876543210",
        "confidence": 0.89,
        "first_appeared": "2026-02-03T10:38:00Z",
        "appearance_count": 3
      }
    ],
    "bank_accounts": [],
    "phishing_links": [
      {
        "value": "https://bankverify-secure.online/login",
        "confidence": 0.94,
        "first_appeared": "2026-02-03T10:40:00Z",
        "appearance_count": 1
      }
    ],
    "email_addresses": []
  },
  "behavior_patterns": {
    "opening_script": "Hi, your account is compromised...",
    "urgency_level": "high",
    "escalation_points": ["threatened account suspension", "requested immediate action"],
    "reward_promises": [],
    "threat_mentions": ["account suspension", "illegal activity", "law enforcement"]
  }
}
```

---

### 6. Export Full Conversation
**Endpoint:** `GET /api/v1/conversation/<conversation_id>/export`  
**Authentication:** Required  
**Description:** Export complete conversation with all details

**Response (200 OK):**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "persona_name": "rajesh_kumar",
  "created_at": "2026-02-03T10:30:00Z",
  "updated_at": "2026-02-03T10:42:00Z",
  
  "message_history": [
    {
      "role": "scammer",
      "content": "Hi, your account is compromised. Verify your UPI immediately.",
      "timestamp": "2026-02-03T10:35:00Z",
      "scam_indicators": ["verify", "urgent", "compromised"],
      "extracted_entities": {
        "upi_ids": [],
        "phone_numbers": [],
        "phishing_links": []
      }
    },
    {
      "role": "victim",
      "content": "Oh God! Really sir? Which bank you are from? I have account in 4 banks.",
      "timestamp": "2026-02-03T10:35:30Z",
      "scam_indicators": [],
      "extracted_entities": {}
    }
    // ... more messages
  ],
  
  "current_state": { /* ... */ },
  "extracted_intelligence": { /* ... */ },
  "behavior_patterns": { /* ... */ },
  "operational_metrics": { /* ... */ },
  "summary": { /* ... */ }
}
```

---

### 7. Delete Conversation
**Endpoint:** `DELETE /api/v1/conversation/<conversation_id>`  
**Authentication:** Required  
**Description:** Delete conversation and all associated data

**Response (200 OK):**
```json
{
  "status": "deleted",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 8. Get System Statistics
**Endpoint:** `GET /api/v1/statistics`  
**Authentication:** Required  
**Description:** Get overall system statistics

**Response (200 OK):**
```json
{
  "timestamp": "2026-02-03T10:45:00Z",
  "active_conversations": 12,
  "api_version": "v1"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized"
}
```

### 403 Forbidden
```json
{
  "error": "IP not authorized"
}
```

### 404 Not Found
```json
{
  "error": "Conversation not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Not yet implemented. Coming in v2.

## Webhooks

Not yet implemented. Coming in v2.

## Versioning

Current version: `v1`  
All endpoints use `/api/v1/` prefix.

---

## Example cURL Commands

### Health Check
```bash
curl http://localhost:5000/health
```

### Create Conversation
```bash
curl -X POST http://localhost:5000/api/v1/conversation \
  -H "X-API-Key: test_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"persona_name": "rajesh_kumar"}'
```

### Send Message
```bash
curl -X POST http://localhost:5000/api/v1/conversation/550e8400-e29b-41d4-a716-446655440000/message \
  -H "X-API-Key: test_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Your account is compromised. Verify your UPI.",
    "sender_role": "scammer"
  }'
```

### Get Conversation
```bash
curl http://localhost:5000/api/v1/conversation/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-API-Key: test_key_12345"
```

### Export Conversation
```bash
curl http://localhost:5000/api/v1/conversation/550e8400-e29b-41d4-a716-446655440000/export \
  -H "X-API-Key: test_key_12345" > conversation.json
```

### Delete Conversation
```bash
curl -X DELETE http://localhost:5000/api/v1/conversation/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-API-Key: test_key_12345"
```

---

**Last Updated:** February 3, 2026  
**Version:** 1.0.0
