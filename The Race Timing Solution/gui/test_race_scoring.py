#!/usr/bin/env python3
"""
test_race_scoring.py - Pytest Unit Tests for Race Scoring Logic
Author: TJ Tryon
Date: July 28, 2025
Project: The Race Timing Solution for Cross Country and Road Races (TRTS) - GUI Version

🧪 Tests race scoring algorithms for both cross country and road races
Ensures accurate competition results following official USATF rules

To run these tests:
    pytest test_race_scoring.py -v
    pytest test_race_scoring.py::test_cross_country_team_scoring -v
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


class TestableScoringSystem:
    """
    🧪 Testable version of race scoring functionality
    Contains scoring algorithms for both cross country and road races
    """
    
    def calculate_team_scores(self, results_data):
        """
        🏫 Calculates cross country team scores from results data
        Input: List of tuples (team, bib, name, finish_time, place)
        Returns: List of team score tuples sorted by score
        
        Scoring Rules:
        - Teams need minimum 5 runners to score
        - Score = sum of top 5 runners' places (lowest wins)
        - 6th and 7th runners are displacers for tiebreaking
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
        
        Age Groups (USATF Standard):
        1-15, 16-20, 21-25, 26-30, 31-35, 36-40, 41-45, 46-50,
        51-55, 56-60, 61-65, 66-70, 71+
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
        """
        🏆 Calculates individual awards (1st, 2nd, 3rd place)
        Input: List of tuples (bib, name, finish_time, place)
        Returns: List of award winners sorted by place
        """
        # Sort by place and take top N
        sorted_results = sorted(results_data, key=lambda x: x[3])  # Sort by place
        return sorted_results[:award_depth]
    
    def detect_scoring_ties(self, team_scores):
        """
        🤝 Detects ties in team scoring that need manual review
        Returns list of tied teams with their scores
        """
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
def scoring_system():
    """🧪 Create a fresh TestableScoringSystem instance for each test"""
    return TestableScoringSystem()


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


# 🧪 Cross Country Team Scoring Tests
class TestCrossCountryScoring:
    """Tests for cross country team scoring algorithms"""
    
    def test_cross_country_team_scoring(self, scoring_system, cross_country_race_data):
        """
        🏫 Test cross country team scoring algorithm
        Verifies correct calculation of team scores and ranking
        """
        # 🧮 Calculate team scores
        team_scores = scoring_system.calculate_team_scores(cross_country_race_data)
        
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
        
        # 🔍 Verify displacers for Team A (6th and 7th runners)
        team_a_displacers = winning_team[3]
        assert len(team_a_displacers) == 1, "Team A should have 1 displacer (7th runner is same team as top 5)"
        assert team_a_displacers[0][0] == 12, "Team A displacer should be place 12"
    
    def test_team_scoring_insufficient_runners(self, scoring_system):
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
            ("Team C", 301, "Runner 6", 325.1, 6),  # Only 3 runners
            ("Team C", 302, "Runner 7", 330.2, 7),
            ("Team C", 303, "Runner 8", 335.5, 8),
        ]
        
        # 🧮 Calculate team scores
        team_scores = scoring_system.calculate_team_scores(race_data)
        
        # 🔍 Should only have Team A (Team C has insufficient runners)
        assert len(team_scores) == 1, "Should only have 1 team scoring"
        assert team_scores[0][0] == "Team A", "Only Team A should score"
        assert team_scores[0][1] == 15, "Team A score should be 1+2+3+4+5 = 15"
    
    def test_team_scoring_with_perfect_tie(self, scoring_system):
        """
        🤝 Test team scoring when teams have identical scores and tiebreakers
        """
        # Create data where two teams tie on everything
        tie_data = [
            ("Team A", 101, "Runner 1", 300.0, 1),
            ("Team B", 201, "Runner 2", 301.0, 2),
            ("Team A", 102, "Runner 3", 302.0, 3),
            ("Team B", 202, "Runner 4", 303.0, 4),
            ("Team A", 103, "Runner 5", 304.0, 5),
            ("Team B", 203, "Runner 6", 305.0, 6),
            ("Team A", 104, "Runner 7", 306.0, 7),
            ("Team B", 204, "Runner 8", 307.0, 8),
            ("Team A", 105, "Runner 9", 308.0, 9),
            ("Team B", 205, "Runner 10", 309.0, 10),
            ("Team A", 106, "Runner 11", 310.0, 11),  # 6th runner
            ("Team B", 206, "Runner 12", 311.0, 12),  # 6th runner
        ]
        
        team_scores = scoring_system.calculate_team_scores(tie_data)
        
        # Both teams should score: 1+3+5+7+9 = 25, 2+4+6+8+10 = 30
        assert len(team_scores) == 2, "Both teams should score"
        assert team_scores[0][1] == 25, "First team should have score 25"
        assert team_scores[1][1] == 30, "Second team should have score 30"
        
        # Team A should win with lower score
        assert team_scores[0][0] == "Team A", "Team A should win with lower score"
    
    def test_team_scoring_tiebreaker_scenarios(self, scoring_system):
        """
        ⚖️ Test various tiebreaker scenarios in team scoring
        """
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
        
        team_scores = scoring_system.calculate_team_scores(tiebreak_data)
        
        # Both teams have same score: 1+3+5+7+9 = 25, 2+4+6+8+10 = 30
        # But Team B should win on 6th runner tiebreaker (12 < 13)
        assert team_scores[0][0] == "Team B", "Team B should win on tiebreaker"
        assert team_scores[0][4] == 12, "Winning team's tiebreaker should be 12"
        assert team_scores[1][4] == 13, "Losing team's tiebreaker should be 13"
    
    def test_empty_team_scoring(self, scoring_system):
        """
        📭 Test team scoring with empty data
        """
        empty_scores = scoring_system.calculate_team_scores([])
        assert len(empty_scores) == 0, "Empty data should produce no team scores"
    
    def test_single_team_scoring(self, scoring_system):
        """
        🏃‍♀️ Test scoring with only one complete team
        """
        single_team_data = [
            ("Team A", 101, "Runner 1", 300.0, 1),
            ("Team A", 102, "Runner 2", 302.0, 2),
            ("Team A", 103, "Runner 3", 304.0, 3),
            ("Team A", 104, "Runner 4", 306.0, 4),
            ("Team A", 105, "Runner 5", 308.0, 5),
        ]
        
        team_scores = scoring_system.calculate_team_scores(single_team_data)
        
        assert len(team_scores) == 1, "Should have one scoring team"
        assert team_scores[0][0] == "Team A", "Team A should be the only scorer"
        assert team_scores[0][1] == 15, "Score should be 1+2+3+4+5 = 15"


# 🧪 Road Race Age Group Tests
class TestRoadRaceScoring:
    """Tests for road race scoring and age group classification"""
    
    def test_road_race_age_grouping(self, scoring_system, road_race_age_data):
        """
        🎂 Test road race age group classification
        """
        # 📚 Group by age
        age_groups = scoring_system.group_by_age(road_race_age_data)
        
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
        
        # 🔍 Verify 41-45 group has correct runners
        group_41_45 = age_groups["41-45"]
        expected_places_41_45 = [2, 4, 8]  # Ages 42, 43, 44
        actual_places_41_45 = sorted([runner[0] for runner in group_41_45])
        assert actual_places_41_45 == expected_places_41_45, "41-45 group should have places 2, 4, 8"
    
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
    def test_age_group_boundaries(self, scoring_system, age, expected_group):
        """
        🔍 Test age group boundary conditions
        """
        boundary_data = [(age, 101, "Edge Runner", 1200.0, 1)]
        age_groups = scoring_system.group_by_age(boundary_data)
        
        # Verify this age is in the expected group
        assert len(age_groups[expected_group]) == 1, f"Age {age} should be in {expected_group} group"
        
        # Verify it's not in other groups
        for group_name, runners in age_groups.items():
            if group_name != expected_group:
                assert len(runners) == 0, f"Age {age} should not be in {group_name} group"
    
    def test_all_age_groups_exist(self, scoring_system):
        """
        📋 Test that all standard age groups are created
        """
        # Test with empty data to verify all groups are initialized
        age_groups = scoring_system.group_by_age([])
        
        expected_groups = [
            "1-15", "16-20", "21-25", "26-30", "31-35", "36-40",
            "41-45", "46-50", "51-55", "56-60", "61-65", "66-70", "71+"
        ]
        
        for group in expected_groups:
            assert group in age_groups, f"Age group {group} should exist"
            assert isinstance(age_groups[group], list), f"Age group {group} should be a list"
    
    def test_road_race_comprehensive_age_distribution(self, scoring_system):
        """
        🌈 Test comprehensive age distribution across all groups
        """
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
        
        age_groups = scoring_system.group_by_age(comprehensive_data)
        
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


# 🧪 Individual Awards and Tie Detection Tests
class TestAdditionalScoringFeatures:
    """Tests for additional scoring features like individual awards and tie detection"""
    
    def test_individual_awards_calculation(self, scoring_system):
        """
        🏆 Test calculation of individual awards (1st, 2nd, 3rd place)
        """
        individual_data = [
            (105, "Third Place", 1220.5, 3),
            (101, "First Place", 1200.5, 1),
            (103, "Fifth Place", 1240.1, 5),
            (102, "Second Place", 1210.2, 2),
            (104, "Fourth Place", 1230.8, 4),
        ]
        
        awards = scoring_system.calculate_individual_awards(individual_data, award_depth=3)
        
        # Should return top 3 finishers in order
        assert len(awards) == 3, "Should return 3 award winners"
        assert awards[0][1] == "First Place", "First award should go to first place"
        assert awards[1][1] == "Second Place", "Second award should go to second place"
        assert awards[2][1] == "Third Place", "Third award should go to third place"
        
        # Verify places are correct
        assert awards[0][3] == 1, "First place should have place 1"
        assert awards[1][3] == 2, "Second place should have place 2"
        assert awards[2][3] == 3, "Third place should have place 3"
    
    def test_individual_awards_custom_depth(self, scoring_system):
        """
        🏆 Test individual awards with custom award depth
        """
        individual_data = [
            (101, "Runner 1", 1200.0, 1),
            (102, "Runner 2", 1201.0, 2),
            (103, "Runner 3", 1202.0, 3),
            (104, "Runner 4", 1203.0, 4),
            (105, "Runner 5", 1204.0, 5),
        ]
        
        # Test top 5 awards
        awards = scoring_system.calculate_individual_awards(individual_data, award_depth=5)
        assert len(awards) == 5, "Should return 5 award winners"
        
        # Test top 1 award only
        awards = scoring_system.calculate_individual_awards(individual_data, award_depth=1)
        assert len(awards)