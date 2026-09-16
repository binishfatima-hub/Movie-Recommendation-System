# -*- coding: utf-8 -*-
"""
Build dataset/movies.csv and download every poster into static/posters/.

Run once (needs internet):

    python tools/build_dataset.py

Why posters are downloaded instead of hot-linked:
the old version linked to hand-typed TMDB URLs, most of which were invalid,
so a lot of cards showed the grey fallback tile. Local files can never break.

Trailer IDs are resolved once here and stored in the CSV, so the running
application never needs the network.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from movies_data import MOVIES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTER_DIR = os.path.join(ROOT, "static", "posters")
CSV_PATH = os.path.join(ROOT, "dataset", "movies.csv")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_cache.json")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def fetch(url, timeout=30):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "movie"


# ---------------------------------------------------------------- posters

def wiki_summary(page):
    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + urllib.parse.quote(page.replace(" ", "_"), safe="")
    )
    try:
        return json.loads(fetch(url).decode("utf-8", "ignore"))
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None


def wiki_search(title, year):
    """Fallback when the hard-coded page title does not resolve."""
    url = (
        "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json"
        "&srlimit=1&srsearch="
        + urllib.parse.quote(f"{title} {year} film")
    )
    try:
        data = json.loads(fetch(url).decode("utf-8", "ignore"))
        hits = data.get("query", {}).get("search", [])
        return hits[0]["title"] if hits else None
    except Exception:
        return None


def poster_candidates(title, year, page):
    """Return candidate image URLs for the film's poster, best first."""
    summary = wiki_summary(page)

    if summary is None or "originalimage" not in summary:
        alternative = wiki_search(title, year)
        if alternative and alternative != page:
            summary = wiki_summary(alternative)

    if not summary:
        return []

    image = summary.get("originalimage") or summary.get("thumbnail")
    if not image:
        return []

    original = image.get("source", "").split("?")[0]
    if not original:
        return []

    candidates = []

    # Wikipedia fair-use posters are already small (~220-300px wide) and
    # cannot be upscaled, so only build a thumb when the source is large.
    if image.get("width", 0) > 600:
        thumb = re.sub(
            r"/(commons|en)/([0-9a-f])/([0-9a-f]{2})/",
            lambda m: "/%s/thumb/%s/%s/" % (m.group(1), m.group(2), m.group(3)),
            original,
        )
        if thumb != original:
            name = thumb.rsplit("/", 1)[-1]
            if name.lower().endswith(".svg"):
                name += ".png"
            candidates.append(f"{thumb}/500px-{name}")

    candidates.append(original)
    return candidates


def existing_poster(slug):
    """Return the stored path if this poster was already downloaded."""
    for extension in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        path = os.path.join(POSTER_DIR, slug + extension)
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            return f"posters/{slug}{extension}"
    return ""


def download_poster(url, destination, attempts=4):
    """Download an image, backing off when Wikimedia rate limits us."""
    last_error = None

    for attempt in range(attempts):
        try:
            data = fetch(url, timeout=45)
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in (429, 503):
                raise
            time.sleep(3 * (attempt + 1))
            continue

        if len(data) < 1000:
            raise ValueError("image too small, probably an error page")

        with open(destination, "wb") as handle:
            handle.write(data)
        return len(data)

    raise last_error


# --------------------------------------------------------------- trailers

def trailer_id_for(title, year):
    """Resolve the YouTube video id of the film's official trailer."""
    query = urllib.parse.quote(f"{title} {year} official trailer")
    url = f"https://www.youtube.com/results?search_query={query}"

    try:
        html = fetch(url, timeout=30).decode("utf-8", "ignore")
    except Exception:
        return ""

    ids = re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', html)
    return ids[0] if ids else ""


# ------------------------------------------------------------------ main

def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            pass
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as handle:
        json.dump(cache, handle, indent=2, ensure_ascii=False)


def main():
    os.makedirs(POSTER_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    cache = load_cache()
    rows = []
    missing_posters = []
    missing_trailers = []

    for index, (title, genre, description, rating, year, page) in enumerate(MOVIES, start=1):
        entry = cache.setdefault(title, {})
        slug = slugify(title)

        # ---- poster -----------------------------------------------------
        poster_value = existing_poster(slug)

        if not poster_value:
            urls = entry.get("poster_urls") or poster_candidates(title, year, page)
            entry["poster_urls"] = urls

            for url in urls:
                # Keep the real extension so Flask serves the right MIME type.
                extension = os.path.splitext(url.split("?")[0])[1].lower()
                if extension not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
                    extension = ".jpg"

                poster_file = slug + extension
                poster_path = os.path.join(POSTER_DIR, poster_file)

                try:
                    size = download_poster(url, poster_path)
                    poster_value = f"posters/{poster_file}"
                    print(f"[{index:3}/{len(MOVIES)}] poster  OK  {title} ({size // 1024} KB)")
                    break
                except Exception as error:
                    print(f"[{index:3}/{len(MOVIES)}] poster retry {title}: {error}")

            if not poster_value:
                missing_posters.append(title)

        # ---- trailer ----------------------------------------------------
        trailer = entry.get("trailer")
        if not trailer:
            trailer = trailer_id_for(title, year)
            if trailer:
                entry["trailer"] = trailer
                print(f"[{index:3}/{len(MOVIES)}] trailer OK  {title} -> {trailer}")
            else:
                print(f"[{index:3}/{len(MOVIES)}] trailer FAIL {title}")
            time.sleep(0.4)  # be polite to YouTube

        if not trailer:
            missing_trailers.append(title)

        rows.append(
            {
                "id": index,
                "title": title,
                "genre": genre,
                "description": description,
                "rating": rating,
                "year": year,
                "poster": poster_value,
                "trailer": trailer or "",
            }
        )

        if index % 10 == 0:
            save_cache(cache)

    save_cache(cache)

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "title", "genre", "description", "rating", "year", "poster", "trailer"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Wrote {len(rows)} movies to {CSV_PATH}")
    print(f"Posters missing : {len(missing_posters)} {missing_posters}")
    print(f"Trailers missing: {len(missing_trailers)} {missing_trailers}")


if __name__ == "__main__":
    main()
