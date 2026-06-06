import os
from dotenv import load_dotenv

def load_config():
    # Load .env file jika ada di direktori eksekusi
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

def get_api_key(provider):
    keys = {
        "gemini": os.getenv("GEMINI_API_KEY"),
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "mistral": os.getenv("MISTRAL_API_KEY"),
        "github": os.getenv("GITHUB_API_KEY"),
        "huggingface": os.getenv("HUGGINGFACE_API_KEY"),
    }
    return keys.get(provider, "")
