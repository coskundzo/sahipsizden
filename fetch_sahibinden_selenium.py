"""
Sahibinden.com'dan araç verilerini Selenium ile çeker
(JavaScript ile yüklenen içerikleri de yakalayabilir)
"""
import sqlite3
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def setup_driver():
    """Chrome driver'ı ayarla"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Tarayıcıyı gösterme
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def fetch_all_cars_selenium():
    """Selenium ile tüm araç verilerini çek"""
    print("🚀 Selenium ile Sahibinden.com'dan veri çekiliyor...")
    print("⏳ Tarayıcı başlatılıyor...\n")
    
    driver = setup_driver()
    all_data = {}
    
    try:
        # Ana sayfaya git
        url = "https://www.sahibinden.com/kategori/vasita/otomobil"
        driver.get(url)
        
        # Sayfanın yüklenmesini bekle
        wait = WebDriverWait(driver, 15)
        
        # Marka dropdown'ını bul
        print("🔍 Marka listesi alınıyor...")
        brand_select_element = wait.until(
            EC.presence_of_element_located((By.ID, "a2"))
        )
        
        brand_select = Select(brand_select_element)
        brands = []
        
        # Tüm markaları topla
        for option in brand_select.options[1:]:  # İlk option genelde "Tümü"
            brand_value = option.get_attribute('value')
            brand_text = option.text
            
            if brand_value and brand_value != '0':
                brands.append({
                    'value': brand_value,
                    'text': brand_text
                })
        
        print(f"✅ {len(brands)} marka bulundu\n")
        
        # Her marka için modelleri çek
        for i, brand in enumerate(brands[:15], 1):  # İlk 15 marka (test için)
            brand_text = brand['text']
            brand_value = brand['value']
            
            print(f"[{i}/{min(15, len(brands))}] 🔍 {brand_text} modelleri çekiliyor...")
            
            try:
                # Markayı seç
                brand_select = Select(driver.find_element(By.ID, "a2"))
                brand_select.select_by_value(brand_value)
                
                # Model dropdown'ının yüklenmesini bekle
                time.sleep(2)  # AJAX isteğinin tamamlanması için
                
                # Model dropdown'ını bul
                model_select_element = driver.find_element(By.ID, "a3")
                model_select = Select(model_select_element)
                
                models = []
                for option in model_select.options[1:]:  # İlk option "Tümü"
                    model_value = option.get_attribute('value')
                    model_text = option.text
                    
                    if model_value and model_value != '0':
                        models.append({
                            'id': model_value,
                            'name': model_text
                        })
                
                if models:
                    all_data[brand_text] = models
                    print(f"    ✅ {len(models)} model bulundu")
                else:
                    print(f"    ⚠️  Model bulunamadı")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"    ❌ Hata: {e}")
                continue
        
    finally:
        driver.quit()
        print("\n✅ Tarayıcı kapatıldı")
    
    return all_data


def save_to_database(cars_data):
    """Verileri veritabanına kaydet"""
    print("\n💾 Veritabanına kaydediliyor...")
    
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()
    
    added = 0
    
    for brand_name, models in cars_data.items():
        for model in models:
            category = "Otomobil"
            series = model['name']
            engine = "Standart"
            package = "Standart"
            year = "2024"
            image = f"/static/images/default_car.jpg"
            
            # Kontrol et
            c.execute("""
                SELECT COUNT(*) FROM cars 
                WHERE brand=? AND series=?
            """, (brand_name, series))
            
            if c.fetchone()[0] == 0:
                c.execute("""
                    INSERT INTO cars (category, brand, series, engine, package, year, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (category, brand_name, series, engine, package, year, image))
                added += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ {added} yeni araç eklendi!")


def save_to_json(data, filename='sahibinden_data.json'):
    """JSON olarak kaydet"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Veriler {filename} dosyasına kaydedildi")


if __name__ == "__main__":
    print("="*60)
    print("🚗 SAHİBİNDEN.COM ARAÇ VERİ ÇEKME ARACI")
    print("="*60)
    print("\n⚠️  Not: Selenium kurulu olmalı (pip install selenium)")
    print("⚠️  Not: ChromeDriver yüklü olmalı\n")
    
    try:
        # Verileri çek
        cars_data = fetch_all_cars_selenium()
        
        if cars_data:
            # Kaydet
            save_to_json(cars_data)
            save_to_database(cars_data)
            
            print(f"\n✨ Başarılı! {len(cars_data)} marka ve modelleri çekildi!")
            
            # İstatistikler
            total_models = sum(len(models) for models in cars_data.values())
            print(f"📊 Toplam {total_models} model")
        else:
            print("\n❌ Veri çekilemedi!")
            
    except Exception as e:
        print(f"\n❌ Kritik hata: {e}")
        print("\n💡 Çözüm önerileri:")
        print("   1. pip install selenium")
        print("   2. ChromeDriver indirin: https://chromedriver.chromium.org/")
        print("   3. ChromeDriver'ı PATH'e ekleyin")
