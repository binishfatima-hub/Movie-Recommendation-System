# 🎬 MovieFlix — AI Movie Recommendation System

Recommends movies using **TF-IDF** and **cosine similarity** over each film's
genres and plot.

- 106 movies, every one with a real poster and a real trailer
- Trailers play **inside the page** — no new tab, no redirect
- Genre filter, text search, and AI "similar movies" on every title
- Responsive: sidebar becomes a drawer on phones

## Two versions, one dataset

| | **Flask version** (root) | **Static version** (`docs/`) |
|---|---|---|
| Needs Python to run | Yes | No — plain HTML/CSS/JS |
| Recommendations | Computed live by scikit-learn | Precomputed into `data.js` (37 KB) — **identical results** |
| Login | Real, passwords hashed server-side | Demo only, stored in the browser |
| Hosting | Render / PythonAnywhere | **GitHub Pages**, free and instant |
| Best for | Submission and viva | A live demo link you can share |

Both read the same `dataset/movies.csv` and the same posters, so you only ever
maintain one set of data. After changing the dataset, run
`python tools/build_static.py` to refresh the static build.

> Why the static one works without Python: TF-IDF only changes when the *dataset*
> changes, not per request. The Flask app recalculates it on every search even
> though the answer is always the same. The static build does that maths once and
> ships the result.

---

## Run it on your own PC

**Windows:** just double-click **`MovieFlix.bat`**. It finds Python, installs the
libraries the first time, starts the server and opens your browser.

**Any OS:**

```bash
pip install -r requirements.txt
python app.py
```

The browser opens on <http://127.0.0.1:5000> automatically.
Create an account on the register page, then log in.

---

## Put it on GitHub

```bash
git init
git add .
git commit -m "MovieFlix - AI movie recommendation system"
git branch -M main
git remote add origin https://github.com/<your-username>/MovieRecommendationSystem.git
git push -u origin main
```

The repo is about 23 MB. The posters account for nearly all of it, and they are
stored twice — once in `static/posters/` for the Flask app and once in
`docs/posters/` because GitHub Pages can only serve files inside the published
folder. That is still far below GitHub's limits.

`users.json` is git-ignored on purpose — it holds password hashes.

---

## Host it live (free)

### Option 1 — GitHub Pages (easiest, no Python host needed)

This publishes the **static version** in `docs/`. No sleeping, no build minutes,
loads instantly.

1. Push to GitHub (above).
2. In your repo: **Settings → Pages**.
3. Under *Build and deployment* → **Source: Deploy from a branch**.
4. Branch: **`main`**, folder: **`/docs`** → **Save**.
5. After a minute your site is live at
   `https://<your-username>.github.io/MovieRecommendationSystem/`

> Pages can only serve static files, which is exactly why `docs/` exists.
> Pointing Pages at the repo root instead would **not** work — `app.py` needs
> a Python host.

### Option 2 — Render (runs the real Flask app)

This repo already contains `render.yaml`, so Render configures itself:

1. Push to GitHub (above).
2. Go to <https://render.com> → sign in with GitHub.
3. **New → Blueprint** → pick your repo → **Apply**.
4. Wait a few minutes. You get a URL like `https://movieflix.onrender.com`.

On the free plan the app sleeps after ~15 minutes idle, so the first visit
after a break takes about 30–60 seconds to wake up.

### Option 3 — PythonAnywhere

Good if you want it always awake. Free tier, no card needed.

1. Sign up at <https://www.pythonanywhere.com>.
2. **Consoles → Bash**, then:
   `git clone https://github.com/<your-username>/MovieRecommendationSystem.git`
3. **Web → Add a new web app → Manual configuration → Python 3.10+**.
4. Set the source directory to the cloned folder, then edit the WSGI file to:

   ```python
   import sys
   path = "/home/<your-username>/MovieRecommendationSystem"
   if path not in sys.path:
       sys.path.insert(0, path)
   from app import app as application
   ```

5. In a Bash console: `pip install --user -r requirements.txt`
6. Hit **Reload**.

### What runs on the server

`Procfile` and `render.yaml` both start it with:

```
gunicorn app:app --bind 0.0.0.0:$PORT
```

`app.py` detects a `PORT` environment variable and then binds `0.0.0.0`,
keeps the debug reloader off, and does not try to open a browser.
Locally, where `PORT` is unset, it stays on `127.0.0.1:5000` and opens a tab.

### One thing to know about accounts

Free hosts use a temporary filesystem, so `users.json` is wiped whenever the app
restarts or you redeploy — registered accounts disappear. That is fine for a
demo. For accounts that stick around you would swap `users.json` for a real
database (SQLite on a persistent disk, or Postgres).

---

## Project layout

```
MovieFlix.bat           Double-click to run the Flask app on Windows
Procfile / render.yaml  How a Python host starts the Flask app
app.py                  Flask routes, login/session handling
recommendation.py       TF-IDF model + all dataset queries
dataset/movies.csv      106 movies (id, title, genre, description,
                        rating, year, poster, trailer)
static/css/style.css    Single stylesheet for every page
static/posters/         106 downloaded poster images
templates/
    base.html           Shared topbar + sidebar + footer
    _movie_card.html    Shared movie card
    index.html          Home (hero, top rated, genres)
    trending.html       Top rated + latest releases
    movies.html         Full collection + filters
    movie_details.html  Details + inline trailer + similar movies
    search.html         AI recommendations
    login/register/exit/error.html
docs/                   STATIC VERSION - what GitHub Pages publishes
    index.html          App shell (topbar, sidebar, auth screen)
    app.js              Routing, rendering, search, inline trailer
    data.js             Generated: movies + precomputed recommendations
    style.css           Generated: copy of static/css/style.css
    posters/            Generated: copy of static/posters/
tools/
    movies_data.py      The master movie list
    build_dataset.py    Downloads posters, resolves trailers, writes the CSV
    build_static.py     Regenerates docs/ from the dataset
users.json              Registered users (passwords are hashed)
```

---

## How the recommender works

1. Each movie's genres (weighted ×3) and description are joined into one string.
2. `TfidfVectorizer` turns those strings into vectors of weighted word
   importance, ignoring English stop words.
3. `cosine_similarity` measures the angle between every pair of vectors.
4. Asking for recommendations returns the highest-scoring other movies, with the
   score shown on the card as a match percentage.

Because it compares *content*, not ratings, `Toy Story` returns
`Inside Out`, `The Lion King`, `Coco`, `Finding Nemo` and `Up` — not simply the
highest-rated films in the dataset.

---

## Rebuilding the dataset

`dataset/movies.csv` is generated. To change the movie list, edit
`tools/movies_data.py` and re-run:

```bash
python tools/build_dataset.py
```

It downloads each poster from Wikipedia into `static/posters/` and resolves each
trailer's YouTube id, caching results in `tools/build_cache.json` so re-runs only
fetch what is missing. Posters are stored locally on purpose — the previous
version hot-linked hand-typed URLs and most of them were dead.

Then refresh the static build so both versions stay in sync:

```bash
python tools/build_static.py
```

That regenerates `docs/data.js` (catalogue + recommendations) and re-copies the
stylesheet and posters into `docs/`.
