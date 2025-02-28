import streamlit as st
from langchain_openai import ChatOpenAI
from config.config import Config
from services.sports_service import SportsService
from services.calendar_service import CalendarService
from agents.query_parser import QueryParser
from agents.sports_finder import SportsFinder
from agents.match_filter import MatchFilter
from agents.calendar_agent import CalendarAgent
from graph.workflow import create_workflow, WorkflowState

st.set_page_config(page_title="Sports Match Scheduler", layout="wide")

@st.cache_resource
def init_services_and_workflow():
    # model = ChatOpenAI(temperature=Config.LLM_TEMPERATURE,  model=Config.LLM_MODEL)
    sports_service = SportsService()
    calendar_service = CalendarService()

    query_parser = QueryParser()
    sports_finder = SportsFinder(sports_service)
    match_filter = MatchFilter()
    calendar_agent = CalendarAgent(calendar_service)

    workflow = create_workflow(
        query_parser,
        sports_finder,
        match_filter,
        calendar_agent
    )
    print(workflow)
    return workflow

workflow = init_services_and_workflow()

# UI Components
st.title("🏆 Sports Match Scheduler")

# Sidebar for favorite teams
st.sidebar.title("⚽ Your Favorite Teams")
with st.sidebar:
    if 'favorite_teams' not in st.session_state:
        st.session_state.favorite_teams = []
    
    new_team = st.text_input("Add a new favorite team:")
    if st.button("Add Team") and new_team:
        if new_team not in st.session_state.favorite_teams:
            st.session_state.favorite_teams.append(new_team)
    
    st.write("Your favorite teams:")
    for team in st.session_state.favorite_teams:
        col1, col2 = st.columns([3,1])
        col1.write(team)
        if col2.button("❌", key=f"delete_{team}"):
            st.session_state.favorite_teams.remove(team)
            st.rerun()

# Main content
query = st.text_input("Ask about sports matches:", 
                     placeholder="Are there any football matches tomorrow?")

if st.button("Search and Schedule"):
    with st.spinner("Processing your request..."):
        # Initialize workflow state
        initial_state: WorkflowState = {
            "query": query,
            "parsed_query": {},
            "matches": [],
            "favorite_teams": st.session_state.favorite_teams,
            "filtered_matches": [],
            "scheduled_events": [],
            "error": ""
        }

        # Execute workflow
        final_state = workflow.invoke(initial_state)

        # Handle results
        if final_state.get('error'):
            st.error(final_state['error'])
        else:
            if final_state['filtered_matches']:
                st.success(f"Found {len(final_state['filtered_matches'])} matches!")
                st.dataframe(final_state['filtered_matches'])
                
                if final_state['scheduled_events']:
                    st.success("Successfully scheduled matches!")
                    for event in final_state['scheduled_events']:
                        st.write(f"Scheduled: {event['summary']}")
            else:
                st.info("No matches found with your favorite teams.")

# Help section
with st.expander("ℹ️ How to use"):
    st.write("""
    1. Add your favorite teams in the sidebar
    2. Ask about matches (e.g., "Are there any football matches tomorrow?")
    3. Click 'Search and Schedule' to find and schedule matches
    """)