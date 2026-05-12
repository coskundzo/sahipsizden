import sqlite3

conn = sqlite3.connect('cars.db')
c = conn.cursor()

# Toplam araç sayısı
c.execute('SELECT COUNT(*) FROM cars')
car_count = c.fetchone()[0]
print(f'📊 Toplam Araç: {car_count}\n')

# Kategori dağılımı
print('🏷️  Kategori Dağılımı:')
c.execute('SELECT category, COUNT(*) as count FROM cars GROUP BY category ORDER BY count DESC')
for category, count in c.fetchall():
    print(f'  • {category}: {count} araç')

# Marka dağılımı
print('\n📋 Marka Dağılımı:')
c.execute('SELECT brand, COUNT(*) as count FROM cars GROUP BY brand ORDER BY count DESC')
for brand, count in c.fetchall():
    print(f'  • {brand}: {count} model')

# Örnek veriler
print('\n🚗 Örnek Araçlar:')
c.execute('SELECT category, brand, series, engine, package, year FROM cars LIMIT 5')
for category, brand, series, engine, package, year in c.fetchall():
    print(f'  • [{category}] {brand} {series} {engine} {package} ({year})')

conn.close()
print('\n✅ Veritabanı başarıyla kontrol edildi!')
