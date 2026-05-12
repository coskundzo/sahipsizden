import sqlite3

conn = sqlite3.connect('cars.db')
c = conn.cursor()

# Motosiklet örnekleri ekle
motorcycles = [
    ("Motosiklet", "HONDA", "CBR 600RR", "600cc", "Sport", "2020", "/static/images/honda_cbr600rr.jpg"),
    ("Motosiklet", "HONDA", "CBR 1000RR", "1000cc", "Sport", "2021", "/static/images/honda_cbr1000rr.jpg"),
    ("Motosiklet", "HONDA", "CB 500F", "500cc", "Naked", "2020", "/static/images/honda_cb500f.jpg"),
    ("Motosiklet", "HONDA", "Africa Twin", "1100cc", "Adventure", "2021", "/static/images/honda_africa_twin.jpg"),
    
    ("Motosiklet", "YAMAHA", "YZF-R1", "1000cc", "Sport", "2020", "/static/images/yamaha_r1.jpg"),
    ("Motosiklet", "YAMAHA", "YZF-R6", "600cc", "Sport", "2021", "/static/images/yamaha_r6.jpg"),
    ("Motosiklet", "YAMAHA", "MT-07", "700cc", "Naked", "2020", "/static/images/yamaha_mt07.jpg"),
    ("Motosiklet", "YAMAHA", "MT-09", "900cc", "Naked", "2021", "/static/images/yamaha_mt09.jpg"),
    
    ("Motosiklet", "KAWASAKI", "Ninja 650", "650cc", "Sport", "2020", "/static/images/kawasaki_ninja650.jpg"),
    ("Motosiklet", "KAWASAKI", "Ninja ZX-10R", "1000cc", "Sport", "2021", "/static/images/kawasaki_zx10r.jpg"),
    ("Motosiklet", "KAWASAKI", "Z900", "900cc", "Naked", "2020", "/static/images/kawasaki_z900.jpg"),
    ("Motosiklet", "KAWASAKI", "Versys 650", "650cc", "Adventure", "2021", "/static/images/kawasaki_versys.jpg"),
    
    ("Motosiklet", "SUZUKI", "GSX-R1000", "1000cc", "Sport", "2020", "/static/images/suzuki_gsxr1000.jpg"),
    ("Motosiklet", "SUZUKI", "GSX-R750", "750cc", "Sport", "2021", "/static/images/suzuki_gsxr750.jpg"),
    ("Motosiklet", "SUZUKI", "V-Strom 650", "650cc", "Adventure", "2020", "/static/images/suzuki_vstrom.jpg"),
    ("Motosiklet", "SUZUKI", "SV650", "650cc", "Naked", "2021", "/static/images/suzuki_sv650.jpg"),
    
    ("Motosiklet", "DUCATI", "Panigale V4", "1100cc", "Sport", "2020", "/static/images/ducati_panigale.jpg"),
    ("Motosiklet", "DUCATI", "Monster 821", "821cc", "Naked", "2021", "/static/images/ducati_monster.jpg"),
    ("Motosiklet", "DUCATI", "Multistrada V4", "1158cc", "Adventure", "2021", "/static/images/ducati_multistrada.jpg"),
    
    ("Motosiklet", "BMW", "S1000RR", "1000cc", "Sport", "2020", "/static/images/bmw_s1000rr.jpg"),
    ("Motosiklet", "BMW", "R1250GS", "1250cc", "Adventure", "2021", "/static/images/bmw_r1250gs.jpg"),
    ("Motosiklet", "BMW", "F900R", "900cc", "Naked", "2020", "/static/images/bmw_f900r.jpg"),
    
    ("Motosiklet", "KTM", "Duke 390", "390cc", "Naked", "2020", "/static/images/ktm_duke390.jpg"),
    ("Motosiklet", "KTM", "Duke 790", "790cc", "Naked", "2021", "/static/images/ktm_duke790.jpg"),
    ("Motosiklet", "KTM", "1290 Super Adventure", "1290cc", "Adventure", "2021", "/static/images/ktm_adventure.jpg"),
]

added = 0
for motorcycle in motorcycles:
    c.execute("""
        INSERT INTO cars (category, brand, series, engine, package, year, image)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, motorcycle)
    added += 1

conn.commit()

# Sonuçları göster
c.execute("SELECT COUNT(*) FROM cars WHERE category='Motosiklet'")
motorcycle_count = c.fetchone()[0]

print(f"✅ {added} motosiklet eklendi")
print(f"📊 Toplam Motosiklet: {motorcycle_count}")

# Kategori dağılımı
print('\n🏷️  Güncel Kategori Dağılımı:')
c.execute('SELECT category, COUNT(*) as count FROM cars GROUP BY category ORDER BY count DESC')
for category, count in c.fetchall():
    print(f'  • {category}: {count} araç')

# Motosiklet markalarını göster
print('\n🏍️  Motosiklet Markaları:')
c.execute("SELECT brand, COUNT(*) as count FROM cars WHERE category='Motosiklet' GROUP BY brand ORDER BY count DESC")
for brand, count in c.fetchall():
    print(f'  • {brand}: {count} model')

conn.close()

print('\n✅ Motosiklet verileri başarıyla eklendi!')
