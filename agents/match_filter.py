from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph

class MatchFilterState(TypedDict):
    matches: List
    favorite_teams: List
    filtered_matches: List
    error: str

class MatchFilter:
    def filter_matches(self, state: MatchFilterState) -> MatchFilterState:
        try:
            filtered = [
                match for match in state['matches']
                if match['team1'] in state['favorite_teams'] or 
                   match['team2'] in state['favorite_teams']
            ]
            state['filtered_matches'] = filtered
            return state
        except Exception as e:
            state['error'] = f"Failed to filter matches: {str(e)}"
            return state