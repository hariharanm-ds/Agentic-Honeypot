"""
Memory Manager - Conversation state & conversation history management
Thread-safe, in-memory store optimized for serverless deployment
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import threading

@dataclass
class Message:
    """Single message in conversation"""
    role: str  # 'scammer' or 'victim'
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    scam_indicators: List[str] = field(default_factory=list)
    extracted_entities: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ConversationState:
    """Current state of conversation"""
    conversation_id: str
    persona_name: str = ""
    scam_detected: bool = False
    scam_type: Optional[str] = None
    current_strategy: str = "identification"
    emotional_state: str = "neutral"
    trust_level: float = 0.0
    honeypot_exposure_risk: float = 0.0
    intelligence_quality_score: float = 0.0

class MemoryStore:
    """
    Single conversation memory store.
    Tracks message history, extracted intelligence, and conversation state.
    """
    
    def __init__(self, conversation_id: str, persona_name: str = ""):
        """Initialize memory store for a conversation"""
        self.conversation_id = conversation_id
        self.persona_name = persona_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_activity = datetime.now()
        
        # Message history
        self.message_history: List[Message] = []
        
        # Conversation state
        self.current_state = ConversationState(
            conversation_id=conversation_id,
            persona_name=persona_name
        )
        
        # Extracted intelligence storage
        self.extracted_intelligence = {
            "upi_ids": [],
            "phone_numbers": [],
            "bank_accounts": [],
            "phishing_links": [],
            "email_addresses": []
        }
        
        # Scammer intelligence
        self.scammer_profile = {
            "opening_script": None,
            "bank_names_mentioned": [],
            "urgency_signals": [],
            "threat_mentions": [],
            "reward_promises": [],
            "technical_requests": [],
            "emotional_tactics": []
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
        self.last_activity = datetime.now()
        
        return message
    
    def get_recent_messages(self, n: int = 10) -> List[Message]:
        """Get last n messages for context"""
        return self.message_history[-n:]
    
    def get_turn_count(self) -> int:
        """Get current turn number"""
        return len(self.message_history) // 2
    
    def get_elapsed_minutes(self) -> float:
        """Get elapsed conversation time in minutes"""
        return (datetime.now() - self.created_at).total_seconds() / 60
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "conversation_id": self.conversation_id,
            "persona_name": self.persona_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "turn_count": self.get_turn_count(),
            "elapsed_minutes": round(self.get_elapsed_minutes(), 2),
            "current_state": asdict(self.current_state),
            "extracted_intelligence": self.extracted_intelligence,
            "scammer_profile": self.scammer_profile
        }

class MemoryManager:
    """
    Thread-safe manager for all conversation memory stores.
    Handles conversation creation, retrieval, and cleanup.
    
    Optimized for serverless:
    - No database calls in hot path
    - In-memory storage (cache-friendly)
    - Thread-safe for concurrent requests
    - Automatic cleanup of old conversations
    """
    
    # Configuration
    MAX_STORED_CONVERSATIONS = 1000
    CONVERSATION_RETENTION_MINUTES = 120  # Keep for 2 hours
    
    def __init__(self):
        """Initialize memory manager"""
        self.conversations: Dict[str, MemoryStore] = {}
        self.lock = threading.Lock()  # Thread safety
        self.creation_times: Dict[str, datetime] = {}
    
    def get_or_create(self, conversation_id: str, persona_name: str = "") -> MemoryStore:
        """Get existing conversation or create new one"""
        with self.lock:
            if conversation_id in self.conversations:
                return self.conversations[conversation_id]
            
            # Create new conversation
            memory_store = MemoryStore(conversation_id, persona_name)
            self.conversations[conversation_id] = memory_store
            self.creation_times[conversation_id] = datetime.now()
            
            # Cleanup old conversations if needed
            if len(self.conversations) > self.MAX_STORED_CONVERSATIONS:
                self._cleanup_old_conversations()
            
            return memory_store
    
    def get(self, conversation_id: str) -> Optional[MemoryStore]:
        """Get conversation by ID"""
        with self.lock:
            return self.conversations.get(conversation_id)
    
    def get_active_count(self) -> int:
        """Get count of active conversations"""
        with self.lock:
            return len(self.conversations)
    
    def get_scam_count_today(self) -> int:
        """Get count of scam detections"""
        with self.lock:
            count = 0
            for memory in self.conversations.values():
                if memory.current_state.scam_detected:
                    count += 1
            return count
    
    def get_total_intelligence_count(self) -> int:
        """Get total extracted intelligence items"""
        with self.lock:
            count = 0
            for memory in self.conversations.values():
                for entity_list in memory.extracted_intelligence.values():
                    count += len(entity_list)
            return count
    
    def _cleanup_old_conversations(self):
        """Remove conversations older than retention time"""
        now = datetime.now()
        to_delete = []
        
        for conv_id, creation_time in self.creation_times.items():
            age_minutes = (now - creation_time).total_seconds() / 60
            if age_minutes > self.CONVERSATION_RETENTION_MINUTES:
                to_delete.append(conv_id)
        
        for conv_id in to_delete:
            del self.conversations[conv_id]
            del self.creation_times[conv_id]
    
    def get_or_create_agent(self, conversation_id: str):
        """Placeholder for agent creation (handled in api_complete.py)"""
        pass
    
    def export_conversation(self, conversation_id: str) -> Optional[dict]:
        """Export conversation for logging/analysis"""
        with self.lock:
            memory = self.conversations.get(conversation_id)
            if memory:
                return memory.to_dict()
            return None
