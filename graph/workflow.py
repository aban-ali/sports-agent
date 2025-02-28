from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from agents.query_parser import QueryParser
from agents.sports_finder import SportsFinder
from agents.match_filter import MatchFilter
from agents.calendar_agent import CalendarAgent

class WorkflowState(TypedDict):
    query: str
    parsed_query: Optional[Dict] = None
    matches: Optional[list] = None
    favorite_teams: Optional[list] = None
    filtered_matches: Optional[list] = None
    scheduled_events: Optional[list] = None
    error: str = ""

def create_workflow(
    query_parser: QueryParser, sports_finder: SportsFinder,
    match_filter: MatchFilter, calendar_agent: CalendarAgent) -> StateGraph:
    
    workflow = StateGraph(state_schema=WorkflowState)

    # Define the nodes
    workflow.add_node("parse_query", query_parser.parse)
    workflow.add_node("find_matches", sports_finder.find_matches)
    workflow.add_node("filter_matches", match_filter.filter_matches)
    workflow.add_node("schedule_matches", calendar_agent.schedule_matches)

    # Define the edges
    workflow.add_edge(START, "parse_query")
    workflow.add_edge("parse_query", "find_matches")
    workflow.add_edge("find_matches", "filter_matches")
    workflow.add_edge("filter_matches", "schedule_matches")
    workflow.add_edge("schedule_matches", END)

    # Define error handling
    def should_end(state: WorkflowState) -> bool:
        return bool(state.get('error'))

    workflow.add_conditional_edges(
        "parse_query",
        should_end,
        {True: END, False: "find_matches"}
    )

    workflow.add_conditional_edges(
        "find_matches",
        should_end,
        {True: END, False: "filter_matches"}
    )

    workflow.add_conditional_edges(
        "filter_matches",
        should_end,
        {True: END, False: "schedule_matches"}
    )

    return workflow.compile()