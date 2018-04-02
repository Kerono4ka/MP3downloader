from .mp3downloader import load_mp3_files_and_filter_by_genre

if __name__ == "__main__":
    load_mp3_files_and_filter_by_genre("../mp3links.xml", "Rock")
