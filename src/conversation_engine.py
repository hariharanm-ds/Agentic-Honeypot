"""
Conversation Engine - Multi-turn conversation handling and adaptive replies
"""

from typing import List, Dict, Optional
import random
from src.agent_controller import StrategyPhase
from src.persona import PersonaEngine

class ConversationEngine:
    """Handle multi-turn conversations with adaptive replies"""
    
    def __init__(self, persona_engine: PersonaEngine):
        """Initialize conversation engine"""
        self.persona = persona_engine
        self.conversation_template = self._build_conversation_templates()
        
    def _build_conversation_templates(self) -> Dict[StrategyPhase, Dict]:
        """Build conversation templates for each strategy phase"""
        return {
            StrategyPhase.IDENTIFICATION: {
                "opening_questions": [
                    "Which bank are you calling from sir?",
                    "How did you get my number?",
                    "What is your employee ID sir?",
                    "Can you tell me your name and department?",
                ],
                "concern_expressions": [
                    "I'm worried sir...",
                    "That sounds serious...",
                    "Oh no, what should I do?",
                    "I'm getting scared sir...",
                ],
                "confirmation_probes": [
                    "Is this a real security call or a scam?",
                    "Can you explain how this happened?",
                    "Why are you calling me specifically?",
                ],
                "fallback": "I'm very confused sir... can you explain again?"
            },
            StrategyPhase.BUILD_TRUST: {
                "compliance_statements": [
                    "Ok sir, I'll do whatever you say.",
                    "Yes sir, I trust you. What should I do?",
                    "I'm listening sir, tell me the steps.",
                ],
                "concern_expressions": [
                    "But sir, will my money be safe?",
                    "Is this risky sir?",
                    "What if something goes wrong?",
                ],
                "reassurance_requests": [
                    "Sir, can you promise this is safe?",
                    "How many people have done this?",
                    "Should I tell my family?",
                ],
                "fallback": "I'm very scared sir... please guide me step by step."
            },
            StrategyPhase.EXTRACT_INTELLIGENCE: {
                "why_questions": [
                    "Can you explain why I need to do this sir?",
                    "How did my account get hacked?",
                    "Why is this method safer?",
                    "What will happen if I don't do this?",
                ],
                "how_questions": [
                    "Can you explain step by step how to do this?",
                    "What exactly should I click on?",
                    "Which app should I use sir?",
                    "Can you show me how to do this?",
                ],
                "alternative_questions": [
                    "Can I do this in a different way?",
                    "Is there an easier method?",
                    "Can I handle this at the bank directly?",
                    "Can someone else do this for me?",
                ],
                "fallback": "I don't understand sir... can you explain differently?"
            },
            StrategyPhase.DELAY_PROBE: {
                "obstacle_introduction": [
                    "Sir, my internet is very slow...",
                    "I'm in the office right now, can I do this later?",
                    "My battery is about to die sir...",
                    "Can you call me back in 10 minutes?",
                ],
                "consistency_checks": [
                    "So you're saying the same thing that happened to my brother?",
                    "Why is every bank doing this security check?",
                    "Are other people getting these calls too?",
                    "Can you verify this on my banking app?",
                ],
                "progress_checks": [
                    "Have I done this correctly so far?",
                    "What's the next step sir?",
                    "How much longer will this take?",
                ],
                "fallback": "Sir, I'm getting confused about all these steps..."
            },
            StrategyPhase.SAFE_EXIT: {
                "exit_statements": [
                    "Sir, my wife just came home... can I call you later?",
                    "I'm too scared to do this right now sir...",
                    "I think I should consult my family about this...",
                    "Can we schedule this for tomorrow?",
                ],
                "contact_requests": [
                    "What's your direct number sir?",
                    "Can you give me your email for record?",
                    "How can I reach you later?",
                    "Will you be available tomorrow?",
                ],
                "fallback": "Thank you sir, I'll think about this and call back."
            }
        }
    
    def generate_response(self, scammer_message: str, strategy_phase: StrategyPhase,
                         memory_context: Dict = None,
                         previous_questions: List[str] = None) -> str:
        """
        Generate contextual response based on strategy
        
        Args:
            scammer_message: Message from scammer
            strategy_phase: Current strategy phase
            memory_context: Context from memory store
            previous_questions: List of previous questions to avoid repetition
            
        Returns:
            Response text
        """
        
        # Select response template based on strategy
        templates = self.conversation_template.get(strategy_phase, {})
        
        # Detect what scammer is asking/saying
        message_lower = scammer_message.lower()
        
        # Choose response category
        if strategy_phase == StrategyPhase.IDENTIFICATION:
            response = self._generate_identification_response(scammer_message, templates)
        
        elif strategy_phase == StrategyPhase.BUILD_TRUST:
            response = self._generate_trust_response(scammer_message, templates)
        
        elif strategy_phase == StrategyPhase.EXTRACT_INTELLIGENCE:
            response = self._generate_extraction_response(scammer_message, templates, previous_questions)
        
        elif strategy_phase == StrategyPhase.DELAY_PROBE:
            response = self._generate_delay_response(scammer_message, templates)
        
        elif strategy_phase == StrategyPhase.SAFE_EXIT:
            response = self._generate_exit_response(scammer_message, templates)
        
        else:
            response = templates.get("fallback", "I'm confused sir, can you explain again?")
        
        # Apply persona modifications
        response = self.persona.inject_language_style(response)
        response = self.persona.inject_mistakes(response)
        
        # Update persona emotional state
        self.persona.update_emotional_state(scammer_message, {})
        
        return response
    
    def _generate_identification_response(self, scammer_message: str, templates: Dict) -> str:
        """Generate response during identification phase"""
        # Scammer initiates - express concern and ask clarifying questions
        message_lower = scammer_message.lower()
        
        if any(word in message_lower for word in ["account", "hacked", "compromised"]):
            return f"{random.choice(templates['concern_expressions'])} {random.choice(templates['opening_questions'])}"
        
        elif any(word in message_lower for word in ["verify", "confirm", "click"]):
            return random.choice(templates['confirmation_probes'])
        
        else:
            return random.choice(templates['opening_questions'])
    
    def _generate_trust_response(self, scammer_message: str, templates: Dict) -> str:
        """Generate response during trust-building phase"""
        message_lower = scammer_message.lower()
        
        # If scammer is asking for action - show compliance with fear
        if any(word in message_lower for word in ["do", "download", "click", "send", "verify"]):
            compliance = random.choice(templates['compliance_statements'])
            concern = random.choice(templates['concern_expressions'])
            return f"{compliance} {concern}"
        
        else:
            # Just show eagerness to comply
            return random.choice(templates['reassurance_requests'])
    
    def _generate_extraction_response(self, scammer_message: str, templates: Dict,
                                     previous_questions: List[str] = None) -> str:
        """Generate response during intelligence extraction phase"""
        message_lower = scammer_message.lower()
        
        # Decide which type of question to ask
        response_type = random.choice(['why', 'how', 'alternative'])
        
        if response_type == 'why':
            question = random.choice(templates['why_questions'])
        elif response_type == 'how':
            question = random.choice(templates['how_questions'])
        else:
            question = random.choice(templates['alternative_questions'])
        
        # Check for repetition
        if previous_questions and question in previous_questions:
            # Use fallback instead
            question = templates['fallback']
        
        # Wrap in context
        if any(word in message_lower for word in ["download", "app", "link"]):
            return f"Sir, {question}"
        else:
            return question
    
    def _generate_delay_response(self, scammer_message: str, templates: Dict) -> str:
        """Generate response during delay/probe phase"""
        message_lower = scammer_message.lower()
        
        # Introduce obstacles or probe for consistency
        if any(word in message_lower for word in ["now", "quickly", "immediately", "urgent"]):
            # Introduce obstacle
            return random.choice(templates['obstacle_introduction'])
        
        else:
            # Probe consistency
            return random.choice(templates['consistency_checks'])
    
    def _generate_exit_response(self, scammer_message: str, templates: Dict) -> str:
        """Generate response during safe exit phase"""
        # Express need to exit gracefully
        exit_stmt = random.choice(templates['exit_statements'])
        
        # Sometimes ask for contact info
        if random.random() > 0.5:
            contact_req = random.choice(templates['contact_requests'])
            return f"{exit_stmt} {contact_req}"
        
        return exit_stmt
    
    def maintain_conversation_coherence(self, victim_response: str, 
                                       scammer_response_to_victim: str) -> bool:
        """Check if conversation is staying coherent"""
        # Simple check - responses shouldn't be completely contradictory
        # This is a basic implementation; in production, use NLP similarity
        
        if len(victim_response) < 5 or len(scammer_response_to_victim) < 5:
            return False
        
        return True
    
    def should_ask_followup(self, conversation_length: int) -> bool:
        """Determine if should ask follow-up question"""
        # Ask follow-ups to keep conversation going and extract more info
        # But not too frequently to seem natural
        
        if conversation_length < 3:
            return False  # Let scammer lead initially
        
        # Ask follow-ups 70% of the time after initial exchanges
        return random.random() < 0.7
