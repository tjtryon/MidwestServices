# 📦 Complete Flask Application Package - Cross Country & Road Race Support

## 📁 Directory Structure
```
web/
├── app.py                           # Main Flask application
├── requirements.txt                 # Python dependencies  
├── templates/
│   ├── html_layout.html            # Base template (existing)
│   ├── footer.html                 # Footer (existing)
│   ├── login.html                  # Login page (existing)
│   ├── admin.html                  # Admin dashboard (existing)
│   ├── about_us.html               # About page (existing)
│   ├── contact_us.html             # Contact form (existing)
│   ├── help.html                   # Help page (existing)
│   ├── documentation.html          # Documentation (existing)
│   ├── usage_notes.html            # Usage notes (existing)
│   ├── edit_results.html           # Edit results (existing)
│   ├── edit_race.html              # Edit race (existing)
│   ├── index.html                  # 🆕 UPDATED - Race type dashboard
│   ├── individual_results.html     # 🆕 UPDATED - Race type aware
│   ├── team_results.html           # 🆕 UPDATED - Cross country scoring
│   ├── cross_country_results.html  # 🆕 NEW - CC race listing
│   ├── road_race_results.html      # 🆕 NEW - RR race listing
│   └── age_group_results.html      # 🆕 NEW - Road race age groups
└── static/
    ├── favicon.png                 # Existing favicon
    └── (other static files)        # Any other existing static files
```

## 📋 Installation Steps

### 1. Create requirements.txt
```txt
Flask==2.3.3
bcrypt==4.0.1
```

### 2. Copy File Contents

Copy each file content from the artifacts below into the corresponding file in your directory structure.

## 🔄 Files to Update/Create

### Main Application File
**File:** `app.py`
- Content provided in "Updated Flask App - Cross Country & Road Race Support" artifact above

### New Template Files
**File:** `templates/index.html`  
- Content provided in "Updated index.html - Race Type Support" artifact above

**File:** `templates/cross_country_results.html`
- Content provided in "cross_country_results.html - Cross Country Race Listing" artifact above

**File:** `templates/road_race_results.html`
- Content provided in "road_race_results.html - Road Race Listing" artifact above

**File:** `templates/age_group_results.html`
- Content provided in "age_group_results.html - Road Race Age Group Results" artifact above

**File:** `templates/individual_results.html`
- Content provided in "Updated individual_results.html - Race Type Support" artifact above

**File:** `templates/team_results.html`
- Content provided in "Updated team_results.html - Cross Country Team Scoring" artifact above

## 🚀 Quick Setup Instructions

### Option 1: Manual Setup
1. **Create the directory structure** shown above
2. **Copy your existing templates** (html_layout.html, footer.html, etc.) to the templates folder
3. **Create/update each file** using the content from the artifacts above
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Run the application**: `python app.py`

### Option 2: Automated Setup Script
Create this setup script as `setup_flask_update.py`:

```python
#!/usr/bin/env python3
"""
Setup script for Flask application update
Run this in your web/ directory to create all necessary files
"""

import os

# File contents (you would paste the actual content here)
files_to_create = {
    'requirements.txt': '''Flask==2.3.3
bcrypt==4.0.1''',
    
    # Add other file contents here from the artifacts above
    # 'templates/index.html': '[content from artifact]',
    # 'templates/cross_country_results.html': '[content from artifact]',
    # etc.
}

def create_files():
    for file_path, content in files_to_create.items():
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write file content
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")

if __name__ == '__main__':
    create_files()
    print("\n🎉 Flask application update complete!")
    print("Run: pip install -r requirements.txt")
    print("Then: python app.py")
```

## 🔧 Configuration Notes

### Database Path
The app expects your database files in `../data/` relative to the web directory:
```
project/
├── console/
├── gui/
├── web/          # Flask app here
└── data/         # Databases here
    ├── config.db
    └── *.db      # Race databases
```

### Port Configuration
The app runs on port 8080 by default. Change in `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port='8080')  # Change port here
```

## ✨ New Features Available

### 🏃‍♀️ Cross Country Support
- Automatic detection of Cross Country databases
- Team scoring with top 5 + displacers
- Professional team standings display
- Tiebreaker handling

### 🏃‍♂️ Road Race Support  
- Automatic detection of Road Race databases
- Age group classification (1-15, 16-20, etc.)
- Individual and age group results
- Age calculated from date of birth

### 🔄 Backward Compatibility
- Works with existing old-format databases
- Maintains all existing admin functionality
- Same authentication system
- Existing URLs still work

## 🧪 Testing the Update

### 1. Test Database Detection
- Create databases using console/GUI applications
- Verify they appear correctly categorized on dashboard

### 2. Test Cross Country Features
- Create CC database with team data
- Import runners with team information
- Complete a race and verify team scoring

### 3. Test Road Race Features
- Create RR database with age data
- Import runners with date of birth
- Complete a race and verify age group results

### 4. Test Backward Compatibility
- Load old database files
- Verify they still display properly
- Check that admin functions work

## 🔍 Troubleshooting

### Common Issues
1. **Templates not found**: Ensure template files are in `/templates` subdirectory
2. **Database not detected**: Check file naming format and location
3. **Race type unknown**: Verify database has `race_type` table
4. **Permission errors**: Check file permissions in data directory

### Debug Mode
Enable debug mode for development:
```python
app.run(debug=True, host='0.0.0.0', port='8080')
```

## 📞 Support
- All features maintain compatibility with console and GUI versions
- Database files are interchangeable between all three applications
- Same authentication system across all applications

---

## 🎉 Deployment Ready!

This updated Flask application provides:
✅ **Complete race type support**  
✅ **Professional results display**  
✅ **Backward compatibility**  
✅ **Integrated authentication**  
✅ **Print-ready formatting**  
✅ **Responsive design**

Your Flask application is now fully integrated with the console and GUI versions!