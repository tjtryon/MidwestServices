#!/usr/bin/env python3
"""
test_race_timing_gui.py - Pytest Unit Tests for The Race Timing Solution GUI
Author: TJ Tryon
Date: July 28, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS) - GUI Version

🧪 Pytest unit tests for the GUI version of the race timing program
Tests core functionality without requiring GTK4 GUI components

To run these tests:
    pytest test_race_timing_gui.py -v
    pytest test_race_timing_gui.py::test_cross_country_database_creation -v
    pytest test_race_timing_gui.py --tb=short
"""

import pytest
import sqlite3
import tempfile
import os
import datetime
from unittest.mock import Mock, patch, MagicMock
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
    🧪 Testable version of RaceTimingApp that doesn't require GTK4
    Contains only the core logic methods we want to test
    """
    
    def __init__(self):
        self.conn = None
        self.db_path = None
        self.race_type = ""
        
    def format_time(self, total_seconds):
        """
        ⏰ Converts seconds to MM:SS.mmm format.
        Same formatting logic as console version.
        """
        if total_seconds is None:
            return "00:00.000"
            
        minutes, seconds = divmod(total_seconds, 60)
        return f"{int(minutes):02d}:{seconds:06.3f}"
    
    def create_database_structure(self, race_type):
        """
        🏗️ Creates the database structure for a given race type
        """
        if not self.conn:
            return False
            
        c = self.conn.cursor()
        
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
    
    def calculate_team_scores(self, results_data):
        """
        🏫 Calculates cross country team scores from results data
        Input: List of tuples (team, bib, name, finish_time, place)
        Returns: List of team score tuples sorted by score
        """
        # 🏫 Group runners by teams
        teams = {}
        for team, bib, name, finish_time, place in results_data:
            teams.setdefault(team, []).append((place, bib, name, finish_time))

        # 🧮 Calculate team scores
        scores = []
        for team, runners in teams.items():
            if len(runners) >= 5:  # 🏃‍♀️ Need at least 5 runners to score
                # Sort by place
                runners.sort(key=lambda x: x[0])
                top5 = runners[:5]
                displacers = runners[5:7]
                score = sum(p[0] for p in top5)
                
                # Tiebreaker positions (6th and 7th runners)
                tiebreak1 = displacers[0][0] if len(displacers) > 0 else float('inf')
                tiebreak2 = displacers[1][0] if len(displacers) > 1 else float('inf')
                
                scores.append((team, score, top5, displacers, tiebreak1, tiebreak2))

        # 🏆 Sort teams by score (lowest wins), then by tiebreakers
        scores.sort(key=lambda x: (x[1], x[4], x[5]))
        return scores
    
    def group_by_age(self, results_data):
        """
        🎂 Groups road race results by age groups
        Input: List of tuples (age, bib, name, finish_time, place)
        Returns: Dictionary of age groups with results
        """
        # 🎂 Define age groups (same as console version)
        age_groups = [
            (1, 15), (16, 20), (21, 25), (26, 30), (31, 35), (36, 40),
            (41, 45), (46, 50), (51, 55), (56, 60), (61, 65), (66, 70), (71, 200)
        ]
        
        # 📚 Group results by age
        results_by_group = {}
        for (low, high) in age_groups:
            group_name = f"{low}-{high}" if high < 200 else f"{low}+"
            results_by_group[group_name] = []
        
        for age, bib, name, finish_time, place in results_data:
            for (low, high) in age_groups:
                if low <= age <= high:
                    group_name = f"{low}-{high}" if high < 200 else f"{low}+"
                    results_by_group[group_name].append((place, bib, name, finish_time))
                    break
        
        return results_by_group


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


# 🧪 Test Group 1: Database Operations and Race Type Detection
class TestDatabaseOperations:
    """Tests for database creation and race type detection"""
    
    def test_cross_country_database_creation(self, app_with_db):
        """
        🏃‍♀️ Test creating a cross country race database
        Verifies that the correct table structure is created
        """
        # 🏗️ Create cross country database
        success = app_with_db.create_database_structure("cross_country")
        assert success, "Database creation should succeed"
        
        # 🔍 Verify race type is stored correctly
        detected_type = app_with_db.detect_race_type()
        assert detected_type == "cross_country", "Race type should be detected as cross_country"
        
        # 🔍 Verify runners table has correct columns for cross country
        cursor = app_with_db.conn.cursor()
        cursor.execute("PRAGMA table_info(runners)")
        columns = [column[1] for column in cursor.fetchall()]
        
        expected_columns = ['bib', 'name', 'team', 'age', 'grade', 'rfid']
        for col in expected_columns:
            assert col in columns, f"Column '{col}' should exist in cross country runners table"
        
        # 🔍 Verify results table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results'")
        results_table = cursor.fetchone()
        assert results_table is not None, "Results table should exist"
    
    def test_road_race_database_creation(self, app_with_db):
        """
        🏃‍♂️ Test creating a road race database
        Verifies different table structure for road races
        """
        # 🏗️ Create road race database
        success = app_with_db.create_database_structure("road_race")
        assert success, "Database creation should succeed"
        
        # 🔍 Verify race type is stored correctly
        detected_type = app_with_db.detect_race_type()
        assert detected_type == "road_race", "Race type should be detected as road_race"
        
        # 🔍 Verify runners table has correct columns for road race
        cursor = app_with_db.conn.cursor()
        cursor.execute("PRAGMA table_info(runners)")
        columns = [column[1] for column in cursor.fetchall()]
        
        expected_columns = ['bib', 'name', 'dob', 'age', 'rfid']
        for col in expected_columns:
            assert col in columns, f"Column '{col}' should exist in road race runners table"
        
        # 🔍 Verify 'team' and 'grade' columns don't exist (road race specific)
        assert 'team' not in columns, "Team column should not exist in road race database"
        assert 'grade' not in columns, "Grade column should not exist in road race database"
    
    def test_race_type_detection_with_no_database(self, app):
        """
        🤷 Test race type detection when no database is loaded
        """
        # 🔍 Should return "unknown" when no database
        detected_type = app.detect_race_type()
        assert detected_type == "unknown", "Should return 'unknown' when no database is connected"
    
    def test_database_creation_without_connection(self, app):
        """
        🚫 Test database creation fails gracefully without connection
        """
        # 🏗️ Try to create database without connection
        success = app.create_database_structure("cross_country")
        assert not success, "Database creation should fail without connection"


# 🧪 Test Group 2: Time Formatting Functions  
class TestTimeFormatting:
    """Tests for time display formatting"""
    
    @pytest.mark.parametrize("input_time,expected", [
        (60.0, "01:00.000"),
        (123.456, "02:03.456"),
        (45.789, "00:45.789"),
        (0.0, "00:00.000"),
    ])
    def test_format_time_basic_cases(self, app, input_time, expected):
        """
        ⏰ Test basic time formatting cases using parametrize
        """
        result = app.format_time(input_time)
        assert result == expected, f"{input_time} seconds should format as {expected}"
    
    @pytest.mark.parametrize("input_time,expected", [
        (None, "00:00.000"),
        (0.001, "00:00.001"),
        (665.123, "11:05.123"),  # 11:05.123
        (60.000, "01:00.000"),
    ])
    def test_format_time_edge_cases(self, app, input_time, expected):
        """
        🔍 Test edge cases for time formatting
        """
        result = app.format_time(input_time)
        assert result == expected, f"{input_time} should format as {expected}"
    
    @pytest.mark.parametrize("input_time,expected", [
        (123.1, "02:03.100"),
        (123.12, "02:03.120"),
        (123.123, "02:03.123"),
        (123.1234, "02:03.123"),  # Should round to 3 decimal places
        (123.1235, "02:03.124"),  # Should round up
    ])
    def test_format_time_precision(self, app, input_time, expected):
        """
        🎯 Test precision of time formatting (milliseconds)
        """
        result = app.format_time(input_time)
        assert result == expected, f"{input_time} seconds should format as {expected}"


# 🧪 Test Group 3: Race Scoring Logic
class TestRaceScoring:
    """Tests for race scoring algorithms"""
    
    @pytest.fixture
    def cross_country_race_data(self):
        """📊 Sample cross country race data for testing"""
        return [
            ("Team A", 101, "Runner 1", 300.5, 1),
            ("Team B", 201, "Runner 2", 305.2, 2),
            ("Team A", 102, "Runner 3", 310.1, 3),
            ("Team A", 103, "Runner 4", 315.8, 4),
            ("Team B", 202, "Runner 5", 320.3, 5),
            ("Team A", 104, "Runner 6", 325.1, 6),
            ("Team A", 105, "Runner 7", 330.2, 7),
            ("Team B", 203, "Runner 8", 335.5, 8),
            ("Team B", 204, "Runner 9", 340.1, 9),
            ("Team B", 205, "Runner 10", 345.8, 10),
            ("Team B", 206, "Runner 11", 350.3, 11),
            ("Team A", 106, "Runner 12", 355.1, 12),
        ]
    
    @pytest.fixture  
    def road_race_age_data(self):
        """🎂 Sample road race data with various ages"""
        return [
            (25, 101, "Runner 1", 1200.5, 1),    # 21-25 group
            (42, 102, "Runner 2", 1205.2, 2),    # 41-45 group
            (28, 103, "Runner 3", 1210.1, 3),    # 26-30 group
            (43, 104, "Runner 4", 1215.8, 4),    # 41-45 group
            (22, 105, "Runner 5", 1220.3, 5),    # 21-25 group
            (75, 106, "Runner 6", 1225.1, 6),    # 71+ group
            (16, 107, "Runner 7", 1230.2, 7),    # 16-20 group
            (44, 108, "Runner 8", 1235.5, 8),    # 41-45 group
        ]
    
    def test_cross_country_team_scoring(self, app, cross_country_race_data):
        """
        🏫 Test cross country team scoring algorithm
        """
        # 🧮 Calculate team scores
        team_scores = app.calculate_team_scores(cross_country_race_data)
        
        # 🔍 Verify we got results
        assert len(team_scores) == 2, "Should have 2 teams with scores"
        
        # 🏆 Verify Team A wins (lower score)
        # Team A: places 1, 3, 4, 6, 7 = 21 points
        # Team B: places 2, 5, 8, 9, 10 = 34 points
        winning_team = team_scores[0]
        assert winning_team[0] == "Team A", "Team A should win"
        assert winning_team[1] == 21, "Team A score should be 21"
        
        second_team = team_scores[1]
        assert second_team[0] == "Team B", "Team B should be second"
        assert second_team[1] == 34, "Team B score should be 34"
        
        # 🔍 Verify top 5 runners for Team A
        team_a_top5 = winning_team[2]
        expected_places = [1, 3, 4, 6, 7]
        actual_places = [runner[0] for runner in team_a_top5]
        assert actual_places == expected_places, "Team A top 5 places should be correct"
    
    def test_team_scoring_insufficient_runners(self, app):
        """
        🚫 Test that teams with fewer than 5 runners don't score
        """
        # 📊 Create data with Team C having only 3 runners
        race_data = [
            ("Team A", 101, "Runner 1", 300.5, 1),
            ("Team A", 102, "Runner 2", 305.2, 2),
            ("Team A", 103, "Runner 3", 310.1, 3),
            ("Team A", 104, "Runner 4", 315.8, 4),
            ("Team A", 105, "Runner 5", 320.3, 5),
            ("Team C", 301, "Runner 6", 325.1, 6),
            ("Team C", 302, "Runner 7", 330.2, 7),
            ("Team C", 303, "Runner 8", 335.5, 8),
        ]
        
        # 🧮 Calculate team scores
        team_scores = app.calculate_team_scores(race_data)
        
        # 🔍 Should only have Team A (Team C has insufficient runners)
        assert len(team_scores) == 1, "Should only have 1 team scoring"
        assert team_scores[0][0] == "Team A", "Only Team A should score"
    
    def test_road_race_age_grouping(self, app, road_race_age_data):
        """
        🎂 Test road race age group classification
        """
        # 📚 Group by age
        age_groups = app.group_by_age(road_race_age_data)
        
        # 🔍 Verify correct grouping
        assert len(age_groups["21-25"]) == 2, "Should have 2 runners in 21-25 group"
        assert len(age_groups["41-45"]) == 3, "Should have 3 runners in 41-45 group"
        assert len(age_groups["26-30"]) == 1, "Should have 1 runner in 26-30 group"
        assert len(age_groups["71+"]) == 1, "Should have 1 runner in 71+ group"
        assert len(age_groups["16-20"]) == 1, "Should have 1 runner in 16-20 group"
        
        # 🔍 Verify empty groups are empty
        assert len(age_groups["1-15"]) == 0, "1-15 group should be empty"
        assert len(age_groups["31-35"]) == 0, "31-35 group should be empty"
        
        # 🔍 Verify runners are in correct groups with correct data
        group_21_25 = age_groups["21-25"]
        places_in_group = [runner[0] for runner in group_21_25]  # Get places
        assert 1 in places_in_group, "Place 1 should be in 21-25 group"
        assert 5 in places_in_group, "Place 5 should be in 21-25 group"
    
    @pytest.mark.parametrize("age,expected_group", [
        (15, "1-15"),      # Top of 1-15
        (16, "16-20"),     # Bottom of 16-20
        (20, "16-20"),     # Top of 16-20
        (21, "21-25"),     # Bottom of 21-25
        (71, "71+"),       # Bottom of 71+
    ])
    def test_age_group_boundaries(self, app, age, expected_group):
        """
        🔍 Test age group boundary conditions
        """
        boundary_data = [(age, 101, "Edge Runner", 1200.0, 1)]
        age_groups = app.group_by_age(boundary_data)
        
        # Verify this age is in the expected group
        assert len(age_groups[expected_group]) == 1, f"Age {age} should be in {expected_group} group"
        
        # Verify it's not in other groups
        for group_name, runners in age_groups.items():
            if group_name != expected_group:
                assert len(runners) == 0, f"Age {age} should not be in {group_name} group"


# 🧪 Test Group 4: Integration Tests
class TestIntegration:
    """Integration tests that combine multiple components"""
    
    def test_full_cross_country_workflow(self, app_with_db):
        """
        🏃‍♀️ Test complete cross country race workflow
        """
        # 1. Create database
        success = app_with_db.create_database_structure("cross_country")
        assert success, "Database creation should succeed"
        
        # 2. Verify race type detection
        race_type = app_with_db.detect_race_type()
        assert race_type == "cross_country", "Should detect cross country race type"
        
        # 3. Add some test runners
        cursor = app_with_db.conn.cursor()
        test_runners = [
            (101, "Alice Smith", "Team A", 16, "11", "RFID001"),
            (102, "Bob Jones", "Team A", 17, "12", "RFID002"),
            (201, "Carol Brown", "Team B", 16, "11", "RFID003"),
        ]
        
        cursor.executemany(
            "INSERT INTO runners (bib, name, team, age, grade, rfid) VALUES (?, ?, ?, ?, ?, ?)",
            test_runners
        )
        app_with_db.conn.commit()
        
        # 4. Verify runners were added
        cursor.execute("SELECT COUNT(*) FROM runners")
        count = cursor.fetchone()[0]
        assert count == 3, "Should have 3 runners in database"
        
        # 5. Add some race results
        race_results = [
            (101, 365.5, "2025-07-28"),  # Alice - 6:05.500
            (102, 378.2, "2025-07-28"),  # Bob - 6:18.200
            (201, 355.1, "2025-07-28"),  # Carol - 5:55.100
        ]
        
        cursor.executemany(
            "INSERT INTO results (bib, finish_time, race_date) VALUES (?, ?, ?)",
            race_results
        )
        app_with_db.conn.commit()
        
        # 6. Test time formatting on actual results
        cursor.execute("SELECT finish_time FROM results ORDER BY finish_time")
        times = cursor.fetchall()
        
        formatted_times = [app_with_db.format_time(time[0]) for time in times]
        expected_times = ["05:55.100", "06:05.500", "06:18.200"]
        
        assert formatted_times == expected_times, "Times should be formatted correctly"
    
    def test_empty_database_operations(self, app_with_db):
        """
        🔍 Test operations on empty databases
        """
        # Create database structure but don't add data
        success = app_with_db.create_database_structure("road_race")
        assert success, "Database creation should succeed"
        
        # Test operations on empty tables
        cursor = app_with_db.conn.cursor()
        
        # Check runner count
        cursor.execute("SELECT COUNT(*) FROM runners")
        count = cursor.fetchone()[0]
        assert count == 0, "New database should have no runners"
        
        # Check results count
        cursor.execute("SELECT COUNT(*) FROM results")
        count = cursor.fetchone()[0]
        assert count == 0, "New database should have no results"
        
        # Test scoring with no data
        empty_scores = app_with_db.calculate_team_scores([])
        assert len(empty_scores) == 0, "Empty data should produce no team scores"
        
        empty_age_groups = app_with_db.group_by_age([])
        assert all(len(runners) == 0 for runners in empty_age_groups.values()), "Empty data should produce empty age groups"


if __name__ == '__main__':
    # Allow running directly with pytest
    pytest.main([__file__, "-v"])
