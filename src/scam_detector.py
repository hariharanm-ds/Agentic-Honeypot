"""
Scam Detection Engine - Pattern matching, NLP classification, and confidence scoring
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

# Download required NLTK data (uncomment on first run)
# nltk.download('vader_lexicon')
# nltk.download('punkt')

class ScamType(Enum):
    """Enumeration of scam types"""
    PHISHING_UPI = "phishing_upi"
    PHISHING_BANKING = "phishing_banking"
    PHISHING_CREDENTIALS = "phishing_credentials"
    LOTTERY_SCAM = "lottery_scam"
    ROMANCE_SCAM = "romance_scam"
    INVESTMENT_FRAUD = "investment_fraud"
    TAX_FRAUD = "tax_fraud"
    TECH_SUPPORT_SCAM = "tech_support_scam"
    UNKNOWN = "unknown"

@dataclass
class ScamDetectionResult:
    """Result of scam detection"""
    is_scam: bool
    scam_type: ScamType
    confidence: float
    detection_method: str
    extracted_keywords: List[str]
    explanation: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "is_scam": self.is_scam,
            "scam_type": self.scam_type.value,
            "confidence": round(self.confidence, 3),
            "detection_method": self.detection_method,
            "extracted_keywords": self.extracted_keywords,
            "explanation": self.explanation
        }

class ScamDetectionEngine:
    """Scam Detection Engine using pattern matching and NLP"""
    
    def __init__(self):
        """Initialize detection engine"""
        self.sia = SentimentIntensityAnalyzer()
        self.pattern_database = self._build_pattern_database()
        self.keyword_weights = self._build_keyword_weights()
        
    def _build_pattern_database(self) -> Dict[ScamType, List[Dict]]:
        """Build database of scam patterns"""
        return {
            ScamType.PHISHING_UPI: [
                {
                    "name": "upi_verification",
                    "patterns": [
                        r"verify.*upi|upi.*verify",
                        r"confirm.*upi|upi.*confirm",
                        r"update.*upi|upi.*update",
                        r"@[a-zA-Z0-9._-]+"
                    ],
                    "keywords": ["verify", "upi", "urgent", "confirm"],
                    "weight": 0.8
                },
                {
                    "name": "account_compromise",
                    "patterns": [
                        r"account.*compr|hack|compromis",
                        r"unauthorized.*access",
                        r"suspicious.*activ"
                    ],
                    "keywords": ["account", "compromised", "hacked", "unauthorized"],
                    "weight": 0.7
                }
            ],
            ScamType.PHISHING_BANKING: [
                {
                    "name": "banking_credential_request",
                    "patterns": [
                        r"confirm.*password|password.*confirm",
                        r"verify.*account|account.*verify",
                        r"banking.*details|credentials"
                    ],
                    "keywords": ["password", "username", "credentials", "login"],
                    "weight": 0.85
                },
                {
                    "name": "bank_impersonation",
                    "patterns": [
                        r"from\s+(?:hdfc|icici|axis|sbi|yes|bob)",
                        r"(?:hdfc|icici|axis|sbi|yes|bob).*bank"
                    ],
                    "keywords": ["bank", "security", "fraud", "alert"],
                    "weight": 0.75
                }
            ],
            ScamType.LOTTERY_SCAM: [
                {
                    "name": "lottery_winning",
                    "patterns": [
                        r"won.*lottery|lottery.*won",
                        r"prize.*claim|claim.*prize",
                        r"congratulation|winner"
                    ],
                    "keywords": ["winner", "won", "prize", "congratulations"],
                    "weight": 0.8
                }
            ],
            ScamType.INVESTMENT_FRAUD: [
                {
                    "name": "investment_promise",
                    "patterns": [
                        r"invest.*return|return.*invest",
                        r"guarantee.*profit|profit.*guarantee",
                        r"double.*money|triple.*return"
                    ],
                    "keywords": ["invest", "profit", "return", "guarantee", "double"],
                    "weight": 0.8
                }
            ]
        }
    
    def _build_keyword_weights(self) -> Dict[str, float]:
        """Build keyword weight dictionary"""
        return {
            # High urgency indicators
            "urgent": 0.9,
            "immediately": 0.9,
            "quickly": 0.8,
            "asap": 0.85,
            "emergency": 0.85,
            
            # Verification/confirmation
            "verify": 0.8,
            "confirm": 0.7,
            "validate": 0.75,
            "authenticate": 0.8,
            
            # Threat indicators
            "blocked": 0.85,
            "locked": 0.8,
            "suspended": 0.8,
            "compromised": 0.9,
            "hacked": 0.9,
            "unauthorized": 0.85,
            
            # Authority markers
            "bank": 0.6,
            "security": 0.6,
            "fraud": 0.7,
            "officer": 0.6,
            "official": 0.5,
            
            # Financial terms
            "otp": 0.85,
            "password": 0.8,
            "credentials": 0.8,
            "account": 0.6,
            "balance": 0.5,
        }
    
    def detect(self, message: str, conversation_history: List[str] = None) -> ScamDetectionResult:
        """
        Detect if message is a scam
        
        Args:
            message: Raw message text
            conversation_history: Previous messages in conversation (optional)
            
        Returns:
            ScamDetectionResult object
        """
        message_lower = message.lower()
        
        # Calculate pattern-based score
        pattern_score, matched_patterns = self._calculate_pattern_score(message_lower)
        
        # Calculate NLP-based score
        nlp_score = self._calculate_nlp_score(message)
        
        # Calculate keyword score
        keyword_score, matched_keywords = self._calculate_keyword_score(message_lower)
        
        # Combine scores - increased pattern weight
        combined_score = (pattern_score * 0.5 + nlp_score * 0.3 + keyword_score * 0.2)
        
        # Determine scam type
        scam_type = self._classify_scam_type(message_lower, matched_patterns)
        
        # Is it a scam? - Threshold at 0.30 to catch clear phishing attempts
        is_scam = combined_score > 0.30
        
        # Build explanation
        explanation = self._build_explanation(matched_patterns, matched_keywords, combined_score)
        
        return ScamDetectionResult(
            is_scam=is_scam,
            scam_type=scam_type,
            confidence=combined_score,
            detection_method="pattern_matching + nlp + keywords",
            extracted_keywords=matched_keywords,
            explanation=explanation
        )
    
    def _calculate_pattern_score(self, message: str) -> Tuple[float, List[str]]:
        """Calculate pattern matching score"""
        matches = []
        total_weight = 0
        matched_count = 0
        
        for scam_type, patterns in self.pattern_database.items():
            for pattern_group in patterns:
                for pattern in pattern_group["patterns"]:
                    if re.search(pattern, message, re.IGNORECASE):
                        matches.append(pattern_group["name"])
                        total_weight += pattern_group["weight"]
                        matched_count += 1
        
        # Normalize score: more matches = higher confidence
        if matched_count == 0:
            return 0.0, []
        
        # Cap at 1.0 and apply diminishing returns
        score = min(matched_count * 0.3, 1.0)
        return score, matches
    
    def _calculate_nlp_score(self, message: str) -> float:
        """Calculate NLP-based score"""
        try:
            # Sentiment analysis - scams often use negative/urgent sentiment
            sentiment = self.sia.polarity_scores(message)
            
            # High negative compound score = concern/threat language
            negative_score = max(0, -sentiment['compound']) * 0.7  # Compound ranges -1 to 1
            
            # Check for imperative/command language (common in scams)
            words = word_tokenize(message.lower())
            imperatives = 0
            for word in words:
                if word.endswith('!') or word.endswith('?'):
                    imperatives += 1
            
            imperative_score = min(imperatives / max(len(words), 1), 1.0) * 0.5
            
            # Urgency language detection
            urgency_keywords = ["must", "should", "need to", "have to", "immediately"]
            urgency_count = sum(1 for keyword in urgency_keywords if keyword in message.lower())
            urgency_score = min(urgency_count / 5, 1.0) * 0.6
            
            combined_nlp = (negative_score * 0.4 + imperative_score * 0.3 + urgency_score * 0.3)
            return min(combined_nlp, 1.0)
        except Exception as e:
            print(f"NLP error: {e}")
            return 0.0
    
    def _calculate_keyword_score(self, message: str) -> Tuple[float, List[str]]:
        """Calculate keyword-based score"""
        matched_keywords = []
        total_weight = 0
        
        for keyword, weight in self.keyword_weights.items():
            if re.search(r'\b' + keyword + r'\b', message, re.IGNORECASE):
                matched_keywords.append(keyword)
                total_weight += weight
        
        if len(matched_keywords) == 0:
            return 0.0, []
        
        # Average weight of matched keywords
        avg_weight = total_weight / len(matched_keywords)
        return avg_weight, matched_keywords
    
    def _classify_scam_type(self, message: str, matched_patterns: List[str]) -> ScamType:
        """Classify scam type based on patterns"""
        if not matched_patterns:
            return ScamType.UNKNOWN
        
        # Simple classification based on matched patterns
        message_lower = message.lower()
        
        if any(pat in matched_patterns for pat in ["upi_verification", "account_compromise"]):
            if "@" in message_lower:
                return ScamType.PHISHING_UPI
            return ScamType.PHISHING_BANKING
        
        if any(pat in matched_patterns for pat in ["banking_credential_request", "bank_impersonation"]):
            return ScamType.PHISHING_BANKING
        
        if any(pat in matched_patterns for pat in ["lottery_winning"]):
            return ScamType.LOTTERY_SCAM
        
        if any(pat in matched_patterns for pat in ["investment_promise"]):
            return ScamType.INVESTMENT_FRAUD
        
        return ScamType.UNKNOWN
    
    def _build_explanation(self, patterns: List[str], keywords: List[str], score: float) -> str:
        """Build human-readable explanation"""
        if score < 0.5:
            return "Message does not match known scam patterns"
        
        explanation_parts = []
        
        if patterns:
            explanation_parts.append(f"Matched patterns: {', '.join(set(patterns))}")
        
        if keywords:
            explanation_parts.append(f"Scam keywords detected: {', '.join(keywords[:3])}")
        
        explanation_parts.append(f"Confidence: {score:.1%}")
        
        return "; ".join(explanation_parts)
