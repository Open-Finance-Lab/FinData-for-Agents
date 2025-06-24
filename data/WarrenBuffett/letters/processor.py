import os
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from PyPDF2 import PdfReader

class LetterDataProcessor:
    def __init__(self, input_dir="./berkshire_letters/", output_dir="./berkshire_letters/processed/"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _extract_text_from_pdf(self, file_path):
        try:
            reader = PdfReader(file_path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text
        except Exception as e:
            print(f"PDF extraction failed: {file_path} ({e})")
            return ""

    def _extract_text_from_html(self, file_path):
        try:
            with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                return soup.get_text(separator="\n")
        except Exception as e:
            print(f"HTML extraction failed: {file_path} ({e})")
            return ""

    def clean_text(self, text):
        text = re.sub(r'\n+', '\n', text)  # 连续换行
        text = re.sub(r'[ \t]+', ' ', text)  # 多空格
        text = re.sub(r'\f', '', text)  # 清除分页符
        return text.strip()

    def process_all_files(self):
        for fname in os.listdir(self.input_dir):
            if fname.endswith(".pdf") or fname.endswith(".html"):
                year = fname.split(".")[0]
                input_path = os.path.join(self.input_dir, fname)
                output_path = os.path.join(self.output_dir, f"{year}.txt")

                if fname.endswith(".pdf"):
                    raw_text = self._extract_text_from_pdf(input_path)
                else:
                    raw_text = self._extract_text_from_html(input_path)

                clean = self.clean_text(raw_text)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(clean)
                print(f"Processed {fname} -> {output_path}")