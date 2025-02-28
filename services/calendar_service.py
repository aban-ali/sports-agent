from typing import Dict, Optional
from datetime import datetime, timedelta
from langchain_google_community.calendar.create_event import CalendarCreateEvent
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from config.config import Config

class CalendarService:
    def __init__(self):
        self.calendar_tool = CalendarCreateEvent(
            credentials_path=Config.GOOGLE_CALENDAR_CREDENTIALS
        )
        
        # Initialize LLM for processing
        self.llm = ChatOpenAI(temperature=0, model="sonar")
        
        # Create an agent that can use the calendar tool
        self.agent = initialize_agent(
            tools=[self.calendar_tool],
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    
    def schedule_match(self, match_details: Dict) -> Optional[Dict]:
        """
        Schedule a match using LangChain's Google Calendar integration
        
        Args:
            match_details: Dictionary containing match information
        """
        try:
            # Format event details for the agent
            event_description = f"""
            Create a calendar event for a {match_details['sport']} match:
            - Teams: {match_details['team1']} vs {match_details['team2']}
            - Date and Time: {match_details['start_time'].isoformat()}
            - Competition: {match_details.get('competition', '')}
            
            Set a reminder for 24 hours before by email and 30 minutes before by popup.
            """
            
            # Use the agent to create the event
            response = self.agent.run(event_description)
            
            # Process the agent's response
            return self.process_agent_response(response)
            
        except Exception as e:
            raise Exception(f"Failed to schedule match: {str(e)}")
    
    def process_agent_response(self, response: str) -> Optional[Dict]:
        try:
            # Use LLM to extract structured data from the response
            prompt = ChatPromptTemplate.from_messages([
                ("system", """
                Extract the created event details from the following response.
                Return a JSON object with the event ID and creation status.
                """),
                ("user", response)
            ])
            
            result = self.llm.invoke(prompt.format_messages())
            
            import json
            return json.loads(result.content)
        except Exception:
            return None