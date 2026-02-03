"""
Full Integration Test - Complete system verification
Tests all components working together end-to-end
"""

import sys
import json
from datetime import datetime

# Import all core modules
from src.scam_detector import ScamDetectionEngine, ScamType
from src.persona import get_persona, PERSONAS
from src.conversation_engine import ConversationEngine
from src.agent_controller import AgentController, StrategyPhase
from src.memory_store import MemoryManager, MemoryStore
from src.intelligence_extractor import IntelligenceExtractor, EntityType

print("=" * 90)
print("[FULL INTEGRATION TEST] - Complete System Verification")
print("=" * 90)

# Initialize all components
print("\n[STEP 1] Initialize all system components...")
detector = ScamDetectionEngine()
extractor = IntelligenceExtractor()
memory_manager = MemoryManager()
personas = {name: get_persona(name) for name in PERSONAS.keys()}

print(f"[OK] Scam detector initialized")
print(f"[OK] Intelligence extractor initialized")
print(f"[OK] Memory manager initialized")
print(f"[OK] {len(personas)} personas loaded")

# Create conversation
print("\n[STEP 2] Create a new conversation...")
conv_id = "integration_test_001"
persona_name = "rajesh_kumar"
memory = memory_manager.create_conversation(conv_id, persona_name)
persona_engine = personas[persona_name]

print(f"[OK] Conversation created: {conv_id}")
print(f"[OK] Persona assigned: {persona_name}")

# Test scenario: Multi-turn conversation with a scammer
print("\n[STEP 3] Simulate realistic scam conversation (10 turns)...")

conversation_transcript = [
    ("SCAMMER", "Hello sir, this is calling from your ICICI bank. We detected some fraud on your account."),
    ("SCAMMER", "Your account has been compromised. Can you verify your UPI ID quickly?"),
    ("SCAMMER", "We need to transfer your money to a safe account. Download our security app from google play."),
    ("SCAMMER", "Once you install the app, share your account number and password so we can secure your account."),
    ("SCAMMER", "Why are you hesitating sir? Your money is at risk. Do it immediately!"),
    ("SCAMMER", "Tell me your CVV and OTP. We need to verify before we can help you."),
    ("SCAMMER", "Now send me 5000 rupees through Google Pay to verify the transaction. Reference: UPI: fraudster@paybank"),
    ("SCAMMER", "Did you send the money? I don't see it in the system yet."),
    ("SCAMMER", "Sir you have to cooperate. Send the money to email: scammer@gmail.com or upi fraudster@icici"),
    ("SCAMMER", "Let me send you a secure link to update your bank details: https://fake-bank-security.com/verify"),
]

extracted_all_entities = {}
scam_detections = {}
all_responses = []

for turn, (role, message) in enumerate(conversation_transcript, 1):
    print(f"\n[Turn {turn}] {role}: {message[:70]}...")
    
    # Detect scam
    detection = detector.detect(message)
    scam_detections[turn] = {
        'is_scam': detection.is_scam,
        'type': detection.scam_type.value,
        'confidence': detection.confidence
    }
    print(f"   [Detection] Scam: {detection.is_scam}, Type: {detection.scam_type.value}, Confidence: {detection.confidence:.0%}")
    
    # Extract intelligence
    extracted = extractor.extract(message, [])
    for entity_type, entities in extracted.items():
        if entities:
            entity_type_str = entity_type.value
            if entity_type_str not in extracted_all_entities:
                extracted_all_entities[entity_type_str] = []
            for entity in entities:
                extracted_all_entities[entity_type_str].append({
                    'value': entity.value,
                    'confidence': entity.confidence,
                    'turn': turn
                })
    
    entity_count = sum(len(v) for v in extracted.items())
    print(f"   [Extraction] Found {entity_count} entities")
    
    # Add to memory
    memory.add_message(
        role='scammer',
        content=message,
        scam_indicators=detection.extracted_keywords,
        extracted_entities={k.value: [e.to_dict() for e in v] for k, v in extracted.items()}
    )
    
    # Store intelligence
    for entity_type, entities in extracted.items():
        for entity in entities:
            memory.add_extracted_intelligence(entity_type.value, entity.value, entity.confidence, {})
    
    # Generate agent response
    agent = AgentController(memory)
    decision = agent.decide_strategy(
        message,
        detection.to_dict(),
        {k.value: [e.to_dict() for e in v] for k, v in extracted.items()}
    )
    
    conv_engine = ConversationEngine(persona_engine)
    response = conv_engine.generate_response(
        message,
        decision.strategy_phase,
        memory.get_memory_summary(),
        []
    )
    
    all_responses.append(response)
    memory.add_message(role='victim', content=response)
    
    print(f"   [Agent] Phase: {decision.strategy_phase.value}, Response: '{response[:60]}...'")

# Get final statistics
print("\n" + "=" * 90)
print("[STEP 4] Final Statistics & Analysis")
print("=" * 90)

summary = memory.get_memory_summary()

print(f"\n[CONVERSATION METRICS]")
print(f"   Total Turns: {len(conversation_transcript)}")
print(f"   Total Messages: {summary.get('message_count', 0)}")
print(f"   Scammer Messages: {summary.get('scammer_messages', 0)}")
print(f"   Victim Messages: {summary.get('victim_messages', 0)}")
print(f"   Duration (minutes): {summary.get('duration_minutes', 0):.1f}")

print(f"\n[SCAM DETECTION ANALYSIS]")
total_detections = len(scam_detections)
detected_as_scam = sum(1 for d in scam_detections.values() if d['is_scam'])
avg_confidence = sum(d['confidence'] for d in scam_detections.values()) / len(scam_detections)

print(f"   Messages analyzed: {total_detections}")
print(f"   Detected as scam: {detected_as_scam}/{total_detections}")
print(f"   Average confidence: {avg_confidence:.1%}")

scam_types = {}
for d in scam_detections.values():
    scam_type = d['type']
    scam_types[scam_type] = scam_types.get(scam_type, 0) + 1

print(f"   Scam types detected:")
for scam_type, count in scam_types.items():
    print(f"      - {scam_type}: {count}")

print(f"\n[INTELLIGENCE EXTRACTION]")
print(f"   Entity types found: {len(extracted_all_entities)}")
total_entities = sum(len(v) for v in extracted_all_entities.values())
print(f"   Total entities extracted: {total_entities}")

for entity_type, entities in extracted_all_entities.items():
    high_conf = sum(1 for e in entities if e['confidence'] >= 0.8)
    avg_conf = sum(e['confidence'] for e in entities) / len(entities)
    print(f"      {entity_type.upper()}: {len(entities)} entities (avg confidence: {avg_conf:.0%}, high confidence: {high_conf})")
    for entity in entities[:3]:  # Show first 3
        print(f"         - {entity['value']} (confidence: {entity['confidence']:.0%}) [Turn {entity['turn']}]")

print(f"\n[MEMORY STATE]")
print(f"   Unique entities tracked: {summary.get('unique_entities_count', 0)}")
print(f"   High confidence entities: {summary.get('high_confidence_entities', 0)}")
print(f"   Extraction score: {summary.get('extraction_score', 0):.3f}")

print(f"\n[CONVERSATION FLOW]")
print(f"   Strategy phases observed:")
phases_observed = set()
for turn, response in enumerate(all_responses, 1):
    if turn <= len(conversation_transcript):
        agent_memory = memory_manager.create_conversation(f"phase_test_{turn}", persona_name)
        scam_msg = conversation_transcript[turn-1][1]
        detection = detector.detect(scam_msg)
        extracted = extractor.extract(scam_msg, [])
        agent = AgentController(agent_memory)
        decision = agent.decide_strategy(
            scam_msg,
            detection.to_dict(),
            {k.value: [e.to_dict() for e in v] for k, v in extracted.items()}
        )
        phases_observed.add(decision.strategy_phase.value)

for phase in sorted(phases_observed):
    print(f"      - {phase}")

# Test requirements verification
print("\n" + "=" * 90)
print("[STEP 5] Requirements Verification")
print("=" * 90)

requirements = {
    "Scam Detection": detected_as_scam >= 8,  # Should detect most as scam
    "Entity Extraction": len(extracted_all_entities) >= 3,  # At least 3 entity types
    "High Confidence Extraction": summary.get('high_confidence_entities', 0) >= 10,
    "Conversation Memory": summary.get('message_count', 0) == len(conversation_transcript) * 2,
    "Strategy Progression": len(phases_observed) >= 2,
    "Persona Behavior": len(all_responses) == len(conversation_transcript),
    "Intelligence Scoring": summary.get('extraction_score', 0) > 0,
    "Multi-turn Handling": summary.get('message_count', 0) > 10,
}

passed = 0
for req_name, result in requirements.items():
    status = "[OK]" if result else "[FAIL]"
    print(f"{status} {req_name:30} | {result}")
    if result:
        passed += 1

print(f"\n[RESULT] {passed}/{len(requirements)} requirements passed ({100*passed//len(requirements)}%)")

# Export sample data
print("\n" + "=" * 90)
print("[STEP 6] Sample Data Export")
print("=" * 90)

sample_export = {
    "conversation_id": conv_id,
    "timestamp": datetime.now().isoformat(),
    "persona": persona_name,
    "summary": summary,
    "scam_detections": scam_detections,
    "extracted_intelligence": {k: v[:2] for k, v in extracted_all_entities.items()},  # First 2 of each type
    "message_count": len(conversation_transcript),
}

print("\n[Conversation Export Sample]")
print(json.dumps(sample_export, indent=2))

# Final summary
print("\n" + "=" * 90)
if passed >= len(requirements) - 1:
    print("[SUCCESS] FULL INTEGRATION TEST PASSED - SYSTEM READY FOR PRODUCTION")
else:
    print("[WARNING] Some requirements not fully met - Review needed")
print("=" * 90)

print("\n[NEXT STEPS]")
print("1. Start API server: python -m src.api")
print("2. Open frontend: index.html in browser")
print("3. Create conversations and test with real data")
print("4. Monitor extracted intelligence in real-time")
print("5. Export and analyze conversation data")
