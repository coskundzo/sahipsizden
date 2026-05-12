import sqlite3

def init_db():
    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        series TEXT,
        engine TEXT,
        package TEXT,
        year TEXT,
        result TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        series TEXT NOT NULL,
        engine TEXT NOT NULL,
        package TEXT NOT NULL,
        year TEXT NOT NULL,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()

def seed_cars():
    conn = sqlite3.connect("cars.db")
    c = conn.cursor()
    
    # Check if data already exists
    c.execute("SELECT COUNT(*) FROM cars")
    if c.fetchone()[0] == 0:
        cars_data = [
            # Alfa Romeo - Otomobil
            ("Otomobil", "Alfa Romeo", "Giulia", "2.0", "Standart", "2020", "/static/images/alfa_romeo_giulia_2023.jpg"),
            ("Otomobil", "Alfa Romeo", "Giulia", "2.0", "Sport", "2021", "/static/images/alfa_romeo_giulia_sport.jpg"),
            
            # Audi - Otomobil
            ("Otomobil", "Audi", "A1", "1.4 TFSI", "Standart", "2020", "/static/images/audi_a1_2020.jpg"),
            ("Otomobil", "Audi", "A2", "1.6 TDI", "Comfort", "2012", "/static/images/audi_a2_2012.jpg"),
            ("Otomobil", "Audi", "A3", "1.5 TFSI", "Standart", "2019", "/static/images/audi_a3_2019.jpg"),
            ("Otomobil", "Audi", "A3", "2.0 TDI", "S-Line", "2020", "/static/images/audi_a3_sline.jpg"),
            ("Otomobil", "Audi", "A4", "2.0 TDI", "Standart", "2018", "/static/images/audi_a4_2018.jpg"),
            ("Otomobil", "Audi", "A4", "2.0 TDI", "Quattro", "2021", "/static/images/audi_a4_quattro.jpg"),
            
            # BMW - Otomobil
            ("Otomobil", "BMW", "1 Serisi", "116d", "Standart", "2016", "/static/images/bmw_1_series_116d.jpg"),
            ("Otomobil", "BMW", "1 Serisi", "118i", "M Sport", "2019", "/static/images/bmw_1_msport.jpg"),
            ("Otomobil", "BMW", "3 Serisi", "320i", "Standart", "2017", "/static/images/bmw_3_320i.jpg"),
            ("Otomobil", "BMW", "3 Serisi", "320d", "M Sport", "2020", "/static/images/bmw_3_msport.jpg"),
            ("Otomobil", "BMW", "5 Serisi", "520d", "Standart", "2018", "/static/images/bmw_5_520d.jpg"),
            ("Otomobil", "BMW", "5 Serisi", "530i", "Luxury", "2021", "/static/images/bmw_5_luxury.jpg"),
            
            # Mercedes-Benz - Otomobil
            ("Otomobil", "Mercedes-Benz", "A Serisi", "A180", "Standart", "2019", "/static/images/mercedes_a180.jpg"),
            ("Otomobil", "Mercedes-Benz", "A Serisi", "A200", "AMG", "2020", "/static/images/mercedes_a200_amg.jpg"),
            ("Otomobil", "Mercedes-Benz", "C Serisi", "C180", "Standart", "2017", "/static/images/mercedes_c180.jpg"),
            ("Otomobil", "Mercedes-Benz", "C Serisi", "C200", "AMG", "2020", "/static/images/mercedes_c200_amg.jpg"),
            ("Otomobil", "Mercedes-Benz", "E Serisi", "E200", "Standart", "2018", "/static/images/mercedes_e200.jpg"),
            ("Otomobil", "Mercedes-Benz", "E Serisi", "E220d", "AMG", "2021", "/static/images/mercedes_e220d_amg.jpg"),
            
            # Volkswagen - Otomobil ve Kamyonet
            ("Otomobil", "Volkswagen", "Golf", "1.6 TDI", "Standart", "2016", "/static/images/vw_golf_2016.jpg"),
            ("Otomobil", "Volkswagen", "Golf", "1.5 TSI", "Highline", "2019", "/static/images/vw_golf_highline.jpg"),
            ("Otomobil", "Volkswagen", "Golf", "2.0 TDI", "GTI", "2020", "/static/images/vw_golf_gti.jpg"),
            ("Otomobil", "Volkswagen", "Passat", "1.6 TDI", "Standart", "2017", "/static/images/vw_passat_2017.jpg"),
            ("Otomobil", "Volkswagen", "Passat", "2.0 TDI", "Highline", "2020", "/static/images/vw_passat_highline.jpg"),
            ("Otomobil", "Volkswagen", "Polo", "1.4 TDI", "Standart", "2018", "/static/images/vw_polo_2018.jpg"),
            ("Otomobil", "Volkswagen", "Polo", "1.0 TSI", "Comfortline", "2020", "/static/images/vw_polo_comfort.jpg"),
            ("Kamyonet", "Volkswagen", "Tiguan", "1.5 TSI", "Standart", "2019", "/static/images/vw_tiguan_2019.jpg"),
            ("Kamyonet", "Volkswagen", "Tiguan", "2.0 TDI", "Highline", "2021", "/static/images/vw_tiguan_highline.jpg"),
            
            # Toyota - Otomobil ve Kamyonet
            ("Otomobil", "Toyota", "Corolla", "1.6", "Standart", "2016", "/static/images/toyota_corolla_2016.jpg"),
            ("Otomobil", "Toyota", "Corolla", "1.8 Hybrid", "Comfort", "2019", "/static/images/toyota_corolla_hybrid.jpg"),
            ("Otomobil", "Toyota", "Corolla", "2.0 Hybrid", "Platinum", "2021", "/static/images/toyota_corolla_platinum.jpg"),
            ("Kamyonet", "Toyota", "C-HR", "1.8 Hybrid", "Standart", "2018", "/static/images/toyota_chr_2018.jpg"),
            ("Kamyonet", "Toyota", "C-HR", "1.8 Hybrid", "Style", "2020", "/static/images/toyota_chr_style.jpg"),
            ("Kamyonet", "Toyota", "RAV4", "2.0", "Standart", "2017", "/static/images/toyota_rav4_2017.jpg"),
            ("Kamyonet", "Toyota", "RAV4", "2.5 Hybrid", "Platinum", "2020", "/static/images/toyota_rav4_hybrid.jpg"),
            ("Otomobil", "Toyota", "Yaris", "1.0", "Standart", "2017", "/static/images/toyota_yaris_2017.jpg"),
            ("Otomobil", "Toyota", "Yaris", "1.5 Hybrid", "Comfort", "2020", "/static/images/toyota_yaris_hybrid.jpg"),
            
            # Renault - Otomobil ve Kamyonet
            ("Otomobil", "Renault", "Clio", "1.5 dCi", "Standart", "2016", "/static/images/renault_clio_2016.jpg"),
            ("Otomobil", "Renault", "Clio", "1.0 TCe", "Icon", "2019", "/static/images/renault_clio_icon.jpg"),
            ("Otomobil", "Renault", "Clio", "1.3 TCe", "RS Line", "2021", "/static/images/renault_clio_rs.jpg"),
            ("Otomobil", "Renault", "Megane", "1.5 dCi", "Standart", "2017", "/static/images/renault_megane_2017.jpg"),
            ("Otomobil", "Renault", "Megane", "1.3 TCe", "Icon", "2020", "/static/images/renault_megane_icon.jpg"),
            ("Kamyonet", "Renault", "Kadjar", "1.5 dCi", "Standart", "2018", "/static/images/renault_kadjar_2018.jpg"),
            ("Kamyonet", "Renault", "Kadjar", "1.3 TCe", "Icon", "2020", "/static/images/renault_kadjar_icon.jpg"),
            ("Kamyonet", "Renault", "Captur", "1.5 dCi", "Standart", "2017", "/static/images/renault_captur_2017.jpg"),
            ("Kamyonet", "Renault", "Captur", "1.0 TCe", "Icon", "2020", "/static/images/renault_captur_icon.jpg"),
            
            # Fiat - Otomobil
            ("Otomobil", "Fiat", "Egea", "1.3 Multijet", "Standart", "2017", "/static/images/fiat_egea_2017.jpg"),
            ("Otomobil", "Fiat", "Egea", "1.4 Fire", "Urban", "2019", "/static/images/fiat_egea_urban.jpg"),
            ("Otomobil", "Fiat", "500", "1.2", "Standart", "2016", "/static/images/fiat_500_2016.jpg"),
            ("Otomobil", "Fiat", "500", "0.9 TwinAir", "Lounge", "2018", "/static/images/fiat_500_lounge.jpg"),
            
            # Ford - Otomobil ve Kamyonet
            ("Otomobil", "Ford", "Focus", "1.5 TDCi", "Standart", "2017", "/static/images/ford_focus_2017.jpg"),
            ("Otomobil", "Ford", "Focus", "1.5 EcoBoost", "Titanium", "2019", "/static/images/ford_focus_titanium.jpg"),
            ("Otomobil", "Ford", "Fiesta", "1.5 TDCi", "Standart", "2016", "/static/images/ford_fiesta_2016.jpg"),
            ("Otomobil", "Ford", "Fiesta", "1.0 EcoBoost", "Titanium", "2019", "/static/images/ford_fiesta_titanium.jpg"),
            ("Kamyonet", "Ford", "Kuga", "1.5 TDCi", "Standart", "2018", "/static/images/ford_kuga_2018.jpg"),
            ("Kamyonet", "Ford", "Kuga", "2.0 EcoBlue", "Titanium", "2020", "/static/images/ford_kuga_titanium.jpg"),
            
            # Peugeot - Otomobil ve Kamyonet
            ("Otomobil", "Peugeot", "208", "1.5 BlueHDi", "Standart", "2017", "/static/images/peugeot_208_2017.jpg"),
            ("Otomobil", "Peugeot", "208", "1.2 PureTech", "Allure", "2020", "/static/images/peugeot_208_allure.jpg"),
            ("Otomobil", "Peugeot", "308", "1.5 BlueHDi", "Standart", "2018", "/static/images/peugeot_308_2018.jpg"),
            ("Otomobil", "Peugeot", "308", "1.2 PureTech", "GT Line", "2020", "/static/images/peugeot_308_gt.jpg"),
            ("Kamyonet", "Peugeot", "3008", "1.5 BlueHDi", "Standart", "2018", "/static/images/peugeot_3008_2018.jpg"),
            ("Kamyonet", "Peugeot", "3008", "1.6 PureTech", "GT Line", "2020", "/static/images/peugeot_3008_gt.jpg"),
            
            # Opel - Otomobil
            ("Otomobil", "Opel", "Astra", "1.6 CDTI", "Standart", "2016", "/static/images/opel_astra_2016.jpg"),
            ("Otomobil", "Opel", "Astra", "1.2 Turbo", "Elegance", "2020", "/static/images/opel_astra_elegance.jpg"),
            ("Otomobil", "Opel", "Corsa", "1.3 CDTI", "Standart", "2017", "/static/images/opel_corsa_2017.jpg"),
            ("Otomobil", "Opel", "Corsa", "1.2 Turbo", "Elegance", "2020", "/static/images/opel_corsa_elegance.jpg"),
            ("Otomobil", "Opel", "Insignia", "1.6 CDTI", "Standart", "2018", "/static/images/opel_insignia_2018.jpg"),
            ("Otomobil", "Opel", "Insignia", "2.0 CDTI", "Elite", "2020", "/static/images/opel_insignia_elite.jpg"),
        ]
        
        c.executemany(
            "INSERT INTO cars (category, brand, series, engine, package, year, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
            cars_data
        )
        
    conn.commit()
    conn.close()

def get_all_cars():
    conn = sqlite3.connect("cars.db")
    c = conn.cursor()
    c.execute("SELECT category, brand, series, engine, package, year, image FROM cars")
    rows = c.fetchall()
    conn.close()
    
    # Convert to nested dict structure
    data = {}
    for category, brand, series, engine, package, year, image in rows:
        if category not in data:
            data[category] = {}
        if brand not in data[category]:
            data[category][brand] = {}
        if series not in data[category][brand]:
            data[category][brand][series] = {}
        if engine not in data[category][brand][series]:
            data[category][brand][series][engine] = {}
        if package not in data[category][brand][series][engine]:
            data[category][brand][series][engine][package] = {}
        data[category][brand][series][engine][package][year] = {"image": image}
    
    return data


def save(brand, series, engine, package, year, result):
    conn = sqlite3.connect("cars.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO reports VALUES (NULL,?,?,?,?,?,?)",
        (brand, series, engine, package, year, result)
    )

    conn.commit()
    conn.close()