# -*- coding: utf-8 -*-
"""
Content based movie recommender.

Genres and plot descriptions are turned into TF-IDF vectors and compared with
cosine similarity, so a movie is "similar" when it shares vocabulary with
another one. Everything is computed once at import time and cached.
"""

import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "movies.csv")

COLUMNS = ["id", "title", "genre", "description", "rating", "year", "poster", "trailer"]


# ==========================================
# LOAD DATASET
# ==========================================

def _load_dataset():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. "
            "Run: python tools/build_dataset.py"
        )

    frame = pd.read_csv(DATASET_PATH)

    # Every column the app relies on must exist, even in an older CSV.
    for column in COLUMNS:
        if column not in frame.columns:
            frame[column] = ""

    frame["title"] = frame["title"].fillna("").astype(str).str.strip()
    frame["genre"] = frame["genre"].fillna("").astype(str).str.strip()
    frame["description"] = frame["description"].fillna("").astype(str).str.strip()
    frame["poster"] = frame["poster"].fillna("").astype(str).str.strip()
    frame["trailer"] = frame["trailer"].fillna("").astype(str).str.strip()

    frame["rating"] = pd.to_numeric(frame["rating"], errors="coerce").fillna(0.0)
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce").fillna(0).astype(int)

    # Drop rows without a title and duplicate titles, then renumber.
    frame = frame[frame["title"] != ""]
    frame = frame.drop_duplicates(subset="title", keep="first")
    frame = frame.reset_index(drop=True)

    # The id is what every URL uses, so derive it from the final row order
    # instead of trusting the file. A stale id can never point at the
    # wrong movie this way.
    frame["id"] = range(1, len(frame) + 1)

    return frame


movies = _load_dataset()


# ==========================================
# TF-IDF + COSINE SIMILARITY
# ==========================================

# Genre is repeated so that it weighs more than a single plot word.
_corpus = (
    (movies["genre"] + " ") * 3 + movies["description"]
).str.replace(",", " ", regex=False)

_vectorizer = TfidfVectorizer(stop_words="english")
_feature_matrix = _vectorizer.fit_transform(_corpus)
_similarity = cosine_similarity(_feature_matrix)

# title (lowercase) -> row position, for O(1) lookups
_title_index = {title.lower(): position for position, title in enumerate(movies["title"])}
_id_index = {int(movie_id): position for position, movie_id in enumerate(movies["id"])}


# ==========================================
# HELPERS
# ==========================================

def _records(frame):
    """Convert a dataframe slice into plain dicts for the templates."""
    return frame[COLUMNS].to_dict("records")


def _position_for_title(title):
    """Find a row position for a title: exact first, then a partial match."""
    if not title:
        return None

    needle = title.strip().lower()
    if not needle:
        return None

    if needle in _title_index:
        return _title_index[needle]

    # "dark knight" should still find "The Dark Knight".
    contains = [
        position
        for name, position in _title_index.items()
        if needle in name
    ]
    if contains:
        # Prefer the shortest title, it is usually the intended one.
        return min(contains, key=lambda position: len(movies.at[position, "title"]))

    # Last resort: any stored title contained in the query,
    # e.g. "inception movie" -> "Inception".
    reverse = [
        position
        for name, position in _title_index.items()
        if len(name) > 2 and name in needle
    ]
    if reverse:
        return max(reverse, key=lambda position: len(movies.at[position, "title"]))

    return None


# ==========================================
# PUBLIC API
# ==========================================

def get_all_movies():
    """Every movie, highest rated first."""
    return _records(movies.sort_values("rating", ascending=False))


def get_movie(movie_id):
    """One movie by id, or None."""
    try:
        position = _id_index[int(movie_id)]
    except (KeyError, TypeError, ValueError):
        return None

    return _records(movies.iloc[[position]])[0]


def get_trending(limit=8):
    """Top rated movies, used on the home page."""
    return _records(movies.sort_values("rating", ascending=False).head(limit))


def _collect_genres():
    found = set()
    for value in movies["genre"]:
        for genre in value.split(","):
            genre = genre.strip()
            if genre:
                found.add(genre)
    return sorted(found)


# Computed once; every request would otherwise rescan the whole column.
_GENRES = _collect_genres()


def get_genres():
    """Sorted list of every distinct genre in the dataset."""
    return list(_GENRES)


def get_movies_by_genre(genre):
    """Every movie tagged with `genre` (case insensitive)."""
    if not genre:
        return get_all_movies()

    needle = genre.strip().lower()
    mask = movies["genre"].str.lower().apply(
        lambda value: needle in [part.strip() for part in value.split(",")]
    )
    return _records(movies[mask].sort_values("rating", ascending=False))


def search_movies(query, limit=None):
    """Free text search across title, genre and description."""
    if not query or not query.strip():
        return []

    needle = query.strip().lower()

    haystack = (
        movies["title"].str.lower()
        + " "
        + movies["genre"].str.lower()
        + " "
        + movies["description"].str.lower()
    )

    matches = movies[haystack.str.contains(needle, regex=False)]
    matches = matches.sort_values("rating", ascending=False)

    if limit:
        matches = matches.head(limit)

    return _records(matches)


def find_movie(query):
    """Resolve a search term to a single movie, or None."""
    position = _position_for_title(query)
    if position is None:
        return None
    return _records(movies.iloc[[position]])[0]


def recommend_movies(movie_title, n=8):
    """
    Movies similar to `movie_title`.

    Returns [] when the title cannot be resolved, so the caller can show a
    "not found" state instead of a misleading empty list.
    """
    position = _position_for_title(movie_title)
    if position is None:
        return []

    scores = list(enumerate(_similarity[position]))
    scores.sort(key=lambda pair: pair[1], reverse=True)

    # scores[0] is the movie itself.
    positions = [
        index
        for index, score in scores
        if index != position and score > 0
    ][:n]

    if not positions:
        return []

    similar = movies.iloc[positions].copy()
    similar["match"] = [
        round(float(_similarity[position][index]) * 100) for index in positions
    ]

    return similar[COLUMNS + ["match"]].to_dict("records")


def recommend_by_id(movie_id, n=6):
    """Similar movies for an id, used on the details page."""
    movie = get_movie(movie_id)
    if movie is None:
        return []
    return recommend_movies(movie["title"], n)


def total_movies():
    return int(len(movies))
