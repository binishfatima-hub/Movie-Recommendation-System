/* =========================================================
   MovieFlix - static build
   Same data and same recommendations as the Flask version,
   but every page is rendered here in the browser.
   ========================================================= */

'use strict';

const STORE_USERS = 'movieflix.users';
const STORE_SESSION = 'movieflix.session';

const BY_ID = new Map(MOVIES.map(m => [m.id, m]));


/* ---------------------------------------------------------
   helpers
   --------------------------------------------------------- */

const $ = id => document.getElementById(id);

/** Escape anything that came from a user or the dataset before it becomes HTML. */
function esc(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/* Some browsers block localStorage on file:// and in private mode. Fall back to
   memory so the page opened straight from disk still works for this visit. */
const memoryStore = {};

const storageWorks = (() => {
    try {
        localStorage.setItem('movieflix.probe', '1');
        localStorage.removeItem('movieflix.probe');
        return true;
    } catch (e) {
        return false;
    }
})();

function read(key, fallback) {
    try {
        const raw = storageWorks ? localStorage.getItem(key) : memoryStore[key];
        return raw === undefined || raw === null ? fallback : JSON.parse(raw);
    } catch (e) {
        return fallback;
    }
}

function write(key, value) {
    const raw = JSON.stringify(value);
    try {
        if (storageWorks) localStorage.setItem(key, raw);
        else memoryStore[key] = raw;
    } catch (e) {
        memoryStore[key] = raw;
    }
}

function remove(key) {
    try {
        if (storageWorks) localStorage.removeItem(key);
    } catch (e) {
        /* ignore */
    }
    delete memoryStore[key];
}

function genresOf(movie) {
    return movie.genre.split(',').map(g => g.trim()).filter(Boolean);
}

const GENRE_EMOJI = {
    Action: '💥', Adventure: '🧭', Animation: '🎨', Biography: '📖',
    Comedy: '😂', Crime: '🔫', Drama: '🎭', Family: '👨‍👩‍👧',
    Fantasy: '🧙', History: '🏛️', Horror: '👻', Music: '🎵',
    Mystery: '🕵️', Romance: '❤️', 'Sci-Fi': '🚀', Sport: '🏅',
    Thriller: '😱', War: '⚔️', Western: '🤠'
};


/* ---------------------------------------------------------
   search / recommendation logic
   (ported from recommendation.py so results match the Flask app)
   --------------------------------------------------------- */

/** Resolve a typed query to one movie: exact title, then partial, then reverse. */
function findMovie(query) {
    const needle = (query || '').trim().toLowerCase();
    if (!needle) return null;

    const exact = MOVIES.find(m => m.title.toLowerCase() === needle);
    if (exact) return exact;

    // "dark knight" -> "The Dark Knight"  (shortest title wins)
    const contains = MOVIES.filter(m => m.title.toLowerCase().includes(needle));
    if (contains.length) {
        return contains.reduce((a, b) => (a.title.length <= b.title.length ? a : b));
    }

    // "inception movie" -> "Inception"  (longest stored title wins)
    const reverse = MOVIES.filter(
        m => m.title.length > 2 && needle.includes(m.title.toLowerCase())
    );
    if (reverse.length) {
        return reverse.reduce((a, b) => (a.title.length >= b.title.length ? a : b));
    }

    return null;
}

/** Free text search across title, genre and description. */
function searchMovies(query, limit) {
    const needle = (query || '').trim().toLowerCase();
    if (!needle) return [];

    const hits = MOVIES.filter(m =>
        (m.title + ' ' + m.genre + ' ' + m.description).toLowerCase().includes(needle)
    ).sort((a, b) => b.rating - a.rating);

    return limit ? hits.slice(0, limit) : hits;
}

/** Precomputed by tools/build_static.py using the exact same TF-IDF model. */
function recommendationsFor(movieId) {
    return (SIMILAR[movieId] || [])
        .map(([id, match]) => {
            const movie = BY_ID.get(id);
            return movie ? Object.assign({}, movie, { match }) : null;
        })
        .filter(Boolean);
}

function moviesByGenre(genre) {
    return MOVIES
        .filter(m => genresOf(m).some(g => g.toLowerCase() === genre.toLowerCase()))
        .sort((a, b) => b.rating - a.rating);
}

const byRating = list => list.slice().sort((a, b) => b.rating - a.rating);

/** Newest first, best rated first within the same year. */
const byYear = list =>
    list.slice().sort((a, b) => b.year - a.year || b.rating - a.rating);


/* ---------------------------------------------------------
   accounts  (demo only - see the note on the sign-in card)
   --------------------------------------------------------- */

const auth = {
    users: () => read(STORE_USERS, {}),

    current: () => read(STORE_SESSION, null),

    register(username, password, confirm) {
        username = username.trim();

        if (username.length < 3) return 'Username must contain at least 3 characters.';
        if (username.length > 20) return 'Username cannot be longer than 20 characters.';
        if (!/^\w+$/.test(username)) return 'Username can only contain letters, numbers and underscores.';
        if (password.length < 4) return 'Password must contain at least 4 characters.';
        if (password !== confirm) return 'Passwords do not match.';

        const users = auth.users();
        if (users[username.toLowerCase()]) return 'Username already exists. Please login.';

        users[username.toLowerCase()] = { username, password };
        write(STORE_USERS, users);
        return null;
    },

    login(username, password) {
        const user = auth.users()[username.trim().toLowerCase()];
        if (!user || user.password !== password) return 'Incorrect username or password.';
        write(STORE_SESSION, user.username);
        return null;
    },

    logout() {
        remove(STORE_SESSION);
    }
};


/* ---------------------------------------------------------
   shared fragments
   --------------------------------------------------------- */

function posterLayers(movie, sizeClass) {
    const fallback =
        '<div class="poster-fallback">' +
            '<span class="fallback-icon">🎬</span>' +
            '<strong>' + esc(movie.title) + '</strong>' +
            '<span class="fallback-tag">MOVIEFLIX</span>' +
        '</div>';

    const image = movie.poster
        ? '<img src="' + esc(movie.poster) + '" alt="' + esc(movie.title) +
          ' poster" loading="lazy" onerror="this.remove();">'
        : '';

    return fallback + image;
}

function movieCard(movie) {
    return '' +
    '<article class="movie-card">' +
        '<a class="poster" href="#/movie/' + movie.id + '">' +
            posterLayers(movie) +
            '<span class="poster-overlay"><span class="play-btn">▶</span></span>' +
            '<span class="rating">⭐ ' + movie.rating.toFixed(1) + '</span>' +
            (movie.match !== undefined
                ? '<span class="ai-label">🤖 ' + movie.match + '% MATCH</span>'
                : '') +
        '</a>' +
        '<div class="movie-info">' +
            '<h3 title="' + esc(movie.title) + '">' + esc(movie.title) + '</h3>' +
            '<p class="movie-genre">' + esc(movie.genre) + '</p>' +
            '<div class="card-bottom">' +
                '<span>📅 ' + movie.year + '</span>' +
                '<a class="details-link" href="#/search?q=' +
                    encodeURIComponent(movie.title) + '">🤖 Similar</a>' +
            '</div>' +
        '</div>' +
    '</article>';
}

const grid = list => '<div class="movie-grid">' + list.map(movieCard).join('') + '</div>';

const footer = () => '' +
    '<footer>' +
        '<div class="footer-brand">🎬 MovieFlix</div>' +
        '<p>AI Powered Movie Recommendation System</p>' +
        '<small>Logged in as ' + esc(auth.current() || '') + '</small><br>' +
        '<small>© 2026 MovieFlix • College Project</small>' +
    '</footer>';

const infoBox = () => '' +
    '<div class="info-box">' +
        '<h2>🤖 How the recommendations work</h2>' +
        '<p>' +
            'Each movie\'s genres and plot are converted into TF-IDF vectors and ' +
            'compared with cosine similarity. Those scores are computed once when ' +
            'the site is built, so this page needs no server to rank them.' +
        '</p>' +
    '</div>';


/* ---------------------------------------------------------
   views
   --------------------------------------------------------- */

function viewHome() {
    const trending = byRating(MOVIES).slice(0, 8);

    return '' +
    '<section class="hero">' +
        '<div class="hero-content">' +
            '<span class="hero-badge">🤖 AI POWERED MOVIE RECOMMENDATIONS</span>' +
            '<h1>Find Your Next <span>Favorite Movie</span></h1>' +
            '<p>Welcome <strong>' + esc(auth.current() || '') + '</strong>! ' +
               'Search any of our ' + MOVIES.length + ' movies and the AI will ' +
               'recommend titles with similar genres and stories.</p>' +
            '<form class="big-search" data-role="search">' +
                '<input type="text" name="q" required ' +
                       'placeholder="Try &quot;Inception&quot;, &quot;Dangal&quot; or &quot;Toy Story&quot;...">' +
                '<button type="submit">🔍 Search</button>' +
            '</form>' +
        '</div>' +
    '</section>' +

    '<section id="trending" class="movie-section">' +
        '<div class="section-heading">' +
            '<div><span class="small-title">NOW WATCHING</span>' +
                 '<h2>🔥 Top Rated Movies</h2></div>' +
            '<a href="#/movies" class="view-all">Explore All →</a>' +
        '</div>' +
        grid(trending) +
    '</section>' +

    '<section id="genres" class="genre-section">' +
        '<div class="section-heading">' +
            '<div><span class="small-title">EXPLORE</span>' +
                 '<h2>🎭 Browse Genres</h2></div>' +
        '</div>' +
        '<div class="genre-grid">' +
            GENRES.map(g =>
                '<a class="genre-card" href="#/movies?genre=' + encodeURIComponent(g) + '">' +
                    '<span class="genre-emoji">' + (GENRE_EMOJI[g] || '🎬') + '</span>' +
                    '<span class="genre-name">' + esc(g) + '</span>' +
                '</a>').join('') +
        '</div>' +
    '</section>' +

    '<section class="ai-banner">' +
        '<div>' +
            '<span>🤖 SMART RECOMMENDATION ENGINE</span>' +
            '<h2>Let AI Find Your Next Movie</h2>' +
            '<p>Every movie is converted into a TF-IDF vector built from its ' +
               'genres and plot. Cosine similarity then ranks the closest matches.</p>' +
        '</div>' +
        '<a href="#/movies">Explore Movies →</a>' +
    '</section>' +

    footer();
}


function viewTrending() {
    return '' +
    '<div class="page-head">' +
        '<span class="small-title">RIGHT NOW</span>' +
        '<h1>🔥 <span>Trending</span> on MovieFlix</h1>' +
        '<p>The highest rated titles in the collection, plus everything that ' +
           'landed most recently.</p>' +
        '<div class="count-pill">🎬 ' + MOVIES.length + ' movies in the library</div>' +
    '</div>' +

    '<section class="movie-section">' +
        '<div class="section-heading">' +
            '<div><span class="small-title">MOST LOVED</span>' +
                 '<h2>⭐ Top Rated</h2></div>' +
            '<a href="#/movies" class="view-all">Browse all →</a>' +
        '</div>' +
        grid(byRating(MOVIES).slice(0, 12)) +
    '</section>' +

    '<section class="movie-section">' +
        '<div class="section-heading">' +
            '<div><span class="small-title">FRESH RELEASES</span>' +
                 '<h2>🆕 Latest Movies</h2></div>' +
        '</div>' +
        grid(byYear(MOVIES).slice(0, 12)) +
    '</section>' +

    '<section class="ai-banner">' +
        '<div>' +
            '<span>🤖 SMART RECOMMENDATION ENGINE</span>' +
            '<h2>Not sure what to watch?</h2>' +
            '<p>Open any movie above and MovieFlix will find titles with ' +
               'similar genres and stories using TF-IDF and cosine similarity.</p>' +
        '</div>' +
        '<a href="#/movies">Explore Movies →</a>' +
    '</section>' +

    footer();
}


function viewMovies(params) {
    const genre = params.get('genre') || '';
    const query = params.get('q') || '';

    let list;
    if (query) list = searchMovies(query);
    else if (genre) list = moviesByGenre(genre);
    else list = byRating(MOVIES);

    let heading;
    if (genre) heading = '<span>' + esc(genre) + '</span> Movies';
    else if (query) heading = 'Results for <span>' + esc(query) + '</span>';
    else heading = 'Movie <span>Collection</span>';

    const chips =
        '<a class="genre-chip' + (!genre && !query ? ' active' : '') + '" href="#/movies">All</a>' +
        GENRES.map(g =>
            '<a class="genre-chip' + (genre === g ? ' active' : '') +
            '" href="#/movies?genre=' + encodeURIComponent(g) + '">' + esc(g) + '</a>').join('');

    const body = list.length
        ? grid(list)
        : '<div class="empty-state">' +
              '<div class="empty-icon">🔍</div>' +
              '<h2>No movies found</h2>' +
              '<p>Nothing in the library matches that filter. Try another genre or search term.</p>' +
              '<a class="primary-btn" href="#/movies">Show all movies</a>' +
          '</div>';

    return '' +
    '<div class="page-head">' +
        '<h1>' + heading + '</h1>' +
        '<p>' + (query
            ? 'Every movie whose title, genre or story matches your search.'
            : 'Browse the full library and open any title for AI recommendations.') + '</p>' +
        '<form class="inline-search" data-role="filter">' +
            '<input type="text" name="q" value="' + esc(query) + '" ' +
                   'placeholder="Filter movies by name, genre or story..." aria-label="Filter movies">' +
            '<button type="submit">Filter</button>' +
            (query || genre ? '<a class="clear-filter" href="#/movies">Clear</a>' : '') +
        '</form>' +
        '<div class="pill-row">' + chips + '</div>' +
        '<div class="count-pill">🎬 ' + list.length + ' movies</div>' +
    '</div>' +
    body +
    infoBox() +
    footer();
}


function viewMovie(id) {
    const movie = BY_ID.get(id);
    if (!movie) { location.hash = '#/movies'; return ''; }

    const similar = recommendationsFor(movie.id).slice(0, 6);

    const trailer = movie.trailer
        ? '<div class="trailer-box" id="trailerBox">' +
              '<button type="button" class="trailer-poster" id="trailerPoster" ' +
                      'aria-label="Play ' + esc(movie.title) + ' trailer">' +
                  '<img src="https://i.ytimg.com/vi/' + esc(movie.trailer) +
                       '/hqdefault.jpg" alt="" onerror="this.remove();">' +
                  '<span class="trailer-play">▶</span>' +
                  '<span class="trailer-caption">Play trailer</span>' +
              '</button>' +
          '</div>' +
          '<p class="trailer-note">The trailer plays on this page — no new tab, no redirect.</p>'
        : '<div class="trailer-box trailer-empty"><div>' +
              '<div class="trailer-icon">🎬</div>' +
              '<h3>Trailer unavailable</h3>' +
              '<p>No trailer has been linked for this title yet.</p>' +
          '</div></div>';

    return '' +
    '<a href="#/movies" class="back-link">← Back to Movies</a>' +

    '<div class="details-container">' +
        '<div class="details-poster">' + posterLayers(movie) + '</div>' +
        '<div class="details-info">' +
            '<div class="rating-box">⭐ ' + movie.rating.toFixed(1) + '/10</div>' +
            '<h1>' + esc(movie.title) + '</h1>' +
            '<div class="meta-row">' +
                genresOf(movie).map(g =>
                    '<a class="meta" href="#/movies?genre=' + encodeURIComponent(g) + '">🎭 ' +
                    esc(g) + '</a>').join('') +
                '<span class="meta">📅 ' + movie.year + '</span>' +
            '</div>' +
            '<p class="description">' + esc(movie.description) + '</p>' +
            '<div class="action-row">' +
                (movie.trailer
                    ? '<button type="button" class="watch-btn" id="watchBtn">▶ Watch Trailer</button>'
                    : '') +
                '<a href="#/search?q=' + encodeURIComponent(movie.title) +
                   '" class="secondary-btn">🤖 Find Similar Movies</a>' +
            '</div>' +
        '</div>' +
    '</div>' +

    '<section class="trailer-section" id="trailer">' +
        '<h2>▶ ' + esc(movie.title) + ' — Official Trailer</h2>' +
        trailer +
    '</section>' +

    (similar.length
        ? '<section class="movie-section similar-section">' +
              '<div class="section-heading">' +
                  '<div><span class="small-title">AI RECOMMENDATIONS</span>' +
                       '<h2>🎯 Because you opened ' + esc(movie.title) + '</h2></div>' +
                  '<a href="#/search?q=' + encodeURIComponent(movie.title) +
                     '" class="view-all">See all →</a>' +
              '</div>' +
              grid(similar) +
          '</section>'
        : '') +

    infoBox() +
    footer();
}


function viewSearch(params) {
    const query = params.get('q') || '';
    const matched = findMovie(query);
    const recommendations = matched ? recommendationsFor(matched.id) : [];
    const suggestions = matched ? [] : searchMovies(query, 8);

    let head;
    if (matched) {
        head = '<h1>Movies similar to <span>' + esc(matched.title) + '</span></h1>' +
               '<p>The AI compared genres and plots across all ' + MOVIES.length +
               ' movies and ranked the closest matches below.</p>';
    } else {
        head = '<h1>Search results for <span>' + esc(query) + '</span></h1>' +
               '<p>No exact title matched, so here is everything related to your search.</p>';
    }

    const strip = matched
        ? '<section class="matched-strip">' +
              '<a class="matched-poster" href="#/movie/' + matched.id + '">' +
                  posterLayers(matched) +
              '</a>' +
              '<div class="matched-info">' +
                  '<span class="matched-tag">YOU SEARCHED FOR</span>' +
                  '<h2>' + esc(matched.title) + '</h2>' +
                  '<div class="meta-row">' +
                      '<span class="meta">⭐ ' + matched.rating.toFixed(1) + '</span>' +
                      '<span class="meta">📅 ' + matched.year + '</span>' +
                      '<span class="meta">🎭 ' + esc(matched.genre) + '</span>' +
                  '</div>' +
                  '<p class="description">' + esc(matched.description) + '</p>' +
                  '<a class="primary-btn" href="#/movie/' + matched.id +
                     '">▶ Open &amp; watch trailer</a>' +
              '</div>' +
          '</section>'
        : '';

    const recSection = recommendations.length
        ? '<section class="movie-section">' +
              '<div class="section-heading">' +
                  '<div><span class="small-title">RANKED BY SIMILARITY</span>' +
                       '<h2>🎯 Recommended for you</h2></div>' +
                  '<span class="view-all">' + recommendations.length + ' AI recommendations</span>' +
              '</div>' +
              grid(recommendations) +
          '</section>'
        : '';

    const sugSection = suggestions.length
        ? '<section class="movie-section">' +
              '<div class="section-heading">' +
                  '<div><span class="small-title">TEXT SEARCH</span>' +
                       '<h2>🔎 Movies matching "' + esc(query) + '"</h2></div>' +
              '</div>' +
              grid(suggestions) +
          '</section>'
        : '';

    const empty = (!recommendations.length && !suggestions.length)
        ? '<div class="empty-state">' +
              '<div class="empty-icon">😔</div>' +
              '<h2>Nothing found for "' + esc(query) + '"</h2>' +
              '<p>That title is not in the library yet. Browse the collection and ' +
                 'pick a movie to get AI recommendations.</p>' +
              '<a class="primary-btn" href="#/movies">🎬 Browse all movies</a>' +
          '</div>'
        : '';

    return '' +
    '<div class="page-head"><span class="small-title">🤖 AI RECOMMENDATION ENGINE</span>' +
        head +
    '</div>' +
    strip + recSection + sugSection + empty +

    '<section class="search-again">' +
        '<h2>Search another movie</h2>' +
        '<p>Type any title from the collection to get a fresh set of recommendations.</p>' +
        '<form data-role="search">' +
            '<input type="text" name="q" placeholder="Enter a movie name..." required>' +
            '<button type="submit">🔍 Recommend</button>' +
        '</form>' +
    '</section>' +

    footer();
}


function viewGenres() {
    return '' +
    '<div class="page-head">' +
        '<h1>Browse <span>Genres</span></h1>' +
        '<p>Pick a genre to see every movie tagged with it.</p>' +
        '<div class="count-pill">🎭 ' + GENRES.length + ' genres • ' +
             MOVIES.length + ' movies</div>' +
    '</div>' +
    '<div class="genre-grid">' +
        GENRES.map(g =>
            '<a class="genre-card" href="#/movies?genre=' + encodeURIComponent(g) + '">' +
                '<span class="genre-emoji">' + (GENRE_EMOJI[g] || '🎬') + '</span>' +
                '<span class="genre-name">' + esc(g) + '</span>' +
            '</a>').join('') +
    '</div>' +
    infoBox() +
    footer();
}


/* ---------------------------------------------------------
   router
   --------------------------------------------------------- */

function parseHash() {
    const raw = location.hash.replace(/^#\/?/, '');
    const [path, search] = raw.split('?');

    return {
        // A stray leading "#" (an old "#/#trending" style link) would otherwise
        // never match a route and fall through to the 404 view.
        path: path.replace(/^#+/, '').replace(/\/$/, ''),
        params: new URLSearchParams(search || '')
    };
}

function render() {
    if (!auth.current()) { showAuth(); return; }

    $('authScreen').hidden = true;
    $('appShell').hidden = false;

    const { path, params } = parseHash();
    const view = $('view');

    let html;
    let active = '';

    if (path === '' || path === 'home') {
        html = viewHome(); active = 'home';
    } else if (path === 'trending') {
        html = viewTrending(); active = 'trending';
    } else if (path === 'movies') {
        html = viewMovies(params); active = 'movies';
    } else if (path === 'genres') {
        html = viewGenres(); active = 'genres';
    } else if (path === 'search') {
        html = viewSearch(params);
    } else if (path.startsWith('movie/')) {
        html = viewMovie(Number(path.slice('movie/'.length)));
        active = 'movies';
    } else if (path === 'exit') {
        auth.logout();
        showAuth('Thank you for using MovieFlix! 👋');
        return;
    } else {
        html = '<div class="empty-state">' +
                   '<div class="error-code">404</div>' +
                   '<h2>Page not found</h2>' +
                   '<p>That page does not exist.</p>' +
                   '<a class="primary-btn" href="#/">← Back to Home</a>' +
               '</div>' + footer();
    }

    view.innerHTML = html;
    window.scrollTo(0, 0);
    document.body.classList.remove('sidebar-open');

    document.querySelectorAll('[data-nav]').forEach(link => {
        link.classList.toggle('active', link.dataset.nav === active);
    });

    $('topSearchInput').value = path === 'search' ? (params.get('q') || '') : '';

    const watch = $('watchBtn');
    const poster = $('trailerPoster');
    if (watch) watch.addEventListener('click', playTrailer);
    if (poster) poster.addEventListener('click', playTrailer);
}


/** Swap the thumbnail for a real YouTube iframe, in place. */
function playTrailer() {
    const box = $('trailerBox');
    if (!box) return;

    if (box.dataset.playing === '1') {
        box.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
    }

    const { path } = parseHash();
    const movie = BY_ID.get(Number(path.slice('movie/'.length)));
    if (!movie || !movie.trailer) return;

    const frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/' + movie.trailer +
                '?autoplay=1&rel=0&modestbranding=1';
    frame.title = movie.title + ' trailer';
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; ' +
                  'gyroscope; picture-in-picture';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';

    box.innerHTML = '';
    box.appendChild(frame);
    box.dataset.playing = '1';
    box.scrollIntoView({ behavior: 'smooth', block: 'center' });
}


/* ---------------------------------------------------------
   auth screen
   --------------------------------------------------------- */

let registerMode = false;

function showAuth(message) {
    $('appShell').hidden = true;
    $('authScreen').hidden = false;

    if (message) setAuthMessage(message, 'login-success');
    else clearAuthMessage();
}

function setAuthMessage(text, className) {
    const box = $('authMessage');
    box.textContent = text;
    box.className = className;
    box.hidden = false;
}

function clearAuthMessage() {
    const box = $('authMessage');
    box.hidden = true;
    box.textContent = '';
}

function setMode(toRegister) {
    registerMode = toRegister;

    $('authTitle').textContent = toRegister ? 'Create Account' : 'Welcome Back';
    $('authSubtitle').textContent = toRegister
        ? 'Register to start discovering movies'
        : 'Sign in to continue to MovieFlix';
    $('authSubmit').textContent = toRegister ? 'Create Account →' : 'Login →';
    $('confirmRow').hidden = !toRegister;
    $('authConfirm').required = toRegister;
    $('authSwitchText').textContent = toRegister
        ? 'Already have an account?'
        : "Don't have an account?";
    $('authSwitch').textContent = toRegister ? 'Login' : 'Create Account';

    clearAuthMessage();
    $('authForm').reset();
}


/* ---------------------------------------------------------
   wiring
   --------------------------------------------------------- */

$('authSwitch').addEventListener('click', event => {
    event.preventDefault();
    setMode(!registerMode);
});

$('authForm').addEventListener('submit', event => {
    event.preventDefault();

    const username = $('authUser').value;
    const password = $('authPass').value;

    if (registerMode) {
        const error = auth.register(username, password, $('authConfirm').value);
        if (error) { setAuthMessage(error, 'login-error'); return; }
        setMode(false);
        setAuthMessage('Registration successful! Please login to continue.', 'login-success');
        return;
    }

    const error = auth.login(username, password);
    if (error) { setAuthMessage(error, 'login-error'); return; }

    if (!location.hash || location.hash === '#/exit') location.hash = '#/';
    render();
});

$('logoutLink').addEventListener('click', event => {
    event.preventDefault();
    auth.logout();
    location.hash = '#/';
    showAuth();
});

$('topSearch').addEventListener('submit', event => {
    event.preventDefault();
    const value = $('topSearchInput').value.trim();
    if (value) location.hash = '#/search?q=' + encodeURIComponent(value);
});

/* Search and filter forms are re-created on every render, so listen once here. */
$('view').addEventListener('submit', event => {
    const form = event.target.closest('form[data-role]');
    if (!form) return;

    event.preventDefault();
    const value = (form.querySelector('[name="q"]').value || '').trim();

    if (form.dataset.role === 'search') {
        if (value) location.hash = '#/search?q=' + encodeURIComponent(value);
    } else {
        location.hash = value ? '#/movies?q=' + encodeURIComponent(value) : '#/movies';
    }
});

window.addEventListener('hashchange', render);


/* ---------------------------------------------------------
   boot
   --------------------------------------------------------- */

(function init() {
    $('sidebarGenres').innerHTML = GENRES.slice(0, 8).map(g =>
        '<a class="genre-chip" href="#/movies?genre=' + encodeURIComponent(g) + '">' +
        esc(g) + '</a>').join('');

    $('sidebarCount').textContent = MOVIES.length + ' movies • College Project';

    const user = auth.current();
    if (user) $('userLabel').textContent = '👤 ' + user;

    setMode(false);
    render();

    // keep the header name in sync after login
    const observer = () => {
        const current = auth.current();
        $('userLabel').textContent = current ? '👤 ' + current : '';
    };
    window.addEventListener('hashchange', observer);
    $('authForm').addEventListener('submit', () => setTimeout(observer, 0));
})();
