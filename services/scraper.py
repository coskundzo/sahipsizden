import requests
from bs4 import BeautifulSoup
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
