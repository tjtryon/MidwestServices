# 🏃‍♂️ The Race Timing Solution (TRTS)

**Professional Cross Country & Road Race Timing Software** ⏱️

Version 0.9.96 - Stable Release 🚀

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [📋 Requirements](#-requirements)
- [🚀 Installation](#-installation)
- [🎯 Quick Start Guide](#-quick-start-guide)
- [📚 Detailed Instructions](#-detailed-instructions)
- [🔄 Race Day Workflow](#-race-day-workflow)
- [📊 Results & Reporting](#-results--reporting)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📞 Support & Contact](#-support--contact)
- [📜 License](#-license)

---

## 🌟 Overview

The Race Timing Solution (TRTS) is a professional GTK4-based Python application designed to manage cross-country and road race events with precision and ease. Built with race directors and timing officials in mind, TRTS provides a complete solution from runner registration to final results publication.

### 🎯 What Makes TRTS Special?

- **Real-time race timing** with millisecond precision ⚡
- **Professional results formatting** ready for 8.5x11 printing 📄
- **Smart button management** prevents user errors 🛡️
- **Dual font system** for perfect data alignment 🔤
- **Comprehensive error handling** with helpful messages 💡
- **Cross-platform compatibility** (Linux, Windows, macOS) 🌐

---

## ✨ Features

### 🗄️ Database Management
- Create new race databases with custom naming
- Load existing race databases for continued work
- Enhanced config tables for comprehensive race tracking
- Coaches table for team and school contact information
- Automatic backup and data safety features

### 👥 Runner Management
- Import runners from CSV files with flexible column detection
- Support for bib numbers, names, teams, and RFID tags
- View all registered runners in organized displays
- Smart validation for data integrity

### ⏱️ Live Race Timing
- Real-time race timer with 100ms precision
- Enter bib numbers as runners finish
- Automatic time recording and runner lookup
- Support for missed bibs (recorded as bib #0 for later correction)
- Type "exit" to cleanly stop timing

### 📊 Results Generation
- **Individual Results**: Runners sorted by finish time
- **Team Results**: Cross-country scoring with top 5 runners
- **Displacer tracking**: 6th and 7th team members
- Print-ready formatting for 8.5x11 paper
- Automatic pagination with headers on every page

### 🎨 User Interface
- Professional dual-font system (Garamond UI + Space Mono data)
- Smart button states prevent user errors
- Curved corners and modern styling
- Comprehensive help system built-in

---

## 📋 Requirements

### 🐍 Python Requirements
- **Python 3.8 or newer** (recommended: Python 3.10+)
- **PyGObject >= 3.42.0** for GTK4 support

### 🖥️ System Requirements
- **GTK 4.0 or newer** graphical toolkit
- **At least 2GB RAM** (recommended for smooth operation)
- **100MB free disk space** minimum
- **Graphical desktop environment** (GUI required)

### 🌍 Operating System Support
- **Linux**: Ubuntu 20.04+, Fedora 35+, Debian 11+, and similar
- **Windows**: Windows 10/11 with GTK4 runtime
- **macOS**: macOS 10.15+ with GTK4 via Homebrew

### 📦 Dependencies

Create a `requirements.txt` file:
```
PyGObject>=3.42.0
```

Built-in Python modules used:
- `sqlite3` - Database operations
- `csv` - CSV file processing  
- `datetime` - Date and time handling
- `os` - File system operations

---

## 🚀 Installation

### 📁 Project Structure
```
race-timing-solution/
├── gui/
│   └── race_timing_gui.py     # Main application file
├── data/                      # Auto-created for race databases
│   ├── config.db             # Admin configuration
│   └── *.db                  # Race database files
├── requirements.txt          # Python dependencies
└── README.md                # This documentation
```

### 🔧 Installation Steps

1. **Clone or download the project** 📥
   ```bash
   git clone <repository-url>
   cd race-timing-solution
   ```

2. **Install Python dependencies** 🐍
   ```bash
   pip install -r requirements.txt
   ```

3. **Install GTK4 system dependencies** 🏗️

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0
   ```

   **Linux (Fedora):**
   ```bash
   sudo dnf install python3-gobject gtk4-devel
   ```

   **Windows:** 📱
   - Install GTK4 runtime from official GTK website
   - Or use MSYS2 package manager

   **macOS:** 🍎
   ```bash
   brew install gtk4 pygobject3
   ```

4. **Run the application** 🎯
   ```bash
   python gui/race_timing_gui.py
   ```

---

## 🎯 Quick Start Guide

### ⚡ 5-Minute Setup

1. **Launch TRTS** 🚀
   ```bash
   python gui/race_timing_gui.py
   ```

2. **First-time setup** 👤
   - Enter admin username and password when prompted
   - This creates your configuration database

3. **Create a new race** 🏁
   - Click "Create New Database"
   - Enter race number (01, 02, etc.)
   - Enter race name/location

4. **Load your runners** 📋
   - Click "Load CSV File to Database"
   - Select your CSV file with columns: `bib`, `full_name`, `team`

5. **Start timing** ⏱️
   - Click "Start the Race" when ready
   - Enter bib numbers as runners finish
   - Type "exit" when done

6. **Generate results** 🏆
   - Click "List Individual Results" for finish order
   - Click "List Team Results" for team scoring

---

## 📚 Detailed Instructions

### 📊 CSV File Format

Your runner data CSV should include these columns:

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `bib` | ✅ Yes | Runner's bib number | 101 |
| `full_name` | ✅ Yes | Runner's complete name | "John Smith" |
| `team` | ✅ Yes | School or team name | "Lincoln High School" |
| `rfid` | ❌ Optional | RFID chip identifier | "ABC123" |

**Flexible column names supported:**
- Bib: `bib`, `Bib`, `BIB`
- Name: `full_name`, `Full Name`, `name`, `Name`
- Team: `team`, `Team`, `TEAM`
- RFID: `rfid`, `RFID`, `Rfid`

### 🗂️ Database Files

**Automatic naming convention:**
```
YYYYMMDD-##-Race_Name.db
```

Examples:
- `20250722-01-State_Championship.db`
- `20250722-02-Regional_Meet.db`

**Database contents:**
- `runners` table: All participant information
- `race_config` table: Race metadata and timing info
- `coaches` table: Team and school contact information

### 🏁 Race Timing Best Practices

1. **Test everything before race day** 🧪
   - Create a test database
   - Practice the timing workflow
   - Verify results generation

2. **Prepare backup plans** 💾
   - Have paper backup sheets ready
   - Test on battery power if using laptop
   - Bring extra computer if possible

3. **Race day setup** 📋
   - Start the program early
   - Load all runners and verify count
   - Position computer for easy bib number entry

4. **During the race** 🏃‍♂️
   - Enter bib numbers immediately as runners finish
   - Press Enter with no bib for missed runners (records as bib #0)
   - Keep paper backup of finish order

5. **After the race** 🏆
   - Generate and review results immediately
   - Print results for posting
   - Keep database file as permanent record

---

## 🔄 Race Day Workflow

### 📅 Pre-Race Setup

1. **Arrive early** ⏰
   - Set up timing computer in clear view of finish line
   - Test power and display visibility

2. **Load race data** 📂
   - Open TRTS application
   - Create new database or load existing
   - Import runner CSV file
   - Verify runner count with entries

3. **Test timing system** 🧪
   - Click "Start the Race" to test
   - Practice entering bib numbers
   - Type "exit" to stop test timing

### 🏁 During the Race

1. **Start official timing** ⏱️
   - Click "Start the Race" at gun time
   - Timer begins automatically

2. **Record finishers** 📝
   - Type bib number and press Enter for each finisher
   - For missed bibs: just press Enter (saves as bib #0)
   - Continue until all runners finish

3. **End timing** 🏁
   - Type "exit" and press Enter
   - Timing window closes automatically

### 📊 Post-Race Results

1. **Generate individual results** 🥇
   - Click "List Individual Results"
   - Review for accuracy
   - Print for posting

2. **Generate team results** 🏆
   - Click "List Team Results"
   - Verify team scoring (sum of top 5 positions)
   - Print for coaches

3. **Handle corrections** ✏️
   - Use database tools to fix bib #0 entries
   - Regenerate results if needed

---

## 📊 Results & Reporting

### 🥇 Individual Results Format
```
THE RACE TIMING SOLUTION (TRTS) - BY MIDWEST EVENT SERVICES, INC.
State Championship at Lincoln Park - July 22, 2025

INDIVIDUAL RESULTS
===============================================================================
POS     BIB     RUNNER NAME                          TEAM                  TIME      
-------------------------------------------------------------------------------
1       101     John Smith                           Lincoln High School   16:23.456 
2       205     Sarah Johnson                        Roosevelt High School 16:45.123 
3       142     Mike Wilson                          Lincoln High School   17:02.789 
```

### 🏆 Team Results Format
```
**Lincoln High School**
__Team Score: 27__
=======================================================
POS     BIB     RUNNER NAME                          TIME      
-------------------------------------------------------
1       101     John Smith                           16:23.456 
3       103     Mike Wilson                          16:45.123 
5       105     Tom Davis                            17:02.789 
8       107     Dave Brown                           17:15.234 
10      109     Steve Miller                         17:28.567 

Displacers:
-------------------------------------------------------
12      111     Paul Anderson                        17:35.890 
15      113     Jim Johnson                          17:42.123 
```

### 📄 Print Specifications
- **Page size**: 8.5" x 11" standard paper
- **Font**: Space Mono 11pt for perfect alignment
- **Margins**: Standard printer margins
- **Headers**: Repeated on each page
- **Page numbers**: Included on all pages

---

## 🛠️ Troubleshooting

### ⚠️ Common Problems & Solutions

#### 🐍 Python/Installation Issues

**Problem**: `ImportError: No module named 'gi'`
**Solution**: Install PyGObject
```bash
pip install PyGObject
```

**Problem**: `Gtk-WARNING: cannot open display`
**Solution**: Ensure you're running on a system with graphical desktop

#### 📁 File & Database Issues

**Problem**: CSV file won't load
**Solutions**:
- Verify CSV has columns: `bib`, `full_name`, `team`
- Check that bib numbers are valid integers
- Ensure file isn't open in Excel or other programs
- Try saving CSV as UTF-8 encoding

**Problem**: Database file corrupted
**Solutions**:
- Create new database (old data may be lost)
- Check available disk space
- Verify write permissions in data directory

#### ⏱️ Timing Issues

**Problem**: Program crashes during race timing
**Solutions**:
- Check available disk space (need space for database writes)
- Restart program and load existing database
- Use paper backup if necessary

**Problem**: Time format shows unwanted hours
**Solutions**:
- This is fixed in version 0.9.96
- Times under 1 hour show as MM:SS.mmm
- Times over 1 hour show as HH:MM:SS.mmm

#### 🖥️ Display Issues

**Problem**: Columns don't align in results
**Solutions**:
- Ensure Space Mono font is installed
- Check that system supports Google Fonts
- Update to latest version (0.9.96+)

**Problem**: Buttons appear disabled when they shouldn't be
**Solutions**:
- Load a database first (Create New or Load Existing)
- Import runners from CSV file
- Check that race has completed runners for results

### 🆘 Getting Help

If you encounter issues not covered here:

1. **Check the console output** for error messages
2. **Verify all requirements** are installed correctly
3. **Try with a fresh database** to isolate the problem
4. **Contact support** (see contact information below)

---

## 🤝 Contributing

We welcome contributions to make TRTS even better! 🌟

### 🍴 How to Contribute

1. **Fork the repository** 🍴
   ```bash
   git clone <your-fork-url>
   cd race-timing-solution
   ```

2. **Create a feature branch** 🌿
   ```bash
   git checkout -b feature/your-awesome-feature
   ```

3. **Make your improvements** ✨
   - Add new features
   - Fix bugs
   - Improve documentation
   - Enhance user interface

4. **Test your changes** 🧪
   - Run the application thoroughly
   - Test edge cases and error conditions
   - Verify compatibility across platforms

5. **Submit a pull request** 📤
   - Describe your changes clearly
   - Include screenshots if UI changes
   - Reference any related issues

### 🎯 Areas We Need Help With

- **🖨️ Print functionality** for results
- **📱 RFID integration** for automatic timing
- **🌐 Web dashboard** development
- **📦 Packaging** for easier installation
- **🧪 Testing** on different platforms
- **📚 Documentation** improvements
- **🌍 Internationalization** (multiple languages)

### 📋 Development Guidelines

- **Code style**: Follow existing patterns and commenting style
- **Documentation**: Keep comments at 5th-grade reading level
- **Error handling**: Include comprehensive error checking
- **Testing**: Test thoroughly before submitting
- **Compatibility**: Ensure GTK4 compliance

---

## 📞 Support & Contact

### 👨‍💻 Developer Contact

**TJ Tryon** - Lead Developer  
📧 **Email**: [tj@tjtryon.com](mailto:tj@tjtryon.com)  
📱 **Phone**: [317-774-8762](tel:317-774-8762)  
🏢 **Company**: Midwest Event Services, Inc.

### 🤝 Getting Support

- **📧 Email support**: Best for detailed technical questions
- **📱 Phone support**: Available for urgent race day issues
- **💻 GitHub Issues**: For bug reports and feature requests
- **📖 Documentation**: Check this README first

### ⏰ Support Hours

- **📧 Email**: Typically respond within 24 hours
- **📱 Phone**: Available during US Central Time business hours
- **🚨 Race Day**: Emergency support available weekends during race season

---

## 📜 License

### 🏛️ MIT License

**Copyright © 2025 TJ Tryon. All rights reserved.**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### 🤝 Contributing Agreement

By contributing to this project, you agree:
- Your contributions will be licensed under the same MIT License
- You have the right to submit the contributions
- Your contributions are your original work or properly attributed

---

## 🙏 Acknowledgments

### 🌟 Special Thanks

- **Cross Country Coaches** who provided feedback and requirements
- **Race Directors** who tested early versions
- **Open Source Community** for GTK4 and Python ecosystem
- **Contributors** who help make TRTS better

### 🔧 Technologies Used

- **🐍 Python** - Core programming language
- **🖼️ GTK 4** - Cross-platform GUI toolkit
- **🗄️ SQLite** - Embedded database engine
- **🔤 Google Fonts** - Typography (Space Mono, Garamond)
- **📊 CSV** - Data import format

---

## 📈 Version History

- **v0.9.96** (Current) - Enhanced documentation and error handling
- **v0.91.85** - Print-ready formatting and pagination
- **v0.91** - Smart button states and dual font system
- **v0.9** - Initial stable release

---

**Made with ❤️ for the running community** 🏃‍♀️🏃‍♂️

*The Race Timing Solution - Precision timing for every race* ⏱️✨