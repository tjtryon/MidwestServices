# 🏁 The Race Timing System for Cross Country and Road Races

#### 🎥 Video Demo:  
https://screencast.apps.chrome/1_XrlQ1KQMBhTI8uI_GSWxkW2fpADs48O?createdTime=2025-07-05T16%3A36%3A31.661Z

---

#### 📄 Description

My program, as submitted, has 2 versions. The current project is the console application found in the `project/console` directory. I additionally have a `project/gui` directory which is an application I intend to work on when I take the CS50 Python class next. For the purposes of this project, the scope is only the `project/console` portion of the application.

---

`project/console` is a fully functional cross country and road race program that works with various timing systems, including RFID chip timing. The program is divided into 2 parts:
- ⚙️ The backend program, responsible for the race logic, is a Python script.
- 🌐 The front end is a Flask application for end user access to race results and admin access to manage the race.

---

The backend Python script is menu driven:
- 🔍 On first launch, it looks for a `config.db` file in the `/data` directory.
    - ✅ If found, it notifies the timing person that the config database is loaded.
    - ❌ If not found, it creates a new one and prompts for a username and password for administrative functions.
- 🛠️ In the timing program, you have options to:
    - ➕ Create a new race database
    - 📂 Load an existing database
    - 👥 Load runners into the database
- 📁 Race databases are in the `/data` directory:
    - Named `YYYYMMDD-##-race.db`
    - The name consists of the date, and the `##` is the race number for that date.

---

Once the race database is created and users are loaded:
- 🏁 Start the race by selecting the start race option. You will be prompted to:
    - ⌨️ Enter a bib number and hit Enter to record a time
    - 🚫 Press Enter without a bib number to record a bib "0"
    - 🔧 Fix unknown bibs after the race
    - ✅ Type `exit` to exit the race timing portion after all runners finish

---

The console application allows you to view:
- 🏃 Individual results
- 🤝 Team results
- 📋 List all runners who were in the race

Finally, you can exit The Race Timing System console by selecting the quit option.

---

Once the race has completed, you can view the results and manage the race from the Flask application:
- 🌍 The Flask application lists all race databases found in the `/data` directory on the `index.html` page, with links to individual and team results.
- The menu also contains links for:
    - ❓ Help, which displays a FAQ
    - ✉️ A contact us form

For admins:
- 🔑 Log in to access the admin console. On the admin console, you will find:
    - 🛠️ A link to edit the race results
    - 📄 View the documentation
    - 📚 View the usage instructions

(Admin access is secured with the password created by the console program.)

---

## 🚧 Future Work

- 🖥️ GTK GUI for desktop use
- 🌐 Enhanced Flask features

In the future, when I work on the CS50 Python class, I will expand this project by building a Python-based GTK GUI. This version will offer greater functionality for race-day management. I will also extend the Flask app to handle post-race tasks such as editing results and providing lookup tools for participants. This work is not part of my CS50x final project but demonstrates how I applied and extended my learning beyond the course.

---

## 🔢 Version Info

### Current Version 
**0.8**

---

### Planned Features for Version 1.0:
- 🖥️ Complete GUI version using Python GTK
- 📊 Improved race day reporting tools
- 👥 Admin user management system
- 🔌 REST API for external race management apps

---

## 🤝 Contributing

If you'd like to contribute:
1. 🍴 Fork the repository
2. 🌱 Create a new branch for your feature or fix
3. 📬 Submit a pull request describing your changes

Contributions are welcome for:
- 🛡️ Improving documentation
- 🐛 Bug fixes
- 🔗 Adding new timing system integrations
- 🎨 Enhancing the user interface

---

## 📝 License

This application is being released under the MIT license.

---

## ©️ Copyright

This project is &copy;2025 by TJ Tryon, All rights reserved.