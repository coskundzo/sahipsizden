import sqlite3
import re

# SQL dosyasını oku
with open('arac_marka_modeller_2022.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Markaları parse et
markalar = {}
marka_pattern = r"\((\d+),(\d+),'([^']+)'\)"
marka_section = re.search(r"INSERT INTO `arac_markalar`.*?VALUES\s+(.*?);", sql_content, re.DOTALL)
if marka_section:
    for match in re.finditer(marka_pattern, marka_section.group(1)):
        id_num, marka_kodu, marka_adi = match.groups()
        markalar[int(marka_kodu)] = marka_adi

print(f"✅ {len(markalar)} marka yüklendi")

# Modelleri parse et
modeller = []
model_pattern = r"\((\d+),(\d+),(\d+),'([^']+)'\)"
model_section = re.search(r"INSERT INTO `arac_modeller`.*?VALUES\s+(.*?);", sql_content, re.DOTALL)
if model_section:
    for match in re.finditer(model_pattern, model_section.group(1)):
        id_num, model_kodu, marka_kodu, model_adi = match.groups()
        if int(marka_kodu) in markalar:
            modeller.append({
                'marka_kodu': int(marka_kodu),
                'marka': markalar[int(marka_kodu)],
                'model': model_adi
            })

print(f"✅ {len(modeller)} model yüklendi")

# Kategori belirleme fonksiyonu
def get_category(marka):
    # Motosiklet markaları
    motorsiklet_brands = ['MOTORSIKLET', 'KTM', 'HONDA', 'YAMAHA', 'KAWASAKI', 'SUZUKI', 'DUCATI']
    
    # Kamyonet/SUV markaları (bazı örnekler)
    kamyonet_keywords = ['PICKUP', 'KAMYONET', 'VAN', 'MINIBUS', 'MINIBÜS', 'KAMYON', 'TRANSPORTER', 
                         'SPRINTER', 'TRANSIT', 'DUCATO', 'MASTER', 'DAILY', 'BOXER']
    
    marka_upper = marka.upper()
    
    if marka_upper in motorsiklet_brands or 'MOTORSiKLET' in marka_upper:
        return 'Motosiklet'
    
    # Marka bazlı kamyonet belirleme
    if marka_upper in ['OTOKAR/MAGIRUS', 'MAN', 'SCANIA', 'VOLVO', 'DAF', 'IVECO', 'TEMSA', 'ASKAM/FARGO/DESOTO', 'KARSAN']:
        return 'Kamyonet'
    
    return 'Otomobil'

# Model isminden motor tipini parse etmeye çalış
def extract_engine(model_name):
    # Motor tipi pattern'leri (örn: 1.6, 2.0 TDI, 1.5 TSI, vb.)
    engine_patterns = [
        r'(\d+\.\d+\s*[A-Z]*\s*[A-Z]*)',  # 1.6 TDI, 2.0 TSI gibi
        r'(\d+\.\d+)',  # Sadece 1.6, 2.0 gibi
    ]
    
    for pattern in engine_patterns:
        match = re.search(pattern, model_name)
        if match:
            return match.group(1).strip()
    
    return "Standart"

# Veritabanına bağlan
conn = sqlite3.connect('cars.db')
c = conn.cursor()

# Mevcut veri sayısını al
c.execute("SELECT COUNT(*) FROM cars")
existing_count = c.fetchone()[0]
print(f"📊 Mevcut veritabanında {existing_count} araç var")

print("\n🔄 Yeni araçlar ekleniyor...")

# Seçili markalardan örnek veriler ekle (tümünü eklemek çok büyük olur)
# Popüler markaları seçelim
popular_brands = ['ALFA ROMEO', 'AUDI', 'BMW', 'MERCEDES', 'VOLKSWAGEN', 'TOYOTA', 
                  'RENAULT', 'RENAULT (OYAK)', 'FORD/OTOSAN', 'FIAT', 'TOFAS-FIAT',
                  'PEUGEOT', 'OPEL', 'HONDA', 'HYUNDAI', 'KIA', 'NISSAN', 'MAZDA',
                  'CITROEN', 'SKODA', 'SEAT', 'VOLVO', 'LAND ROVER', 'JAGUAR',
                  'PORSCHE', 'MINI', 'SMART', 'DACIA', 'SUZUKI', 'MITSUBISHI',
                  'SUBARU', 'LEXUS', 'INFINITI', 'TESLA', 'MOTORSIKLET']

added_count = 0
for model_data in modeller:
    # Sadece popüler markaları ekle
    if model_data['marka'] not in popular_brands:
        continue
    
    category = get_category(model_data['marka'])
    brand = model_data['marka']
    series = model_data['model'][:50]  # Model adını kısalt
    engine = extract_engine(model_data['model'])
    package = "Standart"
    year = "2020"  # Varsayılan yıl
    image = f"/static/images/{brand.lower().replace(' ', '_').replace('/', '_')}_default.jpg"
    
    # Aynı araç zaten var mı kontrol et
    c.execute("""
        SELECT COUNT(*) FROM cars 
        WHERE category=? AND brand=? AND series=? AND engine=? AND package=? AND year=?
    """, (category, brand, series, engine, package, year))
    
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO cars (category, brand, series, engine, package, year, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (category, brand, series, engine, package, year, image))
        added_count += 1
        
        if added_count % 100 == 0:
            print(f"  ⏳ {added_count} araç eklendi...")

conn.commit()

# Yeni toplam
c.execute("SELECT COUNT(*) FROM cars")
new_count = c.fetchone()[0]

# Kategori dağılımı
print("\n📊 Güncel Kategori Dağılımı:")
c.execute('SELECT category, COUNT(*) as count FROM cars GROUP BY category ORDER BY count DESC')
for category, count in c.fetchall():
    print(f'  • {category}: {count} araç')

# Marka dağılımı (ilk 15)
print("\n📋 En Çok Araç Olan Markalar (İlk 15):")
c.execute('SELECT brand, COUNT(*) as count FROM cars GROUP BY brand ORDER BY count DESC LIMIT 15')
for brand, count in c.fetchall():
    print(f'  • {brand}: {count} model')

conn.close()

print(f"\n✅ Toplam {added_count} yeni araç eklendi!")
print(f"📊 Veritabanında şimdi {new_count} araç var (önceden {existing_count})")
