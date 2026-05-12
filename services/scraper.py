import requests
from bs4 import BeautifulSoup
<<<<<<< HEAD
import time

def fetch_data(url):
    """
    Web sitesinden veri çeker
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Yorumları çek (site yapısına göre selector değişebilir)
            comments = []
            comment_elements = soup.find_all('div', class_='complaint-content')
            
            for element in comment_elements[:20]:  # İlk 20 yorum
                text = element.get_text(strip=True)
                if text:
                    comments.append(text)
            
            return ' '.join(comments) if comments else "Veri bulunamadı"
        else:
            return f"Hata: {response.status_code}"
            
    except Exception as e:
        return f"Hata oluştu: {str(e)}"
=======

def fetch_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        texts = []
        for p in soup.find_all("p"):
            t = p.get_text().strip()
            if len(t) > 40:
                texts.append(t)

        return texts[:20]

    except requests.exceptions.Timeout:
        print(f"UYARI: {url} yanıt vermiyor (timeout)")
        return []
    except requests.exceptions.RequestException as e:
        print(f"UYARI: {url} çekilemedi - {str(e)}")
        return []
    except Exception as e:
        print(f"UYARI: Scraping hatası - {str(e)}")
        return []
>>>>>>> c66183f (İlk yükleme: Tüm proje ve veritabanı dosyaları eklendi)
