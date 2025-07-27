# 🏁 TRTS: The Race Timing Solution for Cross Country and Road Races 🏃‍♀️🏃‍♂️

🎉 Welcome to **TRTS** – a super cool and **free** tool to help time runners at **cross country** and **road races**!

TRTS helps coaches, race timers, and volunteers keep track of every runner and show results live online! 📱💨

---

## 📦 What’s in the TRTS System?

TRTS has **3 main parts** that work together:

### 🖥️ 1. Console App (The Brain in the Box)
This runs on a tiny computer (like a Raspberry Pi) inside a **Pelican case** with:
- 🔋 A battery so it works all day
- 📺 A little screen to see times
- 📶 A scanner for RFID tags
- 🌐 A fast **5G internet connection** to send results to the cloud

It can:
- ✅ Record finish times when someone finishes
- ⌛ Save missed times to fix later
- ☁️ Send all data to the website in real time
- 🔔 Beep every time someone finishes!

This part lives in the `/console/` folder.

---

### 👓 2. GUI App (The Race Control Panel)

This is the computer program you use to:
- Click to **start** or **stop** the race 🟢🔴
- Enter bib numbers as runners finish ⌨️
- See team and individual results right away 🏃‍♂️🏆
- Hear a **beep sound** (from `beep.mp3`) each time a runner finishes! 🔊

It lives in the `/gui/` folder on the laptop.

---

### 🌐 3. Web App (The Online Results Page)

This is what runners, fans, and coaches see online:
- 📄 All the races and results
- 👥 Team scores and rankings
- ✏️ Admins can fix bib numbers after the race
- Works on phones, tablets, and computers

The web app runs in the **cloud**, in a folder called `/web/`.

---

## 🧠 How It Works

1. Load runners from a CSV file (just a spreadsheet!)
2. Start the race ⏱️
3. Type bib numbers or scan RFID tags as runners finish
4. Fix any missed numbers later (like bib "0")
5. Results show up instantly on the website! 🖥️📶

---

## 📁 Folder Map (Directory Layout)

Here’s what the TRTS system looks like:

```
📂 / (Main Project Folder)
├── 📁 data/              # Stores all race results and RFID input
│   ├── config.db
│   ├── rfid_input.txt
│   └── YYYYMMDD-##-race.db

├── 📁 docs/              # Help files and instructions

├── 📁 console/           # Console app for reader box
│   └── race_timing_console.py

├── 📁 gui/               # GUI app for laptops
│   ├── race_timing_gui.py
│   └── beep.mp3

├── 📁 web/               # Flask web app in the cloud
│   ├── app.py
│   ├── __pycache__/          # Python cache
│   ├── static/               # Images, CSS, favicon
│   │   └── favicon.ico
│   └── templates/            # Web pages
│       ├── _navbar.html
│       ├── about_us.html
│       ├── admin.html
│       ├── contact_us.html
│       ├── documentation.html
│       ├── footer.html
│       ├── login.html
│       └── usage_notes.html
```

---

## 🎯 How to Run a Race

1. Open the GUI or Console App 🖥️
2. Load the runners list 📋
3. Click “Start Race” 🟢
4. Enter bib numbers or let the scanner read RFID tags
5. When the last runner finishes, type `exit`
6. Results appear online for everyone to see! 🌍

---

## 🔧 What You Need

- 🐍 Python 3.8 or newer
- 🖼️ GTK 4 for the GUI
- 🌐 Flask for the website
- 📦 Some Python tools:
  ```bash
  pip install playsound watchdog flask PyGObject
  ```

---

## 📊 Sample Runners File (CSV)

Here’s what a runners list looks like:

```
bib,full_name,team,rfid
101,John Harvard,Harvard Crimson,30422354
102,Mary Sue,Harvard Crimson,30422355
103,Handsome Dan,Yale Bulldogs,30422356
```

Save this as `runners.csv` and load it into TRTS!

---

## 🏆 What Results Look Like

### 📄 Individual Results:
```
POS   BIB   NAME           TEAM             TIME
1     101   John Harvard   Harvard Crimson  16:45.123
2     103   Dan Bulldog    Yale Bulldogs    17:02.789
```

### 🥇 Team Results:
```
🏆 Harvard Crimson - Score: 25
101 John Harvard    16:45.123
102 Mary Sue        17:10.456
... (top 5 runners + displacers)
```

---

## ☁️ Cloud System

- The console box sends results to the **Red Hat cloud**
- The Flask web app shows them instantly online
- Admins can log in to fix bibs or update times

---

## 🧠 Why It’s Great

- 🆓 It’s totally free!
- 🧩 All files and plans are open-source
- 🛍️ You can build it yourself or buy one ready-to-go
- 📄 MIT License = anyone can use or improve it

---

## 📬 Need Help?

👨‍💻 Developer: **TJ Tryon**  
📧 Email: [tj@tjtryon.com](mailto:tj@tjtryon.com)  
📱 Phone: 317-774-8762  
🏢 Midwest Event Services, Inc.

---

## 📜 License

MIT License © 2025  
You can use it, change it, and share it — just keep it open! 💡🛠️

---

**Made with ❤️ for the running community.**

🏃‍♀️🏃‍♂️ *TRTS: Timing you can trust.* ⏱️🌟
