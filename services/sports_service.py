from typing import List, Dict
from datetime import datetime, timedelta
from langchain.tools import Tool
from langchain.utilities import TavilySearchAPIWrapper
from langchain.agents import load_tools
from config.config import Config

class SportsService:
    def __init__(self):
        # Initialize Tavily Search
        self.search = TavilySearchAPIWrapper(
            tavily_api_key=Config.TAVILY_API_KEY,
            search_depth="advanced",
            max_results=5
        )
        
        # Create search tool
        self.search_tool = Tool(
            name="Sports Search",
            description="Search for sports matches and events",
            func=self.search.run
        )
    
    def get_matches(self, sport_type: str, time_frame: str) -> List[Dict]:
        """
        Fetch matches using LangChain's Tavily integration
        """
        # Calculate date range
        start_date = datetime.now() if '-' not in time_frame else time_frame
        date_str = ""
        
        if time_frame == 'today':
            date_str = datetime.now().strftime('%Y-%m-%d')
        elif time_frame == 'tomorrow':
            start_date += timedelta(days=1)
            date_str = start_date.strftime('%Y-%m-%d')
        elif time_frame == 'week':
            end_date = start_date + timedelta(days=7)
            date_str = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        else:
            date_str = datetime.strptime(time_frame, '%Y-%m-%d').strftime('%Y-%m-%d')

        print(date_str)
        # Construct search query
        search_query = f"{sport_type} matches {date_str} schedule"
        
        try:
            # Use Tavily search through LangChain
            search_results = self.search_tool.run(search_query)
            
            # Process results into structured match data
            matches = self.process_search_results(search_results, sport_type)
            
            return matches
            
        except Exception as e:
            raise Exception(f"Failed to fetch matches: {str(e)}")
    
    def process_search_results(self, results: str, sport_type: str) -> List[Dict]:
        """
        Process search results using LangChain's LLM to extract structured match data
        """
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        
        # Create prompt template for extracting match information
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Extract match information from the following search results.
            Return a JSON array of matches with the following structure:
            [
                {
                    "team1": "team name",
                    "team2": "team name",
                    "start_time": "ISO datetime",
                    "sport": "sport type",
                    "venue": "venue name",
                    "competition": "competition name"
                }
            ]
            Only include matches where you're confident about the information.
            """),
            ("user", f"Sport: {sport_type}\nResults: {results}")
        ])
        
        # Get structured data from LLM
        response = llm.invoke(prompt.format_messages())
        
        try:
            import json
            matches = json.loads(response.content)
            
            # Convert string timestamps to datetime objects
            for match in matches:
                match['start_time'] = datetime.fromisoformat(match['start_time'])
            
            return matches
        except json.JSONDecodeError:
            return []