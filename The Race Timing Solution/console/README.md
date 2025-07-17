# Race Timing Console Application

## Overview

This is a Python console-based race timing and scoring system designed for cross country and similar events. It supports:

- **Individual and team results**
- **Live timing with milliseconds (via system clock)**
- **RFID tag reading via file watcher**
- **Manual time entry by bib number**
- **SQLite database storage per race day**
- **Team scoring** using top 5 finishers plus 2 displacers
- **Sound alerts** on runner finish

## Features

- Import runners from CSV files including bib number, name, team, and optional RFID tag.
- Real-time race timing using RFID scans appended to a file.
- Manual entry for finishers by bib number.
- Separate race numbers to handle multiple heats.
- Team scoring calculates points from top 5 runners and includes 2 displacers.
- Results and runner data saved in SQLite database files named `YYYYMMDDRace.db`.
- Sound alerts played on successful finish time entry.
- Menu-driven CLI interface.

## Requirements

- Python 3.7+
- Packages:
  - `playsound`
  - `watchdog`

Install dependencies via pip:

```bash
pip install playsound watchdog

Setup
Place a short sound file named beep.mp3 in the working directory.

Create a data directory or let the program create it.

Prepare runners CSV files with columns: bib, name, team, and optional rfid.

Start the program using:

bash
Copy code
python race_timing_console.py
Usage
Load Runners CSV: Load runners into the database.

Record manual result: Enter a bib number manually to record a finish.

List race results: Show all finishers for the current race.

Show team scores: Display team rankings and scores based on results.

Change race number: Switch the current race/heat number.

Quit: Exit the program safely.

RFID tags are monitored live by watching the data/rfid_input.txt file. Append RFID codes to this file to record automatic finishes.

File Structure
arduino
Copy code
race_timing_console.py
beep.mp3
data/
  ├── rfid_input.txt
  └── YYYYMMDDRace.db
runners.csv
Notes
Ensure rfid_input.txt is updated by your RFID reader software.

Sound alerts notify you of successful finish recording.

Duplicate bib numbers or RFID tags in runners CSV will be skipped with a warning.

Team scores require at least 5 finishers to calculate.

License
This project is released under the MIT License.
