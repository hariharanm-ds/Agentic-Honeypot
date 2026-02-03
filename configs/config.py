"""
Configuration for Agentic Honeypot System
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    USE_RELOADER = False  # Disable auto-reloader for testing
    
    # Security
    AUTHORIZED_IPS = os.getenv("AUTHORIZED_IPS", "127.0.0.1").split(",")
    API_KEYS = os.getenv("API_KEYS", "test_key_12345").split(",")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///honeypot.db")
    
    # Redis Cache
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    
    # Agent Configuration
    MAX_CONVERSATION_TURNS = int(os.getenv("MAX_CONVERSATION_TURNS", 50))
    CONVERSATION_TIMEOUT_MINUTES = int(os.getenv("CONVERSATION_TIMEOUT_MINUTES", 60))
    
    # Intelligence Extraction
    MIN_ENTITY_CONFIDENCE = float(os.getenv("MIN_ENTITY_CONFIDENCE", 0.75))
    ENABLE_REGEX_EXTRACTION = os.getenv("ENABLE_REGEX_EXTRACTION", "true").lower() == "true"
    ENABLE_NLP_EXTRACTION = os.getenv("ENABLE_NLP_EXTRACTION", "true").lower() == "true"
    
    # Safety Configuration
    HONEYPOT_EXPOSURE_THRESHOLD = float(os.getenv("HONEYPOT_EXPOSURE_THRESHOLD", 0.7))
    ENABLE_SAFETY_CHECKS = os.getenv("ENABLE_SAFETY_CHECKS", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/honeypot.log")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    AUTHORIZED_IPS = os.getenv("AUTHORIZED_IPS", "").split(",")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379

# Configuration selector
CONFIG = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv("FLASK_ENV", "development")
    return CONFIG.get(env, DevelopmentConfig)
