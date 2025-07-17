# ==============================
# Flask App and Database Helpers
# ==============================

# Flask and system imports
from flask import Flask, render_template, request, redirect, g, url_for, flash, session, send_from_directory
import sqlite3
import os
import glob
import bcrypt
from functools import wraps

# Paths to key directories and config database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONSOLE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DATA_DIR = os.path.join(CONSOLE_DIR, 'data')
WEB_DIR = BASE_DIR
CONFIG_DB_PATH = os.path.join(DATA_DIR, 'config.db')

# Flask application initialization
app = Flask(__name__, template_folder=os.path.join(WEB_DIR, 'templates'),
            static_folder=os.path.join(WEB_DIR, 'static'))
app.secret_key = 'Ansol2182$'

# ==============================
# Authentication and Database Utilities
# ==============================

def login_required(f):
    """
    Decorator that restricts access to authenticated users only.
    Redirects to login page if user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db(db_path):
    """
    Opens the specified SQLite database and attaches it to Flask's `g` context for reuse.
    Raises an error if the file is missing.
    """
    db = getattr(g, '_database', None)
    if db is None:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f'Database not found: {db_path}')
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
    return db

def get_config_db():
    """
    Opens the configuration database containing user authentication info.
    """
    db = getattr(g, '_config_database', None)
    if db is None:
        db = g._config_database = sqlite3.connect(CONFIG_DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes database connections when the request context ends.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    config_db = getattr(g, '_config_database', None)
    if config_db is not None:
        config_db.close()

# ==============================
# Public Pages and Routes
# ==============================

@app.route('/')
def index():
    """
    Home page listing all race results by race ID.
    Builds links to individual and team results for each race.
    """
    db_files = glob.glob(os.path.join(DATA_DIR, '*-race.db'))
    race_links = []
    for db_file in db_files:
        filename = os.path.basename(db_file)
        parts = filename.split('-')
        if len(parts) >= 3:
            race_id = f"{parts[0]}-{parts[1]}"
            race_links.append({
                'race_id': race_id,
                'individual_url': url_for('individual_results', race_id=race_id),
                'team_url': url_for('team_results', race_id=race_id)
            })
    # Sort races by date and sequence number
    def race_key(link):
        date_part, race_part = link['race_id'].split('-')
        return (int(date_part), int(race_part))
    race_links.sort(key=race_key)
    return render_template('index.html', race_links=race_links)

@app.route('/title-slide')
def title_slide():
    """
    Redirects to the title_slide.pdf file in the static directory.
    """
    return redirect(url_for('static', filename='title_slide.pdf'))

@app.route('/about_us')
def about_us():
    """
    Displays the About Us static page.
    """
    return render_template('about_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    """
    Displays a contact form and shows a thank-you flash message on submission.
    """
    if request.method == 'POST':
        flash("Thank you for contacting us!", 'success')
        return redirect(url_for('contact_us'))
    return render_template('contact_us.html')

@app.route('/help')
def help():
    """
    Displays the Help static page.
    """
    return render_template('help.html')

@app.route('/individual_results/<race_id>')
def individual_results(race_id):
    """
    Displays a list of individual race results for a given race ID.
    Results are ordered by finish time.
    """
    db_path = os.path.join(DATA_DIR, f"{race_id}-race.db")
    db = get_db(db_path)
    cur = db.execute('''
        SELECT r.bib, ru.name, ru.team, r.finish_time
        FROM results r
        JOIN runners ru ON r.bib = ru.bib
        ORDER BY r.finish_time ASC
    ''')
    runners = cur.fetchall()
    return render_template('individual_results.html', runners=runners, race_id=race_id)

@app.route('/team_results/<race_id>')
def team_results(race_id):
    """
    Displays team scoring for a given race.
    Scores are calculated by adding the places of the first 5 finishers per team.
    """
    db_path = os.path.join(DATA_DIR, f"{race_id}-race.db")
    db = get_db(db_path)
    cur = db.execute('''
        SELECT ru.team, r.bib, ru.name, r.finish_time
        FROM results r
        JOIN runners ru ON r.bib = ru.bib
        ORDER BY r.finish_time ASC
    ''')
    results = cur.fetchall()

    # Group results by team
    team_scores = {}
    for row in results:
        team_scores.setdefault(row['team'], []).append(row)

    # Calculate total scores
    team_totals = []
    for team, runners in team_scores.items():
        score = sum(range(1, min(len(runners), 5) + 1))
        team_totals.append({'team': team, 'score': score, 'members': runners})
    team_totals.sort(key=lambda x: x['score'])

    return render_template('team_results.html', team_totals=team_totals, race_id=race_id)

# ==============================
# Authentication Routes
# ==============================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Displays the login form and processes login requests.
    Verifies the username and bcrypt-hashed password from the config database.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_config_db()
        cur = db.execute('SELECT user_id, username, password_hash FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logs out the current user and clears the session.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# ==============================
# Admin and Management Pages
# ==============================

@app.route('/admin')
@login_required
def admin():
    """
    Displays the admin home page. Requires login.
    """
    return render_template('admin.html')

@app.route('/edit_results')
@login_required
def edit_results():
    """
    Displays a list of available race databases for editing.
    Groups the races by date.
    """
    db_files = glob.glob(os.path.join(DATA_DIR, '*-race.db'))
    grouped = {}
    for path in db_files:
        filename = os.path.basename(path)
        parts = filename.split('-')
        if len(parts) >= 3:
            date = parts[0]
            race_id = f"{parts[0]}-{parts[1]}"
            grouped.setdefault(date, []).append(race_id)
    for races in grouped.values():
        races.sort(key=lambda x: int(x.split('-')[1]))
    return render_template('edit_results.html', grouped_races=grouped)

@app.route('/edit_results/<race_id>', methods=['GET', 'POST'])
@login_required
def edit_race(race_id):
    """
    Allows an admin to edit bib numbers for finish results for a given race.
    Updates the database on form submission.
    """
    db_path = os.path.join(DATA_DIR, f"{race_id}-race.db")
    db = get_db(db_path)
    if request.method == 'POST':
        # Update bib numbers in results
        for key, value in request.form.items():
            if key.startswith('bib_'):
                result_id = key.split('_')[1]
                db.execute('UPDATE results SET bib = ? WHERE id = ?', (value, result_id))
        db.commit()
        flash('Results updated successfully.', 'success')
        return redirect(url_for('edit_race', race_id=race_id))

    cur = db.execute('''
        SELECT r.id as result_id, r.bib, ru.name, r.finish_time
        FROM results r
        LEFT JOIN runners ru ON r.bib = ru.bib
        ORDER BY r.finish_time ASC
    ''')
    results = cur.fetchall()
    return render_template('edit_race.html', race_id=race_id, results=results)

@app.route('/documentation')
@login_required
def documentation():
    """
    Displays the documentation page. Requires login.
    """
    return render_template('documentation.html')

@app.route('/usage_notes')
@login_required
def usage_notes():
    """
    Displays the usage notes page. Requires login.
    """
    return render_template('usage_notes.html')

# ==============================
# Run the Application
# ==============================

if __name__ == '__main__':
    app.run(debug=False)
# ==============================
# Flask App and Database Helpers
# ==============================

# Flask and system imports
from flask import Flask, render_template, request, redirect, g, url_for, flash, session, send_from_directory
import sqlite3
import os
import glob
import bcrypt
from functools import wraps

# Paths to key directories and config database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONSOLE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DATA_DIR = os.path.join(CONSOLE_DIR, 'data')
WEB_DIR = BASE_DIR
CONFIG_DB_PATH = os.path.join(DATA_DIR, 'config.db')

# Flask application initialization
app = Flask(__name__, template_folder=os.path.join(WEB_DIR, 'templates'),
            static_folder=os.path.join(WEB_DIR, 'static'))
app.secret_key = 'Ansol2182$'

# ==============================
# Authentication and Database Utilities
# ==============================

def login_required(f):
    """
    Decorator that restricts access to authenticated users only.
    Redirects to login page if user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db(db_path):
    """
    Opens the specified SQLite database and attaches it to Flask's `g` context for reuse.
    Raises an error if the file is missing.
    """
    db = getattr(g, '_database', None)
    if db is None:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f'Database not found: {db_path}')
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
    return db

def get_config_db():
    """
    Opens the configuration database containing user authentication info.
    """
    db = getattr(g, '_config_database', None)
    if db is None:
        db = g._config_database = sqlite3.connect(CONFIG_DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes database connections when the request context ends.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    config_db = getattr(g, '_config_database', None)
    if config_db is not None:
        config_db.close()

# ==============================
# Public Pages and Routes
# ==============================

@app.route('/')
def index():
    """
    Home page listing all race results by race ID.
    Builds links to individual and team results for each race.
    """
    db_files = glob.glob(os.path.join(DATA_DIR, '*-race.db'))
    race_links = []
    for db_file in db_files:
        filename = os.path.basename(db_file)
        parts = filename.split('-')
        if len(parts) >= 3:
            race_id = f"{parts[0]}-{parts[1]}"
            race_links.append({
                'race_id': race_id,
                'individual_url': url_for('individual_results', race_id=race_id),
                'team_url': url_for('team_results', race_id=race_id)
            })
    # Sort races by date and sequence number
    def race_key(link):
        date_part, race_part = link['race_id'].split('-')
        return (int(date_part), int(race_part))
    race_links.sort(key=race_key)
    return render_template('index.html', race_links=race_links)

@app.route('/title-slide')
def title_slide():
    """
    Redirects to the title_slide.pdf file in the static directory.
    """
    return redirect(url_for('static', filename='title_slide.pdf'))

@app.route('/about_us')
def about_us():
    """
    Displays the About Us static page.
    """
    return render_template('about_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    """
    Displays a contact form and shows a thank-you flash message on submission.
    """
    if request.method == 'POST':
        flash("Thank you for contacting us!", 'success')
        return redirect(url_for('contact_us'))
    return render_template('contact_us.html')

@app.route('/help')
def help():
    """
    Displays the Help static page.
    """
    return render_template('help.html')

@app.route('/individual_results/<race_id>')
def individual_results(race_id):
    """
    Displays a list of individual race results for a given race ID.
    Results are ordered by finish time.
    """
    db_path = os.path.join(DATA_DIR, f"{race_id}-race.db")
    db = get_db(db_path)
    cur = db.execute('''
        SELECT r.bib, ru.name, ru.team, r.finish_time
        FROM results r
        JOIN runners ru ON r.bib = ru.bib
        ORDER BY r.finish_time ASC
    ''')
    runners = cur.fetchall()
    return render_template('individual_results.html', runners=runners, race_id=race_id)

@app.route('/team_results/<race_id>')
def team_results(race_id):
    """
    Displays team scoring for a given race.
    Scores are calculated by adding the places of the first 5 finishers per team.
    """
    db_path = os.path.join(DATA_DIR, f"{race_id}-race.db")
    db = get_db(db_path)
    cur = db.execute('''
        SELECT ru.team, r.bib, ru.name, r.finish_time
        FROM results r
        JOIN runners ru ON r.bib = ru.bib
        ORDER BY r.finish_time ASC
    ''')
    results = cur.fetchall()

    # Group results by team
    team_scores = {}
    for row in results:
        team_scores.setdefault(row['team'], []).append(row)

    # Calculate total scores
    team_totals = []
    for team, runners in team_scores.items():
        score = sum(range(1, min(len(runners), 5) + 1))
        team_totals.append({'team': team, 'score': score, 'members': runners})
    team_totals.sort(key=lambda x: x['score'])

    return render_template('team_results.html', team_totals=team_totals, race_id=race_id)

# ==============================
# Authentication Routes
# ==============================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Displays the login form and processes login requests.
    Verifies the username and bcrypt-hashed password from the config database.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_config_db()
        cur = db.execute('SELECT user_id, username, password_hash FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Logs out the current user and clears the session.
    """
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# ==============================
# Admin and Management Pages
# ==============================

@app.route('/admin')
@login_required
def admin():
    """
    Displays the admin home page. Requires login.
    """
    return render_template('admin.html')

@app.route('/edit_results')
@login_required
def edit_results():
    """
    Displays a list of available race databases for editing.
    Groups the races by date.
    """
    db_files = glob.glob(os.path.join(DATA_DIR, '*-race.db'))
    grouped = {}
    for path in db_files:
        filename = os.path.basename(path)
        parts = filename.split('-')
        if len(parts) >= 3:
            date = parts[0]
            race_id = f"{parts[0]}-{parts[1]}"
            grouped.setdefault(date, []).append(race_id)
    for races in grouped.values():
        races.sort(key=lambda x: int(x.split('-')[1]))
    return render_template('edit_results.html', grouped_races=grouped)

@app.route('/edit_results/<race_id>', methods=['GET', 'POST'])
@login_required
def edit_race(race_id):
    """
    Allows an admin to edit bib numbers for finish results for a given race.
    Updates the database on form submission.
    """
    db_path = os.path.join(DATA_DIR, f"{race_id}-race.db")
    db = get_db(db_path)
    if request.method == 'POST':
        # Update bib numbers in results
        for key, value in request.form.items():
            if key.startswith('bib_'):
                result_id = key.split('_')[1]
                db.execute('UPDATE results SET bib = ? WHERE id = ?', (value, result_id))
        db.commit()
        flash('Results updated successfully.', 'success')
        return redirect(url_for('edit_race', race_id=race_id))

    cur = db.execute('''
        SELECT r.id as result_id, r.bib, ru.name, r.finish_time
        FROM results r
        LEFT JOIN runners ru ON r.bib = ru.bib
        ORDER BY r.finish_time ASC
    ''')
    results = cur.fetchall()
    return render_template('edit_race.html', race_id=race_id, results=results)

@app.route('/documentation')
@login_required
def documentation():
    """
    Displays the documentation page. Requires login.
    """
    return render_template('documentation.html')

@app.route('/usage_notes')
@login_required
def usage_notes():
    """
    Displays the usage notes page. Requires login.
    """
    return render_template('usage_notes.html')

# ==============================
# Run the Application
# ==============================

if __name__ == '__main__':
    app.run(debug=False)
