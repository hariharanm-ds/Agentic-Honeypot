"""
Conversation Engine - Multi-turn conversation templates and state management
Provides contextual responses for each engagement phase
"""

from typing import Dict, List
from enum import Enum
from src.agent_controller import StrategyPhase

class ConversationEngine:
    """
    Manages conversation templates for different engagement phases.
    
    Templates are organized by StrategyPhase:
    1. IDENTIFICATION - Gather caller info
    2. BUILD_TRUST - Show compliance, build rapport
    3. EXTRACT_INTELLIGENCE - Get account/UPI/URLs
    4. DELAY_PROBE - Introduce obstacles, test consistency
    5. SAFE_EXIT - Gracefully disengage
    """
    
    def __init__(self, persona_engine=None):
        """Initialize conversation engine"""
        self.persona_engine = persona_engine
        self.templates = self._build_templates()
    
    def _build_templates(self) -> Dict[StrategyPhase, Dict]:
        """Build conversation templates for each phase"""
        return {
            StrategyPhase.IDENTIFICATION: {
                "opening_questions": [
                    "Which bank are you calling from sir?",
                    "How did you get my number?",
                    "What is your employee ID sir?",
                    "Can you tell me your name and department?",
                    "Who is calling sir?",
                    "Which bank department are you from?",
                    "Can you verify your employee badge number sir?",
                    "What is the reason for this call?",
                ],
                "concern_expressions": [
                    "I'm worried sir...",
                    "That sounds serious...",
                    "Oh no, what should I do?",
                    "I'm getting scared sir...",
                    "This is concerning sir...",
                    "I don't understand sir...",
                ],
                "verification_requests": [
                    "Can you confirm my account details?",
                    "How do I know you're really from the bank?",
                    "Can I call the bank to verify this?",
                    "What's your official employee number?",
                ],
                "fallback": "I'm confused sir... can you explain again?"
            },
            
            StrategyPhase.BUILD_TRUST: {
                "compliance_statements": [
                    "Ok sir, I'll do whatever you say.",
                    "Yes sir, I trust you. What should I do?",
                    "I'm listening sir, tell me the steps.",
                    "I understand sir. I will follow your instructions.",
                    "Ok sir, I'm ready. What do I do?",
                    "Yes sir, I will do it immediately.",
                    "Sir, I completely trust you. Guide me please.",
                ],
                "concern_expressions": [
                    "But sir, will my money be safe?",
                    "Is this risky sir?",
                    "What if something goes wrong?",
                    "Should I be worried sir?",
                    "I'm very nervous about this sir...",
                ],
                "reassurance_requests": [
                    "Sir, can you promise this is safe?",
                    "How many people have done this?",
                    "Should I tell my family?",
                    "Will you stay with me during this process?",
                    "Sir, is this procedure normal?",
                ],
                "deference_expressions": [
                    "Yes sir, whatever you say sir.",
                    "I trust your expertise sir.",
                    "You must know better than me sir.",
                    "I will do exactly as you say sir.",
                ],
                "fallback": "I'm very scared sir... please guide me step by step."
            },
            
            StrategyPhase.EXTRACT_INTELLIGENCE: {
                "why_questions": [
                    "Can you explain why I need to do this sir?",
                    "How did my account get hacked?",
                    "Why is this method safer?",
                    "What will happen if I don't do this?",
                    "Can you explain the reason for this process?",
                    "Why can't the bank do this directly?",
                ],
                "how_questions": [
                    "Can you explain step by step how to do this?",
                    "What exactly should I click on?",
                    "Which app should I use sir?",
                    "Can you show me how to do this?",
                    "Can you guide me through each step?",
                    "Should I do this in a specific way?",
                ],
                "technical_questions": [
                    "What is the name of this application?",
                    "Can you send me the link sir?",
                    "What should I download?",
                    "Is this an official app?",
                    "Where do I find this online?",
                ],
                "clarification_requests": [
                    "Can you explain that more clearly?",
                    "I didn't understand sir... can you repeat?",
                    "Can you break it down into smaller steps?",
                    "What exactly do you mean by that?",
                ],
                "alternative_questions": [
                    "Is there an easier method?",
                    "Can I do this in a different way?",
                    "Can someone else do this for me?",
                    "Can I handle this at the bank directly?",
                ],
                "fallback": "I don't understand sir... can you explain differently?"
            },
            
            StrategyPhase.DELAY_PROBE: {
                "obstacle_introduction": [
                    "Sir, my internet is very slow...",
                    "I'm in the office right now, can I do this later?",
                    "My battery is about to die sir...",
                    "Can you call me back in 10 minutes?",
                    "I'm with someone right now, can I do this privately?",
                    "My phone is having issues sir...",
                    "Can we continue this tomorrow sir?",
                    "I need to go somewhere, can I call back?",
                ],
                "consistency_checks": [
                    "So you're saying the same thing that happened to my brother?",
                    "Why is every bank doing this security check?",
                    "Are other people getting these calls too?",
                    "Can you verify this on my banking app?",
                    "I saw a news article about this... is it real?",
                    "My friend said this is a scam... is it true?",
                ],
                "safety_doubts": [
                    "Is this really safe sir?",
                    "Why can't I just go to the bank?",
                    "What if I make a mistake?",
                    "Is my account protected if something goes wrong?",
                    "Can you guarantee nothing will happen?",
                ],
                "progress_checks": [
                    "Have I done this correctly so far?",
                    "What's the next step sir?",
                    "How much longer will this take?",
                    "Are we almost done sir?",
                    "How many more steps are there?",
                ],
                "fallback": "Sir, I'm getting confused about all these steps..."
            },
            
            StrategyPhase.SAFE_EXIT: {
                "safe_exit": [
                    "Sir, I need to discuss this with my family first.",
                    "My wife is worried about this. Can I call you back tomorrow?",
                    "I'm not feeling comfortable doing this right now sir.",
                    "Let me visit the bank directly and verify this sir.",
                    "I need to think about this more carefully sir.",
                    "Can I call the bank customer service to confirm this?",
                    "My lawyer told me to be careful... let me verify first.",
                    "I'm not sure about giving these details online sir.",
                ],
                "delay_tactics": [
                    "Can you call me later? I'm busy right now.",
                    "I'm not in the right mindset for this now sir.",
                    "Can you send me written instructions sir?",
                    "I need to consult with my accountant first.",
                ],
                "refusal_polite": [
                    "Sir, I think this might be risky. I'd rather not.",
                    "I don't feel comfortable with this sir.",
                    "I think I should just go to the bank directly.",
                    "My instinct says this doesn't feel right.",
                ],
            }
        }
    
    def get_templates(self, strategy_phase: StrategyPhase) -> Dict[str, List[str]]:
        """Get templates for a specific strategy phase"""
        return self.templates.get(strategy_phase, {})
    
    def get_template_by_key(self, strategy_phase: StrategyPhase, key: str) -> List[str]:
        """Get specific template category"""
        phase_templates = self.templates.get(strategy_phase, {})
        return phase_templates.get(key, [])
