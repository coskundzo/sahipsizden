"""
Sahibinden.com'dan araç marka ve modellerini çeker
"""
import requests
import json
import sqlite3
from bs4 import BeautifulSoup
import time

def fetch_brands():
    """Sahibinden.com'dan marka listesini çek"""
    print("🔍 Marka listesi çekiliyor...")
    
    # Sahibinden.com'un kategori sayfası
    url = "https://www.sahibinden.com/kategori/vasita/otomobil"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Marka select box'ını bul (data-attr="a2" genelde marka için kullanılır)
        brands = {}
        
        # Option'ları bul
        brand_select = soup.find('select', {'id': 'a2'})  # Genelde marka id'si a2
        
        if brand_select:
            for option in brand_select.find_all('option'):
                value = option.get('value', '')
                text = option.get_text(strip=True)
                
                if value and value != '0' and text:
                    brands[value] = text
        
        print(f"✅ {len(brands)} marka bulundu")
        return brands
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return {}


def fetch_models_for_brand(brand_id, brand_name):
    """Belirli bir marka için model listesini çek"""
    print(f"  🔍 {brand_name} modelleri çekiliyor...")
    
    # Sahibinden.com'un model API endpoint'i (AJAX)
    url = f"https://www.sahibinden.com/kategori-ara-api/vasita/otomobil?a2={brand_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.sahibinden.com/kategori/vasita/otomobil',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # API yanıtından modelleri parse et
        models = []
        if 'data' in data and 'a3' in data['data']:  # a3 genelde model
            for model in data['data']['a3']:
                if isinstance(model, dict) and 'value' in model and 'label' in model:
                    models.append({
                        'id': model['value'],
                        'name': model['label']
                    })
        
        print(f"    ✅ {len(models)} model bulundu")
        return models
        
    except Exception as e:
        print(f"    ⚠️  {brand_name} için model alınamadı: {e}")
        return []


def fetch_all_cars():
    """Tüm markaları ve modellerini çek"""
    print("\n🚀 Sahibinden.com'dan araç verileri çekiliyor...\n")
    
    # Markaları çek
    brands = fetch_brands()
    
    if not brands:
        print("❌ Marka bulunamadı. Lütfen internet bağlantınızı kontrol edin.")
        return {}
    
    all_data = {}
    
    for brand_id, brand_name in list(brands.items())[:20]:  # İlk 20 marka (testi için)
        models = fetch_models_for_brand(brand_id, brand_name)
        
        if models:
            all_data[brand_name] = models
        
        # Rate limiting - sahibinden.com'u yormamak için
        time.sleep(1)
    
    return all_data


def save_to_database(cars_data):
    """Çekilen verileri veritabanına kaydet"""
    print("\n💾 Veritabanına kaydediliyor...")
    
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    
    added = 0
    
    for brand_name, models in cars_data.items():
        for model in models:
            # Örnek veri oluştur
            category = "Otomobil"
            series = model['name']
            engine = "1.6"  # Varsayılan motor
            package = "Standart"
            year = "2020"
            image = f"/static/images/{brand_name.lower().replace(' ', '_')}_default.jpg"
            
            # Kontrol et, yoksa ekle
            c.execute("""
                SELECT COUNT(*) FROM cars 
                WHERE category=? AND brand=? AND series=?
            """, (category, brand_name, series))
            
            if c.fetchone()[0] == 0:
                c.execute("""
                    INSERT INTO cars (category, brand, series, engine, package, year, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (category, brand_name, series, engine, package, year, image))
                added += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ {added} yeni araç eklendi!")
    return added


def save_to_json(cars_data, filename='sahibinden_cars.json'):
    """Verileri JSON dosyasına kaydet"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cars_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Veriler {filename} dosyasına kaydedildi")


if __name__ == "__main__":
    # Verileri çek
    cars_data = fetch_all_cars()
    
    if cars_data:
        # JSON olarak kaydet
        save_to_json(cars_data)
        
        # Veritabanına kaydet
        save_to_database(cars_data)
        
        print(f"\n✨ Toplam {len(cars_data)} marka ve modelleri başarıyla çekildi!")
    else:
        print("\n❌ Veri çekilemedi!")
