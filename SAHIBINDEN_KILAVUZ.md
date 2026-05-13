# 🚗 Sahibinden.com'dan Araç Verisi Çekme Kılavuzu

Bu proje için Sahibinden.com'dan araç marka ve modellerini çekmek için **2 yöntem** hazırladım.

---

## ⚡ Yöntem 1: Basit HTTP İsteği (ÖNERİLEN - Hızlı)

**Dosya:** `fetch_sahibinden_cars.py`

### Avantajlar:
- ✅ Hızlı çalışır
- ✅ Kurulum basit
- ✅ Daha az kaynak kullanır
- ✅ Tarayıcı gerektirmez

### Kurulum:
```bash
# Gerekli paketler requirements.txt'de mevcut
pip install -r requirements.txt
```

### Kullanım:
```bash
python fetch_sahibinden_cars.py
```

### Çıktılar:
- `sahibinden_cars.json` - Tüm veriler JSON formatında
- `cars.db` - Otomatik olarak veritabanına eklenir

---

## 🌐 Yöntem 2: Selenium ile Tarayıcı Otomasyonu (Tam Kapsamlı)

**Dosya:** `fetch_sahibinden_selenium.py`

### Avantajlar:
- ✅ JavaScript ile yüklenen içeriği yakalayabilir
- ✅ Daha güvenilir (tarayıcı gibi davranır)
- ✅ Tüm dropdown seçeneklerini görebilir

### Kurulum:

#### 1. Selenium Kur:
```bash
pip install selenium
```

#### 2. ChromeDriver İndir:
- **Windows için:** https://googlechromelabs.github.io/chrome-for-testing/
- Chrome sürümünüze uygun olanı indirin (Chrome: Ayarlar → Hakkında → Sürüm)
- `chromedriver.exe` dosyasını proje klasörüne veya PATH'e ekleyin

**Alternatif - Otomatik kurulum:**
```bash
pip install webdriver-manager
```

### Kullanım:
```bash
python fetch_sahibinden_selenium.py
```

---

## 📊 Veritabanı Yapısı

Çekilen veriler şu yapıda kaydedilir:

```sql
CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,      -- Otomobil, Kamyonet, Motosiklet
    brand TEXT NOT NULL,          -- Marka (BMW, Audi, vs.)
    series TEXT NOT NULL,         -- Model/Seri (3 Serisi, A4, vs.)
    engine TEXT NOT NULL,         -- Motor tipi (2.0 TDI, 1.6, vs.)
    package TEXT NOT NULL,        -- Paket (Standart, Comfort, Sport)
    year TEXT NOT NULL,           -- Yıl (2020, 2021, vs.)
    image TEXT                    -- Görsel yolu
)
```

---

## 🎯 Hangi Yöntemi Seçmeliyim?

### Yöntem 1'i kullan eğer:
- ✅ Hızlı sonuç istiyorsanız
- ✅ Basit kurulum tercih ediyorsanız
- ✅ Sunucuda çalıştırıyorsanız (headless)

### Yöntem 2'yi kullan eğer:
- ✅ Tam ve güncel veri istiyorsanız
- ✅ JavaScript ile yüklenen içerik önemliyse
- ✅ Yerel bilgisayarda çalışıyorsanız

---

## 🔧 Özelleştirme

### Daha fazla marka çekmek için:

**fetch_sahibinden_cars.py** - Satır 107:
```python
for brand_id, brand_name in list(brands.items())[:20]:  # 20 yerine istediğiniz sayıyı yazın
```

**fetch_sahibinden_selenium.py** - Satır 88:
```python
for i, brand in enumerate(brands[:15], 1):  # 15 yerine istediğiniz sayıyı yazın
```

### Kategori değiştirmek için:

URL'i değiştirin:
- Otomobil: `/kategori/vasita/otomobil`
- Motosiklet: `/kategori/vasita/motosiklet`
- Kamyonet: `/kategori/vasita/arazi-suv-pickup`

---

## ⚠️ Önemli Notlar

1. **Rate Limiting:** Sahibinden.com'u yormamak için istekler arasında bekleme süresi var
2. **Robot Kontrolü:** Çok fazla istek gönderirseniz IP'niz engellenebilir
3. **Yasal Uyarı:** Ticari kullanım için Sahibinden.com'dan izin alın
4. **Veri Doğruluğu:** Çekilen veriler site yapısı değişirse güncellenmelidir

---

## 🐛 Sorun Giderme

### "Unable to open database file" hatası:
```bash
# Instance klasörü oluştur
mkdir instance
```

### ChromeDriver bulunamadı:
```bash
# Webdriver manager kullan
pip install webdriver-manager
```

Kodda değişiklik:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
```

### Selenium timeout hatası:
- İnternet bağlantınızı kontrol edin
- `WebDriverWait` süresini artırın (15 → 30 saniye)

---

## 📞 Yardım

Sorun yaşarsanız:
1. `check_db.py` ile veritabanını kontrol edin
2. JSON çıktısını kontrol edin
3. Terminal çıktısındaki hataları inceleyin

---

## ✨ Örnek Kullanım

```bash
# 1. Paketleri kur
pip install -r requirements.txt

# 2. Verileri çek (Yöntem 1 - Hızlı)
python fetch_sahibinden_cars.py

# 3. Veritabanını kontrol et
python check_db.py

# 4. Uygulamayı başlat
python app.py
```

Tarayıcıda: http://127.0.0.1:5000
