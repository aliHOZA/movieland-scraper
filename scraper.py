import requests
from bs4 import BeautifulSoup
import os
import shutil

def slugify(title):
    return title.lower().replace(" ", "-").replace(":", "").replace("'", "").replace(",", "")

def generate_url(title, year):
    slug = slugify(title)
    return f"https://cdn1.movieland.af/movies/{year}/{slug}/{slug}_hls/master.m3u8"

def is_valid_stream(url):
    try:
        r = requests.head(url, timeout=5)
        return r.status_code == 200
    except:
        return False

def archive_old_strm_files():
    archive_folder = "Old-strm"
    os.makedirs(archive_folder, exist_ok=True)

    for root, dirs, files in os.walk("streams"):
        for file in files:
            if file.endswith(".strm"):
                old_path = os.path.join(root, file)
                new_path = os.path.join(archive_folder, file)
                shutil.move(old_path, new_path)

def write_strm_file(title, year, url, persian_title=None):
    folder = os.path.join("streams", year)
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{title} ({year}).strm")
    with open(filename, "w", encoding="utf-8") as f:
        if persian_title:
            f.write(f"# {persian_title}\n")
        f.write(url)

def scrape_movieland():
    url = "https://movieland.af/movies"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    archive_old_strm_files()

    for item in soup.select(".movie-item"):
        title = item.select_one(".movie-title").text.strip()
        year = item.select_one(".movie-year").text.strip()
        persian_title = item.select_one(".movie-title-fa").text.strip() if item.select_one(".movie-title-fa") else None
        stream_url = generate_url(title, year)
        if is_valid_stream(stream_url):
            write_strm_file(title, year, stream_url, persian_title)
            print(f"✅ {title} ({year}) — saved to streams/{year}/")

scrape_movieland()
