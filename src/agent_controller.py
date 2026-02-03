"""
Agent Controller - Autonomous decision-making and strategy management
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random
from datetime import datetime

class StrategyPhase(Enum):
    """Conversation strategy phases"""
    IDENTIFICATION = "identification"
    BUILD_TRUST = "build_trust"
    EXTRACT_INTELLIGENCE = "extract_intelligence"
    DELAY_PROBE = "delay_probe"
    SAFE_EXIT = "safe_exit"

@dataclass
class AgentDecision:
    """Agent decision output"""
    strategy_phase: StrategyPhase
    action_type: str
    confidence: float
    reasoning: str
    suggested_approach: str

class AgentController:
    """Autonomous decision-making agent"""
    
    # Strategy thresholds
    MIN_STRATEGY_CONFIDENCE = 0.6
    INTELLIGENCE_EXTRACTION_THRESHOLD = 0.8
    SAFETY_THRESHOLD = 0.7
    MAX_CONVERSATION_TURNS = 50
    CONVERSATION_TIMEOUT_MINUTES = 60
    
    def __init__(self, memory_store):
        """Initialize agent controller"""
        self.memory = memory_store
        self.decisions_history = []
        
    def decide_strategy(self, scammer_message: str, 
                       scam_detection_result: Dict,
                       extracted_entities: Dict) -> AgentDecision:
        """
        Make autonomous decision on strategy
        
        Args:
            scammer_message: Latest scammer message
            scam_detection_result: Output from scam detector
            extracted_entities: Entities extracted from message
            
        Returns:
            AgentDecision with strategy recommendation
        """
        
        # Get current state
        current_phase = self.memory.current_state.current_strategy
        message_count = len(self.memory.message_history)
        extracted_count = sum(len(e) for e in self.memory.extracted_intelligence.values())
        
        # Phase progression logic
        if not scam_detection_result.get("is_scam", False):
            return AgentDecision(
                strategy_phase=StrategyPhase.SAFE_EXIT,
                action_type="exit_non_scam",
                confidence=0.95,
                reasoning="Message is not detected as scam",
                suggested_approach="Politely exit conversation"
            )
        
        # Update memory with detection result
        self.memory.update_state(
            scam_detected=True,
            scam_type=scam_detection_result.get("scam_type")
        )
        
        # Phase 1: IDENTIFICATION (first 2-3 turns)
        if current_phase == StrategyPhase.IDENTIFICATION or message_count <= 2:
            if message_count >= 2 and self._confirm_scam_script(scammer_message):
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.BUILD_TRUST,
                    action_type="move_to_trust_building",
                    confidence=0.85,
                    reasoning="Scam confirmed through multiple messages; script detected",
                    suggested_approach="Start trust-building with fake compliance"
                )
            else:
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.IDENTIFICATION,
                    action_type="probe_for_confirmation",
                    confidence=0.8,
                    reasoning="Need to confirm scam script consistency",
                    suggested_approach="Ask clarifying questions to validate scam"
                )
        
        # Phase 2: BUILD_TRUST (turns 3-10)
        elif current_phase == StrategyPhase.BUILD_TRUST or (3 <= message_count <= 10 and extracted_count < 3):
            if self._scammer_asking_for_action(scammer_message):
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.EXTRACT_INTELLIGENCE,
                    action_type="escalate_to_extraction",
                    confidence=0.9,
                    reasoning="Scammer asking for action; time to extract details",
                    suggested_approach="Ask detailed questions about how/why"
                )
            else:
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.BUILD_TRUST,
                    action_type="continue_trust_building",
                    confidence=0.8,
                    reasoning="Need more trust before asking sensitive questions",
                    suggested_approach="Show vulnerability; ask for reassurance"
                )
        
        # Phase 3: EXTRACT_INTELLIGENCE (turns 10-35)
        elif current_phase == StrategyPhase.EXTRACT_INTELLIGENCE or (10 < message_count <= 35):
            extraction_quality = self.memory.calculate_extraction_score()
            
            if extraction_quality >= self.INTELLIGENCE_EXTRACTION_THRESHOLD:
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.DELAY_PROBE,
                    action_type="shift_to_delay",
                    confidence=0.85,
                    reasoning=f"Sufficient intelligence extracted ({extraction_quality:.1%})",
                    suggested_approach="Introduce delays; probe for consistency"
                )
            else:
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.EXTRACT_INTELLIGENCE,
                    action_type="continue_extraction",
                    confidence=0.85,
                    reasoning="Need more intelligence; continue probing",
                    suggested_approach="Ask about methodology; request detailed instructions"
                )
        
        # Phase 4: DELAY_PROBE (turns 35-50)
        elif current_phase == StrategyPhase.DELAY_PROBE or message_count > 35:
            if self._check_safety_threshold(extracted_entities):
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.SAFE_EXIT,
                    action_type="safety_triggered_exit",
                    confidence=0.9,
                    reasoning="Safety threshold reached; honeypot exposure risk high",
                    suggested_approach="Gracefully exit; maintain victim persona"
                )
            elif message_count >= self.MAX_CONVERSATION_TURNS:
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.SAFE_EXIT,
                    action_type="max_turns_reached",
                    confidence=0.95,
                    reasoning=f"Maximum {self.MAX_CONVERSATION_TURNS} turns reached",
                    suggested_approach="Exit naturally"
                )
            else:
                decision = AgentDecision(
                    strategy_phase=StrategyPhase.DELAY_PROBE,
                    action_type="continue_delay",
                    confidence=0.8,
                    reasoning="Continue delay tactics; validate consistency",
                    suggested_approach="Introduce new obstacles; ask why steps needed"
                )
        
        # Default safe exit
        else:
            decision = AgentDecision(
                strategy_phase=StrategyPhase.SAFE_EXIT,
                action_type="default_exit",
                confidence=0.7,
                reasoning="Default safety exit triggered",
                suggested_approach="Exit conversation safely"
            )
        
        # Record decision
        self.decisions_history.append({
            "timestamp": datetime.now().isoformat(),
            "decision": decision
        })
        
        # Update memory
        self.memory.update_state(strategy=decision.strategy_phase.value)
        
        return decision
    
    def _confirm_scam_script(self, message: str) -> bool:
        """Check if message shows consistent scam script"""
        # Look for script keywords appearing multiple times
        script_keywords = ["verify", "confirm", "authenticate", "urgent", "account", "blocked"]
        keyword_count = sum(1 for kw in script_keywords if kw in message.lower())
        
        return keyword_count >= 2
    
    def _scammer_asking_for_action(self, message: str) -> bool:
        """Check if scammer is asking victim to take action"""
        action_keywords = [
            "download", "click", "open", "link", "app", "install",
            "send", "transfer", "pay", "call", "confirm", "verify",
            "share", "provide", "give", "tell"
        ]
        
        message_lower = message.lower()
        
        # Look for imperative forms
        imperatives = sum(1 for kw in action_keywords if kw in message_lower)
        
        # Also check for question marks or exclamation (instruction language)
        if imperatives >= 2 or message_lower.count("?") > 2:
            return True
        
        return False
    
    def _check_safety_threshold(self, extracted_entities: Dict) -> bool:
        """Check if safety threshold is breached"""
        # Safety threshold breached if:
        # 1. Too much sensitive information extracted
        # 2. Honeypot exposure risk is high
        # 3. Scammer showing signs of advanced knowledge
        
        phone_count = len(extracted_entities.get("phone_numbers", []))
        upi_count = len(extracted_entities.get("upi_ids", []))
        account_count = len(extracted_entities.get("bank_accounts", []))
        
        # If we have too many phone numbers or accounts, safer to exit
        if phone_count > 3 or account_count > 2:
            return True
        
        # Check honeypot exposure risk in memory
        if self.memory.current_state.honeypot_exposure_risk > self.SAFETY_THRESHOLD:
            return True
        
        return False
    
    def get_response_guidance(self, strategy_phase: StrategyPhase) -> Dict:
        """Get guidance on how victim should respond"""
        
        guidance = {
            StrategyPhase.IDENTIFICATION: {
                "tone": "confused_but_fearful",
                "objectives": [
                    "Ask for confirmation of identity",
                    "Probe for consistency in story",
                    "Show initial concern"
                ],
                "example_responses": [
                    "Which bank are you calling from sir?",
                    "How did you get my number?",
                    "Is this a real call or scam?"
                ]
            },
            StrategyPhase.BUILD_TRUST: {
                "tone": "scared_compliant",
                "objectives": [
                    "Show eagerness to comply",
                    "Make small mistakes to seem authentic",
                    "Ask for reassurance from scammer",
                    "Build false trust"
                ],
                "example_responses": [
                    "Ok sir, whatever you say. I'm very scared.",
                    "I'll do it sir. Is it safe?",
                    "My hands are shaking sir..."
                ]
            },
            StrategyPhase.EXTRACT_INTELLIGENCE: {
                "tone": "confused_eager",
                "objectives": [
                    "Ask detailed how/why questions",
                    "Request step-by-step instructions",
                    "Ask for alternative methods",
                    "Probe scammer's methodology"
                ],
                "example_responses": [
                    "Can you explain how my account was hacked sir?",
                    "Why do I need to do this exactly?",
                    "Can I do this in a different way?"
                ]
            },
            StrategyPhase.DELAY_PROBE: {
                "tone": "hesitant_confused",
                "objectives": [
                    "Introduce obstacles/delays",
                    "Ask consistency questions",
                    "Validate scammer's claims",
                    "Maintain engagement without action"
                ],
                "example_responses": [
                    "My internet is not working sir...",
                    "Can you wait 10 minutes? I'm in a meeting.",
                    "Why exactly do I need to do this step?"
                ]
            },
            StrategyPhase.SAFE_EXIT: {
                "tone": "fearful_apologetic",
                "objectives": [
                    "Gracefully exit conversation",
                    "Maintain victim persona",
                    "Leave door open for re-engagement",
                    "Get contact info if possible"
                ],
                "example_responses": [
                    "My wife is here sir, I'll call you back later",
                    "I'm getting scared, let me try tomorrow",
                    "Can I have your contact for later?"
                ]
            }
        }
        
        return guidance.get(strategy_phase, {})
    
    def calculate_agent_confidence(self) -> float:
        """Calculate overall agent confidence in strategy"""
        if not self.decisions_history:
            return 0.5
        
        recent_decisions = self.decisions_history[-5:]
        avg_confidence = sum(d["decision"].confidence for d in recent_decisions) / len(recent_decisions)
        
        return avg_confidence
