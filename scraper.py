import requests
from bs4 import BeautifulSoup

def slugify(title):
    return title.lower().replace(" ", "-").replace(":", "").replace("'", "").replace(",", "")

def generate_url(title, year):
    slug = slugify(title)
    return f"https://cdn1.movieland.af/movies/{year}/{slug}/{slug}_hls/master.m3u8"

def scrape_movieland():
    url = "https://movieland.af/movies"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.select(".movie-item"):
        title = item.select_one(".movie-title").text.strip()
        year = item.select_one(".movie-year").text.strip()
        stream_url = generate_url(title, year)
        print(f"{title} ({year}): {stream_url}")

scrape_movieland()
