"""
Quick Start Test Script - Agentic Honeypot
Run this to verify the system is working
"""

import json
import sys
sys.path.insert(0, '.')

def test_scam_detection():
    """Test scam detection engine"""
    print("\n🔍 Testing Scam Detection Engine...")
    print("-" * 60)
    
    from src.scam_detector import ScamDetectionEngine
    
    detector = ScamDetectionEngine()
    
    test_messages = [
        "Hi, your bank account is compromised. Verify your UPI immediately.",
        "Congratulations! You won 1 lakh rupees. Claim your prize now.",
        "Hello, just checking in with you",
        "Send 100 rupees to scammer@paybank to secure your account"
    ]
    
    for msg in test_messages:
        result = detector.detect(msg)
        print(f"\n📩 Message: {msg}")
        print(f"✅ Is Scam: {result.is_scam}")
        print(f"📊 Type: {result.scam_type.value}")
        print(f"📈 Confidence: {result.confidence:.2%}")
        print(f"🏷️  Keywords: {', '.join(result.extracted_keywords)}")

def test_persona_engine():
    """Test persona engine"""
    print("\n\n👤 Testing Persona Engine...")
    print("-" * 60)
    
    from src.persona import get_persona
    
    persona = get_persona("rajesh_kumar")
    print(f"\n📋 Persona Info:")
    info = persona.get_persona_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test language injection
    test_text = "I will do it"
    modified = persona.inject_language_style(test_text)
    print(f"\n🌐 Language Style Test:")
    print(f"  Original: {test_text}")
    print(f"  Modified: {modified}")
    
    # Test mistake injection
    modified_with_mistakes = persona.inject_mistakes(modified)
    print(f"  With mistakes: {modified_with_mistakes}")

def test_conversation_memory():
    """Test memory store"""
    print("\n\n💾 Testing Memory Store...")
    print("-" * 60)
    
    from src.memory_store import MemoryStore
    
    memory = MemoryStore("test_conv_001", "rajesh_kumar")
    
    # Add messages
    memory.add_message("scammer", "Your account is hacked")
    memory.add_message("victim", "Oh no! What should I do?")
    memory.add_message("scammer", "Send money to scammer@paybank")
    memory.add_message("victim", "Ok sir, I will send")
    
    # Extract intelligence
    memory.add_extracted_intelligence("upi_ids", "scammer@paybank", 0.92)
    memory.add_extracted_intelligence("phone_numbers", "9876543210", 0.89)
    
    print(f"\n📊 Conversation Summary:")
    summary = memory.get_memory_summary()
    for key, value in summary.items():
        if key != "current_state":
            print(f"  {key}: {value}")
    
    print(f"\n📍 Extracted Intelligence:")
    for entity_type, entities in memory.extracted_intelligence.items():
        if entities:
            print(f"  {entity_type}: {[e['value'] for e in entities]}")

def test_intelligence_extraction():
    """Test intelligence extraction"""
    print("\n\n🔎 Testing Intelligence Extraction...")
    print("-" * 60)
    
    from src.intelligence_extractor import IntelligenceExtractor
    
    extractor = IntelligenceExtractor()
    
    test_message = "Send 100 rupees to scammer@paybank. Call me at 9876543210. Use this link: https://fake-bank-login.com/verify"
    
    print(f"\n📝 Test Message: {test_message}")
    print(f"\n🎯 Extracted Entities:")
    
    extracted = extractor.extract(test_message)
    for entity_type, entities in extracted.items():
        if entities:
            for entity in entities:
                print(f"  ✅ {entity_type.value}: {entity.value} (confidence: {entity.confidence:.2%})")

def test_agent_controller():
    """Test agent controller"""
    print("\n\n🤖 Testing Agent Controller...")
    print("-" * 60)
    
    from src.agent_controller import AgentController
    from src.memory_store import MemoryStore
    
    memory = MemoryStore("test_agent_001", "rajesh_kumar")
    agent = AgentController(memory)
    
    # Simulate a scam detection
    scam_result = {
        "is_scam": True,
        "scam_type": "phishing_upi",
        "confidence": 0.94
    }
    
    extracted_entities = {
        "upi_ids": [{"value": "scammer@paybank", "confidence": 0.92}],
        "phone_numbers": [],
        "bank_accounts": [],
        "phishing_links": [],
        "email_addresses": []
    }
    
    decision = agent.decide_strategy(
        "Send money to scammer@paybank to verify",
        scam_result,
        extracted_entities
    )
    
    print(f"\n🎯 Agent Decision:")
    print(f"  Strategy Phase: {decision.strategy_phase.value}")
    print(f"  Action: {decision.action_type}")
    print(f"  Confidence: {decision.confidence:.2%}")
    print(f"  Reasoning: {decision.reasoning}")
    print(f"  Suggested Approach: {decision.suggested_approach}")

def test_conversation_engine():
    """Test conversation engine"""
    print("\n\n💬 Testing Conversation Engine...")
    print("-" * 60)
    
    from src.conversation_engine import ConversationEngine
    from src.persona import get_persona
    from src.agent_controller import StrategyPhase
    
    persona = get_persona("rajesh_kumar")
    engine = ConversationEngine(persona)
    
    scammer_msg = "Your account is compromised. Verify your UPI immediately."
    
    response = engine.generate_response(
        scammer_msg,
        StrategyPhase.IDENTIFICATION
    )
    
    print(f"\n🎤 Conversation Test:")
    print(f"  Scammer: {scammer_msg}")
    print(f"  Victim:  {response}")

def main():
    """Run all tests"""
    print("=" * 60)
    print("🍯 AGENTIC AI HONEYPOT - QUICK START TEST")
    print("=" * 60)
    
    try:
        test_scam_detection()
        test_persona_engine()
        test_conversation_memory()
        test_intelligence_extraction()
        test_agent_controller()
        test_conversation_engine()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n📚 Next Steps:")
        print("1. Start the API server: python -m src.api")
        print("2. Test endpoints: curl http://localhost:5000/health")
        print("3. Read ARCHITECTURE.md for detailed design")
        print("4. Check docs/API_REFERENCE.md for API usage")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
