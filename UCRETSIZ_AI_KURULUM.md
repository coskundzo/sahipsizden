# Ücretsiz AI API Kurulumu

## 🎉 Artık 3 Ücretsiz Seçenek Mevcut!

### 1. **GROQ** (Önerilen - En Kolay)
✅ Tamamen ücretsiz  
✅ Çok hızlı (LPU teknolojisi)  
✅ Güçlü modeller (Llama 3.1 70B)  

**Kurulum:**
1. https://console.groq.com/keys adresine gidin
2. Hesap oluşturun (GitHub ile giriş yapabilirsiniz)
3. API Key alın
4. `.env` dosyasına ekleyin:
   ```
   AI_PROVIDER=groq
   GROQ_API_KEY=gsk_your_key_here
   ```

### 2. **Ollama** (Tamamen Lokal)
✅ Tamamen ücretsiz  
✅ İnternet bağlantısı gerektirmez  
✅ Gizlilik odaklı  

**Kurulum:**
1. https://ollama.com adresinden Ollama'yı indirin
2. Kurulumu tamamlayın
3. Terminal'de çalıştırın:
   ```bash
   ollama pull llama3
   ```
4. `.env` dosyasına ekleyin:
   ```
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   ```

### 3. **Gemini** (Ücretli ama güçlü)
Google'ın AI modeli

**Kurulum:**
1. https://makersuite.google.com/app/apikey adresine gidin
2. API Key alın
3. `.env` dosyasına ekleyin:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   ```

## Hızlı Başlangıç

1. `.env.example` dosyasını `.env` olarak kopyalayın:
   ```bash
   cp .env.example .env
   ```

2. `.env` dosyasını düzenleyin ve seçtiğiniz provider'ı ayarlayın

3. Uygulamayı çalıştırın:
   ```bash
   python app.py
   ```

## Provider Değiştirme

`.env` dosyasında `AI_PROVIDER` değerini değiştirin:
- `groq` - Groq kullan (önerilen)
- `ollama` - Ollama kullan (lokal)
- `gemini` - Google Gemini kullan

Örnek:
```
AI_PROVIDER=groq
```
