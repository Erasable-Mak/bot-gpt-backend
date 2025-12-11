import os
from app import create_app
from app.config import Config

app = create_app()

# validate configuration before running (only enforce when using Groq unless overridden)
try:
    if Config.LLM_PROVIDER == 'groq' and not os.getenv("ALLOW_EMPTY_KEYS"):
        Config.validate_config()
    print("Configuration validated successfully")
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and environment variables")
    exit(1)

if __name__ == '__main__':
    app.run(debug=True)
