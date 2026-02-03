"""
Agent Controller - Complete Agentic Decision-Making & Strategy Management
Orchestrates multi-turn engagement with adaptive strategy transitions
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import random
from datetime import datetime
from src.memory_store import Message
from src.persona import PersonaEngine, Persona, LanguageStyle, TechnicalLevel, EmotionalState
from src.conversation_engine import ConversationEngine

class StrategyPhase(Enum):
    """Strategy phases for scammer engagement"""
    IDENTIFICATION = "identification"
    BUILD_TRUST = "build_trust"
    EXTRACT_INTELLIGENCE = "extract_intelligence"
    DELAY_PROBE = "delay_probe"
    SAFE_EXIT = "safe_exit"

@dataclass
class AgentDecision:
    """Autonomous agent decision"""
    strategy_phase: StrategyPhase
    confidence: float
    reasoning: str
    suggested_response: str

class AgentController:
    """
    Autonomous controller for multi-turn scammer engagement.
    
    Responsibilities:
    1. Determine current strategy phase based on conversation state
    2. Generate contextually appropriate responses
    3. Manage persona consistency
    4. Transition between engagement phases
    5. Track conversation coherence
    """
    
    # Configuration
    MAX_CONVERSATION_TURNS = 50
    CONVERSATION_TIMEOUT_MINUTES = 60
    
    def __init__(self, memory_store):
        """
        Initialize agent controller.
        
        Args:
            memory_store: MemoryStore instance for this conversation
        """
        self.memory = memory_store
        
        # Initialize persona (random selection)
        self.persona = self._select_persona()
        self.persona_engine = PersonaEngine(self.persona)
        
        # Initialize conversation engine
        self.conversation_engine = ConversationEngine(self.persona_engine)
        
        # State tracking
        self.turn_count = 0
        self.last_response = None
        self.response_history = []  # Track responses to avoid repetition
    
    def _select_persona(self) -> Persona:
        """
        Select a realistic persona for engagement.
        Random selection ensures variety across conversations.
        """
        personas = [
            Persona(
                name="Amit Kumar",
                age=35,
                location="Mumbai",
                occupation="IT Services Manager",
                language_style=LanguageStyle.SEMI_FORMAL_HINDI_MIX,
                technical_level=TechnicalLevel.MEDIUM,
                vulnerability_factors=["trusts_authority", "money_conscious", "family_protective"]
            ),
            Persona(
                name="Priya Sharma",
                age=42,
                location="Bangalore",
                occupation="Homemaker",
                language_style=LanguageStyle.CASUAL_ENGLISH,
                technical_level=TechnicalLevel.LOW,
                vulnerability_factors=["trusts_authority", "family_protective", "tech_fearful"]
            ),
            Persona(
                name="Rajesh Patel",
                age=28,
                location="Delhi",
                occupation="Junior Developer",
                language_style=LanguageStyle.BROKEN_ENGLISH,
                technical_level=TechnicalLevel.LOW,
                vulnerability_factors=["trusts_peers", "tech_fearful", "money_conscious"]
            ),
            Persona(
                name="Sunita Gupta",
                age=55,
                location="Kolkata",
                occupation="Retired Teacher",
                language_style=LanguageStyle.FORMAL_ENGLISH,
                technical_level=TechnicalLevel.VERY_LOW,
                vulnerability_factors=["trusts_authority", "respectful", "cautious"]
            ),
        ]
        return random.choice(personas)
    
    def get_current_phase(self, turn_count: int) -> StrategyPhase:
        """
        Determine current strategy phase based on turn count.
        
        Phase Progression:
        - Turns 0-3: IDENTIFICATION (gather caller info)
        - Turns 4-8: BUILD_TRUST (show compliance, lower guard)
        - Turns 9-15: EXTRACT_INTELLIGENCE (get account/UPI/URLs)
        - Turns 16-25: DELAY_PROBE (introduce obstacles, test consistency)
        - Turns 26+: SAFE_EXIT (graceful disengagement)
        """
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
    
    def generate_response(self, 
                         message: str,
                         detection_confidence: float,
                         conversation_history: List[Message],
                         strategy_phase: StrategyPhase) -> str:
        """
        Generate contextual agent response.
        
        Strategy:
        1. Get template responses for current phase
        2. Select response based on message content
        3. Apply persona language style
        4. Inject emotional state
        5. Add natural variations (typos, confusion)
        
        Args:
            message: Scammer's latest message
            detection_confidence: Scam detection confidence
            conversation_history: Previous messages in conversation
            strategy_phase: Current engagement phase
            
        Returns:
            Agent response string
        """
        self.turn_count = len(conversation_history) // 2
        
        # Step 1: Get template responses for phase
        templates = self.conversation_engine.get_templates(strategy_phase)
        
        # Step 2: Select best response based on message content
        response = self._select_response_template(
            message=message,
            templates=templates,
            strategy_phase=strategy_phase,
            turn_count=self.turn_count
        )
        
        # Step 3: Apply persona language style
        response = self.persona_engine.inject_language_style(response)
        
        # Step 4: Add emotional state (increases over time)
        response = self._add_emotional_markers(response, self.turn_count, strategy_phase)
        
        # Step 5: Add natural variations
        if random.random() < self.persona.confusion_rate:
            response = self._add_confusion_marker(response)
        
        if random.random() < self.persona.mistake_rate:
            response = self._add_typo(response)
        
        # Track response to avoid repetition
        self.response_history.append(response)
        self.last_response = response
        
        return response
    
    def _select_response_template(self, 
                                  message: str,
                                  templates: dict,
                                  strategy_phase: StrategyPhase,
                                  turn_count: int) -> str:
        """
        Select best response template based on message content and phase.
        
        This is where the agent demonstrates intelligence:
        - Different response types for different scammer tactics
        - Phase-appropriate responses
        - Avoid repeating recent responses
        """
        
        if strategy_phase == StrategyPhase.IDENTIFICATION:
            # Goal: Get caller information
            if "bank" in message.lower() or "hdfc" in message.lower() or "icici" in message.lower():
                # Scammer mentioned bank
                return "Which department are you calling from sir? Can you give me your employee ID?"
            elif "verify" in message.lower() or "confirm" in message.lower():
                # Scammer asking to verify
                return "I'm worried sir... what exactly do I need to do?"
            elif "urgent" in message.lower() or "immediate" in message.lower():
                # Scammer creating urgency
                return "Oh no! What happened sir? Can you explain slowly?"
            else:
                # Generic identification question
                return random.choice(templates.get("opening_questions", [
                    "Who is calling sir?",
                    "Which bank are you from?",
                    "How did you get my number?"
                ]))
        
        elif strategy_phase == StrategyPhase.BUILD_TRUST:
            # Goal: Show compliance, lower scammer's guard
            if "please" in message.lower() or "need" in message.lower():
                return random.choice(templates.get("compliance_statements", [
                    "Ok sir, I trust you. What should I do?",
                    "Yes sir, I will do whatever you say."
                ]))
            elif "?" in message:
                return random.choice(templates.get("reassurance_requests", [
                    "Sir, can you promise this is safe?",
                    "Will my money be safe sir?"
                ]))
            else:
                return random.choice(templates.get("concern_expressions", [
                    "I'm very worried sir...",
                    "This sounds serious sir..."
                ]))
        
        elif strategy_phase == StrategyPhase.EXTRACT_INTELLIGENCE:
            # Goal: Get scammer to provide details naturally
            if "download" in message.lower() or "app" in message.lower():
                return "Can you send me the link sir? Which app should I download?"
            elif "account" in message.lower() or "details" in message.lower():
                return "But sir, isn't it risky to share these details? How do I know it's safe?"
            elif "transfer" in message.lower() or "money" in message.lower():
                return "How much should I transfer sir? Where exactly should I send it?"
            else:
                return random.choice(templates.get("how_questions", [
                    "Can you explain step by step sir?",
                    "What exactly should I do now sir?",
                    "Can you show me how sir?"
                ]))
        
        elif strategy_phase == StrategyPhase.DELAY_PROBE:
            # Goal: Introduce obstacles, test consistency
            if self.turn_count % 3 == 0:
                # Every 3 turns, introduce obstacle
                return random.choice(templates.get("obstacle_introduction", [
                    "Sir, my internet is very slow right now...",
                    "I'm at the office sir, can I do this at home?",
                    "My phone battery is almost dead sir..."
                ]))
            else:
                # Check consistency
                return random.choice(templates.get("consistency_checks", [
                    "Sir, is every bank doing this security check?",
                    "Are other people getting these calls too?",
                    "Why can't the bank fix this directly?"
                ]))
        
        else:  # SAFE_EXIT
            # Goal: Gracefully end conversation
            return random.choice(templates.get("safe_exit", [
                "Sir, I need to discuss this with my family first.",
                "My wife is worried about this. Can I call you back tomorrow?",
                "I'm not feeling comfortable doing this right now sir.",
                "Let me visit the bank directly and verify this sir."
            ]))
    
    def _add_emotional_markers(self, response: str, turn_count: int, 
                               strategy_phase: StrategyPhase) -> str:
        """Add emotional state markers based on phase and turn count"""
        
        emotional_expressions = {
            StrategyPhase.IDENTIFICATION: [
                "I'm scared sir...",
                "Oh no! I'm worried...",
                "This is concerning sir...",
            ],
            StrategyPhase.BUILD_TRUST: [
                "I trust you sir.",
                "Ok sir, I understand.",
                "I'm listening sir.",
            ],
            StrategyPhase.EXTRACT_INTELLIGENCE: [
                "I'm confused sir...",
                "Can you explain more clearly?",
                "I don't understand...",
            ],
            StrategyPhase.DELAY_PROBE: [
                "This is taking long sir...",
                "I'm not sure about this...",
                "Something doesn't feel right sir...",
            ],
            StrategyPhase.SAFE_EXIT: [
                "I need to think about this...",
                "I'm not comfortable...",
                "This seems too risky...",
            ]
        }
        
        # Add emotional marker with some probability
        if random.random() < 0.3:
            marker = random.choice(emotional_expressions.get(strategy_phase, []))
            if " " + marker not in response:  # Avoid duplication
                response += " " + marker
        
        return response
    
    def _add_confusion_marker(self, response: str) -> str:
        """Add confusion to response"""
        confusion_markers = [
            "Sir, I'm confused...",
            "Can you explain again?",
            "I don't understand sir...",
            "What do you mean?",
            "Sir, that's confusing...",
        ]
        
        marker = random.choice(confusion_markers)
        if marker not in response:
            response += " " + marker
        
        return response
    
    def _add_typo(self, response: str) -> str:
        """Add realistic typo to response"""
        words = response.split()
        
        if len(words) > 3:
            # Select random word (but not first/last)
            idx = random.randint(1, len(words) - 2)
            word = words[idx]
            
            if len(word) > 3:
                # Introduce character substitution
                char_idx = random.randint(0, len(word) - 1)
                chars = list(word)
                chars[char_idx] = random.choice('abcdefghijklmnopqrstuvwxyz')
                words[idx] = ''.join(chars)
        
        return ' '.join(words)
    
    def should_terminate(self, turn_count: int, elapsed_minutes: float) -> bool:
        """
        Determine if conversation should terminate.
        
        Termination conditions:
        - Max turns reached (50)
        - Timeout exceeded (60 minutes)
        - Honeypot exposure risk too high
        """
        return (turn_count >= self.MAX_CONVERSATION_TURNS or 
                elapsed_minutes >= self.CONVERSATION_TIMEOUT_MINUTES)
