"""
Persona Engine - Realistic human persona simulation
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
import random
import time

class LanguageStyle(Enum):
    """Language style profiles"""
    FORMAL_ENGLISH = "formal_english"
    SEMI_FORMAL_HINDI_MIX = "semi_formal_hindi_mix"
    CASUAL_ENGLISH = "casual_english"
    BROKEN_ENGLISH = "broken_english"

class TechnicalLevel(Enum):
    """Technical proficiency levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EmotionalState(Enum):
    """Emotional states during conversation"""
    NEUTRAL = "neutral"
    FEARFUL = "fearful"
    CURIOUS = "curious"
    SKEPTICAL = "skeptical"
    EXCITED = "excited"
    CONFUSED = "confused"
    ANGRY = "angry"
    DESPERATE = "desperate"

@dataclass
class Persona:
    """Persona profile for honeypot victim"""
    name: str
    age: int
    location: str
    occupation: str
    language_style: LanguageStyle
    technical_level: TechnicalLevel
    vulnerability_factors: list
    
    # Behavioral parameters
    typical_response_time_ms: int = 3000
    confusion_rate: float = 0.3  # 30% chance of confused response
    mistake_rate: float = 0.15   # 15% chance of typos/mistakes
    memory_strength: float = 0.7  # 70% chance to remember context
    
    # Current state
    emotional_state: EmotionalState = EmotionalState.NEUTRAL
    fatigue_level: float = 0.0   # 0-1, increases over time
    trust_level: float = 0.0     # 0-1, increases with scammer engagement

class PersonaEngine:
    """Engine for managing and using persona profiles"""
    
    def __init__(self, persona: Persona):
        """Initialize with a persona"""
        self.persona = persona
        self.message_count = 0
        self.last_message_time = time.time()
        self.personality_quirks = self._generate_quirks()
        
    def _generate_quirks(self) -> dict:
        """Generate unique personality quirks based on persona"""
        return {
            "uses_sir_title": self.persona.language_style == LanguageStyle.SEMI_FORMAL_HINDI_MIX,
            "emoji_frequency": 0.2 if self.persona.age < 40 else 0.05,
            "question_suffix": "?" if random.random() > 0.3 else "?????",
            "apology_frequency": 0.4 if "trusting" in self.persona.vulnerability_factors else 0.1,
            "authority_deference": 0.8 if "trusts_authority" in self.persona.vulnerability_factors else 0.3,
            "money_concern": 0.9 if "money_conscious" in self.persona.vulnerability_factors else 0.3,
        }
    
    def inject_language_style(self, text: str) -> str:
        """Apply persona language style to text"""
        if self.persona.language_style == LanguageStyle.SEMI_FORMAL_HINDI_MIX:
            # Add Hindi-English code-switching
            text = self._add_hindi_elements(text)
        elif self.persona.language_style == LanguageStyle.BROKEN_ENGLISH:
            # Add grammatical inconsistencies
            text = self._add_grammatical_errors(text)
        elif self.persona.language_style == LanguageStyle.CASUAL_ENGLISH:
            # Make more casual/informal
            text = self._casualize_text(text)
        
        # Add personality-specific markers
        if self.personality_quirks["uses_sir_title"] and "?" in text:
            text = text.replace("?", " sir?")
        
        # Add apologies if character is apologetic
        if random.random() < self.personality_quirks["apology_frequency"]:
            text = f"Sorry, {text}"
        
        return text
    
    def _add_hindi_elements(self, text: str) -> str:
        """Add Hindi-English code-switching"""
        hindi_elements = {
            "okay": "ok/theek hai",
            "understood": "samajh gaya",
            "what": "kya/what",
            "help me": "meri madad karo/help me",
            "thanks": "shukriya/thanks",
            "please": "please/kripaya",
        }
        
        for english, hindi_mix in hindi_elements.items():
            if english in text.lower():
                if random.random() > 0.5:
                    text = text.replace(english, hindi_mix, 1)
        
        return text
    
    def _add_grammatical_errors(self, text: str) -> str:
        """Add grammatical errors for broken English"""
        if random.random() < 0.3:
            # Remove articles
            text = text.replace("the ", "").replace("a ", "")
        
        if random.random() < 0.2:
            # Swap verb tenses
            replacements = {
                "is": "am",
                "are": "is",
                "was": "were",
                "were": "was",
            }
            for wrong, right in replacements.items():
                if wrong in text.lower() and random.random() > 0.5:
                    text = text.replace(wrong, right, 1)
        
        return text
    
    def _casualize_text(self, text: str) -> str:
        """Make text more casual/informal"""
        casual_replacements = {
            "thank you": "thanks",
            "please": "pls",
            "okay": "ok",
            "understand": "get it",
        }
        
        for formal, casual in casual_replacements.items():
            text = text.replace(formal, casual)
        
        return text
    
    def inject_mistakes(self, text: str) -> str:
        """Inject typos and mistakes based on mistake_rate"""
        if random.random() > self.persona.mistake_rate:
            return text
        
        # Introduce a typo
        if len(text) > 3:
            words = text.split()
            typo_word_idx = random.randint(0, len(words) - 1)
            word = words[typo_word_idx]
            
            if len(word) > 2:
                # Swap adjacent letters
                idx = random.randint(0, len(word) - 2)
                typo_word = word[:idx] + word[idx+1] + word[idx] + word[idx+2:]
                words[typo_word_idx] = typo_word
            
            text = " ".join(words)
        
        return text
    
    def calculate_response_delay(self) -> float:
        """Calculate realistic response delay in seconds"""
        base_delay = self.persona.typical_response_time_ms / 1000.0
        
        # Add fatigue factor (slower as conversation progresses)
        fatigue_factor = 1.0 + (self.persona.fatigue_level * 0.5)
        
        # Add emotional state factor
        emotional_delays = {
            EmotionalState.CONFUSED: 2.0,
            EmotionalState.FEARFUL: 1.5,
            EmotionalState.EXCITED: 0.5,
            EmotionalState.NEUTRAL: 1.0,
        }
        emotional_factor = emotional_delays.get(self.persona.emotional_state, 1.0)
        
        # Add randomness (±30%)
        randomness = random.uniform(0.7, 1.3)
        
        total_delay = base_delay * fatigue_factor * emotional_factor * randomness
        return total_delay
    
    def update_emotional_state(self, scammer_message: str, extracted_entities: dict):
        """Update emotional state based on scammer interaction"""
        message_lower = scammer_message.lower()
        
        # Fear triggers
        if any(word in message_lower for word in ["blocked", "locked", "suspended", "urgent"]):
            self.persona.emotional_state = EmotionalState.FEARFUL
            self.persona.trust_level = min(self.persona.trust_level + 0.1, 1.0)
        
        # Confusion triggers
        elif any(word in message_lower for word in ["verify", "authenticate", "confirm", "download"]):
            self.persona.emotional_state = EmotionalState.CONFUSED
        
        # Excitement triggers (reward promises)
        elif any(word in message_lower for word in ["won", "prize", "reward", "claim"]):
            self.persona.emotional_state = EmotionalState.EXCITED
            self.persona.trust_level = min(self.persona.trust_level + 0.15, 1.0)
        
        # Default neutral
        else:
            self.persona.emotional_state = EmotionalState.NEUTRAL
        
        # Increase fatigue with each message
        self.persona.fatigue_level = min(self.persona.fatigue_level + 0.05, 1.0)
        
        # Increase message count
        self.message_count += 1
    
    def should_show_confusion(self) -> bool:
        """Determine if victim should show confusion"""
        # Higher chance if low technical level
        if self.persona.technical_level == TechnicalLevel.VERY_LOW:
            return random.random() < self.persona.confusion_rate
        elif self.persona.technical_level == TechnicalLevel.LOW:
            return random.random() < self.persona.confusion_rate * 0.7
        
        return False
    
    def should_remember_detail(self) -> bool:
        """Determine if victim remembers previous detail"""
        return random.random() < self.persona.memory_strength
    
    def get_persona_info(self) -> dict:
        """Get current persona information"""
        return {
            "name": self.persona.name,
            "age": self.persona.age,
            "location": self.persona.location,
            "occupation": self.persona.occupation,
            "language_style": self.persona.language_style.value,
            "technical_level": self.persona.technical_level.value,
            "vulnerability_factors": self.persona.vulnerability_factors,
            "emotional_state": self.persona.emotional_state.value,
            "fatigue_level": round(self.persona.fatigue_level, 2),
            "trust_level": round(self.persona.trust_level, 2),
            "message_count": self.message_count,
        }

# Pre-defined personas
PERSONAS = {
    "rajesh_kumar": Persona(
        name="Rajesh Kumar",
        age=58,
        location="Bangalore",
        occupation="Retired Bank Manager",
        language_style=LanguageStyle.SEMI_FORMAL_HINDI_MIX,
        technical_level=TechnicalLevel.VERY_LOW,
        vulnerability_factors=["isolation", "trusts_authority", "money_conscious", "recent_retirement"],
        typical_response_time_ms=3500,
        confusion_rate=0.35,
        mistake_rate=0.2,
        memory_strength=0.65,
    ),
    "priya_sharma": Persona(
        name="Priya Sharma",
        age=32,
        location="Mumbai",
        occupation="Homemaker",
        language_style=LanguageStyle.CASUAL_ENGLISH,
        technical_level=TechnicalLevel.LOW,
        vulnerability_factors=["family_pressure", "financial_worry", "trusts_online_content"],
        typical_response_time_ms=2500,
        confusion_rate=0.25,
        mistake_rate=0.1,
        memory_strength=0.75,
    ),
    "arjun_nair": Persona(
        name="Arjun Nair",
        age=45,
        location="Delhi",
        occupation="Small Business Owner",
        language_style=LanguageStyle.BROKEN_ENGLISH,
        technical_level=TechnicalLevel.LOW,
        vulnerability_factors=["business_pressure", "greed", "overconfidence"],
        typical_response_time_ms=2000,
        confusion_rate=0.2,
        mistake_rate=0.15,
        memory_strength=0.8,
    ),
}

def get_persona(persona_name: str = "rajesh_kumar") -> PersonaEngine:
    """Get persona engine instance"""
    if persona_name not in PERSONAS:
        persona_name = "rajesh_kumar"
    
    return PersonaEngine(PERSONAS[persona_name])
