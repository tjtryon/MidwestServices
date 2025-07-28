#!/usr/bin/env python3
"""
test_time_formatting.py - Pytest Unit Tests for Time Formatting Functions
Author: TJ Tryon
Date: July 28, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS) - GUI Version

🧪 Tests time display formatting functions
Ensures race times are displayed accurately to millisecond precision

To run these tests:
    pytest test_time_formatting.py -v
    pytest test_time_formatting.py::test_format_time_basic_cases -v
"""

import pytest
from unittest.mock import MagicMock
import sys

# Mock the GTK dependencies before importing the main module
sys.modules['gi'] = MagicMock()
sys.modules['gi.repository'] = MagicMock()
sys.modules['gi.repository.Gtk'] = MagicMock()
sys.modules['gi.repository.Gio'] = MagicMock()
sys.modules['gi.repository.GLib'] = MagicMock()
sys.modules['gi.repository.Gdk'] = MagicMock()


class TestableTimeFormatter:
    """
    🧪 Testable version of time formatting functionality
    Contains only the time formatting method we want to test
    """
    
    def format_time(self, total_seconds):
        """
        ⏰ Converts seconds to MM:SS.mmm format.
        Same formatting logic as the main application.
        
        Args:
            total_seconds: Float representing elapsed seconds
            
        Returns:
            String in format MM:SS.mmm (e.g., "02:03.456")
        """
        if total_seconds is None:
            return "00:00.000"
            
        minutes, seconds = divmod(total_seconds, 60)
        return f"{int(minutes):02d}:{seconds:06.3f}"
    
    def format_time_hours(self, total_seconds):
        """
        🕐 Converts seconds to HH:MM:SS.mmm format for longer races.
        Extended formatting for races over 60 minutes.
        
        Args:
            total_seconds: Float representing elapsed seconds
            
        Returns:
            String in format HH:MM:SS.mmm (e.g., "01:23:45.678")
        """
        if total_seconds is None:
            return "00:00:00.000"
            
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"
    
    def parse_time_input(self, time_string):
        """
        📝 Parses time input from string format back to seconds.
        Used for manual time entry and corrections.
        
        Args:
            time_string: String in format "MM:SS.mmm" or "HH:MM:SS.mmm"
            
        Returns:
            Float representing total seconds, or None if invalid
        """
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


# 🔧 Pytest Fixtures
@pytest.fixture
def formatter():
    """🧪 Create a fresh TestableTimeFormatter instance for each test"""
    return TestableTimeFormatter()


# 🧪 Time Formatting Tests
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
    def test_format_time_basic_cases(self, formatter, input_time, expected):
        """
        ⏰ Test basic time formatting cases using parametrize
        Covers common race timing scenarios
        """
        result = formatter.format_time(input_time)
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
    def test_format_time_edge_cases(self, formatter, input_time, expected):
        """
        🔍 Test edge cases for time formatting
        Ensures robust handling of boundary conditions
        """
        result = formatter.format_time(input_time)
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
    def test_format_time_precision(self, formatter, input_time, expected):
        """
        🎯 Test precision of time formatting (milliseconds)
        Critical for accurate race timing display
        """
        result = formatter.format_time(input_time)
        assert result == expected, f"{input_time} seconds should format as {expected}"
    
    def test_format_time_negative_values(self, formatter):
        """
        ⚠️ Test handling of negative time values
        Should handle gracefully even though negative times shouldn't occur
        """
        # Negative times should be handled gracefully
        result = formatter.format_time(-10.5)
        # The exact behavior for negative times can be defined as needed
        # For now, we'll test that it doesn't crash
        assert isinstance(result, str), "Negative time should return a string"
        assert ":" in result, "Result should still be in time format"
    
    def test_format_time_very_large_values(self, formatter):
        """
        🚀 Test formatting of very large time values
        For ultra-marathons or 24-hour races
        """
        # Test 24 hours (86400 seconds)
        result = formatter.format_time(86400.0)
        assert result == "1440:00.000", "24 hours should format correctly"
        
        # Test over 24 hours
        result = formatter.format_time(90061.5)  # 25:01:01.500
        assert result == "1501:01.500", "Over 24 hours should format correctly"
    
    def test_format_time_float_precision_edge_cases(self, formatter):
        """
        🔬 Test floating point precision edge cases
        Ensures consistent behavior with floating point arithmetic
        """
        # Test values that might have floating point precision issues
        test_cases = [
            (0.1 + 0.2, "00:00.300"),  # Classic floating point issue
            (1.0/3.0 * 3, "00:01.000"),  # Should be 1.0 but might have precision error
            (10.0/3.0, "00:03.333"),   # Repeating decimal
        ]
        
        for input_time, expected in test_cases:
            result = formatter.format_time(input_time)
            assert result == expected, f"Floating point case {input_time} should format as {expected}"


class TestExtendedTimeFormatting:
    """Tests for extended time formatting functionality"""
    
    @pytest.mark.parametrize("input_time,expected", [
        (3661.5, "01:01:01.500"),    # Just over one hour
        (7200.0, "02:00:00.000"),    # Exactly 2 hours
        (86400.0, "24:00:00.000"),   # 24 hours
        (90061.123, "25:01:01.123"), # Over 24 hours
        (3600.0, "01:00:00.000"),    # Exactly one hour
        (0.0, "00:00:00.000"),       # Zero time
        (None, "00:00:00.000"),      # None input
    ])
    def test_format_time_hours(self, formatter, input_time, expected):
        """
        🕐 Test HH:MM:SS.mmm format for longer races
        """
        result = formatter.format_time_hours(input_time)
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
    def test_parse_time_input_valid(self, formatter, time_string, expected_seconds):
        """
        📝 Test parsing valid time input strings back to seconds
        """
        result = formatter.parse_time_input(time_string)
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
    def test_parse_time_input_invalid(self, formatter, invalid_input):
        """
        ❌ Test parsing invalid time input strings
        Should return None for invalid inputs
        """
        result = formatter.parse_time_input(invalid_input)
        assert result is None, f"Invalid input '{invalid_input}' should return None"
    
    def test_time_format_round_trip(self, formatter):
        """
        🔄 Test round-trip conversion: seconds → string → seconds
        Ensures formatting and parsing are consistent
        """
        test_times = [60.0, 123.456, 3661.5, 7200.0, 30.5]
        
        for original_time in test_times:
            # Format to string
            if original_time >= 3600:  # Use hours format for times >= 1 hour
                formatted = formatter.format_time_hours(original_time)
            else:
                formatted = formatter.format_time(original_time)
            
            # Parse back to seconds
            parsed = formatter.parse_time_input(formatted)
            
            # Should be very close to original (allowing for floating point precision)
            assert abs(parsed - original_time) < 0.001, f"Round trip failed for {original_time}: {formatted} → {parsed}"


class TestRaceTimingScenarios:
    """Tests based on real race timing scenarios"""
    
    def test_sprint_race_times(self, formatter):
        """
        🏃‍♂️ Test formatting for sprint race times (under 2 minutes)
        """
        sprint_times = [
            (11.5, "00:11.500"),      # 100m world record ~9.58s, but testing 11.5s
            (22.75, "00:22.750"),     # 200m time
            (49.25, "00:49.250"),     # 400m time  
            (95.5, "01:35.500"),      # 800m time
        ]
        
        for time_seconds, expected in sprint_times:
            result = formatter.format_time(time_seconds)
            assert result == expected, f"Sprint time {time_seconds}s should format as {expected}"
    
    def test_distance_race_times(self, formatter):
        """
        🏃‍♀️ Test formatting for distance race times (2+ minutes)
        """
        distance_times = [
            (240.5, "04:00.500"),     # 1500m time
            (300.0, "05:00.000"),     # Mile time
            (900.25, "15:00.250"),    # 5K time
            (1800.75, "30:00.750"),   # 10K time
            (5400.0, "90:00.000"),    # Half marathon time
        ]
        
        for time_seconds, expected in distance_times:
            result = formatter.format_time(time_seconds)
            assert result == expected, f"Distance time {time_seconds}s should format as {expected}"
    
    def test_cross_country_race_times(self, formatter):
        """
        🌲 Test typical cross country race time ranges
        """
        cc_times = [
            (960.5, "16:00.500"),     # Fast 5K XC time
            (1200.25, "20:00.250"),   # Average 5K XC time
            (1500.75, "25:00.750"),   # Slower 5K XC time
            (420.0, "07:00.000"),     # Fast 2-mile XC time
            (540.33, "09:00.330"),    # Average 2-mile XC time
        ]
        
        for time_seconds, expected in cc_times:
            result = formatter.format_time(time_seconds)
            assert result == expected, f"Cross country time {time_seconds}s should format as {expected}"
    
    def test_marathon_times_with_hours(self, formatter):
        """
        🏃‍♂️ Test marathon and ultra-marathon times using hours format
        """
        marathon_times = [
            (7500.0, "02:05:00.000"),    # Elite marathon time
            (10800.5, "03:00:00.500"),   # Good amateur marathon
            (14400.25, "04:00:00.250"),  # Average marathon time
            (18000.0, "05:00:00.000"),   # Slower marathon time
            (28800.75, "08:00:00.750"),  # Ultra-marathon time
        ]
        
        for time_seconds, expected in marathon_times:
            result = formatter.format_time_hours(time_seconds)
            assert result == expected, f"Marathon time {time_seconds}s should format as {expected}"
    
    def test_timing_precision_for_close_finishes(self, formatter):
        """
        🏁 Test precision needed for very close race finishes
        Critical for determining winners in tight races
        """
        close_finish_times = [
            (123.456, "02:03.456"),
            (123.457, "02:03.457"),  # 1ms difference
            (123.458, "02:03.458"),  # 2ms difference
            (123.459, "02:03.459"),  # 3ms difference
            (123.460, "02:03.460"),  # 4ms difference
        ]
        
        formatted_times = []
        for time_seconds, expected in close_finish_times:
            result = formatter.format_time(time_seconds)
            assert result == expected, f"Close finish time {time_seconds}s should format as {expected}"
            formatted_times.append(result)
        
        # Verify all times are different (no precision loss)
        assert len(set(formatted_times)) == len(formatted_times), "All close finish times should be distinguishable"


if __name__ == '__main__':
    # Allow running directly with pytest
    pytest.main([__file__, "-v"])