import requests
from bs4 import BeautifulSoup
import logging

def fetch_web_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:10000]
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return f"Failed to fetch content from {url}"

def search_government_portal(query):
    if "swachh bharat" in query.lower():
        return [
            "https://swachhbharatmission.gov.in/sbm-gramin-overview.html",
            "https://pib.gov.in/PressReleasePage.aspx?PRID=1934567"
        ]
    return []
