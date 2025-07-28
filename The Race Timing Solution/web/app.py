# ==============================
# Flask App and Database Helpers - Updated for Cross Country & Road Race Support
# ==============================

# Flask and system imports
from flask import Flask, render_template, request, redirect, g, url_for, flash, session, send_from_directory
import sqlite3
import os
import glob
import bcrypt
from functools import wraps
import datetime

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
# Database Utilities - Updated for New Format
# ==============================

def get_race_type(db_path):
    """
    Determines the race type from the database.
    Returns 'cross_country', 'road_race', or 'unknown'.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT type FROM race_type")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'unknown'
    except:
        return 'unknown'

def get_race_databases():
    """
    Returns a list of race database information with race type detection.
    Supports both old format (*-race.db) and new format (YYYYMMDD-##-[cc/rr]-Name.db).
    """
    # Look for both old and new format databases
    old_format_files = glob.glob(os.path.join(DATA_DIR, '*-race.db'))
    new_format_files = glob.glob(os.path.join(DATA_DIR, '*-cc-*.db')) + glob.glob(os.path.join(DATA_DIR, '*-rr-*.db'))
    
    race_info = []
    
    # Process old format files
    for db_file in old_format_files:
        filename = os.path.basename(db_file)
        parts = filename.split('-')
        if len(parts) >= 3:
            race_id = f"{parts[0]}-{parts[1]}"
            race_type = get_race_type(db_file)
            race_info.append({
                'race_id': race_id,
                'filename': filename,
                'race_type': race_type,
                'display_name': f"Race {race_id}",
                'db_path': db_file
            })
    
    # Process new format files
    for db_file in new_format_files:
        filename = os.path.basename(db_file)
        parts = filename.replace('.db', '').split('-')
        if len(parts) >= 4:
            date_part = parts[0]
            race_num = parts[1]
            race_type_code = parts[2]
            race_name = '-'.join(parts[3:])
            
            race_id = f"{date_part}-{race_num}"
            race_type = 'cross_country' if race_type_code == 'cc' else 'road_race'
            
            # Format display name nicely
            try:
                date_obj = datetime.datetime.strptime(date_part, '%Y%m%d')
                date_display = date_obj.strftime('%B %d, %Y')
                type_display = 'Cross Country' if race_type == 'cross_country' else 'Road Race'
                display_name = f"{date_display} - Race {race_num} ({type_display}): {race_name.replace('_', ' ')}"
            except:
                display_name = f"Race {race_id} ({race_type_code.upper()}): {race_name.replace('_', ' ')}"
            
            race_info.append({
                'race_id': race_id,
                'filename': filename,
                'race_type': race_type,
                'display_name': display_name,
                'db_path': db_file,
                'race_name': race_name.replace('_', ' ')
            })
    
    # Sort by date and race number
    def race_sort_key(info):
        parts = info['race_id'].split('-')
        return (int(parts[0]), int(parts[1]))
    
    race_info.sort(key=race_sort_key, reverse=True)  # Most recent first
    return race_info

def format_time_display(seconds):
    """
    Formats elapsed seconds into a readable time format.
    """
    if seconds is None:
        return "N/A"
    
    try:
        total_seconds = float(seconds)
        minutes, secs = divmod(total_seconds, 60)
        hours, mins = divmod(int(minutes), 60)
        
        if hours > 0:
            return f"{int(hours)}:{int(mins):02d}:{secs:06.3f}"
        else:
            return f"{int(mins):02d}:{secs:06.3f}"
    except:
        return str(seconds)

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
# Public Pages and Routes - Updated
# ==============================

@app.route('/')
def index():
    """
    Home page listing all race results with race type indicators.
    Now shows separate links for Cross Country and Road Race results.
    """
    race_info = get_race_databases()
    
    # Group races by type for better organization
    cross_country_races = [r for r in race_info if r['race_type'] == 'cross_country']
    road_races = [r for r in race_info if r['race_type'] == 'road_race']
    unknown_races = [r for r in race_info if r['race_type'] == 'unknown']
    
    return render_template('index.html', 
                         cross_country_races=cross_country_races,
                         road_races=road_races,
                         unknown_races=unknown_races)

@app.route('/cross_country_results')
def cross_country_results():
    """
    Lists only Cross Country race databases.
    """
    race_info = get_race_databases()
    cc_races = [r for r in race_info if r['race_type'] == 'cross_country']
    
    return render_template('cross_country_results.html', races=cc_races)

@app.route('/road_race_results')
def road_race_results():
    """
    Lists only Road Race databases.
    """
    race_info = get_race_databases()
    rr_races = [r for r in race_info if r['race_type'] == 'road_race']
    
    return render_template('road_race_results.html', races=rr_races)

@app.route('/individual_results/<race_id>')
def individual_results(race_id):
    """
    Displays individual race results for any race type.
    Works with both old and new database formats.
    """
    # Find the correct database file
    race_info = get_race_databases()
    db_info = next((r for r in race_info if r['race_id'] == race_id), None)
    
    if not db_info:
        flash('Race not found.', 'error')
        return redirect(url_for('index'))
    
    db_path = db_info['db_path']
    race_type = db_info['race_type']
    
    try:
        db = get_db(db_path)
        
        # Query based on database structure
        if race_type == 'cross_country':
            # Cross country: get team info
            cur = db.execute('''
                SELECT results.bib, COALESCE(runners.name,'UNKNOWN') as name, 
                       COALESCE(runners.team,'UNKNOWN') as team, results.finish_time
                FROM results 
                LEFT JOIN runners ON results.bib = runners.bib
                ORDER BY results.finish_time ASC
            ''')
        elif race_type == 'road_race':
            # Road race: get age info
            cur = db.execute('''
                SELECT results.bib, COALESCE(runners.name,'UNKNOWN') as name, 
                       runners.age, results.finish_time
                FROM results 
                LEFT JOIN runners ON results.bib = runners.bib
                ORDER BY results.finish_time ASC
            ''')
        else:
            # Unknown type: try basic query
            cur = db.execute('''
                SELECT results.bib, COALESCE(runners.name,'UNKNOWN') as name, 
                       COALESCE(runners.team,'') as team, results.finish_time
                FROM results 
                LEFT JOIN runners ON results.bib = runners.bib
                ORDER BY results.finish_time ASC
            ''')
        
        runners = cur.fetchall()
        
        # Format times for display
        formatted_runners = []
        for i, runner in enumerate(runners):
            formatted_runners.append({
                'place': i + 1,
                'bib': runner['bib'],
                'name': runner['name'],
                'team': runner.get('team', ''),
                'age': runner.get('age', ''),
                'finish_time_raw': runner['finish_time'],
                'finish_time': format_time_display(runner['finish_time'])
            })
        
        return render_template('individual_results.html', 
                             runners=formatted_runners, 
                             race_info=db_info)
    
    except Exception as e:
        flash(f'Error loading race results: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/team_results/<race_id>')
def team_results(race_id):
    """
    Displays Cross Country team scoring for a given race.
    Uses proper team scoring logic (top 5 + displacers).
    """
    # Find the correct database file
    race_info = get_race_databases()
    db_info = next((r for r in race_info if r['race_id'] == race_id), None)
    
    if not db_info:
        flash('Race not found.', 'error')
        return redirect(url_for('index'))
    
    if db_info['race_type'] != 'cross_country':
        flash('Team results are only available for Cross Country races.', 'warning')
        return redirect(url_for('individual_results', race_id=race_id))
    
    db_path = db_info['db_path']
    
    try:
        db = get_db(db_path)
        cur = db.execute('''
            SELECT COALESCE(runners.team,'UNKNOWN') as team, results.bib, 
                   runners.name, results.finish_time
            FROM results 
            LEFT JOIN runners ON results.bib = runners.bib
            ORDER BY results.finish_time ASC
        ''')
        results = cur.fetchall()

        # Group runners by teams (same logic as console version)
        teams = {}
        for place, row in enumerate(results, 1):
            team = row['team']
            teams.setdefault(team, []).append({
                'place': place,
                'bib': row['bib'],
                'name': row['name'],
                'finish_time_raw': row['finish_time'],
                'finish_time': format_time_display(row['finish_time'])
            })

        # Calculate team scores (same logic as console version)
        team_results = []
        for team, runners in teams.items():
            if len(runners) >= 5:  # Need at least 5 runners to score
                top5 = runners[:5]
                displacers = runners[5:7]  # 6th and 7th runners
                score = sum(r['place'] for r in top5)
                
                # Tiebreaker info
                tiebreak = [r['place'] for r in displacers] + [float('inf'), float('inf')]
                
                team_results.append({
                    'team': team,
                    'score': score,
                    'top5': top5,
                    'displacers': displacers,
                    'tiebreak1': tiebreak[0],
                    'tiebreak2': tiebreak[1]
                })

        # Sort teams by score (lowest wins), then by tiebreakers
        team_results.sort(key=lambda x: (x['score'], x['tiebreak1'], x['tiebreak2']))

        return render_template('team_results.html', 
                             team_results=team_results, 
                             race_info=db_info)
    
    except Exception as e:
        flash(f'Error loading team results: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/age_group_results/<race_id>')
def age_group_results(race_id):
    """
    Displays Road Race age group results for a given race.
    Uses same age group logic as console version.
    """
    # Find the correct database file
    race_info = get_race_databases()
    db_info = next((r for r in race_info if r['race_id'] == race_id), None)
    
    if not db_info:
        flash('Race not found.', 'error')
        return redirect(url_for('index'))
    
    if db_info['race_type'] != 'road_race':
        flash('Age group results are only available for Road races.', 'warning')
        return redirect(url_for('individual_results', race_id=race_id))
    
    db_path = db_info['db_path']
    
    try:
        db = get_db(db_path)
        cur = db.execute('''
            SELECT runners.age, results.bib, runners.name, results.finish_time
            FROM results 
            LEFT JOIN runners ON results.bib = runners.bib
            ORDER BY results.finish_time ASC
        ''')
        results = cur.fetchall()

        # Define age groups (same as console version)
        age_groups = [
            (1, 15), (16, 20), (21, 25), (26, 30), (31, 35), (36, 40),
            (41, 45), (46, 50), (51, 55), (56, 60), (61, 65), (66, 70), (71, 200)
        ]
        
        # Group results by age
        results_by_group = {f"{low}-{high}": [] for (low, high) in age_groups}
        
        for i, row in enumerate(results, 1):
            age = row['age'] if row['age'] else 0
            
            # Find appropriate age group
            for (low, high) in age_groups:
                if low <= age <= high:
                    results_by_group[f"{low}-{high}"].append({
                        'overall_place': i,
                        'bib': row['bib'],
                        'name': row['name'],
                        'age': age,
                        'finish_time_raw': row['finish_time'],
                        'finish_time': format_time_display(row['finish_time'])
                    })
                    break

        # Remove empty age groups and add group place numbers
        final_age_groups = {}
        for group_name, runners in results_by_group.items():
            if runners:
                # Add age group place numbers
                for i, runner in enumerate(runners, 1):
                    runner['age_group_place'] = i
                final_age_groups[group_name] = runners

        return render_template('age_group_results.html', 
                             age_groups=final_age_groups, 
                             race_info=db_info)
    
    except Exception as e:
        flash(f'Error loading age group results: {str(e)}', 'error')
        return redirect(url_for('index'))

# ==============================
# Static Pages
# ==============================

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

# ==============================
# Authentication Routes
# ==============================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Displays the login form and processes login requests.
    Uses the same bcrypt authentication as console/GUI versions.
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
# Admin and Management Pages - Updated
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
    Now supports both race types and new filename format.
    """
    race_info = get_race_databases()
    
    # Group by date for better organization
    grouped = {}
    for race in race_info:
        date_part = race['race_id'].split('-')[0]
        grouped.setdefault(date_part, []).append(race)
    
    # Sort races within each date
    for races in grouped.values():
        races.sort(key=lambda x: int(x['race_id'].split('-')[1]))
    
    return render_template('edit_results.html', grouped_races=grouped)

@app.route('/edit_results/<race_id>', methods=['GET', 'POST'])
@login_required
def edit_race(race_id):
    """
    Allows an admin to edit bib numbers for finish results for a given race.
    Works with both old and new database formats.
    """
    # Find the correct database file
    race_info = get_race_databases()
    db_info = next((r for r in race_info if r['race_id'] == race_id), None)
    
    if not db_info:
        flash('Race not found.', 'error')
        return redirect(url_for('edit_results'))
    
    db_path = db_info['db_path']
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
        SELECT results.id as result_id, results.bib, 
               COALESCE(runners.name,'UNKNOWN') as name, results.finish_time
        FROM results 
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    results = cur.fetchall()
    
    # Format results for display
    formatted_results = []
    for i, result in enumerate(results):
        formatted_results.append({
            'place': i + 1,
            'result_id': result['result_id'],
            'bib': result['bib'],
            'name': result['name'],
            'finish_time': format_time_display(result['finish_time'])
        })
    
    return render_template('edit_race.html', 
                         race_info=db_info, 
                         results=formatted_results)

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
    app.run(debug=False, host='0.0.0.0', port='8080')