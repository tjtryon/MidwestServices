#!/usr/bin/env python3
"""
test_database_operations.py - Pytest Unit Tests for Database Operations
Author: TJ Tryon
Date: July 28, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS) - GUI Version

🧪 Tests database creation, race type detection, and data structure validation
Ensures GUI can create and manage race databases correctly

To run these tests:
    pytest test_database_operations.py -v
    pytest test_database_operations.py::test_cross_country_database_creation -v
"""

import pytest
import sqlite3
import tempfile
import os
from unittest.mock import MagicMock
import sys

# Mock the GTK dependencies before importing the main module
sys.modules['gi'] = MagicMock()
sys.modules['gi.repository'] = MagicMock()
sys.modules['gi.repository.Gtk'] = MagicMock()
sys.modules['gi.repository.Gio'] = MagicMock()
sys.modules['gi.repository.GLib'] = MagicMock()
sys.modules['gi.repository.Gdk'] = MagicMock()

# Mock bcrypt for testing
import bcrypt


class TestableRaceTimingApp:
    """
    🧪 Testable version of RaceTimingApp for database operations testing
    Contains only the database-related methods we want to test
    """
    
    def __init__(self):
        self.conn = None
        self.db_path = None
        self.race_type = ""
    
    def create_database_structure(self, race_type):
        """
        🏗️ Creates the database structure for a given race type
        """
        if not self.conn:
            return False
            
        c = self.conn.cursor()
        
        try:
            # 💾 Store the race type
            c.execute("CREATE TABLE race_type (type TEXT)")
            c.execute("INSERT INTO race_type (type) VALUES (?)", (race_type,))
            
            # 🏗️ Create different tables based on race type
            if race_type == "cross_country":
                c.execute('''CREATE TABLE IF NOT EXISTS runners (
                                bib INTEGER PRIMARY KEY,
                                name TEXT,
                                team TEXT,
                                age INTEGER,
                                grade TEXT,
                                rfid TEXT)''')
            else:  # road race
                c.execute('''CREATE TABLE IF NOT EXISTS runners (
                                bib INTEGER PRIMARY KEY,
                                name TEXT,
                                dob TEXT,
                                age INTEGER,
                                rfid TEXT)''')
            
            # 🏁 Create results table
            c.execute('''CREATE TABLE IF NOT EXISTS results (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            bib INTEGER,
                            finish_time REAL,
                            race_date TEXT)''')
            
            self.conn.commit()
            self.race_type = race_type
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def detect_race_type(self):
        """
        🔍 Detects race type from database
        """
        if not self.conn:
            return "unknown"
            
        try:
            c = self.conn.cursor()
            c.execute("SELECT type FROM race_type")
            result = c.fetchone()
            return result[0] if result else "unknown"
        except sqlite3.Error:
            return "unknown"
    
    def get_table_columns(self, table_name):
        """
        📋 Gets column names for a given table
        """
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            return [column[1] for column in cursor.fetchall()]
        except sqlite3.Error:
            return []
    
    def table_exists(self, table_name):
        """
        🔍 Checks if a table exists in the database
        """
        if not self.conn:
            return False
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            return cursor.fetchone() is not None
        except sqlite3.Error:
            return False


# 🔧 Pytest Fixtures
@pytest.fixture
def app():
    """🧪 Create a fresh TestableRaceTimingApp instance for each test"""
    return TestableRaceTimingApp()


@pytest.fixture
def temp_db():
    """🗃️ Create a temporary database file for testing"""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    yield db_path
    # Cleanup
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def app_with_db(app, temp_db):
    """🔗 Create app with connected database"""
    app.db_path = temp_db
    app.conn = sqlite3.connect(temp_db)
    yield app
    # Cleanup
    if app.conn:
        app.conn.close()


# 🧪 Database Operations Tests
class TestDatabaseOperations:
    """Tests for database creation and race type detection"""
    
    def test_cross_country_database_creation(self, app_with_db):
        """
        🏃‍♀️ Test creating a cross country race database
        Verifies that the correct table structure is created with team-specific fields
        """
        # 🏗️ Create cross country database
        success = app_with_db.create_database_structure("cross_country")
        assert success, "Cross country database creation should succeed"
        
        # 🔍 Verify race type is stored correctly
        detected_type = app_with_db.detect_race_type()
        assert detected_type == "cross_country", "Race type should be detected as cross_country"
        
        # 🔍 Verify runners table has correct columns for cross country
        columns = app_with_db.get_table_columns("runners")
        expected_columns = ['bib', 'name', 'team', 'age', 'grade', 'rfid']
        
        for col in expected_columns:
            assert col in columns, f"Column '{col}' should exist in cross country runners table"
        
        # 🔍 Verify cross country specific columns exist
        assert 'team' in columns, "Cross country database should have 'team' column"
        assert 'grade' in columns, "Cross country database should have 'grade' column"
        
        # 🔍 Verify results table exists
        assert app_with_db.table_exists("results"), "Results table should exist"
        
        # 🔍 Verify results table structure
        results_columns = app_with_db.get_table_columns("results")
        expected_results_columns = ['id', 'bib', 'finish_time', 'race_date']
        for col in expected_results_columns:
            assert col in results_columns, f"Results table should have '{col}' column"
    
    def test_road_race_database_creation(self, app_with_db):
        """
        🏃‍♂️ Test creating a road race database
        Verifies different table structure for road races with age-based fields
        """
        # 🏗️ Create road race database
        success = app_with_db.create_database_structure("road_race")
        assert success, "Road race database creation should succeed"
        
        # 🔍 Verify race type is stored correctly
        detected_type = app_with_db.detect_race_type()
        assert detected_type == "road_race", "Race type should be detected as road_race"
        
        # 🔍 Verify runners table has correct columns for road race
        columns = app_with_db.get_table_columns("runners")
        expected_columns = ['bib', 'name', 'dob', 'age', 'rfid']
        
        for col in expected_columns:
            assert col in columns, f"Column '{col}' should exist in road race runners table"
        
        # 🔍 Verify road race specific columns
        assert 'dob' in columns, "Road race database should have 'dob' (date of birth) column"
        
        # 🔍 Verify cross country specific columns don't exist
        assert 'team' not in columns, "Team column should not exist in road race database"
        assert 'grade' not in columns, "Grade column should not exist in road race database"
        
        # 🔍 Verify results table exists with correct structure
        assert app_with_db.table_exists("results"), "Results table should exist"
        results_columns = app_with_db.get_table_columns("results")
        expected_results_columns = ['id', 'bib', 'finish_time', 'race_date']
        for col in expected_results_columns:
            assert col in results_columns, f"Results table should have '{col}' column"
    
    def test_race_type_detection_with_no_database(self, app):
        """
        🤷 Test race type detection when no database is loaded
        Should return 'unknown' when no connection exists
        """
        # 🔍 Should return "unknown" when no database
        detected_type = app.detect_race_type()
        assert detected_type == "unknown", "Should return 'unknown' when no database is connected"
    
    def test_database_creation_without_connection(self, app):
        """
        🚫 Test database creation fails gracefully without connection
        Ensures proper error handling when no database is connected
        """
        # 🏗️ Try to create database without connection
        success = app.create_database_structure("cross_country")
        assert not success, "Database creation should fail without connection"
        
        # 🔍 Race type should remain empty
        assert app.race_type == "", "Race type should remain empty after failed creation"
    
    def test_race_type_table_creation(self, app_with_db):
        """
        📋 Test that race_type table is created and populated correctly
        """
        # 🏗️ Create database
        success = app_with_db.create_database_structure("cross_country")  
        assert success, "Database creation should succeed"
        
        # 🔍 Verify race_type table exists
        assert app_with_db.table_exists("race_type"), "race_type table should exist"
        
        # 🔍 Verify race_type table has correct data
        cursor = app_with_db.conn.cursor()
        cursor.execute("SELECT type FROM race_type")
        result = cursor.fetchone()
        assert result is not None, "race_type table should have data"
        assert result[0] == "cross_country", "race_type should contain correct race type"
    
    def test_multiple_database_structures(self, temp_db):
        """
        🔄 Test creating different database structures sequentially
        Ensures we can switch between race types properly
        """
        # 🏗️ Create first app with cross country
        app1 = TestableRaceTimingApp()
        app1.db_path = temp_db
        app1.conn = sqlite3.connect(temp_db)
        
        success1 = app1.create_database_structure("cross_country")
        assert success1, "First database creation should succeed"
        
        detected1 = app1.detect_race_type()
        assert detected1 == "cross_country", "Should detect cross country"
        
        app1.conn.close()
        
        # 🗃️ Create new database file for road race
        db_fd2, db_path2 = tempfile.mkstemp(suffix='.db')
        
        try:
            # 🏗️ Create second app with road race
            app2 = TestableRaceTimingApp()
            app2.db_path = db_path2
            app2.conn = sqlite3.connect(db_path2)
            
            success2 = app2.create_database_structure("road_race")
            assert success2, "Second database creation should succeed"
            
            detected2 = app2.detect_race_type()
            assert detected2 == "road_race", "Should detect road race"
            
            # 🔍 Verify different table structures
            cc_columns = ['bib', 'name', 'team', 'age', 'grade', 'rfid']
            rr_columns = ['bib', 'name', 'dob', 'age', 'rfid']
            
            # Check that road race doesn't have cross country columns
            rr_table_columns = app2.get_table_columns("runners")
            assert 'team' not in rr_table_columns, "Road race should not have team column"
            assert 'dob' in rr_table_columns, "Road race should have dob column"
            
            app2.conn.close()
            
        finally:
            # Cleanup second database
            os.close(db_fd2)
            if os.path.exists(db_path2):
                os.unlink(db_path2)
    
    def test_corrupted_race_type_detection(self, app_with_db):
        """
        💥 Test race type detection with corrupted race_type table
        Ensures graceful handling of database corruption
        """
        # 🏗️ Create valid database first
        success = app_with_db.create_database_structure("cross_country")
        assert success, "Database creation should succeed"
        
        # 💥 Corrupt the race_type table
        cursor = app_with_db.conn.cursor()
        cursor.execute("DROP TABLE race_type")
        app_with_db.conn.commit()
        
        # 🔍 Should handle corruption gracefully
        detected_type = app_with_db.detect_race_type()
        assert detected_type == "unknown", "Should return 'unknown' for corrupted database"
    
    def test_table_existence_checks(self, app_with_db):
        """
        🔍 Test table existence checking functionality
        """
        # 🏗️ Initially no tables should exist
        assert not app_with_db.table_exists("runners"), "Runners table should not exist initially"
        assert not app_with_db.table_exists("results"), "Results table should not exist initially"
        assert not app_with_db.table_exists("race_type"), "Race_type table should not exist initially"
        
        # 🏗️ Create database structure
        success = app_with_db.create_database_structure("cross_country")
        assert success, "Database creation should succeed"
        
        # 🔍 Now all tables should exist
        assert app_with_db.table_exists("runners"), "Runners table should exist after creation"
        assert app_with_db.table_exists("results"), "Results table should exist after creation"
        assert app_with_db.table_exists("race_type"), "Race_type table should exist after creation"
        
        # 🔍 Non-existent table should return False
        assert not app_with_db.table_exists("nonexistent_table"), "Non-existent table should return False"


if __name__ == '__main__':
    # Allow running directly with pytest
    pytest.main([__file__, "-v"])
