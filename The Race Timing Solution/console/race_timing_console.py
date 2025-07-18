<<<<<<< Updated upstream
<<<<<<< Updated upstream
""" race_timing_console.py
Author: TJ Tryon
Date: July 17, 2025
Name: The Race Timing Solution for Cross Country and Road Races (TRT)

This program helps time races and store results for cross-country and road races.
It tracks runners and their times, stores them in a database, and lets you view the results.
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream


This program is a timing solution for cross country and road races. This is the main race
logic program for This program is a the backend, which woould be handled by the race timing company. 
    - When this program starts, it checks for a data/config.db and if it does not exist, it creates one,
    It uses SQLite3 databases to store runner and race results,prompting the timing user for an 
    - Administratior password and usernaame. If it finds an existing data/config.db, it assumes you 
    know the administrator username and password. If you do not remember the username and password, 
    delete the data/config.db file and it will recreate the admin username and password in the new 
    data/config.db.
    - The menu gives you the ability to load an existing race database, or to create a database, which
    is located under the data directory, and is named as such: YYYYMMDD-race-##.db where the date
    portion is ISO formatted, and the ## is the number of the race for the date.
    - If you load an existing database to use, it assumes that the users are already loaded. If this is
    the case, and if you have completed the race, the results will already be in the database. If the
    results for the race are not there yet (race has not run), or runners are not in the database, you
    have the option of loading the racers from a CSV file, and starting the race.
    - If you create a new database, you will need to use the option to load the runners into the database
    from a csv file.
    - The runner's CSV file should be under the data folder, and should have runners for an individual race,
    ie. each race will have a separate runner's file, and each race will have it's own database file, 
    in the naming format: YYYYMMDD-race-##.db, where the month is in ISO format, and ## is the 2 digit 
    (with leaading "0" if the race number is less than 10) race number for the day.
    - The runner's csv files should have a name, simmilar to the database name, YYYYMMDD-runners-##.csv, where
    the date is in ISO format, and the ## is the (with leading 0 when necessary) two digit race number
    for the day. The runner's should be listed, one per line, in the following format:
    bib_number, Full Name, Team Name, rfid_tag
    101, John Smith, Southern College, 31242318
    note: bib numbers need to be between 101-999 in the current version. This will be expanded in future
    versions.
    - The menu has an option to view runners in the database. This will show the runner's databse, to ensure
    the runners were properly inserted into the database.
    - There is a menu item to view individual results. This will list, in order of finish, the list of
    individual results.
    - There is a menu item to view the team results. This will list all team results from teams with at least
    5 runners. 
    - There is an option to quit the console application, which will exit the program back to the console shell.
    - The last option is to start the race. This starts the timer, and enters manual interactive mode. In manual
    mode, you can enter a bib number and enter to add a result to the database. If you are unsure of the
    runner's number, you can press enter on a blank line, and the program will enter a time for bib "0", 
    which is able to be fixed after the race, as it incorrect bib numbers. When you are done with the race,
    you can type the word "quit", which will exit the manual interactive mode back to the main meny.
    - Once the race has been run, the times will be in that race's database. You will be able to use the front
    end Flack application, via a web browser to access the administrative mode to correct bib number issues,
    which are secured by the data/config.db administrative username and password. The coaches/runners/parents
    will be able to access the race database results live from the Flack site as well, to show PRELIMINARY
    results for the team as well as the individual.
    - The Flack application, and all documentation is located under the web/ folder, and can be accessed by running:
    "flack run" while in a console window in the web directory, as long as the system has imported the Flack module.
    please see the documentation under the web directory for more information on this feature.
=======
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
"""

import sqlite3
import os
import datetime
import glob
import csv
from playsound import playsound
import bcrypt
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import hashlib
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
import getpass

# Global variables used throughout the program
DB_FILENAME = ""
race_started = False
race_stopped = False
race_start_time = None

def initialize_config_db():
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function creates a special configuration database to store admin info.
    If it doesn’t exist, it will create it and ask for an admin username and password.
=======
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    This checks if the config database exists.
    If not, it creates it and sets up an admin username and password.
>>>>>>> Stashed changes
=======
    This checks if the config database exists.
    If not, it creates it and sets up an admin username and password.
>>>>>>> Stashed changes
=======
    This checks if the config database exists.
    If not, it creates it and sets up an admin username and password.
>>>>>>> Stashed changes
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    config_db_path = os.path.join(data_dir, 'config.db')

    if not os.path.exists(config_db_path):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        print("No config.db found — creating new configuration database in /data/...")
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

        # Create a place to store usernames and passwords
=======
        print("No config.db found — creating one in /data/")
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()
>>>>>>> Stashed changes
=======
        print("No config.db found — creating one in /data/")
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            )
        ''')

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        # Ask for an admin username and password
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        admin_username = input("Enter admin username: ").strip()
        while not admin_username:
            print("Username cannot be empty.")
            admin_username = input("Enter admin username: ").strip()

        admin_password = getpass.getpass("Enter admin password: ").strip()
        while not admin_password:
            print("Password cannot be empty.")
            admin_password = getpass.getpass("Enter admin password: ").strip()

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        # Save the password safely using bcrypt (like locking it in a safe)
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (admin_username, password_hash))

        conn.commit()
        conn.close()
        print("Configuration database created successfully.")
    else:
        print("Config database already exists.")

def get_next_db_filename():
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function helps create a name for a new race database.
    The name will include today's date and a number if there are multiple races.
=======
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    Creates a new race DB filename using today's date and a race number.
    Example: 20250717-01-race.db
>>>>>>> Stashed changes
=======
    Creates a new race DB filename using today's date and a race number.
    Example: 20250717-01-race.db
>>>>>>> Stashed changes
=======
    Creates a new race DB filename using today's date and a race number.
    Example: 20250717-01-race.db
>>>>>>> Stashed changes
    """
    today = datetime.datetime.now().strftime('%Y%m%d')
    os.makedirs('data', exist_ok=True)
    existing = glob.glob(f"data/{today}-??-race.db")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    seq_nums = []
    for fname in existing:
        try:
            seq = int(fname.split("-")[1])
            seq_nums.append(seq)
        except:
            pass
=======
    seq_nums = [int(f.split("-")[1]) for f in existing if "-" in f and f.split("-")[1].isdigit()]
>>>>>>> Stashed changes
=======
    seq_nums = [int(f.split("-")[1]) for f in existing if "-" in f and f.split("-")[1].isdigit()]
>>>>>>> Stashed changes
    next_seq = max(seq_nums) + 1 if seq_nums else 1
=======
    seq_nums = [int(f.split("-")[1]) for f in existing if "-" in f]
    next_seq = max(seq_nums, default=0) + 1
>>>>>>> Stashed changes
=======
    seq_nums = [int(f.split("-")[1]) for f in existing if "-" in f]
    next_seq = max(seq_nums, default=0) + 1
>>>>>>> Stashed changes
=======
    seq_nums = [int(f.split("-")[1]) for f in existing if "-" in f]
    next_seq = max(seq_nums, default=0) + 1
>>>>>>> Stashed changes
    return f"data/{today}-{next_seq:02d}-race.db"

def init_db(new_db=True):
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function sets up the race database.
    If it's a new database, it creates it and sets up places to store race results and runner info.
=======
    Initializes a new or existing race database.
>>>>>>> Stashed changes
=======
    Initializes a new or existing race database.
>>>>>>> Stashed changes
=======
    If new_db is True, it creates a new database file.
    It also creates the runners and results tables if they don’t exist.
>>>>>>> Stashed changes
=======
    If new_db is True, it creates a new database file.
    It also creates the runners and results tables if they don’t exist.
>>>>>>> Stashed changes
=======
    If new_db is True, it creates a new database file.
    It also creates the runners and results tables if they don’t exist.
>>>>>>> Stashed changes
    """
    global DB_FILENAME
    os.makedirs("data", exist_ok=True)

    if new_db:
        DB_FILENAME = get_next_db_filename()
        print(f"[INFO] New database created: {DB_FILENAME}")

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Create a table to store runner info
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    c.execute('''
        CREATE TABLE IF NOT EXISTS runners (
            bib INTEGER PRIMARY KEY,
            name TEXT,
            team TEXT,
            rfid TEXT
        )
    ''')
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Create a table to store race results
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function loads an existing database from the 'data' folder.
    It asks the user for the name of the database to load.
=======
    Prompts the user to load a previous race database from the /data folder.
>>>>>>> Stashed changes
=======
    Prompts the user to load a previous race database from the /data folder.
>>>>>>> Stashed changes
=======
    Ask the user which existing DB to load.
>>>>>>> Stashed changes
=======
    Ask the user which existing DB to load.
>>>>>>> Stashed changes
=======
    Ask the user which existing DB to load.
>>>>>>> Stashed changes
    """
    global DB_FILENAME
    filename = input("Enter DB filename in data/: ").strip()
    path = os.path.join('data', filename)
    if os.path.exists(path):
        DB_FILENAME = path
        print(f"[INFO] Loaded database: {DB_FILENAME}")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
        init_db(new_db=False)
>>>>>>> Stashed changes
=======
        init_db(new_db=False)
>>>>>>> Stashed changes
=======
        init_db(new_db=False)
>>>>>>> Stashed changes
    else:
        print("[ERROR] File does not exist.")

def load_runners_from_csv(csv_file):
    """
    Load runners from a CSV file into the database.
    """
    global DB_FILENAME
    if not DB_FILENAME:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        print("[ERROR] No database loaded. Create or load a DB first.")
=======
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        print("[ERROR] No database loaded.")
>>>>>>> Stashed changes
=======
        print("[ERROR] No database loaded.")
>>>>>>> Stashed changes
=======
        print("[ERROR] No database loaded.")
>>>>>>> Stashed changes
        return

    full_path = os.path.join('data', csv_file)
    if not os.path.exists(full_path):
        print(f"[ERROR] File not found: {full_path}")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    with open(full_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute('''
                INSERT OR REPLACE INTO runners (bib, name, team, rfid)
                VALUES (?, ?, ?, ?)
            ''', (row['bib'], row['name'], row['team'], row['rfid']))
    conn.commit()
    conn.close()
    print(f"[INFO] Loaded runners from {csv_file}")

def start_race():
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function starts the race and begins recording times for runners.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded. Create or load a DB first.")
=======
=======
>>>>>>> Stashed changes
    Starts the race and records the start time.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    Start the race and record start time.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
>>>>>>> Stashed changes
=======
    Start the race and record start time.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
>>>>>>> Stashed changes
=======
    Start the race and record start time.
    """
    global race_started, race_stopped, race_start_time
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
>>>>>>> Stashed changes
        return
    if race_started:
        print("[INFO] Race already running.")
        return
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
=======

>>>>>>> Stashed changes
    race_started = True
    race_stopped = False
    race_start_time = datetime.datetime.now()
    print(f"[INFO] Race started at {race_start_time.strftime('%H:%M:%S')}")
    live_race_input()

def stop_race():
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function stops the race and resets the race status.
=======
    Stops the race and resets the race status.
>>>>>>> Stashed changes
=======
    Stops the race and resets the race status.
>>>>>>> Stashed changes
=======
    Stop the race and reset the state.
>>>>>>> Stashed changes
=======
    Stop the race and reset the state.
>>>>>>> Stashed changes
=======
    Stop the race and reset the state.
>>>>>>> Stashed changes
    """
    global race_started, race_stopped
    if not race_started:
        print("[INFO] Race hasn't started yet.")
        return
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    race_stopped = True
    race_started = False
    print("[INFO] Race stopped.")

def record_result(bib):
    """
    Record a runner's bib and time to the database.
    """
    if not race_started or race_stopped:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        print("[WARNING] Cannot record result — race is not active!")
=======
=======
>>>>>>> Stashed changes
    race_started = False
    race_stopped = True
    print("[INFO] Race stopped.")

def record_result(bib):
    """
    Records a runner's finish time based on their bib number.
    """
    if not race_started or race_stopped:
        print("[WARNING] Race is not active.")
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        print("[WARNING] Race is not active.")
>>>>>>> Stashed changes
=======
        print("[WARNING] Race is not active.")
>>>>>>> Stashed changes
=======
        print("[WARNING] Race is not active.")
>>>>>>> Stashed changes
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    finish_time = datetime.datetime.now()
    elapsed = (finish_time - race_start_time).total_seconds()
    race_date = race_start_time.strftime('%Y-%m-%d')

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Default bib to 0 if unknown
    if bib == "":
        bib_value = 0
    else:
        try:
            bib_value = int(bib)
        except ValueError:
            print("[ERROR] Invalid bib number.")
            return

    # Save the result in the database
=======
=======
>>>>>>> Stashed changes
    try:
        bib_value = int(bib) if bib else 0
    except ValueError:
        print("[ERROR] Invalid bib number.")
        return

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    try:
        bib_value = int(bib) if bib else 0
    except ValueError:
        print("[ERROR] Bib must be a number.")
        return

>>>>>>> Stashed changes
=======
    try:
        bib_value = int(bib) if bib else 0
    except ValueError:
        print("[ERROR] Bib must be a number.")
        return

>>>>>>> Stashed changes
=======
    try:
        bib_value = int(bib) if bib else 0
    except ValueError:
        print("[ERROR] Bib must be a number.")
        return

>>>>>>> Stashed changes
    c.execute('''
        INSERT INTO results (bib, finish_time, race_date)
        VALUES (?, ?, ?)
    ''', (bib_value, elapsed, race_date))
    conn.commit()
    conn.close()

    print(f"[RESULT] Bib {bib_value} finished in {elapsed:.2f}s")

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Play a sound to confirm the finish
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    try:
        playsound('beep.mp3')
    except:
        print("[Sound] Could not play beep.")

def live_race_input():
    """
    Keep asking for bib numbers until race is stopped.
    """
    print("[INPUT MODE] Enter bib or press Enter for unknown.")
    print("Type 'exit' to stop.")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    while race_started and not race_stopped:
        bib = input("> ").strip()
<<<<<<< Updated upstream
        if bib.lower() == 'exit':
            print("[INFO] Exiting live input mode and returning to menu.")
=======
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        if bib.lower() == "exit":
>>>>>>> Stashed changes
=======
    while race_started and not race_stopped:
        bib = input("> ").strip()
        if bib.lower() == "exit":
>>>>>>> Stashed changes
=======
    while race_started and not race_stopped:
        bib = input("> ").strip()
        if bib.lower() == "exit":
>>>>>>> Stashed changes
            stop_race()
            break
        record_result(bib)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
# ==============================
# Results (functions for showing race results)
# ==============================

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
def show_individual_results():
    """
    Show all finishers in order of time.
    """
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return
=======
=======
>>>>>>> Stashed changes
def show_individual_results():
    """
    Shows all runners and their finish times.
    """
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT results.bib, COALESCE(runners.name, 'UNKNOWN'),
               COALESCE(runners.team, 'UNKNOWN'), results.finish_time
        FROM results
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    rows = c.fetchall()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    print("\n=== Individual Results ===")
    for i, row in enumerate(rows, 1):
        print(f"{i}. Place: {i} | Bib: {row[0]}, Name: {row[1]}, Team: {row[2]}, Time: {row[3]:.2f}s")
    conn.close()

def show_team_results():
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    This function shows the team results by calculating scores based on the top finishers.
    """
    global DB_FILENAME
=======
    Shows team scores using top 5 runners and 2 displacers.
    """
>>>>>>> Stashed changes
=======
    Shows team scores using top 5 runners and 2 displacers.
    """
>>>>>>> Stashed changes
=======
    Calculate team scores using top 5 finishers and show team results.
    """
>>>>>>> Stashed changes
=======
    Calculate team scores using top 5 finishers and show team results.
    """
>>>>>>> Stashed changes
=======
    Calculate team scores using top 5 finishers and show team results.
    """
>>>>>>> Stashed changes
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute('''
        SELECT COALESCE(runners.team, 'UNKNOWN') AS team,
               results.bib, results.finish_time
        FROM results
        LEFT JOIN runners ON results.bib = runners.bib
        ORDER BY results.finish_time ASC
    ''')
    rows = c.fetchall()
    conn.close()

    place = 1
    team_places = {}
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

    # Collect places for each team
    for row in rows:
        team = row[0]
        if team not in team_places:
            team_places[team] = []
        team_places[team].append(place)
        place += 1

    print("\n=== Team Results (Scoring by Place: top 5 + 2 displacers) ===")
=======
=======
>>>>>>> Stashed changes
    for row in rows:
        team_places.setdefault(row[0], []).append(place)
        place += 1

    print("\n=== Team Results ===")
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    for team, bib, time in rows:
        team_places.setdefault(team, []).append(place)
        place += 1

    print("\n=== Team Results ===")
>>>>>>> Stashed changes
=======
    for team, bib, time in rows:
        team_places.setdefault(team, []).append(place)
        place += 1

    print("\n=== Team Results ===")
>>>>>>> Stashed changes
=======
    for team, bib, time in rows:
        team_places.setdefault(team, []).append(place)
        place += 1

    print("\n=== Team Results ===")
>>>>>>> Stashed changes
    for team, places in team_places.items():
        scorers = places[:5]
        displacers = places[5:7] if len(places) > 5 else []
        print(f"Team: {team}")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        print(f"  Scorers (places): {scorers} -> Total: {total_score}")
=======
        print(f"  Scorers: {scorers} -> Total: {sum(scorers)}")
>>>>>>> Stashed changes
=======
        print(f"  Scorers: {scorers} -> Total: {sum(scorers)}")
>>>>>>> Stashed changes
=======
        print(f"  Scorers: {scorers} -> Total: {sum(scorers)}")
>>>>>>> Stashed changes
        if displacers:
            print(f"  Displacers: {displacers}")

def show_all_runners():
    """
    Print all runners grouped by team.
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    global DB_FILENAME
=======
=======
>>>>>>> Stashed changes
        print(f"  Scorers: {scorers} -> Total: {total_score}")
        if displacers:
            print(f"  Displacers: {displacers}")

def show_all_runners():
    """
    Displays all runners grouped by team.
    """
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")
        return
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    c.execute('''
        SELECT bib, name, team
        FROM runners
        ORDER BY team ASC, bib ASC
    ''')
=======
    c.execute('SELECT bib, name, team FROM runners ORDER BY team, bib')
>>>>>>> Stashed changes
=======
    c.execute('SELECT bib, name, team FROM runners ORDER BY team, bib')
>>>>>>> Stashed changes
=======
    c.execute('SELECT bib, name, team FROM runners ORDER BY team, bib')
>>>>>>> Stashed changes
=======
    c.execute('SELECT bib, name, team FROM runners ORDER BY team, bib')
>>>>>>> Stashed changes
=======
    c.execute('SELECT bib, name, team FROM runners ORDER BY team, bib')
>>>>>>> Stashed changes
    rows = c.fetchall()
    conn.close()

    if not rows:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        print("[INFO] No runners found in the database.")
=======
        print("[INFO] No runners found.")
>>>>>>> Stashed changes
=======
        print("[INFO] No runners found.")
>>>>>>> Stashed changes
=======
        print("[INFO] No runners found.")
>>>>>>> Stashed changes
=======
        print("[INFO] No runners found.")
>>>>>>> Stashed changes
=======
        print("[INFO] No runners found.")
>>>>>>> Stashed changes
        return

    print("\n=== Runners by Team ===")
    current_team = None
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    for row in rows:
        bib, name, team = row
=======
    for bib, name, team in rows:
>>>>>>> Stashed changes
=======
    for bib, name, team in rows:
>>>>>>> Stashed changes
=======
    for bib, name, team in rows:
>>>>>>> Stashed changes
        if team != current_team:
            current_team = team
            print(f"\nTeam: {current_team}")
        print(f"  Bib: {bib} | Name: {name}")

<<<<<<< Updated upstream
<<<<<<< Updated upstream
def main_menu():
    """
<<<<<<< Updated upstream
    This function shows the main menu and lets the user choose options.
=======
=======
>>>>>>> Stashed changes
    for bib, name, team in rows:
        if team != current_team:
            print(f"\nTeam: {team}")
            current_team = team
        print(f"  Bib: {bib} | Name: {name}")

def main_menu():
    """
    The main menu for console users to run the system.
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
    Display the menu and handle user choices.
>>>>>>> Stashed changes
=======
def main_menu():
    """
    Display the menu and handle user choices.
>>>>>>> Stashed changes
=======
def main_menu():
    """
    Display the menu and handle user choices.
>>>>>>> Stashed changes
    """
    while True:
        print("\n=== Race Timing Menu ===")
        print("1) Create new database")
        print("2) Load existing database")
        print("3) Load runners from CSV")
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # Make sure the config database exists, creating it if missing
    initialize_config_db()
    # Show the main menu
=======
    initialize_config_db()
>>>>>>> Stashed changes
=======
    initialize_config_db()
>>>>>>> Stashed changes
=======
    initialize_config_db()
>>>>>>> Stashed changes
=======
    initialize_config_db()
>>>>>>> Stashed changes
=======
    initialize_config_db()
>>>>>>> Stashed changes
    main_menu()
