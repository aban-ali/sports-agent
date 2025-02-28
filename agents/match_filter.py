from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph

class MatchFilter:
    def filter_matches(self, state):
        try:
            filtered = [
                match for match in state['matches']
                if match['team1'] in state['favorite_teams'] and 
                   match['team2'] in state['favorite_teams']
            ]
            state['filtered_matches'] = filtered
            print(state)
            return state
        except Exception as e:
            state['error'] = f"Failed to filter matches: {str(e)}"
            return state