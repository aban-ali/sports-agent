from datetime import datetime, timedelta
from typing import List, Dict
from models.schemas import Match, SportType

def calculate_date_range(timeframe: str) -> tuple[datetime, datetime]:
    """Calculate start and end dates based on timeframe"""
    start_date = datetime.now()
    
    if timeframe == "tomorrow":
        start_date += timedelta(days=1)
        end_date = start_date + timedelta(days=1)
    elif timeframe == "week":
        end_date = start_date + timedelta(days=7)
    else:  # today
        end_date = start_date + timedelta(days=1)
    
    return start_date, end_date

def filter_matches_by_favorites(
    matches: List[Match],
    favorite_teams: List[str]
) -> List[Match]:
    """Filter matches based on favorite teams"""
    return [
        match for match in matches
        if match.team1 in favorite_teams or match.team2 in favorite_teams
    ]

def format_match_for_display(match: Match) -> Dict:
    """Format match data for display"""
    return {
        "Teams": f"{match.team1} vs {match.team2}",
        "Date": match.start_time.strftime("%Y-%m-%d"),
        "Time": match.start_time.strftime("%H:%M"),
        "Sport": match.sport.value,
        "Venue": match.venue or "TBD",
        "Competition": match.competition or "N/A"
    }