"""
race_timing_console.py
Author: TJ Tryon
Date: July 27, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS)

🎽 This program helps you time cross country and road races! 🏃‍♀️🏃‍♂️

🧠 What it does:
- Lets you choose between a cross country or road race
- Cross country races use **team scoring** (top 5 finishers and 2 displacers)
- Road races use **age group** results (based on date of birth)
- Saves all data in a neat .db file using SQLite
- You can load runner info from a .csv file
- You can start a race and record bib numbers as runners finish
- It even plays a beep sound when someone finishes! 🎵
- View results for individuals, teams, or age groups

🗂 The database file name uses this format:
  YYYYMMDD-##-[cc or rr]-[Race_Name].db
  - "cc" = cross country
  - "rr" = road race
  - Example: 20250727-01-cc-County_Meet.db

💡 This program is great for race timing volunteers, schools, or event directors!
"""

# 📦 We import lots of useful Python tools and packages here
import sqlite3         # 🗃️ lets us talk to the SQLite database
import os              # 📁 helps with file and folder paths
import datetime        # ⏰ helps with time and date
import csv             # 📊 lets us read CSV files
from playsound import playsound  # 🔊 to play a beep when someone finishes
import bcrypt          # 🔒 for secure password storage
import getpass         # 🙈 so passwords are hidden when typed
import time            # ⏱️ for race timing and delays

# ===============================
# 🌍 GLOBAL VARIABLES (like variables the whole program can see)
# ===============================
DB_FILENAME = ""          # 🗂️ this is the filename for the race database
race_started = False      # 🏁 this keeps track of whether the race has started
race_stopped = False      # 🛑 this keeps track of whether the race has ended
race_start_time = None    # ⏰ the exact time the race started
RACE_TYPE = ""            # 🏃 either "cross_country" or "road_race"

# ===============================
# 🔐 SETUP ADMIN LOGIN FOR CONFIGURATION
# ===============================

def initialize_config_db():
    """
    🛠️ Creates the config database and asks for an admin username and password if it doesn't exist yet.
    This helps keep your system secure - like having a password for your computer!
    """
    # 📁 First, we make sure there's a 'data' folder to store our files
    data_dir = os.path.join(os.getcwd(), 'data')  # 🏠 make sure 'data' folder exists
    os.makedirs(data_dir, exist_ok=True)  # 📁 create the folder if it's not there
    config_db_path = os.path.join(data_dir, 'config.db')  # 🗂️ path to our config file

    # 🔍 Check if the config database already exists
    if not os.path.exists(config_db_path):  # 🤔 only create it if it doesn't exist yet
        print("Creating new config database...")  # 📢 tell the user what we're doing
        
        # 🗃️ Connect to the database (this creates it if it doesn't exist)
        conn = sqlite3.connect(config_db_path)
        c = conn.cursor()  # 🖱️ this is like our "pointer" to work with the database
        
        # 🏗️ Create a table to store usernames and passwords
        c.execute('''CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash BLOB NOT NULL)''')
        
        # 👤 Ask user for their admin login info
        username = input("Enter admin username: ").strip()  # 📝 get username, remove extra spaces
        password = getpass.getpass("Enter admin password: ").strip()  # 🙈 get password secretly
        
        # 🔒 Hash the password for security (like scrambling it so hackers can't read it)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # 💾 Save the username and scrambled password to the database
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()  # ✅ save our changes
        conn.close()   # 🚪 close the database connection
        print("Admin login saved.")  # 🎉 tell the user we're done

# ===============================
# 🗃️ DATABASE INITIALIZATION (Setting up where we store race info)
# ===============================

def get_custom_db_filename(race_type):
    """
    🏷️ Asks user for race number and name, then creates a filename in this format:
    YYYYMMDD-##-[cc or rr]-[race_name].db
    This way every race gets its own special name!
    """
    # 📅 Get today's date in a special format like 20250727
    today = datetime.datetime.now().strftime('%Y%m%d')  
    
    # 🔢 Keep asking for a race number until we get a valid one
    while True:
        number = input("Enter race number (e.g., 1): ").zfill(2)  # 📝 pad race number to two digits (01, 02, etc.)
        if number.isdigit():  # 🔍 check if it's actually a number
            break  # ✅ great! we can stop asking now
    
    # 🏃 Ask for the race name and replace spaces with underscores
    name = input("Enter race name: ").strip().replace(" ", "_")
    
    # 🏷️ Choose the right suffix based on race type
    suffix = "cc" if race_type == "cross_country" else "rr"
    
    # 🧩 Put it all together to make the filename
    return os.path.join("data", f"{today}-{number}-{suffix}-{name}.db")

def init_db(new_db=True):
    """
    🏗️ Creates a new race database or re-initializes an existing one.
    This is like setting up a new notebook for keeping track of our race!
    """
    global DB_FILENAME, RACE_TYPE  # 🌍 we're going to change these global variables
    os.makedirs("data", exist_ok=True)  # 📁 make sure our data folder exists

    # 🆕 If this is a brand new database, ask what kind of race it is
    if new_db:
        print("Select race type:")  # 📢 ask the user
        print("1) Cross Country")   # 🏃‍♀️ option 1: cross country (teams matter)
        print("2) Road Race")       # 🏃‍♂️ option 2: road race (age groups matter)
        type_choice = input("Enter choice: ").strip()  # 📝 get their choice
        
        # 🎯 Set the race type based on what they picked
        RACE_TYPE = "cross_country" if type_choice == '1' else "road_race"
        
        # 🏷️ Create a special filename for this race
        DB_FILENAME = get_custom_db_filename(RACE_TYPE)
        print(f"New database: {DB_FILENAME}")  # 📢 tell them what we created

    # 🗃️ Connect to our database
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer

    # 🆕 If this is a new database, remember what type of race it is
    if new_db:
        c.execute("CREATE TABLE race_type (type TEXT)")  # 🏗️ create a table to remember race type
        c.execute("INSERT INTO race_type (type) VALUES (?)", (RACE_TYPE,))  # 💾 save the race type

    # 🏗️ Create different tables based on what kind of race this is
    if RACE_TYPE == "cross_country":
        # 🏃‍♀️ Cross country races care about teams, grades, etc.
        c.execute('''CREATE TABLE IF NOT EXISTS runners (
                        bib INTEGER PRIMARY KEY,
                        name TEXT,
                        team TEXT,
                        age INTEGER,
                        grade TEXT,
                        rfid TEXT)''')
        # 🔢 bib = the number on their shirt
        # 👤 name = runner's name  
        # 🏫 team = what school/team they're on
        # 🎂 age = how old they are
        # 📚 grade = what grade they're in
        # 📡 rfid = special chip for timing (if they have one)
    else:  # road race
        # 🏃‍♂️ Road races care about age groups based on birthday
        c.execute('''CREATE TABLE IF NOT EXISTS runners (
                        bib INTEGER PRIMARY KEY,
                        name TEXT,
                        dob TEXT,
                        age INTEGER,
                        rfid TEXT)''')
        # 🔢 bib = the number on their shirt
        # 👤 name = runner's name
        # 🎂 dob = their birthday (date of birth)
        # 🎂 age = how old they are
        # 📡 rfid = special chip for timing (if they have one)

    # 🏁 Every race needs a table to store who finished when
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bib INTEGER,
                    finish_time REAL,
                    race_date TEXT)''')
    # 🔢 id = unique ID for each result
    # 🔢 bib = which runner finished
    # ⏱️ finish_time = how long it took them
    # 📅 race_date = what day the race happened
    
    conn.commit()  # ✅ save our changes
    conn.close()   # 🚪 close the database

# ===============================
# 📂 LOAD AN EXISTING DATABASE
# ===============================

def load_existing_db():
    """
    📂 Shows a list of saved databases in /data and loads the one the user selects.
    This is like looking through your old notebooks to find the right one!
    """
    global DB_FILENAME, RACE_TYPE  # 🌍 we're going to change these global variables
    
    # 🔍 Look for all database files in our data folder
    dbs = [f for f in os.listdir("data") if f.endswith(".db")]
    
    # 😕 If we don't find any databases, tell the user
    if not dbs:
        print("No .db files found.")
        return  # 🚪 exit this function early
    
    # 📋 Show the user all the databases we found
    for i, f in enumerate(dbs, 1):  # 🔢 number them starting from 1
        print(f"{i}) {f}")
    
    # 📝 Ask the user which one they want to load
    choice = int(input("Pick DB number: "))
    DB_FILENAME = os.path.join("data", dbs[choice - 1])  # 🎯 get the file they picked (subtract 1 because lists start at 0)

    # 🗃️ Connect to the database they picked
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    
    # 🔍 Try to figure out what type of race this is
    try:
        c.execute("SELECT type FROM race_type")  # 🔍 look for the race type
        RACE_TYPE = c.fetchone()[0]              # 📝 get the first result
    except:
        RACE_TYPE = "unknown"  # 🤷 if we can't find it, mark it as unknown
    
    conn.close()  # 🚪 close the database
    print(f"Loaded: {DB_FILENAME} [{RACE_TYPE}]")  # 📢 tell the user what we loaded
    init_db(new_db=False)  # 🔄 set up the database structure (but don't create a new one)

# ===============================
# 📊 LOAD RUNNERS FROM CSV FILES
# ===============================

def load_runners_from_csv():
    """
    📊 This function loads runner information from a CSV file (like a spreadsheet).
    It's like reading a list of students from a class roster!
    """
    global DB_FILENAME, RACE_TYPE  # 🌍 we need to know our database and race type
    
    # 🛑 Make sure we have a database loaded first
    if not DB_FILENAME:
        print("[ERROR] No database loaded.")  # 😟 tell the user they need to load a database first
        return  # 🚪 exit this function
    
    # 🔍 Look for CSV files in our data folder
    files = [f for f in os.listdir("data") if f.endswith(".csv")]
    
    # 📋 Show the user all the CSV files we found
    for i, f in enumerate(files, 1):  # 🔢 number them starting from 1
        print(f"{i}) {f}")
    
    # 📝 Ask the user which CSV file they want to load
    choice = int(input("Pick CSV file number: "))
    csv_file = os.path.join("data", files[choice - 1])  # 🎯 get the file they picked

    # 🗃️ Connect to our race database
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer
    
    # 📖 Open and read the CSV file
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)  # 📊 this reads the CSV like a dictionary (column name -> value)
        
        # 🏃‍♀️ If this is a cross country race...
        if RACE_TYPE == "cross_country":
            # 📋 These are the columns we expect in a cross country CSV
            expected_fields = ['bib', 'name', 'team', 'age', 'grade', 'rfid']
            
            # 🔍 Check if the CSV has the right columns
            if reader.fieldnames != expected_fields:
                print(f"[ERROR] CSV must have: {expected_fields}")  # 😟 tell user what columns we need
                return  # 🚪 exit because the CSV is wrong
            
            # 🔄 Go through each row in the CSV file
            for row in reader:
                # 💾 Add this runner to our database (or update them if they already exist)
                c.execute('''INSERT OR REPLACE INTO runners (bib, name, team, age, grade, rfid)
                             VALUES (?, ?, ?, ?, ?, ?)''',
                          (row['bib'], row['name'], row['team'], row['age'], row['grade'], row['rfid']))
        
        # 🏃‍♂️ If this is a road race...
        else:
            # 📋 These are the columns we expect in a road race CSV
            expected_fields = ['bib', 'name', 'dob', 'rfid']
            
            # 🔍 Check if the CSV has the right columns
            if reader.fieldnames != expected_fields:
                print(f"[ERROR] CSV must have: {expected_fields}")  # 😟 tell user what columns we need
                return  # 🚪 exit because the CSV is wrong
            
            # 🔄 Go through each row in the CSV file
            for row in reader:
                # 🎂 Calculate their age from their birthday
                birthdate = datetime.datetime.strptime(row['dob'], "%Y-%m-%d")  # 📅 convert birthday string to date
                age = int((datetime.datetime.now() - birthdate).days // 365.25)  # 🧮 calculate age in years
                
                # 💾 Add this runner to our database (or update them if they already exist)
                c.execute('''INSERT OR REPLACE INTO runners (bib, name, dob, age, rfid)
                             VALUES (?, ?, ?, ?, ?)''',
                          (row['bib'], row['name'], row['dob'], age, row['rfid']))
    
    conn.commit()  # ✅ save all our changes to the database
    conn.close()   # 🚪 close the database connection
    print("Runners loaded.")  # 🎉 tell the user we're done

# ===============================
# 🏁 RACE TIMING FUNCTIONS (The exciting part!)
# ===============================

def start_race():
    """
    🏁 This function starts the race and keeps track of the time!
    It's like blowing the starting whistle!
    """
    global race_started, race_start_time, race_stopped  # 🌍 we're changing these global variables
    
    # 🛑 Make sure we have a database loaded
    if not DB_FILENAME:
        print("No DB loaded.")  # 😟 can't start a race without a database
        return  # 🚪 exit this function
    
    # 🏁 Set our race flags
    race_started = True    # ✅ the race is now running
    race_stopped = False   # ❌ the race is not stopped
    race_start_time = datetime.datetime.now()  # ⏰ remember exactly when we started
    
    # 📢 Tell everyone the race has started
    print(f"Race started at {race_start_time.strftime('%H:%M:%S')}")  # 🕐 show the start time
    
    # 🎯 Start accepting finish times
    live_race_input()

def stop_race():
    """
    🛑 This function stops the race.
    It's like blowing the whistle to end the race!
    """
    global race_started, race_stopped  # 🌍 we're changing these global variables
    race_started = False  # ❌ the race is no longer running
    race_stopped = True   # ✅ the race is officially stopped
    print("Race stopped.")  # 📢 tell everyone the race is over

def record_result(bib):
    """
    ⏱️ This function records when a runner finishes the race.
    It's like writing down their time on a clipboard!
    
    bib: 🔢 the number on the runner's shirt
    """
    # 🛑 Make sure the race is actually running
    if not race_started or race_stopped:
        print("Race not running.")  # 😟 can't record times if the race isn't happening
        return  # 🚪 exit this function
    
    # 🗃️ Connect to our database to save the result
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer
    
    # ⏰ Calculate how long it took them to finish
    now = datetime.datetime.now()  # 🕐 what time is it right now?
    elapsed = (now - race_start_time).total_seconds()  # 🧮 subtract start time from now = race time
    date = race_start_time.strftime('%Y-%m-%d')  # 📅 what day did the race happen?
    
    # 💾 Save this result to our database
    c.execute('INSERT INTO results (bib, finish_time, race_date) VALUES (?, ?, ?)',
              (int(bib) if bib else 0, elapsed, date))  # 🔢 use 0 if no bib number given
    
    conn.commit()  # ✅ save our changes
    conn.close()   # 🚪 close the database
    
    # 📢 Tell everyone this runner finished
    print(f"Bib {bib or 'UNKNOWN'} finished in {elapsed:.2f}s")
    
    # 🔊 Try to play a beep sound (if we have the sound file)
    try:
        playsound('beep.mp3')  # 🎵 play celebration sound
    except:
        pass  # 🤫 if the sound doesn't work, just keep going quietly

def live_race_input():
    """
    🎯 This function lets you input bib numbers as runners finish the race.
    It's like being the person with the clipboard at the finish line!
    """
    print("")  # 📝 add a blank line for readability
    
    # 🔄 Keep running this loop while the race is happening
    while race_started and not race_stopped:
        # ⏰ Show how much time has passed since the race started
        now = datetime.datetime.now()  # 🕐 what time is it now?
        elapsed = now - race_start_time  # 🧮 how much time has passed?
        minutes, seconds = divmod(elapsed.total_seconds(), 60)  # 🧮 convert to minutes and seconds
        
        # 📺 Show the elapsed time on the screen (this updates constantly)
        print(f"\rElapsed time: {int(minutes):02d}:{seconds:05.2f}", end="")
        
        try:
            # 📝 Ask for the next bib number
            bib = input("\n> ").strip()  # 🔢 get bib number, remove extra spaces
            
            # 🚪 If they type 'exit', stop the race
            if bib.lower() == 'exit':
                stop_race()  # 🛑 stop the race
                break  # 🚪 exit the loop
            
            # ⏱️ Record this runner's finish time
            record_result(bib)
            
        except KeyboardInterrupt:  # 🛑 if they press Ctrl+C
            print("\n[INFO] Interrupted.")  # 📢 tell them we're stopping
            break  # 🚪 exit the loop

# ===============================
# 📊 RESULTS FUNCTIONS (See who won!)
# ===============================

def show_individual_results():
    """
    🏆 This function shows the race results for individual runners.
    It's like posting the results on a bulletin board!
    """
    # 🛑 Make sure we have a database loaded
    if not DB_FILENAME:
        print("No DB loaded.")  # 😟 can't show results without a database
        return  # 🚪 exit this function
    
    # 🗃️ Connect to our database
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer
    
    # 🔍 Get all the results, sorted by who finished first
    c.execute('''SELECT results.bib, COALESCE(runners.name,'UNKNOWN'),
                        results.finish_time
                 FROM results LEFT JOIN runners ON results.bib = runners.bib
                 ORDER BY results.finish_time ASC''')  # ⬆️ fastest times first
    
    rows = c.fetchall()  # 📋 get all the results
    conn.close()  # 🚪 close the database
    
    # 📋 Print each result with their place
    for i, row in enumerate(rows, 1):  # 🔢 start counting from 1 for places
        # 🏆 Format the place number nicely
        place = f"{i}".rjust(2) + "." if i < 100 else f"{i}."
        # 📢 Show: place, bib number, name, and time
        print(f"{place} Bib: {row[0]}, Name: {row[1]}, Time: {row[2]:.2f}s")

def show_team_results():
    """
    🏫 This function shows cross country team results.
    In cross country, teams score points based on where their runners finish!
    The team with the LOWEST score wins (like golf)!
    """
    # 🗃️ Connect to our database
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer
    
    # 🔍 Get all results with team info, sorted by finish time
    c.execute('''SELECT COALESCE(runners.team,'UNKNOWN'), results.bib, runners.name, results.finish_time
                 FROM results LEFT JOIN runners ON results.bib = runners.bib
                 ORDER BY results.finish_time ASC''')  # ⬆️ fastest first
    
    rows = c.fetchall()  # 📋 get all the results
    conn.close()  # 🚪 close the database

    # 🏫 Group runners by their teams
    teams = {}  # 📚 dictionary to hold team info
    for place, (team, bib, name, time) in enumerate(rows, 1):  # 🔢 place = 1st, 2nd, 3rd, etc.
        # 📝 Add this runner to their team's list
        teams.setdefault(team, []).append((place, bib, name, time))

    # 🧮 Calculate team scores
    scores = []  # 📋 list to hold team scores
    for team, runners in teams.items():  # 🔄 go through each team
        # 🏆 Top 5 runners score points (their place = their points)
        top5 = runners[:5]  # 🥇 get first 5 runners
        # 🏃 Displacers are 6th and 7th runners (help break ties)
        displacers = runners[5:7]  # 🏃 get 6th and 7th runners
        
        # 🧮 Team score = add up the places of top 5 runners
        score = sum(p[0] for p in top5)  # 🔢 1st place = 1 point, 2nd = 2 points, etc.
        
        # 🤝 Tiebreaker = places of displacers (in case teams have same score)
        tiebreak = [p[0] for p in displacers] + [float('inf'), float('inf')]  # ♾️ use infinity if no displacers
        
        # 📊 Save this team's info
        scores.append((team, score, top5, displacers, tiebreak[0], tiebreak[1]))

    # 🏆 Sort teams by score (lowest score wins!)
    scores.sort(key=lambda x: (x[1], x[4], x[5]))  # 🥇 sort by score, then tiebreakers
    
    # 📋 Print the team results
    for rank, entry in enumerate(scores, 1):  # 🔢 rank = 1st place team, 2nd place team, etc.
        print(f"\nRank {rank} - Team: {entry[0]}\nTeam Score = {entry[1]}")  # 🏆 show team rank and score
        
        # 🏃‍♀️ Show the top 5 runners who scored
        print("Top 5:")
        for team_place, bib, name, t in entry[2]:
            print(f"  TeamPlace {team_place}, Bib {bib}, {name}, {t:.2f}s")
        
        # 🏃‍♂️ Show the displacers (don't score but help with tiebreaks)
        print("Displacers:")
        for team_place, bib, name, t in entry[3]:
            print(f"  TeamPlace {team_place}, Bib {bib}, {name}, {t:.2f}s")

def show_age_group_results():
    """
    🎂 This function shows road race results grouped by age.
    Road races group people by age so you compete against people your own age!
    """
    # 🗃️ Connect to our database
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer
    
    # 🔍 Get all results with age info, sorted by finish time
    c.execute('''SELECT runners.age, runners.bib, runners.name, results.finish_time
                 FROM results LEFT JOIN runners ON results.bib = runners.bib
                 ORDER BY results.finish_time ASC''')  # ⬆️ fastest first
    
    rows = c.fetchall()  # 📋 get all the results
    conn.close()  # 🚪 close the database

    # 🎂 Define age groups (like different categories)
    age_groups = [
        (1, 15),      # 👶 youth
        (16, 20),     # 🧒 teens  
        (21, 25),     # 👨 young adults
        (26, 30),     # 👩 adults
        (31, 35),     # 👨‍💼 more adults
        (36, 40),     # 👩‍💼 even more adults
        (41, 45),     # 👨‍🦳 getting older
        (46, 50),     # 👩‍🦳 middle aged
        (51, 55),     # 👨‍🦲 older
        (56, 60),     # 👩‍🦲 senior
        (61, 65),     # 👴 getting really senior
        (66, 70),     # 👵 very senior
        (71, 200)     # 🧓 super senior (200 is just a big number)
    ]
    
    # 📚 Create empty lists for each age group
    results_by_group = {f"{low}-{high}": [] for (low, high) in age_groups}
    
    # 🔄 Put each runner in the right age group
    for i, (age, bib, name, time) in enumerate(rows, 1):  # 🔢 i = overall place
        # 🔍 Find which age group this runner belongs to
        for (low, high) in age_groups:
            if low <= age <= high:  # 🎯 if their age fits in this group
                # 📝 Add them to this age group
                results_by_group[f"{low}-{high}"].append((i, bib, name, time))
                break  # 🚪 stop looking, we found their group

    # 📋 Print results for each age group
    for group, result_list in results_by_group.items():  # 🔄 go through each age group
        if result_list:  # 🔍 only show groups that have runners
            print(f"\nAge Group {group}")  # 🎂 show the age group
            print("Place  Bib   Name               Time")  # 📋 header row
            
            # 🔄 Show each runner in this age group
            for i, (place, bib, name, time) in enumerate(result_list, 1):  # 🔢 i = place within age group
                # ⏰ Convert seconds to a nice time format
                min, sec = divmod(time, 60)  # 🧮 convert to minutes and seconds
                hrs, min = divmod(min, 60)   # 🧮 convert to hours and minutes
                
                # 🕐 Format the time nicely (show hours only if race took more than 1 hour)
                if hrs:  # 🕐 if the race took more than an hour
                    formatted = f"{int(hrs)}:{int(min):02}:{int(sec):02}:{int((time % 1)*100):02}"
                else:    # ⏰ if the race was less than an hour
                    formatted = f"{int(min):02}:{int(sec):02}:{int((time % 1)*100):02}"
                
                # 📋 Print this runner's result
                print(f"{i:<6} {bib:<5} {name:<18} {formatted}")

def show_all_runners():
    """
    👥 This function shows all the runners who are registered for the race.
    It's like looking at the sign-up list to see who's racing!
    """
    # 🛑 Make sure we have a database loaded
    if not DB_FILENAME:
        print("[ERROR] No DB loaded.")  # 😟 can't show runners without a database
        return  # 🚪 exit this function
    
    # 🗃️ Connect to our database
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()  # 🖱️ our database pointer
    
    # 🔍 Get all runners, sorted by their bib numbers
    c.execute("SELECT * FROM runners ORDER BY bib ASC")  # ⬆️ lowest bib numbers first
    rows = c.fetchall()  # 📋 get all the runners
    conn.close()  # 🚪 close the database
    
    # 📋 Print each runner's information
    for r in rows:  # 🔄 go through each runner
        print(r)  # 📢 print all their info
    
    # ⏸️ Wait for user to press Enter before going back to menu
    input("\nPress Enter to return to the menu...")  # 🔄 pause so they can read the list

# ===============================
# 🍽️ MAIN MENU (The restaurant menu of our program!)
# ===============================

def main_menu():
    """
    🍽️ This is the main menu of our program!
    It shows all the things you can do and lets you pick what you want to do next.
    It's like the main screen of a video game!
    """
    # 🔄 Keep showing the menu until the user wants to quit
    while True:  # ♾️ infinite loop until they choose to quit
        
        # 📋 Show the current status and menu options
        print(f"\n=== TRTS Menu ===")  # 🏷️ program title
        print(f"Current DB: {DB_FILENAME if DB_FILENAME else '[None]'} [{RACE_TYPE}]")  # 📂 show what database is loaded
        print("1) Create new database")        # 🆕 start a brand new race
        print("2) Load existing database (/data)")  # 📂 open an old race
        print("3) Load runners from CSV (/data)")   # 📊 import runner list from spreadsheet
        print("4) View all runners")               # 👥 see who's signed up
        print("5) Start the race")                 # 🏁 begin timing the race
        print("6) Show individual results")        # 🏆 see who won individually
        
        # 🏃 Show different option 7 based on race type
        if RACE_TYPE == "cross_country":
            print("7) Show team results")          # 🏫 see which team won
        elif RACE_TYPE == "road_race":
            print("7) Show age group results")     # 🎂 see who won in each age group
        else:
            print("7) [Unavailable until race type is loaded]")  # 🚫 can't show results until we know race type
        
        print("8) Quit")  # 🚪 exit the program

        # 📝 Ask the user what they want to do
        choice = input("Choose: ").strip()  # 🎯 get their choice, remove extra spaces
        
        # 🎯 Do different things based on what they picked
        if choice == '1': 
            init_db(new_db=True)           # 🆕 create a new race database
        elif choice == '2': 
            load_existing_db()             # 📂 load an existing race
        elif choice == '3': 
            load_runners_from_csv()        # 📊 import runners from CSV
        elif choice == '4': 
            show_all_runners()             # 👥 show all registered runners
        elif choice == '5': 
            start_race()                   # 🏁 start the race timing
        elif choice == '6': 
            show_individual_results()      # 🏆 show individual race results
        elif choice == '7':
            # 🎯 Show different results based on race type
            if RACE_TYPE == "cross_country":
                show_team_results()        # 🏫 show cross country team results
            elif RACE_TYPE == "road_race":
                show_age_group_results()   # 🎂 show road race age group results
            else:
                print("Race type not known.")  # 😕 we don't know what kind of race this is
        elif choice == '8':
            break  # 🚪 exit the main loop (quit the program)
        else:
            print("Invalid.")  # 😟 they picked something that's not on the menu

# ===============================
# 🎬 ENTRY POINT (Where our program starts!)
# ===============================

if __name__ == "__main__":
    """
    🎬 This is where our program begins!
    It's like the "Once upon a time..." of our story.
    
    First we set up the admin login, then we show the main menu.
    """
    # 🔐 Set up the admin login system first
    initialize_config_db()  # 🛠️ make sure we have a secure login system
    
    # 🍽️ Show the main menu and let the user start using the program
    main_menu()  # 🎯 this is where all the fun happens!