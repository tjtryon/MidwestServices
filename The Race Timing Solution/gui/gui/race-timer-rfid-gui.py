import os
import sys
import time
import threading
import sqlite3
import datetime
import socketserver
import shutil
import queue

from gi.repository import Gtk, GLib
import cv2
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# ====== Config ======
DB_DATE = datetime.datetime.now().strftime("%Y%m%d")
DB_FILE = f"{DB_DATE}race.db"
BACKUP_DIR = "db_backups"
PHOTO_DIR = "photos"
RFID_INPUT_FILE = "rfid_input.txt"
TCP_PORT = 9999  # Change as needed

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)

# ====== Database Setup (SQLAlchemy ORM for Flask admin) ======
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)

class Runner(Base):
    __tablename__ = "runners"
    bib = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    team = Column(String, nullable=False)
    rfid_tag = Column(String, unique=True)

class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    bib = Column(Integer)
    finish_time = Column(Float)
    race_number = Column(Integer)
    photo_path = Column(String)

Base.metadata.create_all(engine)

# ====== Flask App Setup ======
app = Flask(__name__)
admin = Admin(app, name='Race Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Runner, Session()))
admin.add_view(ModelView(Result, Session()))

# Shared queue for RFID bibs scanned (thread safe)
rfid_queue = queue.Queue()

# ====== GTK GUI ======
class RaceTimerGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Race Timing System")
        self.set_default_size(600, 400)

        self.session = Session()
        self.start_time = None
        self.unassigned_times = []  # list of (finish_time float)

        self.current_race = 1  # example race number; you can extend to choose races

        # GUI setup
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Controls
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, False, False, 0)

        self.start_button = Gtk.Button(label="Start Race")
        self.start_button.connect("clicked", self.on_start_race)
        hbox.pack_start(self.start_button, False, False, 0)

        self.stop_button = Gtk.Button(label="Stop Race")
        self.stop_button.connect("clicked", self.on_stop_race)
        hbox.pack_start(self.stop_button, False, False, 0)

        self.assign_rfid_button = Gtk.Button(label="Assign RFID to Runner")
        self.assign_rfid_button.connect("clicked", self.on_assign_rfid)
        hbox.pack_start(self.assign_rfid_button, False, False, 0)

        # Manual Entry
        self.manual_entry = Gtk.Entry()
        self.manual_entry.set_placeholder_text("Enter bib or press spacebar for unassigned time")
        self.manual_entry.connect("activate", self.on_manual_entry)
        vbox.pack_start(self.manual_entry, False, False, 0)

        # Results Text View
        self.results_buffer = Gtk.TextBuffer()
        self.results_view = Gtk.TextView(buffer=self.results_buffer)
        self.results_view.set_editable(False)
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.add(self.results_view)
        vbox.pack_start(scroll, True, True, 0)

        # Start background threads
        self.rfid_running = True
        threading.Thread(target=self.rfid_file_watcher, daemon=True).start()
        threading.Thread(target=self.db_backup_loop, daemon=True).start()
        threading.Thread(target=self.rfid_tcp_server, daemon=True).start()
        threading.Thread(target=self.rfid_queue_processor, daemon=True).start()

        # Webcam capture lock
        self.webcam_lock = threading.Lock()

        # Show initial
        self.update_results_view()

    # GUI Callbacks
    def on_start_race(self, widget):
        self.start_time = time.perf_counter()
        self.unassigned_times.clear()
        self.append_log("Race started.")

    def on_stop_race(self, widget):
        self.start_time = None
        self.append_log("Race stopped.")

    def on_manual_entry(self, widget):
        text = widget.get_text().strip()
        widget.set_text("")
        if text == "":
            self.record_unassigned_time()
        elif text.isdigit():
            if len(text) == 3:
                self.record_time(int(text))
            else:
                self.assign_bib_to_unassigned(int(text))
        else:
            self.append_log("Invalid input.")

    def on_assign_rfid(self, widget):
        dialog = AssignRfidDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            bib = dialog.get_bib()
            rfid = dialog.get_rfid()
            if bib is not None and rfid is not None:
                # Check duplicates
                if self.session.query(Runner).filter_by(bib=bib).first():
                    runner = self.session.query(Runner).filter_by(bib=bib).first()
                    if runner.rfid_tag and runner.rfid_tag != rfid:
                        self.append_log(f"Runner {bib} already has RFID {runner.rfid_tag}.")
                    else:
                        runner.rfid_tag = rfid
                        self.session.commit()
                        self.append_log(f"Assigned RFID {rfid} to runner {bib}.")
                else:
                    self.append_log(f"No runner with bib {bib}.")
        dialog.destroy()

    def append_log(self, msg):
        GLib.idle_add(self._append_log, msg)

    def _append_log(self, msg):
        end_iter = self.results_buffer.get_end_iter()
        self.results_buffer.insert(end_iter, msg + "\n")

    # Core Timing Logic
    def record_unassigned_time(self):
        if self.start_time is None:
            self.append_log("Race not started.")
            return
        elapsed = round(time.perf_counter() - self.start_time, 3)
        self.unassigned_times.append(elapsed)
        self.append_log(f"Unassigned time recorded: {elapsed:.3f}")
        self.update_results_view()

    def record_time(self, bib):
        if self.start_time is None:
            self.append_log("Race not started.")
            return
        elapsed = round(time.perf_counter() - self.start_time, 3)
        # Check if bib already has a result for this race
        existing = self.session.query(Result).filter_by(bib=bib, race_number=self.current_race).first()
        if existing:
            self.append_log(f"Bib {bib} already has a time recorded.")
            return
        # Check bib exists in runners
        runner = self.session.query(Runner).filter_by(bib=bib).first()
        if not runner:
            self.append_log(f"Bib {bib} not found in runners.")
            return

        photo_path = self.capture_webcam_photo(bib)

        result = Result(bib=bib, finish_time=elapsed, race_number=self.current_race, photo_path=photo_path)
        self.session.add(result)
        self.session.commit()
        self.append_log(f"Recorded time for bib {bib}: {elapsed:.3f} sec")
        self.update_results_view()

    def assign_bib_to_unassigned(self, bib):
        if not self.unassigned_times:
            self.append_log("No unassigned times available.")
            return
        runner = self.session.query(Runner).filter_by(bib=bib).first()
        if not runner:
            self.append_log(f"Bib {bib} not found.")
            return
        # Assign earliest unassigned
        elapsed = self.unassigned_times.pop(0)

        photo_path = self.capture_webcam_photo(bib)

        result = Result(bib=bib, finish_time=elapsed, race_number=self.current_race, photo_path=photo_path)
        self.session.add(result)
        self.session.commit()
        self.append_log(f"Assigned bib {bib} to time {elapsed:.3f} sec")
        self.update_results_view()

    # Webcam photo capture
    def capture_webcam_photo(self, bib):
        try:
            with self.webcam_lock:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.append_log("Webcam not available.")
                    return None
                ret, frame = cap.read()
                cap.release()
                if ret:
                    filename = os.path.join(PHOTO_DIR, f"{bib}_{int(time.time())}.jpg")
                    cv2.imwrite(filename, frame)
                    return filename
        except Exception as e:
            self.append_log(f"Webcam capture error: {e}")
        return None

    # Update results text view
    def update_results_view(self):
        def do_update():
            self.results_buffer.set_text("")
            # Show individual results for current race
            results = self.session.query(Result).filter_by(race_number=self.current_race).order_by(Result.finish_time).all()
            lines = ["Individual Results:"]
            for idx, r in enumerate(results, 1):
                runner = self.session.query(Runner).filter_by(bib=r.bib).first()
                lines.append(f"{idx}. Bib {r.bib} - {runner.name if runner else 'Unknown'} - {r.finish_time:.3f}s - Team: {runner.team if runner else 'N/A'}")
            # Show unassigned times
            if self.unassigned_times:
                lines.append("\nUnassigned Times:")
                for ut in self.unassigned_times:
                    lines.append(f"  {ut:.3f}s")
            self.results_buffer.set_text("\n".join(lines))
        GLib.idle_add(do_update)

    # RFID File Watcher Thread
    def rfid_file_watcher(self):
        last_size = 0
        while self.rfid_running:
            try:
                if os.path.exists(RFID_INPUT_FILE):
                    size = os.path.getsize(RFID_INPUT_FILE)
                    if size > last_size:
                        with open(RFID_INPUT_FILE, 'r') as f:
                            f.seek(last_size)
                            new_data = f.read()
                            for line in new_data.strip().splitlines():
                                bib = line.strip()
                                if bib.isdigit():
                                    rfid_queue.put(int(bib))
                        last_size = size
                time.sleep(0.5)
            except Exception as e:
                self.append_log(f"RFID watcher error: {e}")
                time.sleep(1)

    # TCP Server for RFID input
    class TCPHandler(socketserver.StreamRequestHandler):
        def handle(self):
            for line in self.rfile:
                bib = line.strip().decode()
                if bib.isdigit():
                    rfid_queue.put(int(bib))

    def rfid_tcp_server(self):
        server = socketserver.TCPServer(('', TCP_PORT), self.TCPHandler)
        server.timeout = 1
        while self.rfid_running:
            server.handle_request()

    # RFID queue processor
    def rfid_queue_processor(self):
        while self.rfid_running:
            try:
                bib = rfid_queue.get(timeout=1)
                GLib.idle_add(self.record_time, bib)
            except queue.Empty:
                continue

    # Backup DB every 3 minutes
    def db_backup_loop(self):
        while True:
            try:
                time.sleep(180)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = os.path.join(BACKUP_DIR, f"{timestamp}_race.db")
                shutil.copyfile(DB_FILE, backup_name)
                self.append_log(f"Database backed up: {backup_name}")
            except Exception as e:
                self.append_log(f"Backup error: {e}")

    # GTK main quit cleanup
    def on_destroy(self, widget):
        self.rfid_running = False
        self.session.close()
        Gtk.main_quit()

# Dialog for assigning RFID to runner
class AssignRfidDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Assign RFID Tag", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        box = self.get_content_area()

        grid = Gtk.Grid(column_spacing=10, row_spacing=10, margin=10)
        box.add(grid)

        self.bib_entry = Gtk.Entry()
        self.bib_entry.set_placeholder_text("Runner Bib Number")

        self.rfid_entry = Gtk.Entry()
        self.rfid_entry.set_placeholder_text("RFID Tag")

        grid.attach(Gtk.Label(label="Bib Number:"), 0, 0, 1, 1)
        grid.attach(self.bib_entry, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="RFID Tag:"), 0, 1, 1, 1)
        grid.attach(self.rfid_entry, 1, 1, 1, 1)

        self.show_all()

    def get_bib(self):
        text = self.bib_entry.get_text()
        return int(text) if text.isdigit() else None

    def get_rfid(self):
        text = self.rfid_entry.get_text()
        return text.strip() if text else None

# ====== Flask Routes ======
@app.route("/")
def index():
    session = Session()
    results = session.query(Result).order_by(Result.finish_time).all()
    display = []
    for r in results:
        runner = session.query(Runner).filter_by(bib=r.bib).first()
        place_in_team = calculate_place_in_team(session, r)
        display.append({
            "bib": r.bib,
            "name": runner.name if runner else "Unknown",
            "team": runner.team if runner else "N/A",
            "time": f"{r.finish_time:.3f}",
            "photo": r.photo_path,
            "place_in_team": place_in_team,
        })
    session.close()
    return render_template("index.html", results=display)

def calculate_place_in_team(session, result):
    # Calculates place of runner within their team for the race number
    if not result.bib:
        return None
    runner = session.query(Runner).filter_by(bib=result.bib).first()
    if not runner:
        return None
    team_results = session.query(Result).join(Runner, Result.bib == Runner.bib)\
        .filter(Result.race_number == result.race_number, Runner.team == runner.team)\
        .order_by(Result.finish_time).all()
    for idx, res in enumerate(team_results, 1):
        if res.bib == result.bib:
            return idx
    return None

# Additional routes to edit runners/results can be added here...

# Run Flask app in separate thread
def run_flask():
    app.run(port=5000)

# ====== Main Entry Point ======
def main():
    # Start Flask server in a thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start GTK GUI
    gui = RaceTimerGUI()
    gui.connect("destroy", gui.on_destroy)
    gui.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
