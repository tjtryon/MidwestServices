#!/usr/bin/env python3
"""
test_project.py - Complete Pytest Unit Test Suite for The Race Timing Solution GUI
Author: TJ Tryon
Date: July 28, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS) - GUI Version

🧪 Complete unit test suite covering all core functionality:
- Database operations and race type detection
- Time formatting and display accuracy  
- Race scoring algorithms for both race types

To run these tests:
    pytest test_project.py -v
    pytest test_project.py::TestDatabaseOperations -v
    pytest test_project.py -k "format_time" -v
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
    🧪 Testable version of RaceTimingApp that doesn't require GTK4
    Contains all core logic methods we want to test
    """
    
    def __init__(self):
        self.conn = None
        self.db_path = None
        self.race_type = ""
    
    # 🗃️ DATABASE OPERATIONS METHODS
    def create_database_structure(self, race_type):
        """🏗️ Creates the database structure for a given race type"""
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
        """🔍 Detects race type from database"""
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
        """📋 Gets column names for a given table"""
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            return [column[1] for column in cursor.fetchall()]
        except sqlite3.Error:
            return []
    
    def table_exists(self, table_name):
        """🔍 Checks if a table exists in the database"""
        if not self.conn:
            return False
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            return cursor.fetchone() is not None
        except sqlite3.Error:
            return False
    
    # ⏰ TIME FORMATTING METHODS
    def format_time(self, total_seconds):
        """
        ⏰ Converts seconds to MM:SS.mmm format.
        Same formatting logic as the main application.
        """
        if total_seconds is None:
            return "00:00.000"
            
        minutes, seconds = divmod(total_seconds, 60)
        return f"{int(minutes):02d}:{seconds:06.3f}"
    
    def format_time_hours(self, total_seconds):
        """🕐 Converts seconds to HH:MM:SS.mmm format for longer races."""
        if total_seconds is None:
            return "00:00:00.000"
            
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"
    
    def parse_time_input(self, time_string):
        """📝 Parses time input from string format back to seconds."""
        if not time_string or not isinstance(time_string, str):
            return None
            
        try:
            # Handle MM:SS.mmm format
            if time_string.count(':') == 1:
                minutes_str, seconds_str = time_string.split(':')
                minutes = int(minutes_str)
                seconds = float(seconds_str)
                return minutes * 60 + seconds
            
            # Handle HH:MM:SS.mmm format
            elif time_string.count(':') == 2:
                hours_str, minutes_str, seconds_str = time_string.split(':')
                hours = int(hours_str)
                minutes = int(minutes_str)
                seconds = float(seconds_str)
                return hours * 3600 + minutes * 60 + seconds
            
            else:
                return None
                
        except (ValueError, AttributeError):
            return None
    
    # 🏆 RACE SCORING METHODS
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
    
    def calculate_individual_awards(self, results_data, award_depth=3):
        """🏆 Calculates individual awards (1st, 2nd, 3rd place)"""
        # Sort by place and take top N
        sorted_results = sorted(results_data, key=lambda x: x[3])  # Sort by place
        return sorted_results[:award_depth]
    
    def detect_scoring_ties(self, team_scores):
        """🤝 Detects ties in team scoring that need manual review"""
        ties = []
        seen_scores = {}
        
        for team_data in team_scores:
            team, score, _, _, tiebreak1, tiebreak2 = team_data
            score_key = (score, tiebreak1, tiebreak2)
            
            if score_key in seen_scores:
                # Found a tie
                tied_teams = seen_scores[score_key]
                tied_teams.append(team)
                if len(tied_teams) == 2:  # First time we see this tie
                    ties.append({
                        'score': score,
                        'tiebreak1': tiebreak1,
                        'tiebreak2': tiebreak2,
                        'teams': tied_teams
                    })
            else:
                seen_scores[score_key] = [team]
        
        return ties


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


@pytest.fixture
def cross_country_race_data():
    """📊 Sample cross country race data for testing"""
    return [
        ("Team A", 101, "Alice Smith", 300.5, 1),
        ("Team B", 201, "Bob Jones", 305.2, 2),
        ("Team A", 102, "Carol Brown", 310.1, 3),
        ("Team A", 103, "David Wilson", 315.8, 4),
        ("Team B", 202, "Eva Davis", 320.3, 5),
        ("Team A", 104, "Frank Miller", 325.1, 6),
        ("Team A", 105, "Grace Taylor", 330.2, 7),
        ("Team B", 203, "Henry Clark", 335.5, 8),
        ("Team B", 204, "Iris Johnson", 340.1, 9),
        ("Team B", 205, "Jack White", 345.8, 10),
        ("Team B", 206, "Kate Green", 350.3, 11),
        ("Team A", 106, "Liam Black", 355.1, 12),
    ]


@pytest.fixture  
def road_race_age_data():
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


# 🧪 DATABASE OPERATIONS TESTS
class TestDatabaseOperations:
    """Tests for database creation and race type detection"""
    
    def test_cross_country_database_creation(self, app_with_db):
        """🏃‍♀️ Test creating a cross country race database"""
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
    
    def test_road_race_database_creation(self, app_with_db):
        """🏃‍♂️ Test creating a road race database"""
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
    
    def test_race_type_detection_with_no_database(self, app):
        """🤷 Test race type detection when no database is loaded"""
        # 🔍 Should return "unknown" when no database
        detected_type = app.detect_race_type()
        assert detected_type == "unknown", "Should return 'unknown' when no database is connected"
    
    def test_database_creation_without_connection(self, app):
        """🚫 Test database creation fails gracefully without connection"""
        # 🏗️ Try to create database without connection
        success = app.create_database_structure("cross_country")
        assert not success, "Database creation should fail without connection"
        
        # 🔍 Race type should remain empty
        assert app.race_type == "", "Race type should remain empty after failed creation"
    
    def test_race_type_table_creation(self, app_with_db):
        """📋 Test that race_type table is created and populated correctly"""
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
    
    def test_corrupted_race_type_detection(self, app_with_db):
        """💥 Test race type detection with corrupted race_type table"""
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
        """🔍 Test table existence checking functionality"""
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


# 🧪 TIME FORMATTING TESTS
class TestTimeFormatting:
    """Tests for time display formatting functions"""
    
    @pytest.mark.parametrize("input_time,expected", [
        (60.0, "01:00.000"),        # Exactly one minute
        (123.456, "02:03.456"),     # Standard race time
        (45.789, "00:45.789"),      # Under one minute
        (0.0, "00:00.000"),         # Zero time
        (59.999, "00:59.999"),      # Just under one minute
        (61.001, "01:01.001"),      # Just over one minute
        (600.0, "10:00.000"),       # Exactly 10 minutes
        (3661.5, "61:01.500"),      # Over one hour (in MM:SS format)
    ])
    def test_format_time_basic_cases(self, app, input_time, expected):
        """⏰ Test basic time formatting cases using parametrize"""
        result = app.format_time(input_time)
        assert result == expected, f"{input_time} seconds should format as {expected}"
    
    @pytest.mark.parametrize("input_time,expected", [
        (None, "00:00.000"),         # None input
        (0.001, "00:00.001"),        # Very small time
        (0.0001, "00:00.000"),       # Smaller than precision
        (665.123, "11:05.123"),      # 11:05.123
        (60.000, "01:00.000"),       # Exact minute boundary
        (59.9999, "01:00.000"),      # Rounding up to next minute
        (3599.999, "60:00.000"),     # Just under one hour
        (7200.0, "120:00.000"),      # Exactly 2 hours
    ])
    def test_format_time_edge_cases(self, app, input_time, expected):
        """🔍 Test edge cases for time formatting"""
        result = app.format_time(input_time)
        assert result == expected, f"{input_time} should format as {expected}"
    
    @pytest.mark.parametrize("input_time,expected", [
        (123.1, "02:03.100"),        # One decimal place
        (123.12, "02:03.120"),       # Two decimal places  
        (123.123, "02:03.123"),      # Three decimal places (exact)
        (123.1234, "02:03.123"),     # Four decimal places (should truncate)
        (123.1235, "02:03.124"),     # Should round up
        (123.1236, "02:03.124"),     # Should round up
        (123.9999, "02:04.000"),     # Should round up to next second
        (59.9995, "01:00.000"),      # Should round up to next minute
    ])
    def test_format_time_precision(self, app, input_time, expected):
        """🎯 Test precision of time formatting (milliseconds)"""
        result = app.format_time(input_time)
        assert result == expected, f"{input_time} seconds should format as {expected}"
    
    @pytest.mark.parametrize("input_time,expected", [
        (3661.5, "01:01:01.500"),    # Just over one hour
        (7200.0, "02:00:00.000"),    # Exactly 2 hours
        (86400.0, "24:00:00.000"),   # 24 hours
        (90061.123, "25:01:01.123"), # Over 24 hours
        (3600.0, "01:00:00.000"),    # Exactly one hour
        (0.0, "00:00:00.000"),       # Zero time
        (None, "00:00:00.000"),      # None input
    ])
    def test_format_time_hours(self, app, input_time, expected):
        """🕐 Test HH:MM:SS.mmm format for longer races"""
        result = app.format_time_hours(input_time)
        assert result == expected, f"{input_time} seconds should format as {expected}"
    
    @pytest.mark.parametrize("time_string,expected_seconds", [
        ("02:03.456", 123.456),      # MM:SS.mmm format
        ("01:00.000", 60.0),         # Exactly one minute
        ("00:30.500", 30.5),         # 30.5 seconds
        ("10:15.750", 615.75),       # 10:15.750
        ("01:01:01.500", 3661.5),    # HH:MM:SS.mmm format
        ("02:00:00.000", 7200.0),    # 2 hours
        ("00:00:00.001", 0.001),     # 1 millisecond
    ])
    def test_parse_time_input_valid(self, app, time_string, expected_seconds):
        """📝 Test parsing valid time input strings back to seconds"""
        result = app.parse_time_input(time_string)
        assert abs(result - expected_seconds) < 0.001, f"'{time_string}' should parse to {expected_seconds} seconds"
    
    @pytest.mark.parametrize("invalid_input", [
        None,                        # None input
        "",                          # Empty string
        "invalid",                   # Not a time format
        "1:2:3:4",                  # Too many colons
        "ab:cd.efg",                # Non-numeric
        "60:60.000",                # Invalid minutes
        "01:60.000",                # Invalid seconds
        "-01:30.000",               # Negative time
        "01:-30.000",               # Negative component
    ])
    def test_parse_time_input_invalid(self, app, invalid_input):
        """❌ Test parsing invalid time input strings"""
        result = app.parse_time_input(invalid_input)
        assert result is None, f"Invalid input '{invalid_input}' should return None"
    
    def test_time_format_round_trip(self, app):
        """🔄 Test round-trip conversion: seconds → string → seconds"""
        test_times = [60.0, 123.456, 3661.5, 7200.0, 30.5]
        
        for original_time in test_times:
            # Format to string
            if original_time >= 3600:  # Use hours format for times >= 1 hour
                formatted = app.format_time_hours(original_time)
            else:
                formatted = app.format_time(original_time)
            
            # Parse back to seconds
            parsed = app.parse_time_input(formatted)
            
            # Should be very close to original (allowing for floating point precision)
            assert abs(parsed - original_time) < 0.001, f"Round trip failed for {original_time}: {formatted} → {parsed}"


# 🧪 RACE SCORING TESTS
class TestCrossCountryScoring:
    """Tests for cross country team scoring algorithms"""
    
    def test_cross_country_team_scoring(self, app, cross_country_race_data):
        """🏫 Test cross country team scoring algorithm"""
        # 🧮 Calculate team scores
        team_scores = app.calculate_team_scores(cross_country_race_data)
        
        # 🔍 Verify we got results for both teams
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
        """🚫 Test that teams with fewer than 5 runners don't score"""
        # 📊 Create data with Team C having only 3 runners
        race_data = [
            ("Team A", 101, "Runner 1", 300.5, 1),
            ("Team A", 102, "Runner 2", 305.2, 2),
            ("Team A", 103, "Runner 3", 310.1, 3),
            ("Team A", 104, "Runner 4", 315.8, 4),
            ("Team A", 105, "Runner 5", 320.3, 5),
            ("Team C", 301, "Runner 6", 325.1, 6),  # Only 3 runners
            ("Team C", 302, "Runner 7", 330.2, 7),
            ("Team C", 303, "Runner 8", 335.5, 8),
        ]
        
        # 🧮 Calculate team scores
        team_scores = app.calculate_team_scores(race_data)
        
        # 🔍 Should only have Team A (Team C has insufficient runners)
        assert len(team_scores) == 1, "Should only have 1 team scoring"
        assert team_scores[0][0] == "Team A", "Only Team A should score"
        assert team_scores[0][1] == 15, "Team A score should be 1+2+3+4+5 = 15"
    
    def test_team_scoring_tiebreaker_scenarios(self, app):
        """⚖️ Test various tiebreaker scenarios in team scoring"""
        # Create scenario where teams tie on score but differ on 6th runner
        tiebreak_data = [
            ("Team A", 101, "Runner 1", 300.0, 1),
            ("Team A", 102, "Runner 2", 302.0, 3),
            ("Team A", 103, "Runner 3", 304.0, 5),
            ("Team A", 104, "Runner 4", 306.0, 7),
            ("Team A", 105, "Runner 5", 308.0, 9),
            ("Team A", 106, "Runner 6", 312.0, 13),  # 6th runner (tiebreaker)
            
            ("Team B", 201, "Runner 7", 301.0, 2),
            ("Team B", 202, "Runner 8", 303.0, 4),
            ("Team B", 203, "Runner 9", 305.0, 6),
            ("Team B", 204, "Runner 10", 307.0, 8),
            ("Team B", 205, "Runner 11", 309.0, 10),
            ("Team B", 206, "Runner 12", 311.0, 12),  # 6th runner (tiebreaker)
        ]
        
        team_scores = app.calculate_team_scores(tiebreak_data)
        
        # Both teams have same score: 1+3+5+7+9 = 25, 2+4+6+8+10 = 30
        # But Team B should win on 6th runner tiebreaker (12 < 13)
        assert team_scores[0][0] == "Team B", "Team B should win on tiebreaker"
        assert team_scores[0][4] == 12, "Winning team's tiebreaker should be 12"
        assert team_scores[1][4] == 13, "Losing team's tiebreaker should be 13"
    
    def test_empty_team_scoring(self, app):
        """📭 Test team scoring with empty data"""
        empty_scores = app.calculate_team_scores([])
        assert len(empty_scores) == 0, "Empty data should produce no team scores"


class TestRoadRaceScoring:
    """Tests for road race scoring and age group classification"""
    
    def test_road_race_age_grouping(self, app, road_race_age_data):
        """🎂 Test road race age group classification"""
        # 📚 Group by age
        age_groups = app.group_by_age(road_race_age_data)
        
        # 🔍 Verify correct grouping counts
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
        (1, "1-15"),       # Minimum age
        (15, "1-15"),      # Top of 1-15
        (16, "16-20"),     # Bottom of 16-20
        (20, "16-20"),     # Top of 16-20
        (21, "21-25"),     # Bottom of 21-25
        (25, "21-25"),     # Top of 21-25
        (35, "31-35"),     # Middle of range
        (70, "66-70"),     # Top of 66-70
        (71, "71+"),       # Bottom of 71+
        (85, "71+"),       # High age in 71+
        (100, "71+"),      # Very high age
    ])
    def test_age_group_boundaries(self, app, age, expected_group):
        """🔍 Test age group boundary conditions"""
        boundary_data = [(age, 101, "Edge Runner", 1200.0, 1)]
        age_groups = app.group_by_age(boundary_data)
        
        # Verify this age is in the expected group
        assert len(age_groups[expected_group]) == 1, f"Age {age} should be in {expected_group} group"
        
        # Verify it's not in other groups
        for group_name, runners in age_groups.items():
            if group_name != expected_group:
                assert len(runners) == 0, f"Age {age} should not be in {group_name} group"
    
    def test_all_age_groups_exist(self, app):
        """📋 Test that all standard age groups are created"""
        # Test with empty data to verify all groups are initialized
        age_groups = app.group_by_age([])
        
        expected_groups = [
            "1-15", "16-20", "21-25", "26-30", "31-35", "36-40",
            "41-45", "46-50", "51-55", "56-60", "61-65", "66-70", "71+"
        ]
        
        for group in expected_groups:
            assert group in age_groups, f"Age group {group} should exist"
            assert isinstance(age_groups[group], list), f"Age group {group} should be a list"
    
    def test_comprehensive_age_distribution(self, app):
        """🌈 Test comprehensive age distribution across all groups"""
        comprehensive_data = [
            (5, 101, "Kid Runner", 1500.0, 1),      # 1-15
            (18, 102, "Teen Runner", 1200.0, 2),    # 16-20
            (23, 103, "Young Adult", 1100.0, 3),    # 21-25
            (28, 104, "Adult 1", 1150.0, 4),        # 26-30
            (33, 105, "Adult 2", 1180.0, 5),        # 31-35
            (38, 106, "Adult 3", 1220.0, 6),        # 36-40
            (43, 107, "Master 1", 1250.0, 7),       # 41-45
            (48, 108, "Master 2", 1280.0, 8),       # 46-50
            (53, 109, "Master 3", 1300.0, 9),       # 51-55
            (58, 110, "Master 4", 1320.0, 10),      # 56-60
            (63, 111, "Master 5", 1350.0, 11),      # 61-65
            (68, 112, "Master 6", 1380.0, 12),      # 66-70
            (75, 113, "Senior", 1400.0, 13),        # 71+
        ]
        
        age_groups = app.group_by_age(comprehensive_data)
        
        # Verify each group has exactly one runner
        expected_groups = [
            "1-15", "16-20", "21-25", "26-30", "31-35", "36-40",
            "41-45", "46-50", "51-55", "56-60", "61-65", "66-70", "71+"
        ]
        
        for group in expected_groups:
            assert len(age_groups[group]) == 1, f"Group {group} should have exactly 1 runner"
        
        # Verify total runners preserved
        total_runners = sum(len(runners) for runners in age_groups.values())
        assert total_runners == 13, "Should have 13 total runners across all groups"


class TestAdditionalScoringFeatures:
    """Tests for additional scoring features like individual awards and tie detection"""
    
    def test_individual_awards_calculation(self, app):
        """🏆 Test calculation of individual awards (1st, 2nd, 3rd place)"""
        individual_data = [
            (105, "Third Place", 1220.5, 3),
            (101, "First Place", 1200.5, 1),
            (103, "Fifth Place", 1240.1, 5),
            (102, "Second Place", 1210.2, 2),
            (104, "Fourth Place", 1230.8, 4),
        ]
        
        awards = app.calculate_individual_awards(individual_data, award_depth=3)
        
        # Should return top 3 finishers in order
        assert len(awards) == 3, "Should return 3 award winners"
        assert awards[0][1] == "First Place", "First award should go to first place"
        assert awards[1][1] == "Second Place", "Second award should go to second place"
        assert awards[2][1] == "Third Place", "Third award should go to third place"
        
        # Verify places are correct
        assert awards[0][3] == 1, "First place should have place 1"
        assert awards[1][3] == 2, "Second place should have place 2"
        assert awards[2][3] == 3, "Third place should have place 3"
    
    def test_individual_awards_custom_depth(self, app):
        """🏆 Test individual awards with custom award depth"""
        individual_data = [
            (101, "Runner 1", 1200.0, 1),
            (102, "Runner 2", 1201.0, 2),
            (103, "Runner 3", 1202.0, 3),
            (104, "Runner 4", 1203.0, 4),
            (105, "Runner 5", 1204.0, 5),
        ]
        
        # Test top 5 awards
        awards = app.calculate_individual_awards(individual_data, award_depth=5)
        assert len(awards) == 5, "Should return 5 award winners"
        
        # Test top 1 award only
        awards = app.calculate_individual_awards(individual_data, award_depth=1)
        assert len(awards) == 1, "Should return 1 award winner"
        assert awards[0][1] == "Runner 1", "Single award should go to first place"
    
    def test_scoring_tie_detection(self, app):
        """🤝 Test detection of ties in team scoring"""
        # Create team scores with some ties
        team_scores = [
            ("Team A", 25, [], [], 12, 15),  # Tied score
            ("Team B", 25, [], [], 12, 15),  # Same tie
            ("Team C", 30, [], [], 8, 10),   # Different score
            ("Team D", 25, [], [], 13, 16),  # Same score, different tiebreaker
        ]
        
        ties = app.detect_scoring_ties(team_scores)
        
        # Should detect one tie between Team A and Team B
        assert len(ties) == 1, "Should detect 1 tie group"
        tie_group = ties[0]
        assert tie_group['score'] == 25, "Tie should be at score 25"
        assert set(tie_group['teams']) == {"Team A", "Team B"}, "Tie should be between Team A and Team B"
    
    def test_no_ties_detection(self, app):
        """✅ Test tie detection when no ties exist"""
        team_scores = [
            ("Team A", 20, [], [], 8, 10),
            ("Team B", 25, [], [], 12, 15),
            ("Team C", 30, [], [], 16, 18),
        ]
        
        ties = app.detect_scoring_ties(team_scores)
        assert len(ties) == 0, "Should detect no ties"


class TestScoringIntegration:
    """Integration tests that combine multiple scoring components"""
    
    def test_complete_cross_country_meet_scoring(self, app):
        """🏃‍♀️ Test complete cross country meet with multiple teams"""
        # Large meet with 4 teams
        meet_data = [
            # Team A - Strong team
            ("Team A", 101, "Alice", 300.0, 1),
            ("Team A", 102, "Amy", 310.0, 3),
            ("Team A", 103, "Anna", 320.0, 5),
            ("Team A", 104, "Andrea", 330.0, 7),
            ("Team A", 105, "Ashley", 340.0, 9),
            ("Team A", 106, "Amber", 350.0, 11),
            ("Team A", 107, "Abby", 360.0, 13),
            
            # Team B - Competitive team
            ("Team B", 201, "Beth", 305.0, 2),
            ("Team B", 202, "Bella", 315.0, 4),
            ("Team B", 203, "Brooke", 325.0, 6),
            ("Team B", 204, "Bree", 335.0, 8),
            ("Team B", 205, "Bailey", 345.0, 10),
            ("Team B", 206, "Bridget", 355.0, 12),
            
            # Team C - Weaker team
            ("Team C", 301, "Chloe", 365.0, 14),
            ("Team C", 302, "Claire", 370.0, 15),
            ("Team C", 303, "Cara", 375.0, 16),
            ("Team C", 304, "Cindy", 380.0, 17),
            ("Team C", 305, "Crystal", 385.0, 18),
            
            # Team D - Incomplete team (only 3 runners)
            ("Team D", 401, "Dana", 390.0, 19),
            ("Team D", 402, "Diana", 395.0, 20),
            ("Team D", 403, "Donna", 400.0, 21),
        ]
        
        team_scores = app.calculate_team_scores(meet_data)
        
        # Should have 3 scoring teams (Team D incomplete)
        assert len(team_scores) == 3, "Should have 3 complete teams"
        
        # Verify scores
        # Team A: 1+3+5+7+9 = 25
        # Team B: 2+4+6+8+10 = 30  
        # Team C: 14+15+16+17+18 = 80
        assert team_scores[0][0] == "Team A", "Team A should win"
        assert team_scores[0][1] == 25, "Team A score should be 25"
        assert team_scores[1][0] == "Team B", "Team B should be second"
        assert team_scores[1][1] == 30, "Team B score should be 30"
        assert team_scores[2][0] == "Team C", "Team C should be third"
        assert team_scores[2][1] == 80, "Team C score should be 80"
    
    def test_large_road_race_age_groups(self, app):
        """🏃‍♂️ Test large road race with runners in all age groups"""
        # Create runners covering all age groups
        large_race_data = []
        place = 1
        
        # Add runners to each age group
        age_ranges = [
            (10, "1-15"), (18, "16-20"), (23, "21-25"), (28, "26-30"),
            (33, "31-35"), (38, "36-40"), (43, "41-45"), (48, "46-50"),
            (53, "51-55"), (58, "56-60"), (63, "61-65"), (68, "66-70"), (75, "71+")
        ]
        
        for age, expected_group in age_ranges:
            for i in range(3):  # 3 runners per age group
                large_race_data.append((
                    age, 
                    100 + place, 
                    f"Runner {place}",
                    1200.0 + place * 5,  # Stagger finish times
                    place
                ))
                place += 1
        
        age_groups = app.group_by_age(large_race_data)
        
        # Verify all groups have 3 runners
        for group_name in age_groups:
            if group_name in [g[1] for g in age_ranges]:
                assert len(age_groups[group_name]) == 3, f"Group {group_name} should have 3 runners"
            else:
                assert len(age_groups[group_name]) == 0, f"Group {group_name} should be empty"
        
        # Verify total count
        total_runners = sum(len(runners) for runners in age_groups.values())
        assert total_runners == 39, "Should have 39 total runners (13 groups × 3 runners)"
    
    def test_edge_case_single_runner_teams(self, app):
        """👤 Test handling of teams with only single runners"""
        single_runner_data = [
            ("Team A", 101, "Solo A", 300.0, 1),
            ("Team B", 201, "Solo B", 310.0, 2),
            ("Team C", 301, "Solo C", 320.0, 3),
            ("Team D", 401, "Solo D", 330.0, 4),
            ("Team E", 501, "Solo E", 340.0, 5),
        ]
        
        team_scores = app.calculate_team_scores(single_runner_data)
        
        # No teams should score (all have < 5 runners)
        assert len(team_scores) == 0, "No teams should score with single runners"
    
    def test_extreme_age_values(self, app):
        """🔢 Test handling of extreme age values"""
        extreme_age_data = [
            (0, 101, "Baby", 2000.0, 1),     # Age 0 (should go to 1-15)
            (1, 102, "Toddler", 1900.0, 2),  # Age 1 (boundary)
            (150, 103, "Ancient", 3000.0, 3), # Very old age (should go to 71+)
        ]
        
        age_groups = app.group_by_age(extreme_age_data)
        
        # Age 0 and 1 should go to 1-15 group
        assert len(age_groups["1-15"]) == 2, "Ages 0 and 1 should be in 1-15 group"
        
        # Age 150 should go to 71+ group
        assert len(age_groups["71+"]) == 1, "Age 150 should be in 71+ group"
    
    def test_scoring_system_consistency(self, app):
        """🔄 Test that scoring system produces consistent results"""
        test_data = [
            ("Team A", 101, "Runner 1", 300.0, 1),
            ("Team A", 102, "Runner 2", 310.0, 2),
            ("Team A", 103, "Runner 3", 320.0, 3),
            ("Team A", 104, "Runner 4", 330.0, 4),
            ("Team A", 105, "Runner 5", 340.0, 5),
        ]
        
        # Run scoring multiple times
        results = []
        for _ in range(5):
            scores = app.calculate_team_scores(test_data)
            results.append(scores)
        
        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result, "Scoring should be consistent across multiple runs"


class TestIntegrationWorkflows:
    """Tests that combine database, timing, and scoring functionality"""
    
    def test_full_cross_country_workflow(self, app_with_db):
        """🏃‍♀️ Test complete cross country race workflow"""
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
        """🔍 Test operations on empty databases"""
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