#!/usr/bin/env python3
# race_timing_gui.py
# MIT License - TJ Tryon, Midwest Event Services, 2025
# Version 0.91 - Stable Release

"""
The Race Timing Solution (TRTS) - Version 0.91
===============================================
This GTK 4 Python application helps manage cross-country and road race events.

What this program does:
- Keeps track of runners in a race
- Records when the race starts and when each runner finishes
- Calculates who won and which teams did best
- Saves all the information so you can look at it later

Think of it like a digital stopwatch and scorebook combined!

TODO - Future Enhancements:
===========================
□ Support for RFID
  - Add RFID reader integration for automatic finish time detection
  - Support multiple RFID reader protocols (EM4100, Mifare, etc.)
  - Automatic bib number lookup from RFID chip data
  - Backup manual entry when RFID fails
  - RFID chip programming interface for race setup

□ Flask App Integration
  - Create REST API endpoints for race data
  - Real-time web dashboard for live race results
  - Mobile-friendly interface for coaches and spectators
  - Export race data to web formats
  - Synchronize with cloud-based race management systems

□ Further Styling Enhancements
  - Custom color themes (light/dark mode)
  - Enhanced visual feedback for button states
  - Progress bars for long operations (CSV loading, etc.)
  - Custom icons for all buttons and functions
  - Improved spacing and layout optimization
  - Professional splash screen on startup

□ Packaging for End User Install
  - Create installer for Windows (.msi)
  - Create installer for macOS (.dmg)
  - Create installer for Linux (.deb/.rpm)
  - Bundle all dependencies (GTK4, Python, etc.)
  - Desktop shortcuts and file associations
  - Auto-update mechanism for future versions

□ Instructions Button
  - Add comprehensive user manual interface
  - Step-by-step race setup wizard
  - Video tutorials integration
  - Troubleshooting guide
  - Quick reference cards for common tasks
  - Context-sensitive help system
"""

# Import libraries - these are pre-made tools that help us build the program
import os           # Helps us work with files and folders
import sqlite3      # Helps us save data in a database (like a digital filing cabinet)
import datetime     # Helps us work with dates and times
import csv          # Helps us read spreadsheet files
import gi           # Helps us build the windows and buttons

# Tell the computer we want to use GTK version 4 for making windows
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")  # Also need Gdk for styling
from gi.repository import Gtk, Gio, GLib, Gdk

# Figure out where to save our race data
# Since script is run as: python gui/race_timing_gui.py
# We need to find the main folder that contains both 'gui' and 'data' folders
PROJECT_ROOT = os.getcwd()  # This gets the folder we're running the program from
DATA_DIR = os.path.join(PROJECT_ROOT, "data")  # This is where we save race data
CONFIG_DB = os.path.join(DATA_DIR, "config.db")  # This saves admin login info

class RaceTimingApp(Gtk.Application):
    """
    This is our main program class - think of it as the brain of our race timing app.
    It controls everything: windows, buttons, saving data, and timing races.
    """
    
    def __init__(self):
        """
        This runs when we first create our app.
        It sets up empty variables that we'll fill in later.
        """
        super().__init__(application_id="org.midwest.RaceTimingGUI")
        self.main_window = None     # The main window (starts empty)
        self.conn = None           # Database connection (starts empty)
        self.db_path = None        # Where our race database is saved (starts empty)
        self.title_label = None    # The text that shows which database is loaded
        self.start_race_button = None  # Reference to start race button for enabling/disabling
        self.individual_results_button = None  # Reference to individual results button
        self.team_results_button = None  # Reference to team results button
        self.view_runners_button = None  # Reference to view all runners button
        self.load_csv_button = None  # Reference to load CSV button
        
        # Set up consistent font styling for the entire application
        self.setup_application_styling()
    
    def setup_application_styling(self):
        """
        This sets up consistent Space Mono font styling for the entire application.
        All windows, buttons, text, and dialogs will use this monospace font for perfect alignment.
        """
        # Create CSS provider for consistent styling
        css_provider = Gtk.CssProvider()
        
    def setup_application_styling(self):
        """
        This sets up dual font styling for the application:
        - Garamond 15px for general interface (buttons, labels, dialogs)
        - Space Mono 11pt for data displays (results and runner lists)
        """
        # Create CSS provider for consistent styling
        css_provider = Gtk.CssProvider()
        
        # Define CSS styles with dual font system
        css_data = """
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
        
        /* General interface uses Garamond 15px */
        * {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
        }
        
        window {
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
        
        headerbar {
            font-family: "Garamond", "EB Garamond", "Adobe Garamond Pro", "Times New Roman", serif;
            font-size: 15px;
        }
        
        /* Data displays use Space Mono 11pt for perfect alignment */
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
            # Load the CSS styling
            css_provider.load_from_data(css_data.encode())
            
            # Apply styling to the entire application
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        except Exception as e:
            print(f"Could not load custom styling: {e}")
            # Continue without custom styling if there's an error

    def do_activate(self):
        """
        This runs when our app starts up.
        It builds the main window and shows it on screen.
        """
        self.build_main_window()          # Create the main window with all buttons
        self.ensure_config_db()           # Make sure we have admin settings saved
        self.main_window.set_application(self)  # Connect window to our app
        self.main_window.present()        # Show the window on screen

    def build_main_window(self):
        """
        This creates our main window with all the buttons.
        Think of it like building a control panel for race timing.
        """
        # Create the main window with proper title and size
        self.main_window = Gtk.ApplicationWindow(title="The Race Timing Solution (TRTS)")
        self.main_window.set_default_size(400, 400)  # Make it 400 pixels wide, 400 tall
        
        # Set a running shoe icon for the window
        # This creates a simple running shoe icon using text (since we can't load image files easily)
        try:
            # Try to set a custom icon - this will show a running shoe emoji if supported
            self.main_window.set_icon_name("applications-sports")  # Sports/athletics icon
        except:
            # If that doesn't work, try a different approach
            try:
                self.main_window.set_icon_name("media-playback-start")  # Start/play icon as fallback
            except:
                pass  # Use default icon if nothing else works

        # Create a container to hold all our buttons vertically
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10,
                       margin_top=20, margin_bottom=20, margin_start=20, margin_end=20)

        # Create a label to show which database is currently loaded
        self.title_label = Gtk.Label(label="No database loaded")
        vbox.append(self.title_label)

        # Create all our buttons and connect them to functions
        # Each button has a name and tells the computer what to do when clicked
        buttons = [
            ("Create New Database", self.create_new_database),      # Make a new race
            ("Load CSV File to Database", self.load_csv_to_database), # Add runners from spreadsheet
            ("Load Existing Database", self.load_existing_database),  # Open old race
            ("View All Runners", self.view_all_runners),            # See who's racing
            ("Start the Race", self.start_race),                    # Begin timing
            ("List Individual Results", self.list_individual_results), # Show who won
            ("List Team Results", self.list_team_results),          # Show which teams won
            ("Instructions", self.show_instructions),               # Show user manual
            ("Exit", lambda b: self.quit()),                       # Close the program
        ]

        # Add each button to our window
        for label, handler in buttons:
            btn = Gtk.Button(label=label)  # Create the button
            btn.connect("clicked", handler)  # Tell it what to do when clicked
            
            # Keep references to buttons we want to enable/disable
            if label == "Start the Race":
                self.start_race_button = btn
                btn.set_sensitive(False)  # Start disabled until database with runners is loaded
            elif label == "Load CSV File to Database":
                self.load_csv_button = btn
                btn.set_sensitive(False)  # Start disabled until database is loaded
            elif label == "List Individual Results":
                self.individual_results_button = btn
                btn.set_sensitive(False)  # Start disabled until race has results
            elif label == "List Team Results":
                self.team_results_button = btn
                btn.set_sensitive(False)  # Start disabled until race has results
            elif label == "View All Runners":
                self.view_runners_button = btn
                btn.set_sensitive(False)  # Start disabled until database with runners is loaded
            
            vbox.append(btn)  # Add it to our container

        # Put our container of buttons into the main window
        self.main_window.set_child(vbox)

    def ensure_config_db(self):
        """
        This makes sure we have a place to save admin login information.
        If it's the first time running, it asks for admin username and password.
        """
        # Create the data folder if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Data directory: {DATA_DIR}")  # Show where we're saving data
        
        # Check if we already have admin settings saved
        if not os.path.exists(CONFIG_DB):
            # First time running - ask for admin info
            dialog = Gtk.Dialog(title="Admin Setup", transient_for=self.main_window, modal=True)
            dialog.set_transient_for(self.main_window)  # Make sure dialog stays on top
            box = dialog.get_content_area()
            
            # Create text boxes for username and password
            user = Gtk.Entry(placeholder_text="Admin Username")
            pw = Gtk.Entry(placeholder_text="Admin Password")
            pw.set_visibility(False)  # Hide password as you type
            
            # Add the text boxes to the dialog
            box.append(user)
            box.append(pw)
            
            # Add OK and Cancel buttons
            dialog.add_button("OK", Gtk.ResponseType.OK)
            dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
            dialog.show()

            def on_response(dlg, response):
                """
                This runs when user clicks OK or Cancel on the admin setup.
                """
                if response == Gtk.ResponseType.OK:
                    # User clicked OK - save their admin info
                    username = user.get_text()
                    password = pw.get_text()
                    
                    # Make sure they entered both username and password
                    if username and password:
                        try:
                            # Save admin info to database
                            with sqlite3.connect(CONFIG_DB) as conn:
                                # Create admin table if it doesn't exist
                                conn.execute("CREATE TABLE IF NOT EXISTS admin_users (username TEXT PRIMARY KEY, password TEXT NOT NULL)")
                                # Save the username and password
                                conn.execute("INSERT INTO admin_users (username, password) VALUES (?, ?)", (username, password))
                                print(f"Config database created: {CONFIG_DB}")
                        except sqlite3.Error as e:
                            # Something went wrong saving to database
                            self.show_error_dialog(f"Database error: {e}")
                    else:
                        # User didn't fill in both fields
                        self.show_error_dialog("Please enter both username and password.")
                
                # Close the dialog
                dlg.destroy()

            dialog.connect("response", on_response)

    def create_new_database(self, button):
        """
        This creates a brand new race database.
        It asks for a race number and race name, then creates a database file to store all race info.
        """
        # Create a dialog to ask for race number and race name
        dialog = Gtk.Dialog(title="Create New Race Database", transient_for=self.main_window, modal=True)
        dialog.set_transient_for(self.main_window)
        dialog.set_default_size(400, 200)
        box = dialog.get_content_area()
        
        # Create text boxes for race number and race name
        race_num_label = Gtk.Label(label="Race Number (e.g., 01):")
        race_num_label.set_halign(Gtk.Align.START)
        race_num_entry = Gtk.Entry(placeholder_text="Race number (e.g., 01)")
        
        race_name_label = Gtk.Label(label="Race Name/Location:")
        race_name_label.set_halign(Gtk.Align.START)
        race_name_entry = Gtk.Entry(placeholder_text="e.g., State Championship at Lincoln Park")
        
        # Add spacing and organization
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        box.append(race_num_label)
        box.append(race_num_entry)
        box.append(race_name_label)
        box.append(race_name_entry)
        
        # Add Cancel and OK buttons
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.show()

        def on_response(dlg, response):
            """
            This runs when user enters race information and clicks OK.
            """
            if response == Gtk.ResponseType.OK:
                # Get the race number and name they typed
                race_num = race_num_entry.get_text().strip().zfill(2)  # Make sure it's 2 digits (01, 02, etc.)
                race_name = race_name_entry.get_text().strip()
                
                # Make sure they entered both race number and name
                if race_num and race_num != "00" and race_name:
                    # Create database filename with today's date, race number, and race name
                    date_str = datetime.datetime.now().strftime("%Y%m%d")  # Like 20250722
                    
                    # Clean up race name for filename (remove special characters)
                    clean_race_name = "".join(c for c in race_name if c.isalnum() or c in (' ', '-', '_')).strip()
                    clean_race_name = clean_race_name.replace(' ', '_')  # Replace spaces with underscores
                    
                    # Create filename: YYYYMMDD-##-<name of meet>.db
                    db_name = f"{date_str}-{race_num}-{clean_race_name}.db"
                    self.db_path = os.path.join(DATA_DIR, db_name)
                    
                    try:
                        # Create the new database file
                        self.conn = sqlite3.connect(self.db_path)
                        
                        # Create a table to store runner information
                        # Think of this like creating column headers in a spreadsheet
                        self.conn.execute("""
                            CREATE TABLE IF NOT EXISTS runners (
                                bib INTEGER PRIMARY KEY,    -- Runner's number
                                full_name TEXT,            -- Runner's name  
                                team TEXT,                 -- What team they're on
                                rfid TEXT,                 -- Optional chip ID
                                start_time TEXT,           -- When race started
                                finish_time TEXT           -- When they finished
                            )
                        """)
                        
                        # Create enhanced config table to store comprehensive race information
                        self.conn.execute("""
                            CREATE TABLE IF NOT EXISTS race_config (
                                key TEXT PRIMARY KEY,      -- Configuration key
                                value TEXT                 -- Configuration value
                            )
                        """)
                        
                        # Create coaches table to store team and school information
                        self.conn.execute("""
                            CREATE TABLE IF NOT EXISTS coaches (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                team_name TEXT,            -- Team/school name
                                coach_name TEXT,           -- Coach's full name
                                coach_phone TEXT,          -- Coach's phone number
                                school_name TEXT,          -- Official school name
                                school_address TEXT,       -- School mailing address
                                school_phone TEXT,         -- School main phone
                                athletic_director TEXT,    -- Athletic director name
                                treasurer_name TEXT,       -- Secretary/accountant name
                                treasurer_phone TEXT,      -- Secretary/accountant phone
                                treasurer_address TEXT     -- Secretary/accountant address
                            )
                        """)
                        
                        # Store comprehensive race information in config table
                        race_date = datetime.datetime.now().strftime("%B %d, %Y")  # Like "July 22, 2025"
                        planned_start_time = ""  # Will be set when race is planned
                        
                        # Store all race configuration data
                        config_data = [
                            ("Race_Name", race_name),
                            ("Race_Number", race_num),
                            ("Meet_Name", race_name),  # Same as race name for now
                            ("Race_Date", race_date),
                            ("Race_Planned_Start_Time", planned_start_time),
                            ("Race_Actual_Start_Time", ""),  # Set when "Start Race" is clicked
                            ("Race_End_Time", ""),  # Set when timing window is closed
                            ("Database_Created", datetime.datetime.now().isoformat())
                        ]
                        
                        for key, value in config_data:
                            self.conn.execute("INSERT OR REPLACE INTO race_config (key, value) VALUES (?, ?)", (key, value))
                        
                        self.conn.commit()  # Save the changes
                        
                        # Update the title to show which database is loaded
                        self.title_label.set_label(f"Loaded: {db_name}")
                        print(f"Database created: {self.db_path}")
                        
                        # Check if we should enable start race button
                        self.update_start_race_button_state()
                        
                        # Check if we should enable load CSV button
                        self.update_load_csv_button_state()
                        
                        # Check if we should enable view runners button
                        self.update_view_runners_button_state()
                        
                        # Check if we should enable results buttons
                        self.update_results_buttons_state()
                        
                    except sqlite3.Error as e:
                        # Something went wrong creating the database
                        self.show_error_dialog(f"Database error: {e}")
                else:
                    # They didn't enter both required fields
                    self.show_error_dialog("Please enter both a valid race number and race name.")
            
            # Close the dialog
            dlg.destroy()

        dialog.connect("response", on_response)

    def load_csv_to_database(self, button):
        """
        This loads runner information from a CSV file (like Excel) into our race database.
        CSV files contain runner names, bib numbers, and team information.
        """
        # Make sure we have a database open first
        if not self.conn:
            self.show_error_dialog("There is no database loaded. Create a database or load an existing database.")
            return

        print(f"Opening file dialog using FileChooserDialog...")
        
        # Create a file picker dialog to choose CSV file
        file_dialog = Gtk.FileChooserDialog(
            title="Select CSV File",
            parent=self.main_window,
            action=Gtk.FileChooserAction.OPEN
        )
        
        # Add Cancel and Open buttons
        file_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        file_dialog.add_button("_Open", Gtk.ResponseType.ACCEPT)
        
        # Create a filter so we only see CSV files
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("CSV files")
        csv_filter.add_pattern("*.csv")  # Only show files ending in .csv
        file_dialog.add_filter(csv_filter)
        
        # Try to start in our data directory
        try:
            file_dialog.set_current_folder(Gio.File.new_for_path(DATA_DIR))
            print(f"Set current folder to: {DATA_DIR}")
        except Exception as e:
            print(f"Could not set folder: {e}")

        print("About to show FileChooserDialog...")
        
        def on_response(dialog, response):
            """
            This runs when user picks a CSV file and clicks Open.
            """
            print(f"Dialog response: {response}")
            if response == Gtk.ResponseType.ACCEPT:
                # User picked a file and clicked Open
                file = dialog.get_file()
                if file:
                    file_path = file.get_path()
                    print(f"Selected file: {file_path}")
                    # Process the CSV file
                    self.process_csv_file(file_path)
                else:
                    print("No file selected")
            # Close the file picker
            dialog.destroy()

        file_dialog.connect("response", on_response)
        file_dialog.show()
        print("FileChooserDialog shown")

    def process_csv_file(self, file_path):
        """
        This reads a CSV file and adds all the runner information to our database.
        CSV files are like spreadsheets with columns for bib, name, team, etc.
        """
        try:
            # Open and read the CSV file
            with open(file_path, newline="", encoding='utf-8') as csvfile:
                # Try to detect if file has headers
                sample = csvfile.read(1024)
                csvfile.seek(0)  # Go back to beginning
                
                # Create a CSV reader that treats first row as column names
                reader = csv.DictReader(csvfile)
                rows_processed = 0
                
                # Read each row (each runner) from the CSV
                for row in reader:
                    # Handle different possible column names (bib, Bib, BIB all work)
                    bib = row.get('bib') or row.get('Bib') or row.get('BIB')
                    full_name = row.get('full_name') or row.get('Full Name') or row.get('name') or row.get('Name')
                    team = row.get('team') or row.get('Team') or row.get('TEAM')
                    rfid = row.get('rfid', '') or row.get('RFID', '') or row.get('Rfid', '')
                    
                    # Make sure we have the essential information (bib, name, team)
                    if bib and full_name and team:
                        # Add this runner to our database
                        # INSERT OR REPLACE means if bib number already exists, update it
                        self.conn.execute("""
                            INSERT OR REPLACE INTO runners (bib, full_name, team, rfid)
                            VALUES (?, ?, ?, ?)
                        """, (int(bib), full_name, team, rfid))
                        rows_processed += 1
                
                # Save all changes to database
                self.conn.commit()
                
                # Show success message
                self.show_text_window("CSV Import", f"Successfully imported {rows_processed} runners from CSV file.")
                
                # Check if we should enable start race button now that runners are loaded
                self.update_start_race_button_state()
                
                # Check if we should enable view runners button now that runners are loaded
                self.update_view_runners_button_state()
                
                # Check if we should enable results buttons
                self.update_results_buttons_state()
                
        except (csv.Error, ValueError, sqlite3.Error) as e:
            # Something went wrong reading the file or saving to database
            self.show_error_dialog(f"Error processing CSV file: {e}")
        except FileNotFoundError:
            # File doesn't exist
            self.show_error_dialog("CSV file not found.")
        except Exception as e:
            # Something else went wrong
            self.show_error_dialog(f"Unexpected error: {e}")

    def load_existing_database(self, button):
        """
        This opens a race database that was created before.
        Useful for looking at old race results or continuing a race.
        """
        print(f"Opening database dialog using FileChooserDialog...")

        # Create file picker dialog to choose database file
        file_dialog = Gtk.FileChooserDialog(
            title="Open Existing Database",
            parent=self.main_window,
            action=Gtk.FileChooserAction.OPEN
        )
        
        # Add Cancel and Open buttons
        file_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        file_dialog.add_button("_Open", Gtk.ResponseType.ACCEPT)
        
        # Create filter to only show database files
        db_filter = Gtk.FileFilter()
        db_filter.set_name("Database files")
        db_filter.add_pattern("*.db")  # Only show files ending in .db
        file_dialog.add_filter(db_filter)

        # Try to start in our data directory
        try:
            file_dialog.set_current_folder(Gio.File.new_for_path(DATA_DIR))
            print(f"Set current folder to: {DATA_DIR}")
        except Exception as e:
            print(f"Could not set folder: {e}")

        print("About to show FileChooserDialog...")

        def on_response(dialog, response):
            """
            This runs when user picks a database file and clicks Open.
            """
            print(f"Dialog response: {response}")
            if response == Gtk.ResponseType.ACCEPT:
                # User picked a file and clicked Open
                file = dialog.get_file()
                if file:
                    db_path = file.get_path()
                    print(f"Selected database: {db_path}")
                    # Load the database
                    self.load_database(db_path)
                else:
                    print("No file selected")
            # Close the file picker
            dialog.destroy()

        file_dialog.connect("response", on_response)
        file_dialog.show()
        print("FileChooserDialog shown")

    def load_database(self, db_path):
        """
        This actually opens a database file and connects to it.
        It also checks that the database has the right structure.
        """
        try:
            # Test if the database file is valid by trying to open it
            test_conn = sqlite3.connect(db_path)
            
            # Check if it has a 'runners' table (required for race timing)
            cursor = test_conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='runners'")
            if not cursor.fetchone():
                # Database doesn't have runners table - not a valid race database
                test_conn.close()
                self.show_error_dialog("Invalid database file: missing 'runners' table.")
                return
            test_conn.close()
            
            # Close existing database connection if we have one
            if self.conn:
                self.conn.close()
            
            # Connect to the selected database
            self.db_path = db_path
            self.conn = sqlite3.connect(self.db_path)
            
            # Update title to show which database is loaded
            self.title_label.set_label(f"Loaded: {os.path.basename(self.db_path)}")
            
            # Check if we should enable start race button
            self.update_start_race_button_state()
            
            # Check if we should enable load CSV button
            self.update_load_csv_button_state()
            
            # Check if we should enable view runners button
            self.update_view_runners_button_state()
            
            # Check if we should enable results buttons
            self.update_results_buttons_state()
            
        except sqlite3.Error as e:
            # Something went wrong with the database
            self.show_error_dialog(f"Database error: {e}")

    def update_start_race_button_state(self):
        """
        This checks if we have a database loaded with runners and enables/disables 
        the Start Race button accordingly.
        """
        # Default to disabled
        should_enable = False
        
        # Check if we have a database connection and runners loaded
        if self.conn and self.start_race_button:
            try:
                # Check if there are any runners in the database
                cursor = self.conn.execute("SELECT COUNT(*) FROM runners")
                runner_count = cursor.fetchone()[0]
                
                # Enable button only if we have runners
                should_enable = runner_count > 0
                
            except sqlite3.Error:
                # If there's an error checking, keep button disabled
                should_enable = False
        
        # Update button state
        if self.start_race_button:
            self.start_race_button.set_sensitive(should_enable)
            
            # Update button appearance to show why it's disabled
            if not should_enable:
                if not self.conn:
                    self.start_race_button.set_tooltip_text("Load a database first")
                else:
                    self.start_race_button.set_tooltip_text("Load runners from CSV file first")
            else:
                self.start_race_button.set_tooltip_text("Click to start the race timing")

    def update_load_csv_button_state(self):
        """
        This checks if we have a database loaded and enables/disables 
        the Load CSV button accordingly.
        """
        # Default to disabled
        should_enable = False
        
        # Check if we have a database connection
        if self.conn and self.load_csv_button:
            should_enable = True  # Enable if we have any database connection
        
        # Update button state
        if self.load_csv_button:
            self.load_csv_button.set_sensitive(should_enable)
            
            # Update button appearance to show why it's disabled
            if not should_enable:
                self.load_csv_button.set_tooltip_text("Create or load a database first")
            else:
                self.load_csv_button.set_tooltip_text("Load runners from CSV file into database")

    def update_view_runners_button_state(self):
        """
        This checks if we have a database loaded with runners and enables/disables 
        the View All Runners button accordingly.
        """
        # Default to disabled
        should_enable = False
        
        # Check if we have a database connection and runners loaded
        if self.conn and self.view_runners_button:
            try:
                # Check if there are any runners in the database
                cursor = self.conn.execute("SELECT COUNT(*) FROM runners")
                runner_count = cursor.fetchone()[0]
                
                # Enable button only if we have runners
                should_enable = runner_count > 0
                
            except sqlite3.Error:
                # If there's an error checking, keep button disabled
                should_enable = False
        
        # Update button state
        if self.view_runners_button:
            self.view_runners_button.set_sensitive(should_enable)
            
            # Update button appearance to show why it's disabled
            if not should_enable:
                if not self.conn:
                    self.view_runners_button.set_tooltip_text("Load a database first")
                else:
                    self.view_runners_button.set_tooltip_text("Load runners from CSV file first")
            else:
                self.view_runners_button.set_tooltip_text("View all registered runners")

    def update_results_buttons_state(self):
        """
        This checks if we have race results available and enables/disables 
        the results buttons accordingly.
        """
        # Default to disabled
        should_enable = False
        
        # Check if we have a database connection and finished runners
        if self.conn:
            try:
                # Check if there are any runners with both start and finish times (completed race)
                cursor = self.conn.execute("SELECT COUNT(*) FROM runners WHERE start_time IS NOT NULL AND finish_time IS NOT NULL")
                finished_runners = cursor.fetchone()[0]
                
                # Enable buttons only if we have finished runners
                should_enable = finished_runners > 0
                
            except sqlite3.Error:
                # If there's an error checking, keep buttons disabled
                should_enable = False
        
        # Update both results buttons
        if self.individual_results_button:
            self.individual_results_button.set_sensitive(should_enable)
            if not should_enable:
                if not self.conn:
                    self.individual_results_button.set_tooltip_text("Load a database with race results first")
                else:
                    self.individual_results_button.set_tooltip_text("Complete a race to see individual results")
            else:
                self.individual_results_button.set_tooltip_text("View individual race results")
        
        if self.team_results_button:
            self.team_results_button.set_sensitive(should_enable)
            if not should_enable:
                if not self.conn:
                    self.team_results_button.set_tooltip_text("Load a database with race results first")
                else:
                    self.team_results_button.set_tooltip_text("Complete a race to see team results")
            else:
                self.team_results_button.set_tooltip_text("View team race results")

    def view_all_runners(self, button):
        """
        This shows a list of all runners who are registered for the race.
        It displays their bib number, name, and team.
        """
        # Make sure we have a database loaded
        if not self.conn:
            self.show_text_window("All Runners", "No database loaded.")
            return

        try:
            # Get all runners from database, sorted by bib number
            cursor = self.conn.execute("SELECT bib, full_name, team FROM runners ORDER BY bib")
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
            # Something went wrong reading from database
            self.show_text_window("All Runners", f"Database error: {e}")
            return

        # Check if we have any runners loaded
        if not rows:
            self.show_text_window("All Runners", "There are no runners loaded, please load a runners.csv file.")
            return

        # Build text to show all runners with fixed-width columns for 8.5x11 printing
        output = ""
        
        # Page formatting constants for 8.5x11 paper
        LINES_PER_PAGE = 55  # Lines that fit on 8.5x11 with margins
        LINE_WIDTH = 85      # Characters that fit across 8.5x11
        
        # Create page header function
        def create_page_header(page_num):
            header = ""
            header += "ALL REGISTERED RUNNERS\n"
            header += "=" * LINE_WIDTH + "\n"
            header += f"{'BIB':<8}{'RUNNER NAME':<37}{'TEAM':<30}Page {page_num}\n"
            header += "-" * LINE_WIDTH + "\n"
            return header
        
        # Start with first page
        current_page = 1
        lines_on_page = 0
        output += create_page_header(current_page)
        lines_on_page += 4  # Header takes 4 lines
        
        # Format each runner with pagination
        for bib, name, team in rows:
            # Check if we need a new page
            if lines_on_page >= LINES_PER_PAGE:
                current_page += 1
                output += "\n" + "=" * LINE_WIDTH + "\n"
                output += f"Page {current_page-1} of {((len(rows)-1)//LINES_PER_PAGE)+1}\n\n"
                output += create_page_header(current_page)
                lines_on_page = 4
            
            # Truncate long names/teams to fit exactly in columns
            name_display = name[:36] if len(name) > 36 else name
            team_display = team[:29] if len(team) > 29 else team
            output += f"{bib:<8}{name_display:<37}{team_display:<30}\n"
            lines_on_page += 1
        
        # Add final page footer
        total_pages = ((len(rows)-1)//LINES_PER_PAGE)+1 if rows else 1
        output += "\n" + "=" * LINE_WIDTH + "\n"
        output += f"Page {current_page} of {total_pages}\n"
        
        # Show the list in a window
        self.show_text_window("All Runners", output)

    def start_race(self, button):
        """
        This starts the race timing system.
        It records the start time and opens a special timing window.
        """
        # Make sure we have a database loaded
        if not self.conn:
            self.show_text_window("Start Race", "No database loaded.")
            return

        # Record the current time as race start time
        now = datetime.datetime.now().isoformat()  # Gets current date and time
        try:
            # Set start time for all runners in the database
            self.conn.execute("UPDATE runners SET start_time = ?", (now,))
            
            # Record the actual race start time in config
            self.conn.execute("INSERT OR REPLACE INTO race_config (key, value) VALUES (?, ?)", ("Race_Actual_Start_Time", now))
            
            self.conn.commit()  # Save the changes
            
            # Open the special race timing window
            self.open_race_timing_window(now)
            
            # After starting race, update results buttons (they might become available after race completion)
            self.update_results_buttons_state()
            
        except sqlite3.Error as e:
            # Something went wrong with database
            self.show_error_dialog(f"Database error: {e}")

    def open_race_timing_window(self, start_time):
        """
        This creates a special window for timing the race.
        It has a big timer, a place to enter bib numbers, and shows results as they come in.
        """
        # Create race timing window with proper title
        timing_window = Gtk.Window(title="The Race Timing Solution (TRTS) - Race IN PROGRESS")
        timing_window.set_default_size(500, 400)
        timing_window.set_transient_for(self.main_window)  # Stay on top of main window
        timing_window.set_modal(True)  # Must deal with this window first
        
        # Create container to hold everything vertically
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10,
                       margin_top=20, margin_bottom=20, margin_start=20, margin_end=20)
        
        # Create big timer display
        timer_label = Gtk.Label()
        timer_label.set_markup("<span size='24000' weight='bold'>00:00:00.000</span>")
        vbox.append(timer_label)
        
        # Show when race started
        start_label = Gtk.Label(label=f"Race started: {start_time}")
        vbox.append(start_label)
        
        # Add a line to separate sections
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.append(separator)
        
        # Add instructions for using the timing system
        instructions = Gtk.Label()
        instructions.set_markup(
            "<b>Instructions:</b>\n"
            "• Enter bib number and press Enter to record finish time\n"
            "• Press Enter with no bib to record time for bib #0 (to fix later)\n"
            "• Type 'exit' and press Enter to stop timing"
        )
        instructions.set_justify(Gtk.Justification.LEFT)
        vbox.append(instructions)
        
        # Create text box for entering bib numbers
        bib_entry = Gtk.Entry(placeholder_text="Enter bib number or 'exit'")
        vbox.append(bib_entry)
        
        # Create area to show results as they come in
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        
        # Create text area for showing finish times
        results_textview = Gtk.TextView()
        results_textview.set_editable(False)  # User can't type in it
        results_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        results_buffer = results_textview.get_buffer()
        results_buffer.set_text("Finish times will appear here...\n")
        
        scrolled_window.set_child(results_textview)
        vbox.append(scrolled_window)
        
        timing_window.set_child(vbox)
        
        # Convert start time to datetime object for calculations
        start_datetime = datetime.datetime.fromisoformat(start_time)
        finish_count = 0  # Keep track of how many runners have finished
        
        def update_timer():
            """
            This function runs every 100 milliseconds to update the race timer.
            It calculates how much time has passed since the race started.
            """
            current_time = datetime.datetime.now()  # Get current time
            elapsed = current_time - start_datetime  # Calculate time since race started
            
            # Convert elapsed time to hours:minutes:seconds.milliseconds format
            total_seconds = elapsed.total_seconds()
            hours = int(total_seconds // 3600)           # How many full hours
            minutes = int((total_seconds % 3600) // 60)  # How many full minutes left
            seconds = total_seconds % 60                 # Remaining seconds and fractions
            
            # Format as HH:MM:SS.mmm (like 01:23:45.678)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
            timer_label.set_markup(f"<span size='24000' weight='bold'>{time_str}</span>")
            
            return True  # Tell system to keep calling this function
        
        # Start the timer update (calls update_timer every 100ms)
        timer_id = GLib.timeout_add(100, update_timer)
        
        def on_bib_entry_activate(entry):
            """
            This runs when someone types in the bib entry box and presses Enter.
            It records the finish time for that runner.
            """
            nonlocal finish_count  # We need to modify the finish_count variable
            
            # Get what the user typed and remove extra spaces
            bib_text = entry.get_text().strip()
            entry.set_text("")  # Clear the text box for next entry
            
            # Check if user typed 'exit' to stop timing
            if bib_text.lower() == 'exit':
                # Record when race timing ended
                try:
                    race_end_time = datetime.datetime.now().isoformat()
                    self.conn.execute("INSERT OR REPLACE INTO race_config (key, value) VALUES (?, ?)", ("Race_End_Time", race_end_time))
                    self.conn.commit()
                except sqlite3.Error as e:
                    print(f"Error recording race end time: {e}")
                
                GLib.source_remove(timer_id)  # Stop updating the timer
                timing_window.destroy()        # Close the timing window
                return
            
            # Record the exact time this runner finished
            finish_time = datetime.datetime.now().isoformat()
            finish_count += 1  # One more runner has finished
            
            # Figure out what bib number to use
            if bib_text == "":
                # Nothing entered - use bib 0 (to fix later)
                bib_number = 0
            else:
                try:
                    # Try to convert typed text to a number
                    bib_number = int(bib_text)
                except ValueError:
                    # Couldn't convert to number - use bib 0
                    bib_number = 0
            
            # Save finish time to database
            try:
                # Look up this runner's information
                cursor = self.conn.execute("SELECT full_name FROM runners WHERE bib = ?", (bib_number,))
                runner_data = cursor.fetchone()
                
                if runner_data or bib_number == 0:
                    # Runner found (or using bib 0) - update their finish time
                    self.conn.execute("UPDATE runners SET finish_time = ? WHERE bib = ?", (finish_time, bib_number))
                    self.conn.commit()  # Save to database
                    
                    # Calculate how long this runner took to finish
                    elapsed_seconds = (datetime.datetime.fromisoformat(finish_time) - start_datetime).total_seconds()
                    elapsed_display = self.elapsed_time_for_display(elapsed_seconds)
                    
                    # Create text to show in results area
                    runner_name = runner_data[0] if runner_data else "UNKNOWN - FIX LATER"
                    result_text = f"{finish_count:3d}. Bib {bib_number:3d} - {runner_name} - {elapsed_display}\n"
                    
                    # Add this result to the display
                    end_iter = results_buffer.get_end_iter()
                    results_buffer.insert(end_iter, result_text)
                    
                    # Scroll to bottom so newest results are visible
                    mark = results_buffer.get_insert()
                    results_textview.scroll_mark_onscreen(mark)
                    
                    # Update results buttons since we now have finish times
                    self.update_results_buttons_state()
                    
                else:
                    # Bib number not found - still record it as bib 0 for later fixing
                    self.conn.execute("UPDATE runners SET finish_time = ? WHERE bib = ?", (finish_time, 0))
                    self.conn.commit()
                    
                    # Calculate elapsed time
                    elapsed_seconds = (datetime.datetime.fromisoformat(finish_time) - start_datetime).total_seconds()
                    elapsed_display = self.elapsed_time_for_display(elapsed_seconds)
                    
                    # Show that bib wasn't found
                    result_text = f"{finish_count:3d}. Bib {bib_text} NOT FOUND - Recorded as Bib 0 - {elapsed_display}\n"
                    end_iter = results_buffer.get_end_iter()
                    results_buffer.insert(end_iter, result_text)
                    
                    # Scroll to show newest result
                    mark = results_buffer.get_insert()
                    results_textview.scroll_mark_onscreen(mark)
                    
                    # Update results buttons since we now have finish times
                    self.update_results_buttons_state()
                    
            except sqlite3.Error as e:
                # Something went wrong with database
                print(f"Database error: {e}")
        
        # Connect the bib entry box to our function
        bib_entry.connect("activate", on_bib_entry_activate)
        
        def on_window_close(window):
            """
            This runs if user closes the timing window.
            It stops the timer and records the race end time.
            """
            # Record when race timing ended
            try:
                race_end_time = datetime.datetime.now().isoformat()
                self.conn.execute("INSERT OR REPLACE INTO race_config (key, value) VALUES (?, ?)", ("Race_End_Time", race_end_time))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error recording race end time: {e}")
            
            GLib.source_remove(timer_id)  # Stop the timer updates
            return False
        
        # Connect window close to our function
        timing_window.connect("close-request", on_window_close)
        
        # Show the timing window and focus on bib entry
        timing_window.present()
        bib_entry.grab_focus()  # Put cursor in bib entry box

    def format_elapsed_time(self, total_seconds):
        """
        This converts seconds into a nice time format like 01:23:45.678
        Used for showing how long each runner took to finish.
        """
        hours = int(total_seconds // 3600)           # How many full hours
        minutes = int((total_seconds % 3600) // 60)  # How many full minutes left  
        seconds = total_seconds % 60                 # Remaining seconds and fractions
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

    def list_individual_results(self, button):
        """
        This shows race results for individual runners.
        It lists runners in order from fastest to slowest with proper print formatting.
        """
        # Make sure we have a database loaded
        if not self.conn:
            self.show_text_window("Individual Results", "No database loaded.")
            return

        try:
            # Get all runners who have both start and finish times
            cursor = self.conn.execute("SELECT bib, full_name, start_time, finish_time FROM runners WHERE start_time IS NOT NULL AND finish_time IS NOT NULL")
            runners = cursor.fetchall()
        except sqlite3.Error as e:
            # Something went wrong with database
            self.show_error_dialog(f"Database error: {e}")
            return

        # Check if any runners have finished
        if not runners:
            self.show_text_window("Individual Results", "There are no times in the database, has the race been completed?")
            return

        # Get race information from config table
        race_name = "Unknown Race"
        race_date = datetime.datetime.now().strftime("%B %d, %Y")
        try:
            cursor = self.conn.execute("SELECT value FROM race_config WHERE key = ?", ("Race_Name",))
            result = cursor.fetchone()
            if result:
                race_name = result[0]
            
            cursor = self.conn.execute("SELECT value FROM race_config WHERE key = ?", ("Race_Date",))
            result = cursor.fetchone()
            if result:
                race_date = result[0]
        except sqlite3.Error:
            # Config table might not exist in older databases
            pass

        # Sort runners by their finish time (fastest first)
        # elapsed_seconds calculates how long each runner took to finish
        runners.sort(key=lambda r: self.elapsed_seconds(r[2], r[3]))
        
        # Build formatted results for 8.5x11 printing with pagination
        output = ""
        
        # Page formatting constants for 8.5x11 paper
        LINES_PER_PAGE = 50  # Lines that fit on 8.5x11 with margins and headers
        LINE_WIDTH = 85      # Characters that fit across 8.5x11
        
        # Create page header function
        def create_page_header(page_num):
            header = ""
            # Header Line 1 (L1 style - main title)
            header += "THE RACE TIMING SOLUTION (TRTS) - BY MIDWEST EVENT SERVICES, INC.\n"
            # Header Line 2 (L2 style - race details)
            header += f"{race_name} - {race_date}\n\n"
            # Column headers
            header += "INDIVIDUAL RESULTS\n"
            header += "=" * LINE_WIDTH + "\n"
            header += f"{'POS':<8}{'BIB':<8}{'RUNNER NAME':<37}{'TEAM':<22}{'TIME':<10}Page {page_num}\n"
            header += "-" * LINE_WIDTH + "\n"
            return header
        
        # Start with first page
        current_page = 1
        lines_on_page = 0
        output += create_page_header(current_page)
        lines_on_page += 7  # Header takes 7 lines
        
        # List all results with pagination
        for position, r in enumerate(runners, 1):
            # Check if we need a new page
            if lines_on_page >= LINES_PER_PAGE:
                current_page += 1
                total_pages = ((len(runners)-1)//(LINES_PER_PAGE-7))+1
                output += "\n" + "=" * LINE_WIDTH + "\n"
                output += f"Page {current_page-1} of {total_pages}\n\n"
                output += create_page_header(current_page)
                lines_on_page = 7
            
            # Calculate how long this runner took
            elapsed = self.elapsed_time(r[2], r[3])
            
            # Format with exact column widths for 8.5x11
            name_display = r[1][:36] if len(r[1]) > 36 else r[1]
            
            # Get team name from database
            try:
                team_cursor = self.conn.execute("SELECT team FROM runners WHERE bib = ?", (r[0],))
                team_result = team_cursor.fetchone()
                team = team_result[0] if team_result else ""
                team_display = team[:21] if len(team) > 21 else team
            except:
                team_display = ""
            
            output += f"{position:<8}{r[0]:<8}{name_display:<37}{team_display:<22}{elapsed:<10}\n"
            lines_on_page += 1
        
        # Add final page footer
        total_pages = ((len(runners)-1)//(LINES_PER_PAGE-7))+1 if runners else 1
        output += "\n" + "=" * LINE_WIDTH + "\n"
        output += f"Generated: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
        output += f"Page {current_page} of {total_pages}\n"
        
        # Show the results in a window
        self.show_text_window("Individual Results", output)

    def list_team_results(self, button):
        """
        This shows team results for the race.
        In cross country, teams score by adding up the finish positions of their top 5 runners.
        The team with the LOWEST score wins (like golf).
        """
        # Make sure we have a database loaded
        if not self.conn:
            self.show_text_window("Team Results", "No database loaded.")
            return

        try:
            # Get all runners who finished the race
            cursor = self.conn.execute("SELECT bib, full_name, team, start_time, finish_time FROM runners WHERE start_time IS NOT NULL AND finish_time IS NOT NULL")
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            # Something went wrong with database
            self.show_error_dialog(f"Database error: {e}")
            return

        # Check if any runners have finished
        if not rows:
            self.show_text_window("Team Results", "There are no times in the database, has the race been completed?")
            return

        # Get race information from config table
        race_name = "Unknown Race"
        race_date = datetime.datetime.now().strftime("%B %d, %Y")
        try:
            cursor = self.conn.execute("SELECT value FROM race_config WHERE key = ?", ("Race_Name",))
            result = cursor.fetchone()
            if result:
                race_name = result[0]
            
            cursor = self.conn.execute("SELECT value FROM race_config WHERE key = ?", ("Race_Date",))
            result = cursor.fetchone()
            if result:
                race_date = result[0]
        except sqlite3.Error:
            # Config table might not exist in older databases
            pass

        # Sort all runners by finish time (fastest to slowest)
        # This gives us the overall finish positions (1st place, 2nd place, etc.)
        rows.sort(key=lambda r: self.elapsed_seconds(r[3], r[4]))
        
        # Group runners by team and assign finish positions
        teams = {}
        for idx, r in enumerate(rows):
            team = r[2]  # Team name
            if team not in teams:
                teams[team] = []
            # Store: (overall finish position, runner data)
            teams[team].append((idx + 1, r))

        # Calculate team scores (only for teams with at least 5 finishers)
        scored_teams = []
        for team, runners in teams.items():
            if len(runners) >= 5:
                # Team score = sum of top 5 runners' finish positions
                # In cross country: 1st + 3rd + 5th + 8th + 10th = 27 points
                score = sum(pos for pos, _ in runners[:5])
                scored_teams.append((score, team, runners))

        # Sort teams by score (lowest score wins)
        scored_teams.sort()
        
        # Build the formatted results with fixed-width columns
        output = ""
        
        # Header Line 1 (L1 style - main title)
        output += "THE RACE TIMING SOLUTION (TRTS) - BY MIDWEST EVENT SERVICES, INC.\n"
        
        # Header Line 2 (L2 style - race details)
        output += f"{race_name} - {race_date}\n"
        
        # Blank line for spacing
        output += "\n"
        
        # Main section header
        output += "TEAM RESULTS\n"
        output += "=" * 75 + "\n\n"
        
        for score, team, runners in scored_teams:
            # Team header with name and score (bold and underlined effect using text)
            output += f"**{team}**\n"  # Bold effect with asterisks
            output += f"__Team Score: {score}__\n"  # Underlined effect with underscores
            output += "=" * 55 + "\n"
            output += f"{'POS':<6}{'BIB':<6}{'RUNNER NAME':<30}{'TIME':<13}\n"
            output += "-" * 55 + "\n"
            
            # Show the 5 scoring runners with fixed-width formatting
            for i, (pos, r) in enumerate(runners[:5]):
                elapsed = self.elapsed_time(r[3], r[4])
                name_display = r[1][:29] if len(r[1]) > 29 else r[1]
                output += f"{pos:<6}{r[0]:<6}{name_display:<30}{elapsed:<13}\n"
            
            # Show displacers (6th and 7th runners) if they exist
            displacers = runners[5:7]  # Get runners 6 and 7 (if they exist)
            if displacers:
                output += "\nDisplacers:\n"
                output += "-" * 55 + "\n"
                for pos, r in displacers:
                    elapsed = self.elapsed_time(r[3], r[4])
                    name_display = r[1][:29] if len(r[1]) > 29 else r[1]
                    output += f"{pos:<6}{r[0]:<6}{name_display:<30}{elapsed:<13}\n"
            
            # Add blank lines between teams
            output += "\n\n"
        
        # Add page footer
        output += "-" * 75 + "\n"
        output += f"Generated: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        output += f"{' ' * 25}Page 1 of 1\n"
        
        # Show the results
        self.show_text_window("Team Results", output)

    def show_instructions(self, button):
        """
        This shows comprehensive instructions for using the race timing application.
        Provides step-by-step guidance for all major functions.
        """
        instructions_text = """
THE RACE TIMING SOLUTION (TRTS) - USER INSTRUCTIONS
===================================================

GETTING STARTED:
================
1. Create New Database
   • Click "Create New Database"
   • Enter race number (01, 02, etc.)
   • Enter race name/location (e.g., "State Championship at Lincoln Park")
   • Database file will be saved with format: YYYYMMDD-##-Race_Name.db

2. Load Runner Data
   • Click "Load CSV File to Database"
   • Select your runners.csv file
   • CSV should have columns: bib, full_name, team (and optionally rfid)
   • Program handles various column name formats (bib/Bib/BIB, etc.)

RACE DAY OPERATIONS:
===================
3. Review Runners
   • Click "View All Runners" to see loaded participants
   • Verify all teams and runners are present

4. Start Race Timing
   • Click "Start the Race" when ready to begin
   • Live timing window opens with running clock
   • Enter bib numbers as runners finish and press Enter
   • Press Enter with no bib to record time as bib #0 (fix later)
   • Type "exit" and press Enter to stop timing

RESULTS GENERATION:
==================
5. Individual Results
   • Click "List Individual Results" after race completion
   • Shows runners in finish order with times
   • Formatted for printing on 8.5x11 paper

6. Team Results
   • Click "List Team Results" for team scoring
   • Cross country scoring: sum of top 5 positions
   • Shows scoring runners and displacers
   • Teams ranked by lowest score (best)

DATABASE MANAGEMENT:
===================
7. Load Existing Database
   • Click "Load Existing Database" to open previous races
   • Select .db file to continue working with past events

TROUBLESHOOTING:
===============
• Buttons are grayed out until prerequisites are met
• "Start Race" requires database with runners loaded
• "Results" buttons require completed race with finish times
• CSV import handles missing or incorrectly named columns
• Race timing continues even if window is minimized

SUPPORT:
========
For technical support, contact Midwest Event Services, Inc.
All race data is automatically saved and backed up in database files.

VERSION: 0.91 - Stable Release
"""
        
        self.show_text_window("Instructions - User Manual", instructions_text)

    def elapsed_seconds(self, start, end):
        """
        This calculates how many seconds passed between start and finish times.
        Used for sorting runners by their finish times.
        """
        try:
            # Convert text times back to datetime objects
            s = datetime.datetime.fromisoformat(start)
            e = datetime.datetime.fromisoformat(end)
            # Calculate difference and return total seconds
            return (e - s).total_seconds()
        except ValueError:
            # If times are invalid, return 0 so sorting still works
            return 0

    def elapsed_time_for_display(self, total_seconds):
        """
        This converts seconds into a display format without unnecessary hours.
        Shows time like "23:45.678" (minutes:seconds.milliseconds) for races under 1 hour
        or "01:23:45.678" (hours:minutes:seconds.milliseconds) for longer races.
        """
        hours = int(total_seconds // 3600)           # How many full hours
        minutes = int((total_seconds % 3600) // 60)  # How many full minutes left  
        seconds = total_seconds % 60                 # Remaining seconds and fractions
        
        # Format based on whether there are hours or not
        if hours > 0:
            # Show hours if race lasted over 1 hour
            return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
        else:
            # Skip hours for typical cross country races (under 1 hour)
            return f"{minutes:02d}:{seconds:06.3f}"

    def elapsed_time(self, start, end):
        """
        This converts start and finish times into a nice display format.
        Shows time like "01:23:45.678" (hours:minutes:seconds.milliseconds)
        """
        # Get total seconds between start and finish
        seconds = self.elapsed_seconds(start, end)
        
        # Break it down into hours, minutes, and seconds
        mins, secs = divmod(seconds, 60)        # Split seconds into minutes and leftover seconds
        hrs, mins = divmod(int(mins), 60)       # Split minutes into hours and leftover minutes
        
        # Format as HH:MM:SS.mmm
        return f"{int(hrs):02}:{int(mins):02}:{secs:06.3f}"

    def show_error_dialog(self, message):
        """
        This shows an error message to the user in a popup window.
        Used when something goes wrong (like database errors).
        """
        # Create a simple dialog to show error messages
        dialog = Gtk.Dialog(title="Error", transient_for=self.main_window, modal=True)
        dialog.set_transient_for(self.main_window)  # Make sure it stays on top
        dialog.set_default_size(400, 150)
        
        # Get the content area and add our error message
        content_area = dialog.get_content_area()
        
        # Create a label with the error message using consistent styling
        error_label = Gtk.Label(label=message)
        error_label.set_wrap(True)  # Allow text to wrap if it's long
        error_label.set_margin_top(20)
        error_label.set_margin_bottom(20)
        error_label.set_margin_start(20)
        error_label.set_margin_end(20)
        
        # Apply consistent styling (Garamond font will be applied via CSS)
        error_label.add_css_class("dialog-text")
        
        content_area.append(error_label)
        
        # Add an OK button (Garamond font will be applied via CSS)
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.connect("response", lambda d, r: d.destroy())  # Close when OK clicked
        dialog.show()

    def show_text_window(self, title, content):
        """
        This shows text content (like results or runner lists) in a scrollable window.
        Used for displaying race results, runner lists, etc.
        Window size adapts based on content type.
        """
        # Create a dialog window to show the text
        dialog = Gtk.Dialog(title=title, transient_for=self.main_window, modal=True)
        dialog.set_transient_for(self.main_window)  # Keep on top of main window
        
        # Set window size based on content type and length
        if "No database loaded" in content or "no runners loaded" in content or "no times in the database" in content:
            # Small window for error/info messages
            dialog.set_default_size(400, 150)
        elif "Successfully imported" in content:
            # Small window for success messages
            dialog.set_default_size(350, 120)
        elif title == "All Runners":
            # Narrow window for runner lists (remove extra whitespace)
            dialog.set_default_size(450, 400)
        elif title in ["Individual Results", "Team Results"]:
            # Wide window for results that might have long content
            dialog.set_default_size(600, 450)
        else:
            # Default size for other content
            dialog.set_default_size(500, 350)
        
        content_area = dialog.get_content_area()

        # Create a scrollable area in case there's lots of text
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)  # Can grow vertically
        scrolled_window.set_hexpand(True)  # Can grow horizontally

        # Create text area to display the content
        textview = Gtk.TextView()
        textview.set_editable(False)            # User can't change the text
        textview.set_wrap_mode(Gtk.WrapMode.WORD)  # Wrap long lines at word boundaries
        
        # Apply consistent styling (Garamond font will be applied via CSS)
        textview.add_css_class("results-text")
        
        buffer = textview.get_buffer()
        buffer.set_text(content)                # Put our text in the display area

        # Put the text area inside the scrollable area
        scrolled_window.set_child(textview)
        content_area.append(scrolled_window)
        
        # Add an OK button to close the window
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.connect("response", lambda d, r: d.destroy())  # Close when OK clicked
        dialog.show()

# This runs when the program starts
if __name__ == '__main__':
    # Create our race timing app and run it
    app = RaceTimingApp()
    app.run()