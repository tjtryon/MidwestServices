# 🖥️ The Race Timing Solution (TRTS) - GUI Version 🏃‍♀️🏃‍♂️

---

### Video Demo: https://youtu.be/dtW6u3oPXfM

---

## 🎯 Overview

This is a modern **GTK4-based graphical interface** for the Race Timing Solution, providing an intuitive visual alternative to the console version. The GUI maintains **100% compatibility** with the console version's databases and authentication system while offering a user-friendly point-and-click experience.

### 🏆 Race Types Supported
- **🏃‍♀️ Cross Country Races** - Team scoring with top 5 finishers and 2 displacers
- **🏃‍♂️ Road Races** - Age group results based on date of birth

## ✨ Key Features

### 🔄 **Complete Console Compatibility**
- **Identical database formats** - works with any database created by console version
- **Same authentication system** - uses existing `config.db` with bcrypt encryption
- **Cross-platform compatibility** - race data fully interchangeable between versions
- **Same race type detection** - automatically identifies cross country vs road race databases

### 🎨 **Modern User Interface**
- **Professional styling** with dual-font system:
  - **Garamond 15px** for interface elements (buttons, labels, dialogs)
  - **Space Mono 11pt** for data displays (results, runner lists)
- **Smart button states** - buttons only enabled when prerequisites are met
- **Intuitive workflows** - guided setup with clear dialogs
- **Responsive design** - adapts to different content sizes

### 🗃️ **Database Management**
- **Visual database creation** with race type selection dialogs
- **File browser integration** for loading existing databases and CSV files
- **Smart database naming**: `YYYYMMDD-##-[cc or rr]-[Race_Name].db`
  - `cc` = Cross Country, `rr` = Road Race
  - Example: `20250727-01-cc-County_Meet.db`
- **Automatic race type detection** from loaded databases

### 📊 **Runner Management**
- **CSV import with validation** - different formats for each race type:
  - **Cross Country**: `bib, name, team, age, grade, rfid`
  - **Road Race**: `bib, name, dob, rfid` (age calculated automatically)
- **Visual runner list display** with formatted columns
- **Import progress feedback** with success/error reporting

### ⏱️ **Live Race Timing**
- **Dedicated timing window** with large, real-time race clock
- **Clean timing interface** optimized for race day operations
- **Manual bib entry** with instant feedback
- **Live results display** showing finishers as they complete
- **Audio feedback** (when beep.mp3 file available)
- **Safe exit procedures** with 'exit' command

### 🏆 **Intelligent Results Display**

#### 🎯 **Dynamic Results Button**
- **Adapts to race type** automatically:
  - Cross Country databases → "Show Team Results"
  - Road Race databases → "Show Age Group Results"
  - No database loaded → "Show Results (Load database first)"

#### 🏃‍♀️ **Cross Country Team Scoring**
- **Professional team standings** with comprehensive breakdowns
- **Top 5 scoring runners** clearly identified
- **Displacers display** (6th and 7th runners for tiebreaking)
- **Lowest score wins** scoring system (like golf)

#### 🏃‍♂️ **Road Race Age Groups**
- **Automatic age classification** into standard divisions:
  - 1-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, 46-50
  - 51-55, 56-60, 61-65, 66-70, 71+ years
- **Age calculated from birth date** for accuracy
- **Separate standings** for each age group

#### 👤 **Individual Results**
- **Overall finish order** with positions and times
- **Professional formatting** ready for printing or sharing
- **Time display** in MM:SS.mmm format

### 🛡️ **Security & Authentication**
- **First-run setup** prompts for admin credentials
- **bcrypt password hashing** identical to console version
- **Secure credential storage** in compatible `config.db`
- **Admin validation** before sensitive operations

## 🛠️ Requirements

### System Requirements
- **Linux/Unix system** (Debian, Ubuntu, etc.)
- **Python 3.7+**
- **GTK4** with Python bindings
- **PyGObject** for GTK integration

### Dependencies
Install required packages:

```bash
# System packages (Ubuntu/Debian)
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0

# Python packages
pip install bcrypt
```

### Required Python Packages
- **`gi`** (PyGObject) - GTK4 interface
- **`sqlite3`** - Database operations (built-in)
- **`bcrypt`** - Secure password hashing
- **`csv`** - CSV file processing (built-in)
- **`datetime`** - Time and date handling (built-in)
- **`os`** - File system operations (built-in)

### Optional Audio
- **`beep.mp3`** in root directory for finish alerts

## 🚀 Setup & Installation

### 1. **System Preparation** 🔧
```bash
# Install GTK4 and Python bindings
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0

# Install Python dependencies
pip install bcrypt
```

### 2. **Directory Structure** 📁
```
project/
├── gui/
│   └── race_timing_gui.py
├── data/                    # Auto-created
│   ├── config.db           # Admin credentials (shared with console)
│   ├── *.csv               # Runner data files
│   └── *.db                # Race databases (shared with console)
└── beep.mp3                # Optional audio alert
```

### 3. **First Run Setup** 🔐
On first launch, the GUI will prompt for admin credentials:
- **Username** and **password** setup dialog
- **Secure storage** with bcrypt hashing
- **Compatible** with console version credentials

## 🎮 Usage Guide

### Starting the GUI
```bash
cd project
python3 gui/race_timing_gui.py
```

### 🖱️ Main Interface

The main window displays:
- **Current database status** with race type indicator
- **Action buttons** that enable/disable based on current state
- **Professional styling** with clear visual hierarchy

### 📋 Main Menu Functions

1. **Create New Database** 🆕
   - **Race type selection** dialog (Cross Country or Road Race)
   - **Race details entry** (number and name)
   - **Automatic database creation** with proper naming

2. **Load Existing Database** 📂
   - **File browser** for database selection
   - **Automatic race type detection**
   - **Immediate interface updates** based on loaded race

3. **Load Runners from CSV** 📊
   - **File browser** for CSV selection
   - **Format validation** based on race type
   - **Import progress** with detailed feedback

4. **View All Runners** 👥
   - **Formatted display** of all registered participants
   - **Race-specific information** (teams vs age data)
   - **Professional layout** ready for printing

5. **Start the Race** 🏁
   - **Dedicated timing window** with live clock
   - **Real-time bib entry** interface
   - **Instant results feedback**

6. **Show Individual Results** 🏆
   - **Complete finish order** with times
   - **Professional formatting** for official results

7. **Dynamic Results Button** 📊
   - **"Show Team Results"** (Cross Country races)
   - **"Show Age Group Results"** (Road races)
   - **Automatically adapts** to loaded race type

8. **Instructions** 📖
   - **Comprehensive user guide** within the application
   - **Step-by-step procedures** for all functions

9. **Exit** 🚪
   - **Safe program termination**

### 🏃‍♀️ CSV File Formats

#### Cross Country Races
```csv
bib,name,team,age,grade,rfid
101,John Smith,Lincoln High,16,11,ABC123
102,Jane Doe,Roosevelt MS,14,8,DEF456
103,Mike Jones,Central HS,17,12,GHI789
```

#### Road Races
```csv
bib,name,dob,rfid
201,Sarah Johnson,1985-03-15,JKL012
202,Tom Wilson,1992-07-22,MNO345
203,Lisa Brown,1978-11-08,PQR678
```

### ⏱️ Live Race Timing Interface

The timing window provides:
- **Large digital clock** showing elapsed race time
- **Simple bib entry** field with Enter-to-record
- **Live results scroll** showing finishers as they complete
- **Clear instructions** displayed in window
- **Exit command** ('exit' + Enter) to stop timing

**Timing Procedures:**
1. **Enter bib number** as runner finishes
2. **Press Enter** to record time
3. **View confirmation** in results scroll
4. **Continue** until all runners finish
5. **Type 'exit'** to end timing session

## 🎨 Interface Design

### 🎯 **Button State Management**
- **Smart enabling/disabling** based on prerequisites
- **Helpful tooltips** explain why buttons are disabled
- **Visual feedback** guides user through proper workflow

### 📊 **Data Display**
- **Monospace font** for perfect column alignment
- **Professional formatting** for all results
- **Scrollable windows** for large datasets
- **Print-ready layouts**

### 🔄 **Race Type Adaptation**
- **Interface automatically adapts** to loaded race type
- **Relevant buttons shown/hidden** based on race format
- **Consistent behavior** with console version

## 🔧 Technical Features

### 🗃️ **Database Compatibility**
- **100% compatible** with console version databases
- **Shared authentication** system
- **Identical table structures** and data formats
- **Cross-version workflow** support

### 🛡️ **Error Handling**
- **Graceful error recovery** with user-friendly messages
- **Input validation** prevents data corruption
- **File operation safety** checks

### 🎨 **Professional Styling**
- **Custom CSS** for consistent appearance
- **Dual-font system** optimizes readability
- **Responsive dialogs** adapt to content

## 🚨 Troubleshooting

### Common Issues

**🖥️ GTK4 Not Found**
```bash
# Install GTK4 development packages
sudo apt install libgtk-4-dev python3-gi-dev
```

**🔊 Audio Not Working**
- Ensure `beep.mp3` exists in root directory
- Audio failure doesn't affect timing functionality
- Check system audio settings

**📂 Permission Errors**
- Ensure write permissions in project directory
- Check `data/` folder permissions
- Verify user has database access rights

**🗃️ Database Loading Issues**
- Confirm database file isn't corrupted
- Check file permissions
- Verify database was created by compatible version

**📊 CSV Import Problems**
- Verify CSV has exact column headers required
- Check date format (YYYY-MM-DD) for road races
- Ensure file encoding is UTF-8

### Debug Mode
Run with debug output:
```bash
python3 gui/race_timing_gui.py 2>&1 | tee debug.log
```

## 🔄 Workflow Integration

### 🖥️ **Console + GUI Workflow**
1. **Setup race** using either console or GUI
2. **Import runners** from either interface
3. **Time race** using preferred interface
4. **View results** from either version
5. **Share databases** between team members

### 📊 **Race Day Recommendations**
- **Use GUI** for setup and post-race analysis
- **Either interface** works great for live timing
- **Multiple operators** can use different interfaces
- **Real-time collaboration** through shared database

## 🎯 Best Practices

### 🏁 **Race Setup**
1. **Create database** well before race day
2. **Import and verify** runner data
3. **Test timing interface** with practice entries
4. **Backup database** before live race

### 📱 **User Experience**
1. **Use tooltips** to understand button states
2. **Follow guided workflows** for best results
3. **Check status display** for current race information
4. **Use Instructions button** for in-app help

### 🔒 **Data Management**
1. **Regular backups** of race databases
2. **Consistent file naming** for organization
3. **Version compatibility** maintained between updates

## 🏆 Professional Features

### 📊 **Production Ready**
- **Stable GTK4 interface** tested on Linux systems
- **Professional result formatting** ready for publication
- **Scalable design** handles races of any size
- **Reliable timing accuracy** for official events

### 🎓 **Educational Value**
- **Clear interface design** teaches good UX principles
- **Well-documented code** for learning GUI development
- **Professional software patterns** demonstrated

## 📜 License

This project is released under the **MIT License**.

---

## 🙋‍♂️ Support

### Getting Help
- **Use Instructions button** in the application for detailed guidance
- **Check console output** for debug information during issues
- **Verify system requirements** for GTK4 compatibility

### Compatibility Notes
- **Fully compatible** with console version databases
- **Shared configuration** files and authentication
- **Cross-platform** data portability

**🎉 Happy Racing with the GUI! 🖥️🏃‍♀️🏃‍♂️**
