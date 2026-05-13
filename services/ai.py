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
