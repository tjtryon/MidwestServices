# The Race TIming System for Cross Country and Road Races (TRTS)

This is a simple Flask web application for managing and displaying cross country race results. This program is used in conjunction with the console version of the The Race TIming System for Cross Country and Road Races (TRTS). This Flask application supports the web functions of The Race TIming System for Cross Country and Road Races (TRTS), which is specifically to allow the end users (runners, coaches, officials, supporters) to look up a runner's individual results, as well as results for the team. While it is tailored to showing the results of a cross country meet, the individual_results portion can be used by itself to show results of any sort of running race, be it a simple 5K to a marathon, and beyond. It has been built to handle multiple databases, to allow for viewing the results of an entire cross country meet, with multiple age group, grade, or gender races, utilizing the same databases that the console version of The Race TIming System for Cross Country and Road Races (TRTS). 


It supports:
- Listing all races.
- Viewing individual results.
- Viewing team results.
- Admin pages for editing results, usage instructions, and documentation.

---

## 📂 Project Structure for the Flask Application

```
/console/
├── /web/              # Contains app.py and templates
│   ├── app.py
│   ├── /templates/
│   │   ├── index.html
│   │   ├── individual_results.html
│   │   ├── team_results.html
│   │   ├── admin.html
│   │   ├── edit_results.html
│   │   ├── race_timing_system_documentation.html
│   │   ├── usage_notes.html
│   │   ├── _navbar.html
│   └── /static/      # (Optional) for CSS/JS if needed
├── /data/             # Stores SQLite race databases and runners.csv files
│   ├── YYYYMMDD-##-race.db
│   ├── runners.csv
│  
│   
│
 ```

## ⚙️ Requirements

- Python 3.8+
- Flask

Install dependencies:
```bash
pip install Flask
```

---

## 🚀 Running the Application

From the `/console/web` directory, run:

```bash
python app.py
```

The app will start in debug mode and be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🗂️ Features

### Home Page
- Lists all available races (SQLite files in `/data`).
- Links to individual and team results for each race.

### Individual Results
- Shows ordered finish times for all runners.

### Team Results
- Groups runners by team and calculates team scores based on finish positions.

### Admin Pages
- **Admin Dashboard**: Links to edit results, documentation, and usage notes.
- **Edit Results**: Select a race and update bib numbers inline. Changes are saved back to the database.
- **Documentation**: Shows any relevant system documentation.
- **Usage Instructions**: Displays usage notes for the system.

---

## 🗃️ Database Files

- Race databases must be named: `YYYYMMDD-##-race.db`
  - Example: `20240616-01-race.db`
- They must be located inside the `/console/data/` directory.
- Each race database must have a `results` table and `runners` table:
  - `results`: Should include bib numbers, finish times, etc.
  - `runners`: Should map bib numbers to names and teams and optionally to the bib RFID tag number.

---

## 🗃️ Runner Import Files

- Runner import files may be baned anything, but it is suggested to use the format: `YYYYMMDD-##-race.db`
    where YYYYMMDD is the year, month and 2 digit day, ## is the 2 digit race number.
  - Example: `20240616-01-race.csv`
- They must be located inside the `/console/data/` directory.
- Each runner import file must be a CSV (Comma Separated Values) in the following format:
    Bib, Name, Team, RFID
    101, John Harvard, Harvard Crimson,30422354
    102, Mary Sue, Harvard Crimson,30422355
    103, Handsome Dan, Yale Bulldogs,30422356


---

## ✏️ Editing Results

1. Go to `/edit_results`.
2. Select a race from the dropdown.
3. Edit bib numbers inline.
4. Click **Save Changes** to update the database.

---

## 📝 Notes

- Templates automatically include a navigation bar (`_navbar.html`) to switch between admin pages.
- Be sure to shut down the server before directly modifying `.db` files.
- For production, configure proper paths and security settings.

---

## ✅ To Do

- Add authentication for admin pages.
- Implement advanced validation when updating bib numbers.
- Improve styling with Bootstrap or custom CSS.

---

## 📄 License

This project released under the MIT License

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Please fork the repository and submit pull requests.

For questions or support, please contact TJ Tryon at tj@tjtryon.com
