from typing import TypedDict, List
from langgraph.graph import StateGraph
from services.calendar_service import CalendarService

class CalendarAgentState(TypedDict):
    filtered_matches: List
    scheduled_events: List
    error: str

class CalendarAgent:
    def __init__(self, calendar_service: CalendarService):
        self.calendar_service = calendar_service

    def schedule_matches(self, state: CalendarAgentState) -> CalendarAgentState:
        try:
            scheduled = []
            for match in state['filtered_matches']:
                event = self.calendar_service.schedule_match(match)
                if event:
                    scheduled.append(event)
            state['scheduled_events'] = scheduled
            return state
        except Exception as e:
            state['error'] = f"Failed to schedule matches: {str(e)}"
            return state