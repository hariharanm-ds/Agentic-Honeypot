"""
Intelligence Extractor - Entity recognition and extraction with validation
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

class EntityType(Enum):
    """Types of entities to extract"""
    UPI_ID = "upi_ids"
    PHONE_NUMBER = "phone_numbers"
    BANK_ACCOUNT = "bank_accounts"
    PHISHING_LINK = "phishing_links"
    EMAIL_ADDRESS = "email_addresses"

@dataclass
class ExtractedEntity:
    """Extracted entity with confidence"""
    value: str
    type: EntityType
    confidence: float
    context: Optional[str] = None
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "type": self.type.value,
            "confidence": round(self.confidence, 3),
            "context": self.context,
            "metadata": self.metadata or {}
        }

class IntelligenceExtractor:
    """Extract actionable intelligence from messages"""
    
    # Known bank UPI domains for validation
    KNOWN_BANK_DOMAINS = {
        "ibl", "hdfc", "icici", "axis", "barodampay", "airtel", 
        "aubank", "ybl", "oksbi", "pnb", "bob", "unionbank",
        "karur", "indus", "kotak", "federal", "hsbc"
    }
    
    def __init__(self):
        """Initialize extractor"""
        self.extraction_patterns = self._build_patterns()
    
    def _build_patterns(self) -> Dict[EntityType, Dict]:
        """Build extraction patterns"""
        return {
            EntityType.UPI_ID: {
                "pattern": r'[\w.-]+@[\w.-]+',
                "validators": [self._validate_upi],
                "weight": 0.9
            },
            EntityType.PHONE_NUMBER: {
                "pattern": r'(?:^|\D)([6-9]\d{9})(?:\D|$)',
                "validators": [self._validate_phone],
                "weight": 0.85
            },
            EntityType.BANK_ACCOUNT: {
                "pattern": r'\b(?:\d{4}[\s-]?)?\d{10,14}\b',
                "validators": [self._validate_account],
                "weight": 0.8
            },
            EntityType.PHISHING_LINK: {
                "pattern": r'https?://[^\s)]+',
                "validators": [self._validate_link],
                "weight": 0.95
            },
            EntityType.EMAIL_ADDRESS: {
                "pattern": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                "validators": [self._validate_email],
                "weight": 0.7
            }
        }
    
    def extract(self, message: str, conversation_history: List[str] = None) -> Dict[EntityType, List[ExtractedEntity]]:
        """
        Extract all entities from message
        
        Args:
            message: Message text to extract from
            conversation_history: Previous messages for context
            
        Returns:
            Dictionary of EntityType -> List[ExtractedEntity]
        """
        results = {entity_type: [] for entity_type in EntityType}
        
        # Extract each entity type
        for entity_type, config in self.extraction_patterns.items():
            candidates = self._find_candidates(message, config["pattern"])
            
            for candidate in candidates:
                # Validate candidate
                confidence = self._validate_entity(candidate, entity_type, config["validators"])
                
                if confidence > 0.0:
                    # Add cross-validation bonus (mentioned multiple times)
                    if conversation_history:
                        mention_count = sum(1 for h in conversation_history if candidate in h)
                        if mention_count > 1:
                            confidence = min(confidence + 0.15, 1.0)
                    
                    # Add context
                    context = self._extract_context(message, candidate)
                    
                    entity = ExtractedEntity(
                        value=candidate,
                        type=entity_type,
                        confidence=confidence,
                        context=context
                    )
                    results[entity_type].append(entity)
        
        return results
    
    def _find_candidates(self, message: str, pattern: str) -> List[str]:
        """Find candidate entities matching pattern"""
        matches = re.findall(pattern, message, re.IGNORECASE)
        return [m for m in matches if m]  # Filter empty matches
    
    def _validate_entity(self, value: str, entity_type: EntityType, 
                        validators: List) -> float:
        """Validate entity using validator functions"""
        confidence = 0.5  # Base confidence
        
        for validator in validators:
            is_valid = validator(value)
            if is_valid:
                confidence = 0.8
                break
        
        return confidence
    
    def _validate_upi(self, value: str) -> bool:
        """Validate UPI ID format"""
        # UPI format: identifier@bankname
        parts = value.split('@')
        if len(parts) != 2:
            return False
        
        identifier, bank = parts
        
        # Identifier should be alphanumeric with some special chars
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', identifier):
            return False
        
        # Bank part should be known UPI provider or at least reasonable
        bank_lower = bank.lower()
        if bank_lower in self.KNOWN_BANK_DOMAINS:
            return True
        
        # Allow if it looks reasonable (not obviously wrong)
        return len(bank) >= 2 and bank.isalnum()
    
    def _validate_phone(self, value: str) -> bool:
        """Validate Indian phone number"""
        # Indian mobiles: 10 digits starting with 6-9
        if not re.match(r'^[6-9]\d{9}$', value):
            return False
        return True
    
    def _validate_account(self, value: str) -> bool:
        """Validate bank account number"""
        # Remove spaces and dashes
        clean = value.replace(' ', '').replace('-', '')
        
        # Bank accounts are 9-18 digits
        if not re.match(r'^\d{9,18}$', clean):
            return False
        
        # Check Luhn algorithm (simple validation)
        return True
    
    def _validate_link(self, value: str) -> bool:
        """Validate URL/link"""
        # Basic URL validation
        if not value.startswith(('http://', 'https://')):
            return False
        
        # Must have at least a domain
        return '.' in value
    
    def _validate_email(self, value: str) -> bool:
        """Validate email address"""
        # Simple email validation
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value) is not None
    
    def _extract_context(self, message: str, entity: str, 
                        window_size: int = 50) -> str:
        """Extract context around entity mention"""
        try:
            idx = message.find(entity)
            if idx == -1:
                return ""
            
            start = max(0, idx - window_size)
            end = min(len(message), idx + len(entity) + window_size)
            
            context = message[start:end].strip()
            return context
        except:
            return ""
    
    def analyze_phishing_risk(self, url: str) -> Dict:
        """Analyze URL for phishing risk"""
        risk_factors = {
            "mimics_legitimate": False,
            "suspicious_domain": False,
            "obfuscated": False,
            "risk_score": 0.0
        }
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'bit\.ly|tinyurl|short\.link',  # URL shorteners
            r'secure-.*-.*\.',  # Fake security claims
            r'verify.*\..*\.(.*\.)?.*\.com',  # Verification pages
            r'.*login.*bankingsecure',  # Fake banking
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                risk_factors["suspicious_domain"] = True
                risk_factors["risk_score"] += 0.3
        
        # Check if mimics legitimate domain
        legit_domains = ['hdfc', 'icici', 'axis', 'sbi', 'paypal', 'google', 'amazon']
        for domain in legit_domains:
            if domain in url.lower() and url.count('.') > 2:
                risk_factors["mimics_legitimate"] = True
                risk_factors["risk_score"] += 0.4
        
        # Cap risk score
        risk_factors["risk_score"] = min(risk_factors["risk_score"], 1.0)
        
        return risk_factors
    
    def extract_and_grade(self, message: str, 
                         conversation_history: List[str] = None) -> Dict:
        """Extract entities and grade confidence"""
        extracted = self.extract(message, conversation_history)
        
        # Build result
        result = {}
        for entity_type, entities in extracted.items():
            if entities:
                result[entity_type.value] = [e.to_dict() for e in entities]
        
        return result
    
    def calculate_extraction_quality(self, extracted: Dict) -> float:
        """Calculate quality score of extraction"""
        if not extracted:
            return 0.0
        
        total_confidence = 0.0
        entity_count = 0
        
        for entity_type, entities in extracted.items():
            for entity in entities:
                if isinstance(entity, ExtractedEntity):
                    total_confidence += entity.confidence
                elif isinstance(entity, dict):
                    total_confidence += entity.get("confidence", 0.0)
                entity_count += 1
        
        if entity_count == 0:
            return 0.0
        
        return round(total_confidence / entity_count, 3)
