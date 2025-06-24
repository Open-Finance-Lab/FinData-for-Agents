import os
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class LetterDownloader:
    def __init__(self, base_url="https://www.berkshirehathaway.com/letters/", save_dir="./berkshire_letters/"):
        self.base_url = base_url
        self.save_dir = save_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
        os.makedirs(self.save_dir, exist_ok=True)

    def download_file(self, url, save_path):
        try:
            response = requests.get(url, headers=self.headers, stream=True, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"Download failed: {url} ({response.status_code})")
                return False
            
        except Exception as e:
            print(f"Download error: {url} ({e})")
            return False

    def extract_letters(self):
        try:
            response = requests.get(self.base_url + "letters.html", headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href'].strip()
                match = re.search(r'(\d{4})(ltr)?\.(html|pdf)$', href)
                if match:
                    year = match.group(1)
                    file_type = match.group(3)
                    full_url = href if href.startswith("http") else self.base_url + href
                    links.append((year, full_url, file_type))
            return links
        
        except Exception as e:
            print(f"Failed to extract: {e}")
            return []

    def download_all_letters(self, file_types=("html", "pdf")):
        letters = self.extract_letters()
        letters = [l for l in letters if l[2] in file_types]
        print(f"Found {len(letters)} letters")

        for year, url, file_type in tqdm(letters, desc="Downloading"):
            path = os.path.join(self.save_dir, f"{year}.{file_type}")
            if not os.path.exists(path):
                self.download_file(url, path)
            else:
                print(f"Exists: {year}.{file_type}")

        print(f"Saved to: {os.path.abspath(self.save_dir)}")


