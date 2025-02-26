from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph
from services.sports_service import SportsService

class SportsFinderState(TypedDict):
    parsed_query: Dict
    matches: List
    error: str

class SportsFinder:
    def __init__(self, sports_service: SportsService):
        self.sports_service = sports_service

    def find_matches(self, state: SportsFinderState) -> SportsFinderState:
        try:
            parsed_query = state['parsed_query']
            matches = self.sports_service.get_matches(
                parsed_query['sport'],
                parsed_query['timeframe']
            )
            state['matches'] = matches
            return state
        except Exception as e:
            state['error'] = f"Failed to find matches: {str(e)}"
            return state