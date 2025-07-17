# Race Timing System GUI

## Overview

This Race Timing System provides a complete solution for timing, scoring, and managing cross-country or similar races. It supports individual and team results, live timing with milliseconds precision, RFID tag integration, and a web-based interface for management and real-time result viewing.

---

## Features

- **Race Timing & Scoring**
  - Record finish times manually by bib number or using spacebar input.
  - Live timing with millisecond precision.
  - Individual and team scoring (top 5 finishers plus 2 displacers).
  - Supports multiple races/heats by race number.
  - Prevents duplicate bibs and RFID tags.

- **RFID Integration**
  - Reads finish times from RFID tag scans.
  - Supports live RFID reading through file watching or TCP scanning.
  - On-site RFID assignment via GUI.
  - Bulk import of RFID mappings from CSV.

- **Data Management**
  - Stores data in SQLite databases named by race date (`YYYYMMDDRace.db`).
  - Supports multiple race days and merges databases if needed.
  - Backup system running every 3 minutes.
  - Load previous race results by date for viewing and printing.

- **Web Interface (Flask)**
  - Upload runner CSV files.
  - Assign RFID tags to runners.
  - View individual and team results by race.
  - Real-time results viewing with place ranking.
  - Editable runner and result tables via web form.
  - Documentation and usage notes pages.
  - Admin panel for centralized management.

- **GUI Application**
  - GTK4-based GUI for race timing and RFID scan handling.
  - Sound alerts on RFID scans.
  - Support for manual and RFID timing modes.
  - File rotation and race number support.

- **Export & Reporting**
  - Export results in HTML with Bootstrap CSS styling.
  - Generate charts using Matplotlib for race statistics.

---

## Installation

### Prerequisites

- Python 3.8+
- GTK4 (for GUI)
- Required Python packages:
  - Flask
  - matplotlib
  - sqlite3 (built-in)
  - watchdog (for file watching RFID input)
  - PyGObject (for GTK GUI)

Install dependencies using:

```bash
pip install flask matplotlib watchdog PyGObject


Starting the Flask web server:
from the web/ directory, run:

python app.py

Navigate to http://localhost:5000



Running the GTK GUI
From the gui/ directory, run:
python race-timer-rfid-gui.py



How to Use
Upload runners via the web interface (CSV format with bib, name, team, RFID).

Assign RFID tags manually or in bulk.

Start races and enter finish times manually or via RFID scans.

View individual and team results by race date.

Export results and generate reports via the web interface.

Use the admin panel for system management.

File Naming Conventions
Runner CSV files: runners_YYYYMMDD.csv

SQLite databases: YYYYMMDDRace.db

Backup databases: stored in data/backups/ with timestamps.

RFID input file (for live reading): rfid_input.txt


Contributing
Contributions, bug reports, and feature requests are welcome! Please fork the repository and submit pull requests.


License
MIT License

For questions or support, please contact TJ Tryon at tj@tjtryon.com
