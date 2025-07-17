import sqlite3
from flask import abort

# Helper: list all race DB files available
def list_race_databases():
    db_files = []
    for f in os.listdir(DATA_DIR):
        if f.endswith('Race.db') and len(f) == len('YYYYMMDDRace.db'):
            db_files.append(f)
    db_files.sort(reverse=True)  # most recent first
    return db_files

# Helper: open connection to a race DB by filename
def get_db_connection(db_filename):
    db_path = os.path.join(DATA_DIR, db_filename)
    if not os.path.isfile(db_path):
        abort(404, description=f"Database file {db_filename} not found")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn

# Route: list all race databases (dates) with links
@app.route('/races')
def races():
    db_files = list_race_databases()
    # pass filenames to template for selection
    return render_template('races.html', db_files=db_files)

# Route: show individual results for a specific race DB
@app.route('/race/<db_filename>/individual_results')
def individual_results(db_filename):
    conn = get_db_connection(db_filename)
    cursor = conn.cursor()
    # Example SQL, adjust according to your DB schema
    cursor.execute("""
        SELECT bib, name, team, finish_time, place
        FROM runners_results
        ORDER BY finish_time ASC
    """)
    results = cursor.fetchall()
    conn.close()
    return render_template('individual_results.html', results=results, race=db_filename)

# Route: show team results for a specific race DB
@app.route('/race/<db_filename>/team_results')
def team_results(db_filename):
    conn = get_db_connection(db_filename)
    cursor = conn.cursor()
    # Example SQL for team scoring; adjust as needed
    cursor.execute("""
        SELECT team, SUM(place) as team_score
        FROM runners_results
        GROUP BY team
        ORDER BY team_score ASC
    """)
    teams = cursor.fetchall()
    conn.close()
    return render_template('team_results.html', teams=teams, race=db_filename)
