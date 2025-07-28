# 🚀 TRTS Quick Start Guide 🏃‍♀️🏃‍♂️

**Get up and running with The Race Timing Solution in under 10 minutes!**

---

## ⚡ Before You Start

**What you need:**
- Computer with Python 3.7+ installed
- Spreadsheet with runner information (CSV format)
- 5-10 minutes for setup

**Choose your interface:**
- 🖥️ **Console** - Simple, reliable, great for learning
- 🎨 **GUI** - Visual interface, user-friendly
- 🌐 **Web** - Online results viewing (requires Console or GUI for timing)

---

## 📦 Step 1: Installation

### Option A: Console Application (Recommended for beginners)
```bash
# Install required packages
pip install bcrypt playsound

# Download and navigate to project
cd race-timing-solution
```

### Option B: GUI Application  
```bash
# Linux/Ubuntu - Install GTK4
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0
pip install bcrypt

# Navigate to project
cd race-timing-solution
```

### Option C: Web Application (For results viewing)
```bash
# Navigate to web directory
cd race-timing-solution/web
pip install -r requirements.txt
```

---

## 🔐 Step 2: First-Time Setup (30 seconds)

**Run any application to create admin account:**

```bash
# Console
python3 console/race_timing_console.py

# OR GUI
python3 gui/race_timing_gui.py
```

**Follow the prompts:**
1. Enter admin username (remember this!)
2. Enter admin password (remember this!)
3. ✅ Setup complete!

---

## 🏃‍♀️ Step 3A: Cross Country Race (3 minutes)

### Create Race Database
**Console:** Choose option `1) Create new database`
**GUI:** Click `Create New Database`

1. Select **"Cross Country"** as race type
2. Enter race number: `01`
3. Enter race name: `County_Meet`
4. ✅ Database created: `20250727-01-cc-County_Meet.db`

### Prepare Runner Data
**Create CSV file** with this format:
```csv
bib,name,team,age,grade,rfid
101,John Smith,Lincoln High,16,11,
102,Jane Doe,Roosevelt MS,14,8,
103,Mike Johnson,Central HS,17,12,
```

### Import Runners
**Console:** Choose option `3) Load runners from CSV`
**GUI:** Click `Load Runners from CSV`

1. Select your CSV file
2. ✅ Runners imported!

### Start Race
**Console:** Choose option `5) Start the race`
**GUI:** Click `Start the Race`

**During race:**
- Enter bib numbers as runners finish: `101 [Enter]`
- Race clock shows elapsed time
- Type `exit` when done

### View Results
**Console:** 
- Option `6) Show individual results`
- Option `7) Show team results`

**GUI:** 
- Click `Show Individual Results`
- Click `Show Team Results`

---

## 🏃‍♂️ Step 3B: Road Race (3 minutes)

### Create Race Database
**Console:** Choose option `1) Create new database`
**GUI:** Click `Create New Database`

1. Select **"Road Race"** as race type
2. Enter race number: `01`
3. Enter race name: `5K_Fun_Run`
4. ✅ Database created: `20250727-01-rr-5K_Fun_Run.db`

### Prepare Runner Data
**Create CSV file** with this format:
```csv
bib,name,dob,rfid
201,Sarah Wilson,1985-03-15,
202,Tom Brown,1992-07-22,
203,Lisa Davis,1978-11-08,
```

### Import Runners
**Console:** Choose option `3) Load runners from CSV`
**GUI:** Click `Load Runners from CSV`

1. Select your CSV file
2. ✅ Runners imported!

### Start Race
**Console:** Choose option `5) Start the race`
**GUI:** Click `Start the Race`

**During race:**
- Enter bib numbers as runners finish: `201 [Enter]`
- Race clock shows elapsed time
- Type `exit` when done

### View Results
**Console:** 
- Option `6) Show individual results`
- Option `7) Show age group results`

**GUI:** 
- Click `Show Individual Results`
- Click `Show Age Group Results`

---

## 🌐 Step 4: Web Results (Optional - 2 minutes)

### Start Web Application
```bash
cd web
python3 app.py
```

### View Results Online
1. Open browser: http://localhost:8080
2. See your race results instantly!
3. **Admin login** (use credentials from Step 2):
   - Go to: http://localhost:8080/admin
   - Edit results if needed

---

## 🎯 Quick Reference

### File Locations
```
project/
├── console/race_timing_console.py    # Console app
├── gui/race_timing_gui.py           # GUI app  
├── web/app.py                       # Web app
└── data/                            # Auto-created
    ├── config.db                    # Your admin login
    ├── *.csv                        # Runner files you create
    └── *.db                         # Race databases
```

### CSV Formats
| Race Type | Required Columns |
|-----------|------------------|
| **Cross Country** | `bib,name,team,age,grade,rfid` |
| **Road Race** | `bib,name,dob,rfid` |

### Database Naming
| Format | Example |
|--------|---------|
| Cross Country | `20250727-01-cc-County_Meet.db` |
| Road Race | `20250727-01-rr-5K_Fun_Run.db` |

---

## 🚨 Quick Troubleshooting

### "Button is grayed out"
- **Console**: Load database first, then import runners
- **GUI**: Follow the button states - they guide you through the process

### "CSV import failed"
- Check column headers match exactly
- Cross Country: `bib,name,team,age,grade,rfid`
- Road Race: `bib,name,dob,rfid`

### "No results showing"
- Complete at least one race first
- Check you entered bib numbers during timing

### "Can't login to web app"
- Create admin account with Console or GUI first
- Use same username/password across all apps

---

## 🎉 You're Ready!

**What you can do now:**
- ✅ Time races with Console or GUI
- ✅ View results in professional format
- ✅ Share results online with Web app
- ✅ Edit results after races
- ✅ Handle both Cross Country and Road Races

**Next steps:**
- Read full documentation for advanced features
- Customize for your specific needs
- Train volunteers on your preferred interface

---

## 📞 Need Help?

**Quick answers:** Check the troubleshooting section above
**Detailed help:** See the main README.md for each component
**Support:** Contact TJ Tryon at tj@tjtryon.com

---

**🏃‍♀️🏃‍♂️ Happy Racing! ⏱️**

*Time to focus on the race, not the technology.*