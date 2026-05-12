<<<<<<< HEAD
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze(comments, brand, series, engine, package, year):
    """
    AI ile araç analizi yapar
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
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analiz sırasında hata oluştu: {str(e)}"
=======
import requests
from config import OLLAMA_URL, MODEL_NAME, TIMEOUT

def analyze(comments, brand, series, engine, package, year):
    # 🔥 performans optimizasyonu
    comments = comments[:5]
    comments = [c[:150] for c in comments]

    text = "\n".join(comments)

    prompt = f"""
Kısa ve net cevap ver.

Araç: {brand} {series} {engine} {package} {year}

Yorumlar:
{text}

Şunları yaz:
- Kronik sorunlar
- En sık olan
- Risk seviyesi (Düşük/Orta/Yüksek)
"""

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False  # Disable streaming to get single JSON response
            },
            timeout=TIMEOUT
        )

        res.raise_for_status()
        
        # Parse JSON response
        try:
            data = res.json()
        except ValueError as json_err:
            return f"HATA: Ollama yanıtı parse edilemedi. Streaming kapalı mı kontrol edin. Detay: {str(json_err)}"

        return data.get("message", {}).get("content", "Cevap alınamadı")

    except requests.exceptions.Timeout:
        return "HATA: Ollama servisi yanıt vermiyor (timeout). Lütfen Ollama servisinin çalıştığından emin olun."
    except requests.exceptions.ConnectionError:
        return f"HATA: Ollama servisine bağlanılamıyor ({OLLAMA_URL}). Lütfen Ollama'nın çalıştığını kontrol edin."
    except requests.exceptions.RequestException as e:
        return f"HATA: İstek hatası - {str(e)}"
    except Exception as e:
        return f"HATA: Beklenmeyen hata - {str(e)}"
>>>>>>> c66183f (İlk yükleme: Tüm proje ve veritabanı dosyaları eklendi)
