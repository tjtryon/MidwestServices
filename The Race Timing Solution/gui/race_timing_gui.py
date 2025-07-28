#!/usr/bin/env python3
"""
race_timing_gui.py - Claude Artifact Update #11
Author: TJ Tryon
Date: July 27, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS) - GUI Version

🎽 This is the GUI version of the race timing program! 🏃‍♀️🏃‍♂️

🧠 What it does:
- Modern graphical interface for timing races
- Fully compatible with console version databases
- Supports both cross country and road races
- Uses same config.db and race database formats
- Real-time race timing with visual feedback
- Complete results display and management

🗂 Compatible with console version database formats:
  - config.db (same bcrypt authentication)
  - YYYYMMDD-##-[cc or rr]-[Race_Name].db race databases
  - Identical table structures for cross country and road races

💡 Perfect for race directors who prefer a visual interface!
"""

# 📦 Import all the tools we need for the GUI and database compatibility
import os           # 📁 helps with file and folder paths
import sqlite3      # 🗃️ lets us talk to the SQLite database
import datetime     # ⏰ helps with time and date
import csv          # 📊 lets us read CSV files
import gi           # 🖼️ helps us build the windows and buttons
import bcrypt       # 🔒 for secure password storage (same as console version)

# Tell the computer we want to use GTK version 4 for making windows
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk

# 📍 Figure out where to save our race data (compatible with console version)
PROJECT_ROOT = os.getcwd()  # 🏠 This gets the folder we're running the program from
DATA_DIR = os.path.join(PROJECT_ROOT, "data")  # 📂 This is where we save race data
CONFIG_DB = os.path.join(DATA_DIR, "config.db")  # 🔐 This saves admin login info

class RaceTimingApp(Gtk.Application):
    """
    🧠 This is our main program class - the brain of our race timing GUI app.
    It's fully compatible with the console version's database formats and authentication.
    """
    
    def __init__(self):
        """
        🎬 This runs when we first create our app.
        Sets up empty variables that we'll fill in later.
        """
        super().__init__(application_id="org.midwest.RaceTimingGUI")
        self.main_window = None     # 🏠 The main window (starts empty)
        self.conn = None           # 🗃️ Database connection (starts empty)
        self.db_path = None        # 📍 Where our race database is saved (starts empty)
        self.race_type = ""        # 🏃 Either "cross_country" or "road_race" (same as console)
        self.title_label = None    # 📝 The text that shows which database is loaded
        
        # 🎮 References to buttons for enabling/disabling
        self.start_race_button = None
        self.individual_results_button = None
        self.dynamic_results_button = None  # 🏃 This button changes based on race type
        self.view_runners_button = None
        self.load_csv_button = None
        
        # 🎨 Set up consistent font styling for the entire application
        self.setup_application_styling()
    
    def setup_application_styling(self):
        """
        🎨 This sets up dual font styling for the application:
        - Garamond 15px for general interface (buttons, labels, dialogs)
        - Space Mono 11pt for data displays (results and runner lists)
        """
        # Create CSS provider for consistent styling
        css_provider = Gtk.CssProvider()
        
        # Define CSS styles with dual font system
        css_data = """
        /* 🎨 General interface uses Garamond 15px */
        * {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
        }
        
        button {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
            padding: 8px 16px;
            border-radius: 8px;
        }
        
        label {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
        }
        
        entry {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
            border-radius: 6px;
        }
        
        dialog {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
            border-radius: 12px;
        }
        
        /* 📊 Data displays use Space Mono 11pt for perfect alignment */
        .results-text {
            font-family: "Space Mono", "Courier New", "Consolas", "Monaco", monospace;
            font-size: 11pt;
        }
        
        textview {
            font-family: "Space Mono", "Courier New", "Consolas", "Monaco", monospace;
            font-size: 11pt;
            border-radius: 6px;
        }
        """
        
        try:
            # 🎨 Load the CSS styling
            css_provider.load_from_data(css_data.encode())
            
            # Apply styling to the entire application
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        except Exception as e:
            print(f"Could not load custom styling: {e}")
            # 🤷 Continue without custom styling if there's an error

    def do_activate(self):
        """
        🎬 This runs when our app starts up.
        It builds the main window and shows it on screen.
        """
        self.build_main_window()          # 🏗️ Create the main window with all buttons
        self.ensure_config_db()           # 🔐 Make sure we have admin settings saved (same as console)
        self.main_window.set_application(self)  # 🔗 Connect window to our app
        self.main_window.present()        # 📺 Show the window on screen

    def build_main_window(self):
        """
        🏗️ This creates our main window with all the buttons.
        Think of it like building a control panel for race timing.
        """
        # 🏠 Create the main window with proper title and size
        self.main_window = Gtk.ApplicationWindow(title="The Race Timing Solution (TRTS) - GUI Version")
        self.main_window.set_default_size(450, 500)  # 📏 Make it 450 pixels wide, 500 tall
        
        # 🏃 Set a running shoe icon for the window
        try:
            self.main_window.set_icon_name("applications-sports")  # 🏃 Sports/athletics icon
        except:
            try:
                self.main_window.set_icon_name("media-playback-start")  # ▶️ Start/play icon as fallback
            except:
                pass  # 🤷 Use default icon if nothing else works

        # 📦 Create a container to hold all our buttons vertically
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10,
                       margin_top=20, margin_bottom=20, margin_start=20, margin_end=20)

        # 📝 Create a label to show which database is currently loaded and race type
        self.title_label = Gtk.Label(label="No database loaded")
        vbox.append(self.title_label)

        # 🎮 Create all our buttons and connect them to functions
        # 🏗️ First create the static buttons that are always present
        static_buttons = [
            ("Create New Database", self.create_new_database),
            ("Load Existing Database", self.load_existing_database),
            ("Load Runners from CSV", self.load_csv_to_database),
            ("View All Runners", self.view_all_runners),
            ("Start the Race", self.start_race),
            ("Show Individual Results", self.show_individual_results),
        ]

        # 🔄 Add static buttons to our window
        for label, handler in static_buttons:
            btn = Gtk.Button(label=label)  # 🆕 Create the button
            btn.connect("clicked", handler)  # 🔗 Tell it what to do when clicked
            
            # 🔍 Debug print for Create New Database button
            if label == "Create New Database":
                print(f"Connected '{label}' button to handler: {handler}")
            
            # 📌 Keep references to buttons we want to enable/disable
            if label == "Start the Race":
                self.start_race_button = btn
                btn.set_sensitive(False)  # 🚫 Start disabled until database with runners is loaded
            elif label == "Load Runners from CSV":
                self.load_csv_button = btn
                btn.set_sensitive(False)  # 🚫 Start disabled until database is loaded
            elif label == "Show Individual Results":
                self.individual_results_button = btn
                btn.set_sensitive(False)  # 🚫 Start disabled until race has results
            elif label == "View All Runners":
                self.view_runners_button = btn
                btn.set_sensitive(False)  # 🚫 Start disabled until database with runners is loaded
            
            vbox.append(btn)  # ➕ Add it to our container

        # 🏃 Create the dynamic results button (changes based on race type)
        # This will show "Show Team Results" for cross country or "Show Age Group Results" for road race
        self.dynamic_results_button = Gtk.Button(label="Show Results (Load database first)")
        self.dynamic_results_button.set_sensitive(False)  # 🚫 Start disabled
        self.dynamic_results_button.connect("clicked", self.show_dynamic_results)
        vbox.append(self.dynamic_results_button)

        # 🎮 Add the remaining static buttons
        final_buttons = [
            ("Instructions", self.show_instructions),
            ("Exit", lambda b: self.quit()),
        ]

        for label, handler in final_buttons:
            btn = Gtk.Button(label=label)
            btn.connect("clicked", handler)
            vbox.append(btn)

        # 🏠 Put our container of buttons into the main window
        self.main_window.set_child(vbox)

    def ensure_config_db(self):
        """
        🔐 This makes sure we have admin login information saved.
        Uses exact same bcrypt authentication as console version.
        If it's the first time running, asks for admin username and password.
        """
        # 📁 Create the data folder if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Data directory: {DATA_DIR}")
        
        # 🔍 Check if we already have admin settings saved (same format as console)
        if not os.path.exists(CONFIG_DB):
            # 🆕 First time running - ask for admin info
            dialog = Gtk.Dialog(title="Admin Setup", transient_for=self.main_window, modal=True)
            dialog.set_default_size(350, 200)
            box = dialog.get_content_area()
            box.set_spacing(10)
            box.set_margin_top(20)
            box.set_margin_bottom(20)
            box.set_margin_start(20)
            box.set_margin_end(20)
            
            # 📝 Create instructions
            instructions = Gtk.Label()
            instructions.set_markup("<b>First-time setup:</b>\nCreate admin credentials for race management")
            instructions.set_justify(Gtk.Justification.CENTER)
            box.append(instructions)
            
            # 📝 Create text boxes for username and password
            user = Gtk.Entry(placeholder_text="Admin Username")
            pw = Gtk.Entry(placeholder_text="Admin Password")
            pw.set_visibility(False)  # 🙈 Hide password as you type
            
            box.append(user)
            box.append(pw)
            
            # 🎮 Add OK and Cancel buttons
            dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
            dialog.add_button("OK", Gtk.ResponseType.OK)
            dialog.show()

            def on_response(dlg, response):
                """
                🎯 This runs when user clicks OK or Cancel on the admin setup.
                """
                if response == Gtk.ResponseType.OK:
                    # ✅ User clicked OK - save their admin info using bcrypt (same as console)
                    username = user.get_text().strip()
                    password = pw.get_text().strip()
                    
                    # 🔍 Make sure they entered both username and password
                    if username and password:
                        try:
                            # 💾 Save admin info using exact same format as console version
                            conn = sqlite3.connect(CONFIG_DB)
                            c = conn.cursor()
                            
                            # 🏗️ Create users table identical to console version
                            c.execute('''CREATE TABLE users (
                                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            username TEXT UNIQUE NOT NULL,
                                            password_hash BLOB NOT NULL)''')
                            
                            # 🔒 Hash the password for security using bcrypt (same as console)
                            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                            
                            # 💾 Save the username and scrambled password (same format as console)
                            c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
                            conn.commit()
                            conn.close()
                            print(f"Config database created: {CONFIG_DB}")
                        except sqlite3.Error as e:
                            # 😟 Something went wrong saving to database
                            self.show_error_dialog(f"Database error: {e}")
                    else:
                        # 😟 User didn't fill in both fields
                        self.show_error_dialog("Please enter both username and password.")
                elif response == Gtk.ResponseType.CANCEL:
                    # 🚪 User cancelled - exit the application
                    self.quit()
                
                # 🚪 Close the dialog
                dlg.destroy()

            dialog.connect("response", on_response)

    def create_new_database(self, button):
        """
        🆕 This creates a brand new race database.
        First asks for race type (cross country vs road race), then race details.
        Creates database with exact same structure as console version.
        """
        print("create_new_database called")  # Debug print
        
        # 🎯 First ask what type of race this is (same as console version)
        type_dialog = Gtk.Dialog(title="Select Race Type", transient_for=self.main_window, modal=True)
        type_dialog.set_default_size(350, 250)
        
        print("Dialog created")  # Debug print
        
        # Get the content area and set up proper spacing
        box = type_dialog.get_content_area()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_spacing(15)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        # 📝 Instructions label
        instructions = Gtk.Label()
        instructions.set_markup("<b>Select race type:</b>\n\nChoose the type of race you want to create:")
        instructions.set_justify(Gtk.Justification.CENTER)
        box.append(instructions)
        
        print("Instructions added")  # Debug print
        
        # 🏃‍♀️ Cross Country button
        cc_button = Gtk.Button(label="Cross Country")
        cc_button.set_size_request(200, 40)
        box.append(cc_button)
        
        # 🏃‍♂️ Road Race button  
        rr_button = Gtk.Button(label="Road Race")
        rr_button.set_size_request(200, 40)
        box.append(rr_button)
        
        print("Buttons added")  # Debug print
        
        def on_cc_selected(btn):
            """🏃‍♀️ User selected Cross Country"""
            print("Cross Country selected")  # Debug print
            self.race_type = "cross_country"
            type_dialog.destroy()
            # Use GLib.idle_add to ensure dialog is fully destroyed before showing next one
            GLib.idle_add(self.create_database_details)
            
        def on_rr_selected(btn):
            """🏃‍♂️ User selected Road Race"""
            print("Road Race selected")  # Debug print
            self.race_type = "road_race"
            type_dialog.destroy()
            # Use GLib.idle_add to ensure dialog is fully destroyed before showing next one
            GLib.idle_add(self.create_database_details)
        
        # Connect the button signals
        cc_button.connect("clicked", on_cc_selected)
        rr_button.connect("clicked", on_rr_selected)
        
        print("Button signals connected")  # Debug print
        
        # Show the dialog - try multiple methods
        type_dialog.show()
        print("Dialog.show() called")  # Debug print
        
        # Also try present() as backup
        type_dialog.present()
        print("Dialog.present() called")  # Debug print

    def create_database_details(self):
        """
        📝 This asks for race number and name, then creates the database.
        Uses exact same filename format as console version.
        """
        # 📝 Create a dialog to ask for race number and race name
        dialog = Gtk.Dialog(title="Create New Race Database", transient_for=self.main_window, modal=True)
        dialog.set_default_size(400, 220)
        box = dialog.get_content_area()
        
        # 📝 Race type confirmation
        type_label = Gtk.Label()
        type_label.set_markup(f"<b>Creating: {self.race_type.replace('_', ' ').title()} Race</b>")
        box.append(type_label)
        
        # 🔢 Create text boxes for race number and race name
        race_num_label = Gtk.Label(label="Race Number (e.g., 01):")
        race_num_label.set_halign(Gtk.Align.START)
        race_num_entry = Gtk.Entry(placeholder_text="Race number (e.g., 01)")
        
        race_name_label = Gtk.Label(label="Race Name:")
        race_name_label.set_halign(Gtk.Align.START)
        race_name_entry = Gtk.Entry(placeholder_text="e.g., County_Meet")
        
        # 📦 Add spacing and organization
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        box.append(race_num_label)
        box.append(race_num_entry)
        box.append(race_name_label)
        box.append(race_name_entry)
        
        # 🎮 Add Cancel and OK buttons
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.show()

        def on_response(dlg, response):
            """🎯 This runs when user enters race information and clicks OK."""
            if response == Gtk.ResponseType.OK:
                # 📝 Get the race number and name they typed
                race_num = race_num_entry.get_text().strip().zfill(2)  # 🔢 Make sure it's 2 digits
                race_name = race_name_entry.get_text().strip()
                
                # 🔍 Make sure they entered both race number and name
                if race_num and race_num != "00" and race_name:
                    # 🏷️ Create database filename with exact same format as console version
                    today = datetime.datetime.now().strftime('%Y%m%d')  # 📅 Like 20250727
                    
                    # 🧹 Clean up race name for filename
                    clean_race_name = race_name.replace(" ", "_")
                    
                    # 🏷️ Create filename: YYYYMMDD-##-[cc or rr]-[race_name].db (same as console)
                    suffix = "cc" if self.race_type == "cross_country" else "rr"
                    db_name = f"{today}-{race_num}-{suffix}-{clean_race_name}.db"
                    self.db_path = os.path.join(DATA_DIR, db_name)
                    
                    try:
                        # 🗃️ Create the new database file
                        self.conn = sqlite3.connect(self.db_path)
                        c = self.conn.cursor()
                        
                        # 💾 Store the race type (exact same as console version)
                        c.execute("CREATE TABLE race_type (type TEXT)")
                        c.execute("INSERT INTO race_type (type) VALUES (?)", (self.race_type,))
                        
                        # 🏗️ Create different tables based on race type (identical to console)
                        if self.race_type == "cross_country":
                            # 🏃‍♀️ Cross country races care about teams, grades, etc.
                            c.execute('''CREATE TABLE IF NOT EXISTS runners (
                                            bib INTEGER PRIMARY KEY,
                                            name TEXT,
                                            team TEXT,
                                            age INTEGER,
                                            grade TEXT,
                                            rfid TEXT)''')
                        else:  # road race
                            # 🏃‍♂️ Road races care about age groups based on birthday
                            c.execute('''CREATE TABLE IF NOT EXISTS runners (
                                            bib INTEGER PRIMARY KEY,
                                            name TEXT,
                                            dob TEXT,
                                            age INTEGER,
                                            rfid TEXT)''')
                        
                        # 🏁 Every race needs a table to store results (identical to console)
                        c.execute('''CREATE TABLE IF NOT EXISTS results (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        bib INTEGER,
                                        finish_time REAL,
                                        race_date TEXT)''')
                        
                        self.conn.commit()  # ✅ Save the changes
                        
                        # 📝 Update the title to show which database is loaded
                        self.title_label.set_label(f"Loaded: {db_name} [{self.race_type}]")
                        print(f"Database created: {self.db_path}")
                        
                        # 🔄 Check button states
                        self.update_button_states()
                        
                    except sqlite3.Error as e:
                        # 😟 Something went wrong creating the database
                        self.show_error_dialog(f"Database error: {e}")
                else:
                    # 😟 They didn't enter both required fields
                    self.show_error_dialog("Please enter both a valid race number and race name.")
            
            # 🚪 Close the dialog
            dlg.destroy()

        dialog.connect("response", on_response)

    def load_existing_database(self, button):
        """
        📂 This opens a race database that was created before.
        Detects race type automatically from database (same as console version).
        """
        print(f"Opening database dialog...")

        # 📂 Create file picker dialog to choose database file
        file_dialog = Gtk.FileChooserDialog(
            title="Load Existing Database",
            parent=self.main_window,
            action=Gtk.FileChooserAction.OPEN
        )
        
        # 🎮 Add Cancel and Open buttons
        file_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        file_dialog.add_button("_Open", Gtk.ResponseType.ACCEPT)
        
        # 🔍 Create filter to only show database files
        db_filter = Gtk.FileFilter()
        db_filter.set_name("Database files")
        db_filter.add_pattern("*.db")
        file_dialog.add_filter(db_filter)

        # 📁 Try to start in our data directory
        try:
            file_dialog.set_current_folder(Gio.File.new_for_path(DATA_DIR))
        except Exception as e:
            print(f"Could not set folder: {e}")

        def on_response(dialog, response):
            """🎯 This runs when user picks a database file and clicks Open."""
            if response == Gtk.ResponseType.ACCEPT:
                # ✅ User picked a file and clicked Open
                file = dialog.get_file()
                if file:
                    db_path = file.get_path()
                    print(f"Selected database: {db_path}")
                    # 📂 Load the database
                    self.load_database(db_path)
            # 🚪 Close the file picker
            dialog.destroy()

        file_dialog.connect("response", on_response)
        file_dialog.show()

    def load_database(self, db_path):
        """
        🔗 This actually opens a database file and connects to it.
        Detects race type automatically (same logic as console version).
        """
        try:
            # 🔍 Close existing database connection if we have one
            if self.conn:
                self.conn.close()
            
            # 🔗 Connect to the selected database
            self.db_path = db_path
            self.conn = sqlite3.connect(self.db_path)
            c = self.conn.cursor()
            
            # 🔍 Try to figure out what type of race this is (same as console)
            try:
                c.execute("SELECT type FROM race_type")
                self.race_type = c.fetchone()[0]
            except:
                self.race_type = "unknown"
            
            # 📝 Update title to show which database is loaded
            db_name = os.path.basename(self.db_path)
            self.title_label.set_label(f"Loaded: {db_name} [{self.race_type}]")
            
            # 🔄 Check button states
            self.update_button_states()
            
        except sqlite3.Error as e:
            # 😟 Something went wrong with the database
            self.show_error_dialog(f"Database error: {e}")

    def load_csv_to_database(self, button):
        """
        📊 This loads runner information from a CSV file.
        Handles different CSV formats for cross country vs road race (same as console).
        """
        # 🛑 Make sure we have a database open first
        if not self.conn:
            self.show_error_dialog("No database loaded. Create or load a database first.")
            return

        # 📂 Create a file picker dialog to choose CSV file
        file_dialog = Gtk.FileChooserDialog(
            title="Select CSV File",
            parent=self.main_window,
            action=Gtk.FileChooserAction.OPEN
        )
        
        # 🎮 Add Cancel and Open buttons
        file_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        file_dialog.add_button("_Open", Gtk.ResponseType.ACCEPT)
        
        # 🔍 Create a filter so we only see CSV files
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("CSV files")
        csv_filter.add_pattern("*.csv")
        file_dialog.add_filter(csv_filter)
        
        # 📁 Try to start in our data directory
        try:
            file_dialog.set_current_folder(Gio.File.new_for_path(DATA_DIR))
        except Exception as e:
            print(f"Could not set folder: {e}")

        def on_response(dialog, response):
            """🎯 This runs when user picks a CSV file and clicks Open."""
            if response == Gtk.ResponseType.ACCEPT:
                # ✅ User picked a file and clicked Open
                file = dialog.get_file()
                if file:
                    file_path = file.get_path()
                    print(f"Selected file: {file_path}")
                    # 📊 Process the CSV file
                    self.process_csv_file(file_path)
            # 🚪 Close the file picker
            dialog.destroy()

        file_dialog.connect("response", on_response)
        file_dialog.show()

    def process_csv_file(self, file_path):
        """
        📊 This reads a CSV file and adds runner information to database.
        Uses exact same logic as console version for different race types.
        """
        try:
            # 📖 Open and read the CSV file
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows_processed = 0
                
                # 🔄 Read each row (each runner) from the CSV
                if self.race_type == "cross_country":
                    # 🏃‍♀️ Cross country CSV should have these columns (same as console)
                    expected_fields = ['bib', 'name', 'team', 'age', 'grade', 'rfid']
                    
                    # 🔍 Check if the CSV has the right columns
                    if reader.fieldnames != expected_fields:
                        self.show_error_dialog(f"CSV must have columns: {expected_fields}")
                        return
                    
                    # 🔄 Process each runner
                    for row in reader:
                        # 💾 Add this runner using same format as console
                        self.conn.execute('''INSERT OR REPLACE INTO runners (bib, name, team, age, grade, rfid)
                                             VALUES (?, ?, ?, ?, ?, ?)''',
                                          (row['bib'], row['name'], row['team'], row['age'], row['grade'], row['rfid']))
                        rows_processed += 1
                        
                else:  # road_race
                    # 🏃‍♂️ Road race CSV should have these columns (same as console)
                    expected_fields = ['bib', 'name', 'dob', 'rfid']
                    
                    # 🔍 Check if the CSV has the right columns
                    if reader.fieldnames != expected_fields:
                        self.show_error_dialog(f"CSV must have columns: {expected_fields}")
                        return
                    
                    # 🔄 Process each runner
                    for row in reader:
                        # 🎂 Calculate age from birthday (same logic as console)
                        birthdate = datetime.datetime.strptime(row['dob'], "%Y-%m-%d")
                        age = int((datetime.datetime.now() - birthdate).days // 365.25)
                        
                        # 💾 Add this runner using same format as console
                        self.conn.execute('''INSERT OR REPLACE INTO runners (bib, name, dob, age, rfid)
                                             VALUES (?, ?, ?, ?, ?)''',
                                          (row['bib'], row['name'], row['dob'], age, row['rfid']))
                        rows_processed += 1
                
                # ✅ Save all changes to database
                self.conn.commit()
                
                # 🎉 Show success message
                self.show_text_window("CSV Import", f"Successfully imported {rows_processed} runners.")
                
                # 🔄 Update button states
                self.update_button_states()
                
        except (csv.Error, ValueError, sqlite3.Error) as e:
            # 😟 Something went wrong reading the file or saving to database
            self.show_error_dialog(f"Error processing CSV file: {e}")
        except FileNotFoundError:
            # 📂 File doesn't exist
            self.show_error_dialog("CSV file not found.")
        except Exception as e:
            # 🤷 Something else went wrong
            self.show_error_dialog(f"Unexpected error: {e}")

    def show_dynamic_results(self, button):
        """
        🎯 This function is called by the dynamic results button.
        It determines what type of results to show based on the loaded race type.
        Same logic as console version menu option 7.
        """
        if self.race_type == "cross_country":
            # 🏃‍♀️ Show team results for cross country races
            self.show_team_results(button)
        elif self.race_type == "road_race":
            # 🏃‍♂️ Show age group results for road races
            self.show_age_group_results(button)
        else:
            # 🤷 Race type unknown - shouldn't happen if button states are managed correctly
            self.show_error_dialog("Race type not known. Please load a valid race database.")

    def update_button_states(self):
        """
        🔄 This checks what we have loaded and enables/disables buttons accordingly.
        Updates the dynamic results button label and functionality based on race type.
        """
        # 🔍 Check if we have database connection
        has_db = self.conn is not None
        has_runners = False
        has_results = False
        
        if has_db:
            try:
                # 🔍 Check if there are any runners in the database
                cursor = self.conn.execute("SELECT COUNT(*) FROM runners")
                runner_count = cursor.fetchone()[0]
                has_runners = runner_count > 0
                
                # 🔍 Check if there are any race results
                cursor = self.conn.execute("SELECT COUNT(*) FROM results WHERE finish_time IS NOT NULL")
                result_count = cursor.fetchone()[0]
                has_results = result_count > 0
                
            except sqlite3.Error:
                # 😟 If there's an error checking, keep buttons disabled
                pass
        
        # 🎮 Update static button states
        if self.load_csv_button:
            self.load_csv_button.set_sensitive(has_db)
            
        if self.view_runners_button:
            self.view_runners_button.set_sensitive(has_runners)
            
        if self.start_race_button:
            self.start_race_button.set_sensitive(has_runners)
            
        if self.individual_results_button:
            self.individual_results_button.set_sensitive(has_results)
            
        # 🏃 Update dynamic results button based on race type (same logic as console)
        if self.dynamic_results_button:
            if self.race_type == "cross_country":
                # 🏃‍♀️ Cross country race loaded - show team results option
                self.dynamic_results_button.set_label("Show Team Results")
                self.dynamic_results_button.set_sensitive(has_results)
                if has_results:
                    self.dynamic_results_button.set_tooltip_text("View cross country team scoring results")
                else:
                    self.dynamic_results_button.set_tooltip_text("Complete a race to see team results")
                    
            elif self.race_type == "road_race":
                # 🏃‍♂️ Road race loaded - show age group results option
                self.dynamic_results_button.set_label("Show Age Group Results")
                self.dynamic_results_button.set_sensitive(has_results)
                if has_results:
                    self.dynamic_results_button.set_tooltip_text("View road race age group results")
                else:
                    self.dynamic_results_button.set_tooltip_text("Complete a race to see age group results")
                    
            else:
                # 🤷 No race type detected or no database loaded
                self.dynamic_results_button.set_label("Show Results (Load database first)")
                self.dynamic_results_button.set_sensitive(False)
                if not has_db:
                    self.dynamic_results_button.set_tooltip_text("Load a race database first")
                else:
                    self.dynamic_results_button.set_tooltip_text("Race type not detected")

    def view_all_runners(self, button):
        """
        👥 This shows a list of all runners registered for the race.
        Display format depends on race type (same data structure as console).
        """
        # 🛑 Make sure we have a database loaded
        if not self.conn:
            self.show_text_window("All Runners", "No database loaded.")
            return

        try:
            # 🔍 Get all runners from database, sorted by bib number
            if self.race_type == "cross_country":
                cursor = self.conn.execute("SELECT bib, name, team, age, grade FROM runners ORDER BY bib")
            else:  # road_race
                cursor = self.conn.execute("SELECT bib, name, dob, age FROM runners ORDER BY bib")
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
            # 😟 Something went wrong reading from database
            self.show_text_window("All Runners", f"Database error: {e}")
            return

        # 🔍 Check if we have any runners loaded
        if not rows:
            self.show_text_window("All Runners", "No runners loaded. Please load a CSV file.")
            return

        # 📝 Build text to show all runners
        output = "ALL REGISTERED RUNNERS\n"
        output += "=" * 70 + "\n"
        
        if self.race_type == "cross_country":
            # 🏃‍♀️ Cross country format
            output += f"{'BIB':<8}{'NAME':<25}{'TEAM':<20}{'AGE':<5}{'GRADE'}\n"
            output += "-" * 70 + "\n"
            
            for bib, name, team, age, grade in rows:
                output += f"{bib:<8}{name[:24]:<25}{team[:19]:<20}{age:<5}{grade}\n"
        else:
            # 🏃‍♂️ Road race format
            output += f"{'BIB':<8}{'NAME':<30}{'DOB':<12}{'AGE'}\n"
            output += "-" * 70 + "\n"
            
            for bib, name, dob, age in rows:
                output += f"{bib:<8}{name[:29]:<30}{dob:<12}{age}\n"
        
        # 📺 Show the list in a window
        self.show_text_window("All Runners", output)

    def start_race(self, button):
        """
        🏁 This starts the race timing system.
        Records start time and opens timing window (compatible with console results format).
        """
        # 🛑 Make sure we have a database loaded
        if not self.conn:
            self.show_text_window("Start Race", "No database loaded.")
            return

        # ⏰ Record the current time as race start time
        race_start_time = datetime.datetime.now()
        race_date = race_start_time.strftime('%Y-%m-%d')
        
        try:
            # 📊 Open the race timing window
            self.open_race_timing_window(race_start_time, race_date)
            
        except sqlite3.Error as e:
            # 😟 Something went wrong with database
            self.show_error_dialog(f"Database error: {e}")

    def open_race_timing_window(self, start_time, race_date):
        """
        ⏱️ This creates the race timing window.
        Records finish times in same format as console version.
        """
        # 🏠 Create race timing window
        timing_window = Gtk.Window(title="Race Timing - IN PROGRESS")
        timing_window.set_default_size(600, 500)
        timing_window.set_transient_for(self.main_window)
        timing_window.set_modal(True)
        
        # 📦 Create container for everything
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10,
                       margin_top=20, margin_bottom=20, margin_start=20, margin_end=20)
        
        # ⏰ Create big timer display
        timer_label = Gtk.Label()
        timer_label.set_markup("<span size='24000' weight='bold'>00:00:00</span>")
        vbox.append(timer_label)
        
        # 📝 Show when race started
        start_label = Gtk.Label(label=f"Race started: {start_time.strftime('%H:%M:%S')}")
        vbox.append(start_label)
        
        # ➖ Add separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.append(separator)
        
        # 📝 Instructions
        instructions = Gtk.Label()
        instructions.set_markup(
            "<b>Instructions:</b>\n"
            "• Enter bib number and press Enter to record finish\n"
            "• Type 'exit' and press Enter to stop timing"
        )
        instructions.set_justify(Gtk.Justification.LEFT)
        vbox.append(instructions)
        
        # 📝 Create text box for entering bib numbers
        bib_entry = Gtk.Entry(placeholder_text="Enter bib number or 'exit'")
        vbox.append(bib_entry)
        
        # 📺 Create area to show results
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        
        results_textview = Gtk.TextView()
        results_textview.set_editable(False)
        results_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        results_buffer = results_textview.get_buffer()
        results_buffer.set_text("Finish times will appear here...\n")
        
        scrolled_window.set_child(results_textview)
        vbox.append(scrolled_window)
        
        timing_window.set_child(vbox)
        
        finish_count = 0  # 🔢 Keep track of finishers
        
        def update_timer():
            """⏰ Updates the race timer every second."""
            current_time = datetime.datetime.now()
            elapsed = current_time - start_time
            
            # 🕐 Format as HH:MM:SS
            total_seconds = elapsed.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            timer_label.set_markup(f"<span size='24000' weight='bold'>{time_str}</span>")
            
            return True  # 🔄 Keep calling this function
        
        # ⏰ Start the timer (updates every second)
        timer_id = GLib.timeout_add(1000, update_timer)
        
        def on_bib_entry_activate(entry):
            """🎯 This runs when someone enters a bib number and presses Enter."""
            nonlocal finish_count
            
            # 📝 Get what the user typed
            bib_text = entry.get_text().strip()
            entry.set_text("")  # 🧹 Clear for next entry
            
            # 🚪 Check if user wants to exit
            if bib_text.lower() == 'exit':
                GLib.source_remove(timer_id)  # ⏹️ Stop timer
                timing_window.destroy()        # 🚪 Close window
                self.update_button_states()    # 🔄 Update buttons
                return
            
            # ⏰ Record finish time
            finish_time = datetime.datetime.now()
            elapsed_seconds = (finish_time - start_time).total_seconds()
            finish_count += 1
            
            # 🔢 Determine bib number
            try:
                bib_number = int(bib_text) if bib_text else 0
            except ValueError:
                bib_number = 0
            
            # 💾 Save to database (same format as console version)
            try:
                self.conn.execute('INSERT INTO results (bib, finish_time, race_date) VALUES (?, ?, ?)',
                                  (bib_number, elapsed_seconds, race_date))
                self.conn.commit()
                
                # 📝 Show result in timing window
                elapsed_display = self.format_time(elapsed_seconds)
                result_text = f"{finish_count:3d}. Bib {bib_number:3d} - {elapsed_display}\n"
                
                end_iter = results_buffer.get_end_iter()
                results_buffer.insert(end_iter, result_text)
                
                # 📜 Scroll to show newest result
                mark = results_buffer.get_insert()
                results_textview.scroll_mark_onscreen(mark)
                
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        
        # 🔗 Connect bib entry to function
        bib_entry.connect("activate", on_bib_entry_activate)
        
        def on_window_close(window):
            """🚪 Cleanup when timing window closes."""
            GLib.source_remove(timer_id)
            self.update_button_states()
            return False
        
        timing_window.connect("close-request", on_window_close)
        
        # 📺 Show timing window
        timing_window.present()
        bib_entry.grab_focus()

    def show_individual_results(self, button):
        """
        🏆 Shows individual race results.
        Uses same calculation logic as console version.
        """
        if not self.conn:
            self.show_text_window("Individual Results", "No database loaded.")
            return

        try:
            # 🔍 Get all results, join with runner info
            cursor = self.conn.execute('''
                SELECT results.bib, COALESCE(runners.name,'UNKNOWN'), results.finish_time
                FROM results LEFT JOIN runners ON results.bib = runners.bib
                ORDER BY results.finish_time ASC
            ''')
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
            return

        if not rows:
            self.show_text_window("Individual Results", "No race results found.")
            return

        # 📝 Build formatted results
        output = "INDIVIDUAL RACE RESULTS\n"
        output += "=" * 60 + "\n"
        output += f"{'POS':<5}{'BIB':<8}{'NAME':<25}{'TIME':<12}\n"
        output += "-" * 60 + "\n"
        
        for position, (bib, name, finish_time) in enumerate(rows, 1):
            time_str = self.format_time(finish_time)
            name_display = name[:24] if name else "UNKNOWN"
            output += f"{position:<5}{bib:<8}{name_display:<25}{time_str:<12}\n"
        
        self.show_text_window("Individual Results", output)

    def show_team_results(self, button):
        """
        🏫 Shows cross country team results.
        Uses same scoring logic as console version.
        """
        if not self.conn:
            self.show_text_window("Team Results", "No database loaded.")
            return
            
        if self.race_type != "cross_country":
            self.show_error_dialog("Team results are only available for cross country races.")
            return

        try:
            # 🔍 Get all results with team info
            cursor = self.conn.execute('''
                SELECT COALESCE(runners.team,'UNKNOWN'), results.bib, runners.name, results.finish_time
                FROM results LEFT JOIN runners ON results.bib = runners.bib
                ORDER BY results.finish_time ASC
            ''')
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
            return

        if not rows:
            self.show_text_window("Team Results", "No race results found.")
            return

        # 🏫 Group runners by teams (same logic as console)
        teams = {}
        for place, (team, bib, name, time) in enumerate(rows, 1):
            teams.setdefault(team, []).append((place, bib, name, time))

        # 🧮 Calculate team scores (same logic as console)
        scores = []
        for team, runners in teams.items():
            if len(runners) >= 5:  # 🏃‍♀️ Need at least 5 runners to score
                top5 = runners[:5]
                displacers = runners[5:7]
                score = sum(p[0] for p in top5)
                tiebreak = [p[0] for p in displacers] + [float('inf'), float('inf')]
                scores.append((team, score, top5, displacers, tiebreak[0], tiebreak[1]))

        # 🏆 Sort teams by score (lowest wins)
        scores.sort(key=lambda x: (x[1], x[4], x[5]))
        
        # 📝 Build results display
        output = "CROSS COUNTRY TEAM RESULTS\n"
        output += "=" * 70 + "\n\n"
        
        for rank, (team, score, top5, displacers, _, _) in enumerate(scores, 1):
            output += f"Rank {rank} - Team: {team}\n"
            output += f"Team Score = {score}\n"
            output += "Top 5:\n"
            for place, bib, name, time in top5:
                time_str = self.format_time(time)
                output += f"  Place {place}, Bib {bib}, {name}, {time_str}\n"
            
            if displacers:
                output += "Displacers:\n"
                for place, bib, name, time in displacers:
                    time_str = self.format_time(time)
                    output += f"  Place {place}, Bib {bib}, {name}, {time_str}\n"
            output += "\n"
        
        self.show_text_window("Team Results", output)

    def show_age_group_results(self, button):
        """
        🎂 Shows road race age group results.
        Uses same age grouping logic as console version.
        """
        if not self.conn:
            self.show_text_window("Age Group Results", "No database loaded.")
            return
            
        if self.race_type != "road_race":
            self.show_error_dialog("Age group results are only available for road races.")
            return

        try:
            # 🔍 Get all results with age info
            cursor = self.conn.execute('''
                SELECT runners.age, runners.bib, runners.name, results.finish_time
                FROM results LEFT JOIN runners ON results.bib = runners.bib
                ORDER BY results.finish_time ASC
            ''')
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            self.show_error_dialog(f"Database error: {e}")
            return

        if not rows:
            self.show_text_window("Age Group Results", "No race results found.")
            return

        # 🎂 Define age groups (same as console version)
        age_groups = [
            (1, 15), (16, 20), (21, 25), (26, 30), (31, 35), (36, 40),
            (41, 45), (46, 50), (51, 55), (56, 60), (61, 65), (66, 70), (71, 200)
        ]
        
        # 📚 Group results by age
        results_by_group = {f"{low}-{high}": [] for (low, high) in age_groups}
        
        for i, (age, bib, name, time) in enumerate(rows, 1):
            for (low, high) in age_groups:
                if low <= age <= high:
                    results_by_group[f"{low}-{high}"].append((i, bib, name, time))
                    break

        # 📝 Build results display
        output = "ROAD RACE AGE GROUP RESULTS\n"
        output += "=" * 70 + "\n\n"
        
        for group, result_list in results_by_group.items():
            if result_list:
                output += f"Age Group {group}\n"
                output += f"{'PLACE':<8}{'BIB':<8}{'NAME':<25}{'TIME'}\n"
                output += "-" * 60 + "\n"
                
                for i, (place, bib, name, time) in enumerate(result_list, 1):
                    time_str = self.format_time(time)
                    name_display = name[:24] if name else "UNKNOWN"
                    output += f"{i:<8}{bib:<8}{name_display:<25}{time_str}\n"
                output += "\n"
        
        self.show_text_window("Age Group Results", output)

    def format_time(self, total_seconds):
        """
        ⏰ Converts seconds to MM:SS.mmm format.
        Same formatting logic as console version.
        """
        if total_seconds is None:
            return "00:00.000"
            
        minutes, seconds = divmod(total_seconds, 60)
        return f"{int(minutes):02d}:{seconds:06.3f}"

    def show_instructions(self, button):
        """
        📖 Shows comprehensive user instructions.
        """
        instructions_text = """
THE RACE TIMING SOLUTION (TRTS) - GUI VERSION
============================================

GETTING STARTED:
1. Create New Database
   • Choose race type: Cross Country or Road Race
   • Enter race number and name
   • Database saved as: YYYYMMDD-##-[cc/rr]-Name.db

2. Load Runner Data  
   • Click "Load Runners from CSV"
   • Cross Country CSV: bib, name, team, age, grade, rfid
   • Road Race CSV: bib, name, dob, rfid

RACE TIMING:
3. Start Race
   • Click "Start the Race" to open timing window
   • Enter bib numbers as runners finish
   • Type 'exit' to stop timing

RESULTS:
4. View Results
   • Individual Results: All runners by finish time
   • Team Results: Cross country team scoring
   • Age Group Results: Road race age divisions

COMPATIBILITY:
• Fully compatible with console version databases
• Same authentication and file formats
• Results can be viewed in either version

DATABASE MANAGEMENT:
• Load existing databases from previous races
• All data automatically saved
• Compatible with console version files
"""
        
        self.show_text_window("Instructions", instructions_text)

    def show_error_dialog(self, message):
        """
        😟 Shows an error message in a popup dialog.
        """
        dialog = Gtk.Dialog(title="Error", transient_for=self.main_window, modal=True)
        dialog.set_default_size(400, 150)
        
        content_area = dialog.get_content_area()
        content_area.set_spacing(10)
        content_area.set_margin_top(20)
        content_area.set_margin_bottom(20)
        content_area.set_margin_start(20)
        content_area.set_margin_end(20)
        
        error_label = Gtk.Label(label=message)
        error_label.set_wrap(True)
        content_area.append(error_label)
        
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()

    def show_text_window(self, title, content):
        """
        📺 Shows text content in a scrollable window.
        """
        dialog = Gtk.Dialog(title=title, transient_for=self.main_window, modal=True)
        
        # 📏 Set window size based on content
        if len(content) < 200:
            dialog.set_default_size(400, 200)
        elif "RESULTS" in title.upper():
            dialog.set_default_size(700, 500)
        else:
            dialog.set_default_size(500, 400)
        
        content_area = dialog.get_content_area()

        # 📜 Create scrollable text area
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)

        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.add_css_class("results-text")  # 🎨 Apply monospace font
        
        buffer = textview.get_buffer()
        buffer.set_text(content)

        scrolled_window.set_child(textview)
        content_area.append(scrolled_window)
        
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()

# 🎬 Main program entry point
if __name__ == '__main__':
    # 🚀 Create and run our race timing GUI app
    app = RaceTimingApp()
    app.run()