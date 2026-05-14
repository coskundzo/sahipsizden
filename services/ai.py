import requests
from config import AI_PROVIDER, GROK_API_KEY, GEMINI_API_KEY, GROQ_API_KEY, OLLAMA_BASE_URL, OLLAMA_MODEL

def analyze(comments, brand, series, engine, package, year):
    """
    AI ile araç analizi yapar - Ücretsiz providers destekler
    """
    
    prompt = f"""
Sen bir otomotiv uzmanısın. Aşağıdaki {brand} {series} {engine} {package} ({year}) modeli hakkında 
kullanıcı yorumlarını analiz et ve detaylı bir rapor hazırla.

Yorumlar:
{comments[:3000]}  # İlk 3000 karakter

Lütfen şu başlıklar altında analiz yap:
1. Genel Değerlendirme
2. En Çok Şikayet Edilen Konular
3. Olumlu Yönler
4. Motor ve Performans
5. Yakıt Tüketimi
6. Konfor ve İç Mekan
7. Güvenilirlik Skoru (1-10)
8. Satın Alma Önerisi

Türkçe ve detaylı bir analiz yap.
"""
    
    try:
        if AI_PROVIDER == "grok":
            return analyze_grok(prompt)
        elif AI_PROVIDER == "groq":
            return analyze_groq(prompt)
        elif AI_PROVIDER == "ollama":
            return analyze_ollama(prompt)
        elif AI_PROVIDER == "gemini":
            return analyze_gemini(prompt)
        else:
            return "Geçersiz AI provider. Lütfen config.py'de AI_PROVIDER ayarlayın."
    except Exception as e:
        return f"Analiz sırasında hata oluştu: {str(e)}"


def analyze_grok(prompt):
    """Grok (xAI) ile analiz - Elon Musk'ın AI'ı"""
    url = "https://api.x.ai/v1/responses"
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "grok-4.20-reasoning",
        "input": prompt
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        # Grok API response yapısına göre
        if "response" in result:
            return result["response"]
        elif "output" in result:
            return result["output"]
        else:
            return str(result)
    except requests.exceptions.HTTPError as e:
        error_detail = response.text if hasattr(response, 'text') else str(e)
        return f"Grok API Hatası: {e.response.status_code} - {error_detail}"
    except Exception as e:
        return f"Grok bağlantı hatası: {str(e)}"


def analyze_groq(prompt):
    """Groq ile analiz - ÜCRETSIZ ve ÇOK HIZLI"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-70b-versatile",  # Ücretsiz ve güçlü
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def analyze_ollama(prompt):
    """Ollama ile lokal analiz - TAMAMEN ÜCRETSIZ"""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["response"]


def analyze_gemini(prompt):
    """Google Gemini ile analiz"""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
