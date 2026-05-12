import os
<<<<<<< HEAD
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
=======

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3-coder:30b")  # hızlı model
TIMEOUT = int(os.getenv("TIMEOUT", "60"))  # 60 saniye daha makul
>>>>>>> c66183f (İlk yükleme: Tüm proje ve veritabanı dosyaları eklendi)
