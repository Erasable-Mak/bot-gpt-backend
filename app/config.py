import os

class Config:
    """Configuration class that reads from environment variables"""

    # Security additional feature
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-bot-gpt-a7x9b2c8'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///botgpt.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # LLM Configuration NEED CHANGES BELOW
    # LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'groq').lower()
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'stub').lower()

    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')

    # HuggingFace settings
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
    HUGGINGFACE_MODEL = os.environ.get('HUGGINGFACE_MODEL', 'meta-llama/Meta-Llama-3-8B-Instruct')

    # gemini settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')

    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        if Config.LLM_PROVIDER == 'groq' and not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required when using groq provider")
        elif Config.LLM_PROVIDER == 'huggingface' and not Config.HUGGINGFACE_API_KEY:
            raise ValueError("HUGGINGFACE_API_KEY environment variable is required when using huggingface provider")
        elif Config.LLM_PROVIDER == 'gemini' and not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required when using gemini provider")
