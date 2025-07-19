# race_timing_gui.py
# Author: TJ Tryon
# Date: July 17, 2025
# The Race Timing Solution - GTK 4 GUI

import gi
import os
import sys
from datetime import datetime
import sqlite3

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

# Add console directory to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "console")))
import race_timing_console as rtc

#class RaceTimingApp(Gtk.Application):
#    def __init__(self):
#        super().__init__(application_id="org.midwestservices.RaceTimingGUI")
#        self.builder = Gtk.Builder()
#        self.window = None

#    def do_activate(self, app):


class RaceTimingApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.midwestservices.RaceTimingGUI")

    def do_activate(self):
        # your GUI initialization hereI


        rtc.initialize_config_db()

        # Load the UI file
        ui_path = os.path.join(os.path.dirname(__file__), "ui.ui")
        self.builder.add_from_file(ui_path)

        # Manually connect signals
        self.builder.get_object("create_button").connect("clicked", self.on_create_clicked)
        self.builder.get_object("load_button").connect("clicked", self.on_load_clicked)
        self.builder.get_object("load_runners_button").connect("clicked", self.on_load_runners_clicked)
        self.builder.get_object("start_race_button").connect("clicked", self.on_start_race_clicked)
        self.builder.get_object("individual_results_button").connect("clicked", self.on_show_individual_clicked)
        self.builder.get_object("team_results_button").connect("clicked", self.on_show_team_clicked)
        self.builder.get_object("all_runners_button").connect("clicked", self.on_show_runners_clicked)
        self.builder.get_object("quit_button").connect("clicked", self.on_quit_clicked)

        # Set up main window
        self.window = self.builder.get_object("main_window")
        self.window.set_application(self)
        self.window.present()

    # === Button Handlers ===

    def on_create_clicked(self, button):
        dialog = Gtk.AlertDialog.new()
        dialog.set_title("Create New Database")
        dialog.set_modal(True)
        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter race number (e.g., 1)")
        dialog.set_child(entry)

        def on_response(dialog, response):
            if response == Gtk.ResponseType.OK:
                text = entry.get_text().strip()
                if text.isdigit():
                    rtc.create_race_database(int(text))
            dialog.destroy()

        dialog.add_button("Create", Gtk.ResponseType.OK)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.connect("response", on_response)
        dialog.show()

    def on_load_clicked(self, button):
        dialog = Gtk.FileChooserNative.new(
            "Select Race Database", self.window,
            Gtk.FileChooserAction.OPEN, "Open", "Cancel"
        )
        filter_db = Gtk.FileFilter()
        filter_db.set_name("SQLite DB Files")
        filter_db.add_pattern("*.db")
        dialog.add_filter(filter_db)

        def on_response(source, result):
            file = dialog.get_file()
            if file:
                rtc.DB_FILENAME = file.get_path()
                rtc.init_db(new_db=False)

        dialog.connect("response", on_response)
        dialog.show()

    def on_load_runners_clicked(self, button):
        dialog = Gtk.FileChooserNative.new(
            "Load Runners from CSV", self.window,
            Gtk.FileChooserAction.OPEN, "Load", "Cancel"
        )
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV Files")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        def on_response(source, result):
            file = dialog.get_file()
            if file:
                rtc.load_runners_from_csv(file.get_path())

        dialog.connect("response", on_response)
        dialog.show()

    def on_start_race_clicked(self, button):
        def ask_bib():
            dialog = Gtk.AlertDialog.new()
            dialog.set_title("Enter Bib Number")
            dialog.set_modal(True)
            entry = Gtk.Entry()
            entry.set_placeholder_text("Enter BIB or blank to finish")
            dialog.set_child(entry)

            def on_response(dialog, response):
                bib = entry.get_text().strip()
                dialog.destroy()
                if bib:
                    rtc.record_finish(bib)
                    ask_bib()  # Ask again

            dialog.add_button("OK", Gtk.ResponseType.OK)
            dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
            dialog.connect("response", on_response)
            dialog.show()

        ask_bib()

    def on_show_individual_clicked(self, button):
        content = rtc.get_individual_results()
        self.show_text_dialog("Individual Results", content)

    def on_show_team_clicked(self, button):
        content = rtc.get_team_results()
        self.show_text_dialog("Team Results", content)

    def on_show_runners_clicked(self, button):
        content = rtc.get_all_runners()
        self.show_text_dialog("All Runners", content)

    def on_quit_clicked(self, button):
        self.quit()

    def show_text_dialog(self, title, content):
        dialog = Gtk.Window.new()
        dialog.set_title(title)
        dialog.set_default_size(600, 400)

        scrolled = Gtk.ScrolledWindow()
        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.get_buffer().set_text(content)
        scrolled.set_child(textview)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.append(scrolled)

        close_button = Gtk.Button.new_with_label("Close")
        close_button.connect("clicked", lambda btn: dialog.close())
        box.append(close_button)

        dialog.set_child(box)
        dialog.present()


CONFIG_DB = os.path.join("data", "config.db")


def initialize_config_db():
    if not os.path.exists(CONFIG_DB):
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(CONFIG_DB)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)
        cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "password"))
        conn.commit()
        conn.close()
        print(f"Created new config database at {CONFIG_DB}")
    else:
        print(f"Config database already exists at {CONFIG_DB}")


if __name__ == "__main__":
    app = RaceTimingApp()
    app.run(sys.argv)
