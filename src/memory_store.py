"""
Memory & Context Store - Conversation history and pattern tracking
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

@dataclass
class Message:
    """Single message in conversation"""
    role: str  # 'scammer' or 'victim'
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    scam_indicators: List[str] = field(default_factory=list)
    extracted_entities: Dict = field(default_factory=dict)

@dataclass
class ConversationState:
    """Current state of conversation"""
    conversation_id: str
    persona_name: str
    scam_detected: bool = False
    scam_type: Optional[str] = None
    current_strategy: str = "identification"
    emotional_state: str = "neutral"
    trust_level: float = 0.0
    honeypot_exposure_risk: float = 0.0

class MemoryStore:
    """Memory store for honeypot conversations"""
    
    def __init__(self, conversation_id: str, persona_name: str):
        """Initialize memory store"""
        self.conversation_id = conversation_id
        self.persona_name = persona_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Short-term memory (active conversation)
        self.message_history: List[Message] = []
        self.current_state = ConversationState(
            conversation_id=conversation_id,
            persona_name=persona_name
        )
        
        # Tracked entities across conversation
        self.mentioned_entities = defaultdict(list)
        
        # Long-term memory (intelligence repository)
        self.extracted_intelligence = {
            "upi_ids": [],
            "phone_numbers": [],
            "bank_accounts": [],
            "phishing_links": [],
            "email_addresses": []
        }
        
        self.behavior_patterns = {
            "opening_script": None,
            "urgency_level": "unknown",
            "escalation_points": [],
            "reward_promises": [],
            "threat_mentions": [],
        }
        
        self.operational_metrics = {
            "estimated_skill_level": "unknown",
            "targeting_method": "unknown",
            "response_consistency": [],
            "time_pressure_applied": False,
            "involvement_level": "single_scammer"
        }
    
    def add_message(self, role: str, content: str, 
                   scam_indicators: List[str] = None,
                   extracted_entities: Dict = None) -> Message:
        """Add message to conversation history"""
        message = Message(
            role=role,
            content=content,
            scam_indicators=scam_indicators or [],
            extracted_entities=extracted_entities or {}
        )
        
        self.message_history.append(message)
        self.updated_at = datetime.now()
        
        # Track entities
        if extracted_entities:
            for entity_type, entities in extracted_entities.items():
                if entities:
                    self.mentioned_entities[entity_type].extend(entities)
        
        return message
    
    def get_recent_messages(self, n: int = 5) -> List[Message]:
        """Get last n messages"""
        return self.message_history[-n:]
    
    def get_full_conversation(self) -> str:
        """Get full conversation as formatted string"""
        lines = []
        for msg in self.message_history:
            role = "SCAMMER" if msg.role == "scammer" else "VICTIM"
            lines.append(f"[{role}] {msg.content}")
        return "\n".join(lines)
    
    def update_state(self, 
                    scam_detected: bool = None,
                    scam_type: str = None,
                    strategy: str = None,
                    emotional_state: str = None,
                    trust_level: float = None,
                    exposure_risk: float = None):
        """Update conversation state"""
        if scam_detected is not None:
            self.current_state.scam_detected = scam_detected
        if scam_type is not None:
            self.current_state.scam_type = scam_type
        if strategy is not None:
            self.current_state.current_strategy = strategy
        if emotional_state is not None:
            self.current_state.emotional_state = emotional_state
        if trust_level is not None:
            self.current_state.trust_level = trust_level
        if exposure_risk is not None:
            self.current_state.honeypot_exposure_risk = exposure_risk
        
        self.updated_at = datetime.now()
    
    def add_extracted_intelligence(self, entity_type: str, value: str, 
                                  confidence: float, metadata: Dict = None):
        """Add extracted intelligence"""
        if entity_type in self.extracted_intelligence:
            self.extracted_intelligence[entity_type].append({
                "value": value,
                "confidence": confidence,
                "metadata": metadata or {},
                "first_appeared": self._find_first_mention(value),
                "appearance_count": self._count_mentions(value)
            })
    
    def add_behavior_pattern(self, pattern_type: str, value: Any):
        """Add observed behavior pattern"""
        if pattern_type in self.behavior_patterns:
            if isinstance(self.behavior_patterns[pattern_type], list):
                self.behavior_patterns[pattern_type].append(value)
            else:
                self.behavior_patterns[pattern_type] = value
    
    def add_operational_metric(self, metric_type: str, value: Any):
        """Add operational metric"""
        if metric_type in self.operational_metrics:
            self.operational_metrics[metric_type] = value
    
    def _find_first_mention(self, value: str) -> Optional[str]:
        """Find when value was first mentioned"""
        for msg in self.message_history:
            if value in msg.content:
                return msg.timestamp
        return None
    
    def _count_mentions(self, value: str) -> int:
        """Count how many times value is mentioned"""
        count = 0
        for msg in self.message_history:
            if value in msg.content:
                count += 1
        return count
    
    def get_entity_by_type(self, entity_type: str) -> List[Dict]:
        """Get all extracted entities of a type"""
        return self.extracted_intelligence.get(entity_type, [])
    
    def get_high_confidence_entities(self, threshold: float = 0.8) -> Dict:
        """Get entities above confidence threshold"""
        result = {}
        for entity_type, entities in self.extracted_intelligence.items():
            high_confidence = [e for e in entities if e["confidence"] >= threshold]
            if high_confidence:
                result[entity_type] = high_confidence
        return result
    
    def calculate_extraction_score(self) -> float:
        """Calculate overall extraction score (0-1)"""
        total_entities = sum(len(e) for e in self.extracted_intelligence.values())
        
        if total_entities == 0:
            return 0.0
        
        # Weight different entity types
        weighted_total = (
            len(self.extracted_intelligence["phishing_links"]) * 1.0 +  # High value
            len(self.extracted_intelligence["upi_ids"]) * 0.9 +
            len(self.extracted_intelligence["phone_numbers"]) * 0.7 +
            len(self.extracted_intelligence["bank_accounts"]) * 0.8 +
            len(self.extracted_intelligence["email_addresses"]) * 0.5
        )
        
        # Normalize: assume max ~10 weighted entities
        score = min(weighted_total / 10, 1.0)
        return round(score, 2)
    
    def get_memory_summary(self) -> Dict:
        """Get summary of memory state"""
        return {
            "conversation_id": self.conversation_id,
            "persona": self.persona_name,
            "duration_minutes": round((self.updated_at - self.created_at).total_seconds() / 60, 1),
            "message_count": len(self.message_history),
            "scammer_messages": sum(1 for m in self.message_history if m.role == "scammer"),
            "victim_messages": sum(1 for m in self.message_history if m.role == "victim"),
            "current_state": asdict(self.current_state),
            "unique_entities_count": sum(len(e) for e in self.extracted_intelligence.values()),
            "high_confidence_entities": len(self.get_high_confidence_entities()),
            "extraction_score": self.calculate_extraction_score(),
            "mentioned_entity_types": {
                k: len(v) for k, v in self.mentioned_entities.items() if v
            }
        }
    
    def should_avoid_repetition(self, question: str) -> bool:
        """Check if we've already asked similar question"""
        # Simple string similarity check
        question_lower = question.lower()
        for msg in self.message_history:
            if msg.role == "victim":
                if question_lower[:20] in msg.content.lower():
                    return True
        return False
    
    def export_to_dict(self) -> Dict:
        """Export complete memory state to dictionary"""
        return {
            "conversation_id": self.conversation_id,
            "persona_name": self.persona_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_history": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "scam_indicators": m.scam_indicators,
                    "extracted_entities": m.extracted_entities
                }
                for m in self.message_history
            ],
            "current_state": asdict(self.current_state),
            "extracted_intelligence": self.extracted_intelligence,
            "behavior_patterns": self.behavior_patterns,
            "operational_metrics": self.operational_metrics,
            "summary": self.get_memory_summary()
        }

class MemoryManager:
    """Manager for multiple conversation memories"""
    
    def __init__(self):
        """Initialize memory manager"""
        self.active_conversations: Dict[str, MemoryStore] = {}
    
    def create_conversation(self, conversation_id: str, persona_name: str) -> MemoryStore:
        """Create new conversation memory"""
        memory = MemoryStore(conversation_id, persona_name)
        self.active_conversations[conversation_id] = memory
        return memory
    
    def get_conversation(self, conversation_id: str) -> Optional[MemoryStore]:
        """Get existing conversation memory"""
        return self.active_conversations.get(conversation_id)
    
    def delete_conversation(self, conversation_id: str):
        """Delete conversation memory"""
        if conversation_id in self.active_conversations:
            del self.active_conversations[conversation_id]
    
    def get_active_count(self) -> int:
        """Get number of active conversations"""
        return len(self.active_conversations)
