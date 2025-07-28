# 🏃‍♀️ The Race Timing Solution (TRTS) - Console Version 🏃‍♂️

## 🎯 Overview

This is a comprehensive Python console-based race timing and scoring system designed for **cross country meets** and **road races**. The program provides professional-grade timing capabilities with an educational codebase that's perfect for learning programming concepts.

### 🏆 Race Types Supported
- **🏃‍♀️ Cross Country Races** - Team scoring with top 5 finishers and 2 displacers
- **🏃‍♂️ Road Races** - Age group results based on date of birth

## ✨ Key Features

### 🗃️ Database Management
- **Secure admin authentication** using bcrypt password hashing
- **Smart database naming**: `YYYYMMDD-##-[cc or rr]-[Race_Name].db`
  - `cc` = Cross Country
  - `rr` = Road Race
  - Example: `20250727-01-cc-County_Meet.db`
- **Race type detection** - automatically identifies cross country vs road race databases
- **SQLite database storage** with proper table structures for each race type

### 📊 Runner Management
- **CSV import support** with different formats for each race type:
  - **Cross Country**: `bib, name, team, age, grade, rfid`
  - **Road Race**: `bib, name, dob, rfid` (age calculated automatically)
- **Comprehensive runner information** storage and display
- **Data validation** ensures CSV files have correct column structure

### ⏱️ Race Timing
- **Live race timing** with real-time clock display
- **Manual bib number entry** as runners finish
- **Automatic time recording** with precise elapsed time calculation
- **🔊 Audio feedback** with beep sound on successful time entry
- **Exit command** (`exit`) to stop timing gracefully

### 🏆 Results & Scoring

#### 🏃‍♀️ Cross Country Team Scoring
- **Team scores** calculated from top 5 runners' finish positions
- **Displacers** (6th and 7th runners) used for tiebreaking
- **Lowest score wins** (like golf scoring)
- **Comprehensive team standings** with detailed breakdowns

#### 🏃‍♂️ Road Race Age Groups
- **Automatic age group classification**:
  - 1-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, 46-50
  - 51-55, 56-60, 61-65, 66-70, 71+ years
- **Age calculated from date of birth** for accuracy
- **Separate results** for each age group

#### 👤 Individual Results
- **Overall finish order** with positions and times
- **Time formatting** in MM:SS.mmm or HH:MM:SS.mmm
- **Runner identification** with bib numbers and names

### 🎓 Educational Features
- **Extensively commented code** - every function, loop, and operation explained
- **5th-grade friendly explanations** using analogies and simple language
- **Emoji indicators** throughout code for visual learning
- **Programming concept explanations** embedded in comments
- **Race logic tutorials** explaining team scoring and age group competition

## 🛠️ Requirements

### Python Version
- **Python 3.7+** required

### Dependencies
Install required packages via pip:

```bash
pip install playsound bcrypt
```

### Required Packages
- **`sqlite3`** - Database operations (built-in)
- **`bcrypt`** - Secure password hashing
- **`playsound`** - Audio feedback on finish recording
- **`csv`** - CSV file processing (built-in)
- **`datetime`** - Time and date handling (built-in)
- **`os`** - File system operations (built-in)
- **`getpass`** - Secure password input (built-in)

## 🚀 Setup & Installation

### 1. **Audio Setup** 🔊
Place a sound file named `beep.mp3` in the root directory for finish alerts.

### 2. **Directory Structure** 📁
The program automatically creates the required directory structure:
```
project/
├── console/
│   └── race_timing_console.py
├── data/                    # Auto-created
│   ├── config.db           # Admin credentials
│   ├── *.csv               # Runner data files
│   └── *.db                # Race databases
└── beep.mp3                # Audio alert file
```

### 3. **First Run Setup** 🔐
On first run, the program will prompt you to create admin credentials:
- Enter admin username
- Enter admin password (securely hashed with bcrypt)

## 🎮 Usage Guide

### Starting the Program
```bash
cd project
python3 console/race_timing_console.py
```

### 📋 Main Menu Options

1. **Create new database** 🆕
   - Choose race type (Cross Country or Road Race)
   - Enter race number (e.g., 01, 02)
   - Enter race name/location
   - Creates properly named database file

2. **Load existing database** 📂
   - Browse saved race databases
   - Automatically detects race type
   - Continues previous race or reviews results

3. **Load runners from CSV** 📊
   - Import runner data from spreadsheet
   - Validates CSV format for race type
   - Updates existing runners or adds new ones

4. **View all runners** 👥
   - Display all registered participants
   - Shows different info based on race type
   - Formatted for easy reading/printing

5. **Start the race** 🏁
   - Opens live timing interface
   - Real-time race clock display
   - Manual bib number entry system

6. **Show individual results** 🏆
   - Overall finish order
   - Position, bib, name, and time
   - Available after race completion

7. **Show team/age group results** 📊
   - **Cross Country**: Team scoring with top 5 + displacers
   - **Road Race**: Age group classifications
   - Adapts automatically to race type

8. **Quit** 🚪
   - Safe program exit

### 🏃‍♀️ CSV File Formats

#### Cross Country Races
```csv
bib,name,team,age,grade,rfid
101,John Smith,Lincoln High,16,11,ABC123
102,Jane Doe,Roosevelt MS,14,8,DEF456
```

#### Road Races
```csv
bib,name,dob,rfid
201,Mike Johnson,1985-03-15,GHI789
202,Sarah Wilson,1992-07-22,JKL012
```

### ⏱️ Live Race Timing

During race timing:
- **Enter bib numbers** as runners finish
- **Press Enter** to record finish time
- **Empty entry** records as bib #0 (for later correction)
- **Type 'exit'** to stop timing
- **Audio feedback** confirms each entry
- **Real-time clock** shows elapsed race time

## 🗃️ Database Structure

### Race Type Storage
```sql
CREATE TABLE race_type (type TEXT)
-- Stores "cross_country" or "road_race"
```

### Cross Country Runner Table
```sql
CREATE TABLE runners (
    bib INTEGER PRIMARY KEY,
    name TEXT,
    team TEXT,
    age INTEGER,
    grade TEXT,
    rfid TEXT
)
```

### Road Race Runner Table
```sql
CREATE TABLE runners (
    bib INTEGER PRIMARY KEY,
    name TEXT,
    dob TEXT,           -- Date of birth (YYYY-MM-DD)
    age INTEGER,        -- Calculated automatically
    rfid TEXT
)
```

### Results Table (Both Race Types)
```sql
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bib INTEGER,
    finish_time REAL,   -- Elapsed seconds from race start
    race_date TEXT      -- Race date (YYYY-MM-DD)
)
```

## 🎓 Educational Value

This program serves as an excellent learning tool for:

### 📚 Programming Concepts
- **Database operations** with SQLite
- **File I/O** and CSV processing
- **Object-oriented design** principles
- **Error handling** and validation
- **User interface** design for console applications
- **Security** with password hashing

### 🏃‍♀️ Race Management
- **Cross country team scoring** rules and calculations
- **Age group classification** systems
- **Race timing** procedures and best practices
- **Data management** for athletic events

### 🧮 Mathematical Concepts
- **Statistical calculations** (team scoring, age groups)
- **Time calculations** and formatting
- **Sorting algorithms** for results ranking
- **Data aggregation** and reporting

## 🔧 Technical Features

### 🔒 Security
- **Bcrypt password hashing** for admin authentication
- **Input validation** prevents data corruption
- **Error handling** ensures program stability

### 📊 Data Management
- **Automatic database creation** with proper schemas
- **Race type detection** from existing databases
- **CSV format validation** prevents import errors
- **Backup-friendly** database files

### 🎨 User Experience
- **Clear menu navigation** with numbered options
- **Helpful error messages** guide users
- **Progress feedback** during operations
- **Consistent formatting** across all displays

## 🚨 Troubleshooting

### Common Issues

**📂 File Not Found Errors**
- Ensure you're running from the correct directory
- Check that `data/` directory exists (auto-created)

**🔊 Audio Not Working**
- Verify `beep.mp3` exists in root directory
- Audio failure doesn't affect timing functionality

**📊 CSV Import Errors**
- Check CSV file has correct column headers
- Ensure race type matches CSV format
- Verify date format (YYYY-MM-DD) for road races

**🗃️ Database Errors**
- Ensure write permissions in `data/` directory
- Check available disk space
- Verify Python has SQLite support

## 📁 File Structure
```
project/
├── console/
│   └── race_timing_console.py     # Main program file
├── data/                          # Auto-created data directory
│   ├── config.db                  # Admin authentication
│   ├── runners_cc.csv             # Cross country runner sample
│   ├── runners_rr.csv             # Road race runner sample
│   ├── 20250727-01-cc-Meet.db     # Cross country race database
│   └── 20250727-02-rr-5K.db       # Road race database
├── beep.mp3                       # Audio alert file
└── README.md                      # This documentation
```

## 🎯 Best Practices

### 📊 Race Setup
1. **Create database** before race day
2. **Import runners** from registration system
3. **Test timing** with practice entries
4. **Backup database** before live race

### ⏱️ Race Day Operations
1. **Start timing** when race begins
2. **Enter bib numbers** as runners finish
3. **Use audio cues** to confirm entries
4. **Monitor elapsed time** display

### 📋 Post-Race
1. **Generate results** immediately
2. **Backup database** files
3. **Export results** for publication
4. **Verify team scores** or age groups

## 🏆 Professional Features

### 📊 Reporting
- **Print-ready formatting** for all results
- **Professional headers** with race information
- **Consistent column alignment** for easy reading
- **Scalable output** handles any number of participants

### 🔄 Workflow Integration
- **Compatible database format** works with GUI version
- **Standard CSV formats** integrate with registration systems
- **Portable data files** for easy backup and sharing

## 📜 License

This project is released under the **MIT License**.

---

## 🙋‍♂️ Support

For questions, issues, or contributions:
- Review the extensive code comments for implementation details
- Check troubleshooting section for common problems
- The educational comments make the code self-documenting

**🎉 Happy Racing! 🏃‍♀️🏃‍♂️**