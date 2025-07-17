import sqlite3
import os
import datetime
import glob
import csv
from playsound import playsound
import bcrypt
import hashlib
import getpass

# ==============================
# Globals
# ==============================

# DB_FILENAME stores the path to the active race database file
DB_FILENAME = ""
# race_started and race_stopped track whether a race is currently running or stopped
race_started = False
race_stopped = False
# race_start_time records the datetime when the race starts
race_start_time = None

# ==============================
# Database helpers
# ==============================

def initialize_config_db():
    """
    Creates the configuration database in /data/ if it does not exist.
    Prompts the user to set up an admin username and password (bcrypt hashed).
    Creates the 'users' table for authentication.
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    config_db_path = os.path.join(data_dir, 'config.db')

    if not os.path.exists(config_db_path):
        print("No config.db found — creating new configuration database in /data/...")
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()

        # Create a users table to store login credentials
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            )
        ''')

        # Prompt for an admin account setup
        admin_username = input("Enter admin username: ").strip()
        while not admin_username:
            print("Username cannot be empty.")
            admin_username = input("Enter admin username: ").strip()

        admin_password = getpass.getpass("Enter admin password: ").strip()
        while not admin_password:
            print("Password cannot be empty.")
            admin_password = getpass.getpass("Enter admin password: ").strip()

        # Hash and store the admin password
        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                  (admin_username, password_hash))

        conn.commit()
        conn.close()
        print("Configuration database created successfully at /data/config.db.")
    else:
        print("Config database already exists at /data/config.db.")

def get_next_db_filename():
    """
    Generates a filename for a new race database in the format YYYYMMDD-##-race.db.
    Increments the sequence number (##) if multiple races occur on the same day.
    """
    today = datetime.datetime.now().strftime('%Y%m%d')
    os.makedirs('data', exist_ok=True)
    existing = glob.glob(f"data/{today}-??-race.db")
    seq_nums = []
    for fname in existing:
        try:
            seq = int(fname.split("-")[1])
            seq_nums.append(seq)
        except:
            pass
    next_seq = max(seq_nums) + 1 if seq_nums else 1
    return f"data/{today}-{next_seq:02d}-race.db"

def init_db(new_db=True):
    """
    Creates a new race database or opens an existing one.
    Sets up the runners and results tables if they do not exist.
    """
    global DB_FILENAME
    os.makedirs("data", exist_ok=True)

    if new_db:
        DB_FILENAME = get_next_db_filename()
        print(f"[INFO] New database created: {DB_FILENAME}")

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    # Create the runners table
    c.execute('''
        CREATE TABLE IF NOT EXISTS runners (
            bib INTEGER PRIMARY KEY,
            name TEXT,
            team TEXT,
            rfid TEXT
        )
    ''')
    # Create the results table
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bib INTEGER,
            finish_time REAL,
            race_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_existing_db():
    """
    Prompts the user for a filename to load an existing race database from the /data directory.
    """
    global DB_FILENAME
    filename = input("Enter DB filename in data/: ").strip()
    path = os.path.join('data', filename)
    if os.path.exists(path):
        DB_FILENAME = path
        print(f"[INFO] Loaded database: {DB_FILENAME}")
    else:
        print("[ERROR] File does not exist.")
        return
    init_db(new_db=False)

# Path to the config database
CONFIG_DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'config.db')

# ==============================
# Race logic
# ==============================

def load_runners_from_csv(csv_file):
    """
    Loads runner information from a CSV file and populates the runners table.
    Each runner has a bib, name, team, and optional RFID tag.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded. Create or load a DB first.")
        return

    full_path = os.path.join('data', csv_file)
    if not os.path.exists(full_path):
        print(f"[ERROR] File not found: {full_path}")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    with open(full_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            c.execute('''
                INSERT OR REPLACE INTO runners (bib, name, team, rfid)
                VALUES (?, ?, ?, ?)
            ''', (row['bib'], row['name'], row['team'], row['rfid']))
    conn.commit()
    conn.close()
    print(f"[INFO] Loaded runners from {full_path}")

def start_race():
    """
    Starts the race and initializes the race start time.
    Begins accepting bib inputs in live race mode.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded. Create or load a DB first.")
        return
    if race_started:
        print("[INFO] Race is already running.")
        return
    race_started = True
    race_stopped = False
    race_start_time = datetime.datetime.now()
    print(f"[INFO] Race started at {race_start_time.strftime('%H:%M:%S')}")
    live_race_input()

def stop_race():
    """
    Stops the race and resets race tracking variables.
    """
    global race_started, race_stopped
    if not race_started:
        print("[INFO] Race hasn't started yet.")
        return
    race_stopped = True
    race_started = False
    print("[INFO] Race stopped. Returning to menu.")

def record_result(bib):
    """
    Records the finish time of a runner when they cross the finish line.
    Accepts a bib number or leaves it blank for unknown finishers.
    """
    if not race_started or race_stopped:
        print("[WARNING] Cannot record result — race is not active!")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    finish_time = datetime.datetime.now()
    elapsed = (finish_time - race_start_time).total_seconds()
    race_date = race_start_time.strftime('%Y-%m-%d')

    # Default bib to 0 if unknown
    if bib == "":
        bib_value = 0
    else:
        try:
            bib_value = int(bib)
        except ValueError:
            print("[ERROR] Invalid bib number.")
            return

    # Store result in the database
    c.execute('''
        INSERT INTO results (bib, finish_time, race_date)
        VALUES (?, ?, ?)
    ''', (bib_value, elapsed, race_date))
    conn.commit()
    conn.close()

    bib_display = bib if bib else "UNKNOWN"
    print(f"[RESULT] Bib {bib_display} finished in {elapsed:.2f}s")

    # Play a sound to confirm the finish
    try:
        playsound('beep.mp3')
    except:
        print("[Sound] Could not play sound.")

def live_race_input():
    """
    Continuously prompts for runner bib numbers while the race is running.
    Type 'exit' to stop taking inputs.
    """
    print("[INPUT MODE] Race is active. Enter bib number, or just Enter for unknown finisher.")
    print("Type 'exit' to stop recording and return to menu.")
    while race_started and not race_stopped:
        bib = input("> ").strip()
        if bib.lower() == 'exit':
            print("[INFO] Exiting live input mode and returning to menu.")
            stop_race()
            break
        record_result(bib)

# ==============================
# Results
# ==============================

def show_individual_results():
    """
    Displays a list of individual results ordered by finish time.
    Shows bib, name, team, and finish time for each runner.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT 
            results.bib,
            COALESCE(runners.name, 'UNKNOWN'),
            COALESCE(runners.team, 'UNKNOWN'),
            results.finish_time
        FROM results
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    rows = c.fetchall()

    print("\n=== Individual Results ===")
    for i, row in enumerate(rows, 1):
        print(f"{i}. Place: {i} | Bib: {row[0]}, Name: {row[1]}, Team: {row[2]}, Time: {row[3]:.2f}s")
    conn.close()

def show_team_results():
    """
    Calculates team scores by summing the places of the top 5 finishers for each team.
    Displays each team's scoring places and displacers.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT 
            COALESCE(runners.team, 'UNKNOWN') AS team,
            results.bib,
            results.finish_time
        FROM results
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    rows = c.fetchall()
    conn.close()

    place = 1
    team_places = {}

    # Collect places for each team
    for row in rows:
        team = row[0]
        if team not in team_places:
            team_places[team] = []
        team_places[team].append(place)
        place += 1

    print("\n=== Team Results (Scoring by Place: top 5 + 2 displacers) ===")
    for team, places in team_places.items():
        scorers = places[:5]
        displacers = places[5:7] if len(places) > 5 else []
        total_score = sum(scorers)
        print(f"Team: {team}")
        print(f"  Scorers (places): {scorers} -> Total: {total_score}")
        if displacers:
            print(f"  Displacers (places): {displacers}")

def show_all_runners():
    """
    Lists all runners in the database, grouped by team.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT bib, name, team
        FROM runners
        ORDER BY team ASC, bib ASC
    ''')
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("[INFO] No runners found in the database.")
        return

    print("\n=== Runners by Team ===")
    current_team = None
    for row in rows:
        bib, name, team = row
        if team != current_team:
            current_team = team
            print(f"\nTeam: {current_team}")
        print(f"  Bib: {bib} | Name: {name}")

# ==============================
# Menu
# ==============================

def main_menu():
    """
    Displays the main console menu and handles user input.
    Provides options to manage databases, runners, races, and results.
    """
    while True:
        print("\n=== Race Timing Menu ===")
        print("1) Create new database")
        print("2) Load existing database")
        print("3) Load runners from CSV (data/)")
        print("4) Start Race")
        print("5) Show Individual Results")
        print("6) Show Team Results")
        print("7) Show All Runners")
        print("8) Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            init_db(new_db=True)
        elif choice == "2":
            load_existing_db()
        elif choice == "3":
            csv_file = input("CSV filename (in data/): ").strip()
            load_runners_from_csv(csv_file)
        elif choice == "4":
            start_race()
        elif choice == "5":
            show_individual_results()
        elif choice == "6":
            show_team_results()
        elif choice == "7":
            show_all_runners()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    # Ensure the config database exists, creating it if missing
    initialize_config_db()
    # Launch the main menu interface
    main_menu()
import sqlite3
import os
import datetime
import glob
import csv
from playsound import playsound
import bcrypt
import hashlib
import getpass

# ==============================
# Globals
# ==============================

# DB_FILENAME stores the path to the active race database file
DB_FILENAME = ""
# race_started and race_stopped track whether a race is currently running or stopped
race_started = False
race_stopped = False
# race_start_time records the datetime when the race starts
race_start_time = None

# ==============================
# Database helpers
# ==============================

def initialize_config_db():
    """
    Creates the configuration database in /data/ if it does not exist.
    Prompts the user to set up an admin username and password (bcrypt hashed).
    Creates the 'users' table for authentication.
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    config_db_path = os.path.join(data_dir, 'config.db')

    if not os.path.exists(config_db_path):
        print("No config.db found — creating new configuration database in /data/...")
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()

        # Create a users table to store login credentials
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            )
        ''')

        # Prompt for an admin account setup
        admin_username = input("Enter admin username: ").strip()
        while not admin_username:
            print("Username cannot be empty.")
            admin_username = input("Enter admin username: ").strip()

        admin_password = getpass.getpass("Enter admin password: ").strip()
        while not admin_password:
            print("Password cannot be empty.")
            admin_password = getpass.getpass("Enter admin password: ").strip()

        # Hash and store the admin password
        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                  (admin_username, password_hash))

        conn.commit()
        conn.close()
        print("Configuration database created successfully at /data/config.db.")
    else:
        print("Config database already exists at /data/config.db.")

def get_next_db_filename():
    """
    Generates a filename for a new race database in the format YYYYMMDD-##-race.db.
    Increments the sequence number (##) if multiple races occur on the same day.
    """
    today = datetime.datetime.now().strftime('%Y%m%d')
    os.makedirs('data', exist_ok=True)
    existing = glob.glob(f"data/{today}-??-race.db")
    seq_nums = []
    for fname in existing:
        try:
            seq = int(fname.split("-")[1])
            seq_nums.append(seq)
        except:
            pass
    next_seq = max(seq_nums) + 1 if seq_nums else 1
    return f"data/{today}-{next_seq:02d}-race.db"

def init_db(new_db=True):
    """
    Creates a new race database or opens an existing one.
    Sets up the runners and results tables if they do not exist.
    """
    global DB_FILENAME
    os.makedirs("data", exist_ok=True)

    if new_db:
        DB_FILENAME = get_next_db_filename()
        print(f"[INFO] New database created: {DB_FILENAME}")

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    # Create the runners table
    c.execute('''
        CREATE TABLE IF NOT EXISTS runners (
            bib INTEGER PRIMARY KEY,
            name TEXT,
            team TEXT,
            rfid TEXT
        )
    ''')
    # Create the results table
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bib INTEGER,
            finish_time REAL,
            race_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_existing_db():
    """
    Prompts the user for a filename to load an existing race database from the /data directory.
    """
    global DB_FILENAME
    filename = input("Enter DB filename in data/: ").strip()
    path = os.path.join('data', filename)
    if os.path.exists(path):
        DB_FILENAME = path
        print(f"[INFO] Loaded database: {DB_FILENAME}")
    else:
        print("[ERROR] File does not exist.")
        return
    init_db(new_db=False)

# Path to the config database
CONFIG_DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'config.db')

# ==============================
# Race logic
# ==============================

def load_runners_from_csv(csv_file):
    """
    Loads runner information from a CSV file and populates the runners table.
    Each runner has a bib, name, team, and optional RFID tag.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded. Create or load a DB first.")
        return

    full_path = os.path.join('data', csv_file)
    if not os.path.exists(full_path):
        print(f"[ERROR] File not found: {full_path}")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    with open(full_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            c.execute('''
                INSERT OR REPLACE INTO runners (bib, name, team, rfid)
                VALUES (?, ?, ?, ?)
            ''', (row['bib'], row['name'], row['team'], row['rfid']))
    conn.commit()
    conn.close()
    print(f"[INFO] Loaded runners from {full_path}")

def start_race():
    """
    Starts the race and initializes the race start time.
    Begins accepting bib inputs in live race mode.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded. Create or load a DB first.")
        return
    if race_started:
        print("[INFO] Race is already running.")
        return
    race_started = True
    race_stopped = False
    race_start_time = datetime.datetime.now()
    print(f"[INFO] Race started at {race_start_time.strftime('%H:%M:%S')}")
    live_race_input()

def stop_race():
    """
    Stops the race and resets race tracking variables.
    """
    global race_started, race_stopped
    if not race_started:
        print("[INFO] Race hasn't started yet.")
        return
    race_stopped = True
    race_started = False
    print("[INFO] Race stopped. Returning to menu.")

def record_result(bib):
    """
    Records the finish time of a runner when they cross the finish line.
    Accepts a bib number or leaves it blank for unknown finishers.
    """
    if not race_started or race_stopped:
        print("[WARNING] Cannot record result — race is not active!")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    finish_time = datetime.datetime.now()
    elapsed = (finish_time - race_start_time).total_seconds()
    race_date = race_start_time.strftime('%Y-%m-%d')

    # Default bib to 0 if unknown
    if bib == "":
        bib_value = 0
    else:
        try:
            bib_value = int(bib)
        except ValueError:
            print("[ERROR] Invalid bib number.")
            return

    # Store result in the database
    c.execute('''
        INSERT INTO results (bib, finish_time, race_date)
        VALUES (?, ?, ?)
    ''', (bib_value, elapsed, race_date))
    conn.commit()
    conn.close()

    bib_display = bib if bib else "UNKNOWN"
    print(f"[RESULT] Bib {bib_display} finished in {elapsed:.2f}s")

    # Play a sound to confirm the finish
    try:
        playsound('beep.mp3')
    except:
        print("[Sound] Could not play sound.")

def live_race_input():
    """
    Continuously prompts for runner bib numbers while the race is running.
    Type 'exit' to stop taking inputs.
    """
    print("[INPUT MODE] Race is active. Enter bib number, or just Enter for unknown finisher.")
    print("Type 'exit' to stop recording and return to menu.")
    while race_started and not race_stopped:
        bib = input("> ").strip()
        if bib.lower() == 'exit':
            print("[INFO] Exiting live input mode and returning to menu.")
            stop_race()
            break
        record_result(bib)

# ==============================
# Results
# ==============================

def show_individual_results():
    """
    Displays a list of individual results ordered by finish time.
    Shows bib, name, team, and finish time for each runner.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT 
            results.bib,
            COALESCE(runners.name, 'UNKNOWN'),
            COALESCE(runners.team, 'UNKNOWN'),
            results.finish_time
        FROM results
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    rows = c.fetchall()

    print("\n=== Individual Results ===")
    for i, row in enumerate(rows, 1):
        print(f"{i}. Place: {i} | Bib: {row[0]}, Name: {row[1]}, Team: {row[2]}, Time: {row[3]:.2f}s")
    conn.close()

def show_team_results():
    """
    Calculates team scores by summing the places of the top 5 finishers for each team.
    Displays each team's scoring places and displacers.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT 
            COALESCE(runners.team, 'UNKNOWN') AS team,
            results.bib,
            results.finish_time
        FROM results
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    rows = c.fetchall()
    conn.close()

    place = 1
    team_places = {}

    # Collect places for each team
    for row in rows:
        team = row[0]
        if team not in team_places:
            team_places[team] = []
        team_places[team].append(place)
        place += 1

    print("\n=== Team Results (Scoring by Place: top 5 + 2 displacers) ===")
    for team, places in team_places.items():
        scorers = places[:5]
        displacers = places[5:7] if len(places) > 5 else []
        total_score = sum(scorers)
        print(f"Team: {team}")
        print(f"  Scorers (places): {scorers} -> Total: {total_score}")
        if displacers:
            print(f"  Displacers (places): {displacers}")

def show_all_runners():
    """
    Lists all runners in the database, grouped by team.
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT bib, name, team
        FROM runners
        ORDER BY team ASC, bib ASC
    ''')
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("[INFO] No runners found in the database.")
        return

    print("\n=== Runners by Team ===")
    current_team = None
    for row in rows:
        bib, name, team = row
        if team != current_team:
            current_team = team
            print(f"\nTeam: {current_team}")
        print(f"  Bib: {bib} | Name: {name}")

# ==============================
# Menu
# ==============================

def main_menu():
    """
    Displays the main console menu and handles user input.
    Provides options to manage databases, runners, races, and results.
    """
    while True:
        print("\n=== Race Timing Menu ===")
        print("1) Create new database")
        print("2) Load existing database")
        print("3) Load runners from CSV (data/)")
        print("4) Start Race")
        print("5) Show Individual Results")
        print("6) Show Team Results")
        print("7) Show All Runners")
        print("8) Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            init_db(new_db=True)
        elif choice == "2":
            load_existing_db()
        elif choice == "3":
            csv_file = input("CSV filename (in data/): ").strip()
            load_runners_from_csv(csv_file)
        elif choice == "4":
            start_race()
        elif choice == "5":
            show_individual_results()
        elif choice == "6":
            show_team_results()
        elif choice == "7":
            show_all_runners()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    # Ensure the config database exists, creating it if missing
    initialize_config_db()
    # Launch the main menu interface
    main_menu()

