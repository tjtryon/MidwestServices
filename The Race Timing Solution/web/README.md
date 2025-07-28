# 🌐 The Race Timing Solution (TRTS) - Flask Web Application 🏃‍♀️🏃‍♂️

## 🎯 Overview

This is the **Flask web application** component of The Race Timing Solution, providing a modern web interface for viewing and managing cross country and road race results. The application is **fully compatible** with the console and GUI versions, sharing the same database formats and authentication system.

### 🏆 Race Types Supported
- **🏃‍♀️ Cross Country Races** - Team scoring with top 5 finishers and 2 displacers
- **🏃‍♂️ Road Races** - Age group results based on date of birth
- **📊 Legacy Races** - Backward compatibility with older database formats

## ✨ Key Features

### 🔄 **Complete Application Integration**
- **100% compatible** with console and GUI application databases
- **Shared authentication** using same `config.db` with bcrypt encryption
- **Identical race type detection** from database content
- **Cross-platform data** fully interchangeable between all versions

### 🎨 **Modern Web Interface**
- **Responsive Bootstrap design** for desktop and mobile viewing
- **Race type organization** with separate sections for Cross Country and Road Race
- **Professional results formatting** ready for printing or sharing
- **Real-time dashboard** showing recent races by type

### 🗃️ **Advanced Database Support**
- **New filename format** support: `YYYYMMDD-##-[cc or rr]-[Race_Name].db`
- **Automatic race type detection** from database structure
- **Backward compatibility** with legacy `*-race.db` files
- **Multi-format time display** with proper MM:SS.mmm formatting

### 🏃‍♀️ **Cross Country Features**
- **Professional team standings** with comprehensive scoring breakdown
- **Team scoring logic** identical to console version (top 5 + displacers)
- **Lowest score wins** system (like golf scoring)
- **Tiebreaker display** showing 6th and 7th runners
- **Team-by-team breakdowns** with scoring and non-scoring runners clearly identified

### 🏃‍♂️ **Road Race Features**
- **Age group classification** using standard divisions:
  - 1-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, 46-50
  - 51-55, 56-60, 61-65, 66-70, 71+ years
- **Age automatically calculated** from date of birth data
- **Separate standings** for each age group with place numbering
- **Age group summaries** with participation statistics

### 🛡️ **Security & Administration**
- **bcrypt authentication** identical to console and GUI versions
- **Admin control panel** for race management
- **Result editing capabilities** for post-race corrections
- **User session management** with secure logout

## 🛠️ Requirements

### System Requirements
- **Python 3.7+**
- **Web browser** (Chrome, Firefox, Safari, Edge)
- **Network access** for Bootstrap CDN (or local Bootstrap installation)

### Dependencies
```bash
pip install Flask==2.3.3 bcrypt==4.0.1
```

### Required Components
- **Flask** - Web framework
- **bcrypt** - Password hashing (same as console/GUI)
- **Bootstrap 5.3** - UI framework (loaded via CDN)

## 🚀 Installation & Setup

### 1. **Directory Structure** 📁
```
project/
├── console/                    # Console application
├── gui/                       # GUI application  
├── web/                       # Flask application (this)
│   ├── app.py                # Main Flask application
│   ├── requirements.txt      # Python dependencies
│   ├── templates/            # HTML templates
│   │   ├── html_layout.html  # Base template
│   │   ├── index.html        # Dashboard
│   │   ├── individual_results.html
│   │   ├── team_results.html
│   │   ├── age_group_results.html
│   │   ├── cross_country_results.html
│   │   ├── road_race_results.html
│   │   ├── admin.html        # Admin panel
│   │   ├── login.html        # Authentication
│   │   ├── edit_results.html # Result editing
│   │   ├── edit_race.html    # Race editing
│   │   ├── about_us.html     # Static pages
│   │   ├── contact_us.html
│   │   ├── help.html
│   │   ├── documentation.html
│   │   ├── usage_notes.html
│   │   └── footer.html
│   └── static/               # Static files
│       ├── favicon.png
│       └── (other static files)
└── data/                     # Shared data directory
    ├── config.db            # Authentication (shared)
    ├── *.csv               # Runner import files
    └── *.db                # Race databases (shared)
```

### 2. **Installation Steps** 🔧
```bash
# Navigate to web directory
cd project/web

# Install Python dependencies
pip install -r requirements.txt

# Ensure data directory exists (usually created by console/GUI)
mkdir -p ../data
```

### 3. **First Run Setup** 🔐
- **Admin credentials** must be created using the console or GUI application first
- **Race databases** should be created using console or GUI applications
- **Flask app** will automatically detect and display existing races

## 🎮 Usage Guide

### Starting the Web Application
```bash
cd project/web
python app.py
```

**Default Access:**
- **URL:** http://localhost:8080
- **Admin Panel:** http://localhost:8080/admin
- **Login:** http://localhost:8080/login

### 🌐 **Public Interface** (No Login Required)

#### **Dashboard** (`/`)
- **Race type organization** with separate Cross Country and Road Race sections
- **Recent races** display with quick access to results
- **Navigation cards** to race type specific pages

#### **Cross Country Results** (`/cross_country_results`)
- **Complete listing** of all Cross Country race databases
- **Direct links** to individual and team results for each race
- **Race information** including date, race number, and name

#### **Road Race Results** (`/road_race_results`)
- **Complete listing** of all Road Race databases
- **Direct links** to individual and age group results for each race
- **Race information** with type identification

#### **Individual Results** (`/individual_results/<race_id>`)
- **Overall finish order** with positions, bib numbers, names, and times
- **Race type adaptation** - shows team info for CC, age for RR
- **Professional formatting** ready for printing
- **Navigation** to corresponding team or age group results

#### **Team Results** (`/team_results/<race_id>`)
- **Cross Country team scoring** with complete breakdowns
- **Top 5 scoring runners** clearly identified with points
- **Displacers** (6th and 7th runners) for tiebreaking
- **Team rankings** with total scores and individual contributions

#### **Age Group Results** (`/age_group_results/<race_id>`)
- **Road Race age group standings** by division
- **Age group and overall places** for each runner
- **Summary statistics** showing participation by age group

#### **Static Pages**
- **Help** (`/help`) - FAQ and user guidance
- **About Us** (`/about_us`) - Application information
- **Contact Us** (`/contact_us`) - Contact form

### 🔐 **Admin Interface** (Login Required)

#### **Admin Dashboard** (`/admin`)
- **Central control panel** for all admin functions
- **Quick access** to editing, documentation, and system management

#### **Edit Results** (`/edit_results`)
- **Race selection** grouped by date for easy navigation
- **Bib number correction** for individual race results
- **Database updates** with immediate effect

#### **Edit Race** (`/edit_results/<race_id>`)
- **Individual result editing** with finish order preservation
- **Bib number updates** for misassigned finishers
- **Real-time database** updates

#### **Documentation** (`/documentation`)
- **System documentation** and technical information
- **Installation guides** and configuration notes

#### **Usage Notes** (`/usage_notes`)
- **Step-by-step procedures** for race management
- **Best practices** for race day operations
- **Troubleshooting guidance**

## 📊 Database Compatibility

### 🆕 **New Format Support**
- **Cross Country:** `YYYYMMDD-##-cc-[Race_Name].db`
- **Road Race:** `YYYYMMDD-##-rr-[Race_Name].db`
- **Automatic detection** of race type from filename and database content

### 🔄 **Legacy Format Support**
- **Old format:** `YYYYMMDD-##-race.db`
- **Race type detection** from database structure
- **Seamless integration** with existing data

### 🗃️ **Database Structure**

#### **Cross Country Database**
```sql
-- Race type identification
CREATE TABLE race_type (type TEXT);  -- 'cross_country'

-- Runner information
CREATE TABLE runners (
    bib INTEGER PRIMARY KEY,
    name TEXT,
    team TEXT,
    age INTEGER,
    grade TEXT,
    rfid TEXT
);

-- Race results
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bib INTEGER,
    finish_time REAL,          -- Elapsed seconds
    race_date TEXT
);
```

#### **Road Race Database**
```sql
-- Race type identification
CREATE TABLE race_type (type TEXT);  -- 'road_race'

-- Runner information
CREATE TABLE runners (
    bib INTEGER PRIMARY KEY,
    name TEXT,
    dob TEXT,                  -- Date of birth (YYYY-MM-DD)
    age INTEGER,               -- Calculated automatically
    rfid TEXT
);

-- Race results (same structure)
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bib INTEGER,
    finish_time REAL,          -- Elapsed seconds
    race_date TEXT
);
```

#### **Authentication Database** (`config.db`)
```sql
-- Shared with console and GUI applications
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL    -- bcrypt hashed
);
```

## 🔧 Configuration

### **Application Settings**
```python
# In app.py - modify these settings as needed:

# Server configuration
app.run(debug=False, host='0.0.0.0', port='8080')

# Security
app.secret_key = 'your-secret-key-here'  # Change for production

# Paths (relative to app.py)
DATA_DIR = '../data'          # Shared data directory
CONFIG_DB_PATH = '../data/config.db'  # Authentication database
```

### **Production Deployment**
```python
# Use a production WSGI server like Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### **Environment Variables**
```bash
# Optional environment configuration
export FLASK_ENV=production
export FLASK_DEBUG=False
export DATA_DIRECTORY=/path/to/data
```

## 🎨 User Interface

### **Design Principles**
- **Bootstrap 5.3** for responsive, modern design
- **Race type color coding** - Blue for Cross Country, Green for Road Race
- **Professional typography** optimized for readability
- **Print-friendly** CSS for physical result distribution

### **Navigation Flow**
```
Dashboard → Race Type Listing → Individual Race → Specific Results
    ↓              ↓                    ↓              ↓
   Home    Cross Country/Road    Individual Race    Team/Age Group
                  Results           Results           Results
```

### **Responsive Design**
- **Mobile optimized** tables and navigation
- **Tablet friendly** admin interfaces
- **Desktop enhanced** with additional information display

## 🚨 Troubleshooting

### **Common Issues**

#### **🗃️ Database Problems**
```
Problem: "No race results found"
Solutions:
✅ Verify database files exist in ../data/
✅ Check database was created with console/GUI app
✅ Ensure race has completed with results
✅ Verify file permissions allow read access
```

#### **🔐 Authentication Issues**
```
Problem: "Login fails" or "Admin user not found"
Solutions:
✅ Create admin user with console or GUI application first
✅ Verify config.db exists in data directory
✅ Check bcrypt installation: pip install bcrypt
✅ Ensure password is entered correctly
```

#### **🌐 Web Server Problems**
```
Problem: "Flask app won't start"
Solutions:
✅ Check Python version (3.7+ required)
✅ Install dependencies: pip install -r requirements.txt
✅ Verify port 8080 is available
✅ Check file paths and permissions
```

#### **📊 Results Display Issues**
```
Problem: "Team results show as individual only"
Solutions:
✅ Verify race type is correctly detected
✅ Check runners have team information
✅ Ensure minimum 5 runners per team for scoring
✅ Verify database structure matches expected format
```

### **Debug Mode**
```python
# Enable debug mode for development
app.run(debug=True, host='0.0.0.0', port='8080')

# Check database detection
print(f"Found databases: {get_race_databases()}")

# Verify race type detection
print(f"Race type: {get_race_type(db_path)}")
```

### **Log Analysis**
```bash
# Run with logging
python app.py 2>&1 | tee flask.log

# Check for common error patterns
grep -i "error\|exception\|traceback" flask.log
```

## 🔄 Integration Workflow

### **Console → Flask**
1. **Create race** using console application
2. **Import runners** and complete timing
3. **Results automatically available** in Flask interface
4. **Admin editing** available through web interface

### **GUI → Flask**
1. **Create race** using GUI application
2. **Import runners** and complete timing
3. **Results automatically available** in Flask interface
4. **Cross-platform viewing** of same data

### **Flask → Other Applications**
1. **View and edit** results through web interface
2. **Database changes** immediately available to console/GUI
3. **Shared authentication** across all applications

## 🎯 Best Practices

### **🏁 Race Day Setup**
1. **Start Flask app** before race begins
2. **Test admin access** and result editing capabilities
3. **Verify database connectivity** with console/GUI timing
4. **Prepare result display** for spectators and coaches

### **📱 Multi-Device Access**
1. **Timing station** - Use console or GUI for live timing
2. **Results display** - Use Flask on tablet/laptop for public viewing
3. **Admin station** - Use Flask admin panel for corrections
4. **Mobile access** - Responsive design works on phones

### **🔒 Security Considerations**
1. **Change default secret key** for production use
2. **Use HTTPS** in production environments
3. **Restrict admin access** to authorized personnel only
4. **Regular backups** of database files

### **📊 Result Management**
1. **Immediate availability** - Results appear as soon as timing is complete
2. **Real-time updates** - Changes in console/GUI immediately visible
3. **Professional presentation** - Print-ready formatting for distribution
4. **Historical access** - All past races remain accessible

## 📈 Performance & Scalability

### **Database Performance**
- **SQLite efficiency** for race-sized datasets (typically < 1000 runners)
- **Indexed queries** for fast result retrieval
- **Connection pooling** for multiple simultaneous users

### **Web Performance**
- **Bootstrap CDN** for fast UI loading
- **Responsive images** and optimized static files
- **Efficient templating** with Jinja2

### **Concurrent Users**
- **Multi-user support** for viewing results
- **Admin session management** for secure editing
- **Read-only operations** scale well for spectator access

## 📜 License

This project is released under the **MIT License**.

---

## 🙋‍♂️ Support & Documentation

### **Getting Help**
- **Check troubleshooting section** for common issues
- **Review usage notes** for operational procedures
- **Consult help page** in application for user guidance

### **Integration Support**
- **Full compatibility** with console and GUI versions
- **Shared data formats** ensure seamless operation
- **Cross-platform authentication** maintains security

### **Development Notes**
- **Well-documented code** for customization and extension
- **Modern Flask patterns** following best practices
- **Bootstrap framework** for UI consistency and responsiveness

**🎉 Professional Race Management with Modern Web Interface! 🌐🏃‍♀️🏃‍♂️**