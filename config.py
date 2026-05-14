import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider seçimi: 'grok', 'groq', 'ollama', 'gemini'
AI_PROVIDER = os.getenv("AI_PROVIDER", "grok")

# API Keys
GROK_API_KEY = os.getenv("GROK_API_KEY")  # xAI Grok API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Groq API

# Ollama Config
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
