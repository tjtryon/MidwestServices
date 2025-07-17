# Midwest Event Services, Inc.

**MidwestServices** is the official GitHub repository hub for all software projects maintained by [Midwest Event Services, Inc.](https://midwest.services), an Indiana-based not-for-profit organization. This repository houses applications and tools designed to support events and race management systems, particularly cross-country and road race timing solutions.

---

## 🎯 Mission

To build open-source, cross-platform, and accessible timing and event software that meets the needs of race organizers, schools, and community events — with reliability, accuracy, and ease of use in mind.

---

## 🏁 Featured Project: Race Timing System

A robust, flexible race timing and scoring system built in Python with optional GUI and web interface support.

### 🔧 Features

- ✅ Console and GTK-based GUI modes
- ✅ RFID chip timing via file watcher and TCP/telnet
- ✅ Manual timing with keyboard input
- ✅ Sound alerts on runner detection
- ✅ Live team and individual scoring
- ✅ SQLite database per race (with auto backups)
- ✅ Flask web server for real-time results
- ✅ Bootstrap-styled Jinja templates for clean output
- ✅ Camera photo capture integration
- ✅ Admin tools for editing and managing runners
- ✅ Exportable HTML, CSV, and Matplotlib charts
- ✅ Support for multiple races, heats, and backup/restore

### 📂 Directory Structure

```
MidwestServices/
├── console/              # Console version of race timing app
│   ├── race_timing_console.py
│   └── data/
├── gui/                  # GTK GUI version
├── web/                  # Flask web server
│   ├── app.py
│   └── templates/
└── docs/                 # User manuals and technical specs
```

### 🚀 Get Started

```bash
cd console
python3 race_timing_console.py
```

Or run the web interface:

```bash
cd web
python3 app.py
```

---

## 📁 Other Projects

This repository will grow to include additional utilities, timing extensions, and event management tools, such as:

- 🗂️ Registration import/export tools
- 📊 Reporting dashboards
- 📱 Mobile-compatible timer interfaces
- 🎥 Live results display boards

---

## 🤝 Contributing

We welcome community contributions, ideas, and bug reports. Feel free to open an issue or submit a pull request!

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Maintained by

**Midwest Event Services, Inc.**  
Arcadia, Indiana  
[https://midwest.services](https://midwest.services)
