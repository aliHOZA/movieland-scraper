import requests
from bs4 import BeautifulSoup
import os

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

def write_strm_file(title, year, url):
    filename = f"{title} ({year}).strm"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(url)

def scrape_movieland():
    url = "https://movieland.af/movies"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select(".movie-item"):
        title = item.select_one(".movie-title").text.strip()
        year = item.select_one(".movie-year").text.strip()
        stream_url = generate_url(title, year)
        if is_valid_stream(stream_url):
            write_strm_file(title, year, stream_url)
            print(f"✅ {title} ({year}) — .strm file created")

scrape_movieland()
