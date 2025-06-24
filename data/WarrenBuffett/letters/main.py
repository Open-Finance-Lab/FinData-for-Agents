from downloader import LetterDownloader
from processor import LetterDataProcessor

if __name__ == "__main__":
    # Step 1: download all letters
    downloader = LetterDownloader()
    downloader.download_all_letters()

    # Step 2: data processing
    processor = LetterDataProcessor()
    processor.process_all_files()