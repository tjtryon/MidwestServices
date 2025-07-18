"""
race_timing_console.py
Author: TJ Tryon
Date: July 18, 2025
Program: The Race Timing Solution (TRT)

This Python program helps time cross country and road races.
It allows race organizers to:
- Create a race database
- Load runners from a CSV file
- Start a race and record finish times
- View individual and team results

You can use it in the terminal (console) or with the GUI.
Results are saved in an SQLite database.
"""

import sqlite3
import os
import datetime
import glob
import csv
from playsound import playsound
import bcrypt
import getpass

# Global variables used throughout the program
DB_FILENAME = ""
race_started = False
race_stopped = False
race_start_time = None

def initialize_config_db():
    """
    Checks if the config.db exists. If not, it creates it and
    asks the user to set an admin username and password.
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    config_db_path = os.path.join(data_dir, 'config.db')

    if not os.path.exists(config_db_path):
        print("No config.db found — creating one in /data/")
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            )
        ''')

        admin_username = input("Enter admin username: ").strip()
        while not admin_username:
            print("Username cannot be empty.")
            admin_username = input("Enter admin username: ").strip()

        admin_password = getpass.getpass("Enter admin password: ").strip()
        while not admin_password:
            print("Password cannot be empty.")
            admin_password = getpass.getpass("Enter admin password: ").strip()

        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (admin_username, password_hash))

        conn.commit()
        conn.close()
        print("Config database created and admin user saved.")
    else:
        print("Config database already exists.")

def get_next_db_filename():
    """
    Generates a unique filename for today's race in the format:
    data/YYYYMMDD-XX-race.db
    """
    today = datetime.datetime.now().strftime('%Y%m%d')
    os.makedirs('data', exist_ok=True)
    existing = glob.glob(f"data/{today}-??-race.db")
    seq_nums = [int(f.split("-")[1]) for f in existing if "-" in f and f.split("-")[1].isdigit()]
    next_seq = max(seq_nums) + 1 if seq_nums else 1
    return f"data/{today}-{next_seq:02d}-race.db"

def init_db(new_db=True):
    """
    Initializes a new or existing race database.
    """
    global DB_FILENAME
    os.makedirs("data", exist_ok=True)

    if new_db:
        DB_FILENAME = get_next_db_filename()
        print(f"[INFO] New database created: {DB_FILENAME}")

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runners (
            bib INTEGER PRIMARY KEY,
            name TEXT,
            team TEXT,
            rfid TEXT
        )
    ''')
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
    Prompts the user to load a previous race database from the /data folder.
    """
    global DB_FILENAME
    filename = input("Enter DB filename in data/: ").strip()
    path = os.path.join('data', filename)
    if os.path.exists(path):
        DB_FILENAME = path
        print(f"[INFO] Loaded database: {DB_FILENAME}")
        init_db(new_db=False)
    else:
        print("[ERROR] File does not exist.")

def load_runners_from_csv(csv_file):
    """
    Loads runners from a CSV file and saves them to the database.
    CSV should contain: bib, name, team, rfid
    """
    global DB_FILENAME
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
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
    Starts the race and records the start time.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
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
    Stops the race and resets the race status.
    """
    global race_started, race_stopped
    if not race_started:
        print("[INFO] Race hasn't started yet.")
        return
    race_started = False
    race_stopped = True
    print("[INFO] Race stopped.")

def record_result(bib):
    """
    Records a runner's finish time based on their bib number.
    """
    if not race_started or race_stopped:
        print("[WARNING] Race is not active.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    finish_time = datetime.datetime.now()
    elapsed = (finish_time - race_start_time).total_seconds()
    race_date = race_start_time.strftime('%Y-%m-%d')

    try:
        bib_value = int(bib) if bib else 0
    except ValueError:
        print("[ERROR] Invalid bib number.")
        return

    c.execute('''
        INSERT INTO results (bib, finish_time, race_date)
        VALUES (?, ?, ?)
    ''', (bib_value, elapsed, race_date))
    conn.commit()
    conn.close()

    bib_display = bib if bib else "UNKNOWN"
    print(f"[RESULT] Bib {bib_display} finished in {elapsed:.2f}s")

    try:
        playsound('beep.mp3')
    except:
        print("[Sound] Could not play beep sound.")

def live_race_input():
    """
    Lets user enter bib numbers as runners finish.
    """
    print("[INPUT] Enter bib number, or press Enter for unknown finisher.")
    print("Type 'exit' to stop the race.")
    while race_started and not race_stopped:
        bib = input("> ").strip()
        if bib.lower() == 'exit':
            stop_race()
            break
        record_result(bib)

def show_individual_results():
    """
    Shows all runners and their finish times.
    """
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
    Shows team scores using top 5 runners and 2 displacers.
    """
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
    for row in rows:
        team_places.setdefault(row[0], []).append(place)
        place += 1

    print("\n=== Team Results ===")
    for team, places in team_places.items():
        scorers = places[:5]
        displacers = places[5:7] if len(places) > 5 else []
        total_score = sum(scorers)
        print(f"Team: {team}")
        print(f"  Scorers: {scorers} -> Total: {total_score}")
        if displacers:
            print(f"  Displacers: {displacers}")

def show_all_runners():
    """
    Displays all runners grouped by team.
    """
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('SELECT bib, name, team FROM runners ORDER BY team, bib')
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("[INFO] No runners found.")
        return

    print("\n=== Runners by Team ===")
    current_team = None
    for bib, name, team in rows:
        if team != current_team:
            print(f"\nTeam: {team}")
            current_team = team
        print(f"  Bib: {bib} | Name: {name}")

def main_menu():
    """
    The main menu for console users to run the system.
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
    initialize_config_db()
    main_menu()
