# -*- coding: utf-8 -*-
"""
MovieFlix - AI powered movie recommendation system.

Start it with:

    python app.py

The browser opens on http://127.0.0.1:5000 automatically.
"""

import json
import os
import threading
import webbrowser
from functools import wraps

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from recommendation import (
    find_movie,
    get_all_movies,
    get_genres,
    get_movie,
    get_movies_by_genre,
    get_recent,
    get_trending,
    recommend_by_id,
    recommend_movies,
    search_movies,
    total_movies,
)


# ==========================================
# FLASK APPLICATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "users.json")

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
app.secret_key = os.environ.get("MOVIEFLIX_SECRET", "movieflix_college_project_secret")


# ==========================================
# USER STORAGE
# ==========================================

def load_users():
    """Read users.json, returning {} when it is missing or corrupt."""
    if not os.path.exists(USER_FILE):
        return {}

    try:
        with open(USER_FILE, "r", encoding="utf-8") as handle:
            users = json.load(handle)
    except (OSError, ValueError):
        return {}

    return users if isinstance(users, dict) else {}


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as handle:
        json.dump(users, handle, indent=4)


def login_required(view):
    """Send signed-out visitors to the login page."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


@app.context_processor
def inject_globals():
    """Values every template needs, so no view has to pass them."""
    return {
        "username": session.get("username", ""),
        "all_genres": get_genres(),
        "movie_total": total_movies(),
    }


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("logged_in"):
        return redirect(url_for("home"))

    if request.method != "POST":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    def fail(message):
        return render_template("register.html", error=message, username=username)

    if len(username) < 3:
        return fail("Username must contain at least 3 characters.")

    if len(username) > 20:
        return fail("Username cannot be longer than 20 characters.")

    if not username.replace("_", "").isalnum():
        return fail("Username can only contain letters, numbers and underscores.")

    if len(password) < 4:
        return fail("Password must contain at least 4 characters.")

    if password != confirm_password:
        return fail("Passwords do not match.")

    users = load_users()

    if username.lower() in users:
        return fail("Username already exists. Please login.")

    users[username.lower()] = {
        "username": username,
        "password": generate_password_hash(password),
    }
    save_users(users)

    return redirect(url_for("login", registered=1))


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in") and request.method == "GET":
        return redirect(url_for("home"))

    if request.method != "POST":
        return render_template("login.html", registered=request.args.get("registered"))

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    users = load_users()
    user = users.get(username.lower())

    # Same message for both cases so the form cannot be used to
    # discover which usernames exist.
    if user is None or not check_password_hash(user.get("password", ""), password):
        return render_template(
            "login.html",
            error="Incorrect username or password.",
            username=username,
        )

    session.clear()
    session["logged_in"] = True
    session["username"] = user["username"]
    session.permanent = bool(request.form.get("remember"))

    return redirect(url_for("home"))


# ==========================================
# HOME
# ==========================================

@app.route("/")
@login_required
def home():
    return render_template(
        "index.html",
        trending=get_trending(8),
        genres=get_genres(),
    )


# ==========================================
# TRENDING
# ==========================================

@app.route("/trending")
@login_required
def trending_page():
    return render_template(
        "trending.html",
        top_rated=get_trending(12),
        latest=get_recent(12),
    )


# ==========================================
# ALL MOVIES  (supports ?genre= and ?q=)
# ==========================================

@app.route("/movies")
@login_required
def movies_page():
    genre = request.args.get("genre", "").strip()
    query = request.args.get("q", "").strip()

    if query:
        movies = search_movies(query)
    elif genre:
        movies = get_movies_by_genre(genre)
    else:
        movies = get_all_movies()

    return render_template(
        "movies.html",
        movies=movies,
        active_genre=genre,
        query=query,
    )


# ==========================================
# AI RECOMMENDATIONS
# ==========================================

@app.route("/search")
@login_required
def search():
    query = request.args.get("movie", "").strip()

    if not query:
        return redirect(url_for("home"))

    matched = find_movie(query)
    recommendations = recommend_movies(query, n=8)

    # Nothing matched the title, so offer a plain text search instead of a
    # dead end.
    suggestions = [] if matched else search_movies(query, limit=8)

    return render_template(
        "search.html",
        movie=query,
        matched=matched,
        recommendations=recommendations,
        suggestions=suggestions,
    )


# ==========================================
# MOVIE DETAILS
# ==========================================

@app.route("/movie/<int:movie_id>")
@login_required
def movie_details(movie_id):
    movie = get_movie(movie_id)

    if movie is None:
        return redirect(url_for("movies_page"))

    return render_template(
        "movie_details.html",
        movie=movie,
        similar=recommend_by_id(movie_id, n=6),
    )


# ==========================================
# LOGOUT / EXIT
# ==========================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/exit")
def exit_page():
    session.clear()
    return render_template("exit.html")


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404,
                           message="This page does not exist."), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", code=500,
                           message="Something went wrong on our side."), 500


# ==========================================
# RUN
# ==========================================

def open_browser():
    webbrowser.open_new(f"http://127.0.0.1:{PORT}/")


if __name__ == "__main__":
    # Hosting platforms (Render, Railway, PythonAnywhere...) inject PORT and
    # expect the app on 0.0.0.0. Locally neither is set, so it stays on
    # 127.0.0.1:5000 and opens a browser tab.
    on_server = "PORT" in os.environ
    host = "0.0.0.0" if on_server else HOST

    # The reloader is a development convenience: it re-executes this file in a
    # child process, which fails when there is no console (double-clicked .bat)
    # and must never run on a server. Opt in with MOVIEFLIX_DEBUG=1.
    debug = os.environ.get("MOVIEFLIX_DEBUG") == "1"

    if not on_server and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.2, open_browser).start()

    print(f"\n  MovieFlix running on http://{host}:{PORT}/\n")

    app.run(host=host, port=PORT, debug=debug)
