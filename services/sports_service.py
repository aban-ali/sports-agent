from typing import List, Dict
from datetime import datetime, timedelta
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
import json
from config.config import Config
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class SportsService:
    def __init__(self):
        self.search = TavilySearchAPIWrapper(
            tavily_api_key=Config.TAVILY_API_KEY
        )
    
    def get_matches(self, sport_type: str, time_frame: str) -> List[Dict]:        
        search_query = f"{sport_type} matches scheduled for {time_frame}."
        
        try:
            search_results = self.search.results(search_query)
            fixtures = ""
            for res in search_results:
                fixtures += f"{res['content']}\n"

            matches = self.process_search_results(fixtures, sport_type)
            
            return matches
            
        except Exception as e:
            raise Exception(f"Failed to fetch matches: {str(e)}")
    
    def process_search_results(self, results: str, sport_type: str) -> List[Dict]:
        llm = ChatOpenAI(temperature=0, model_name="sonar")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            Extract match information from unstructured raw search results.
            Return a JSON array of matches with the following structure in string format **with no extra text/description**:
            [
                {{
                    "team1": "team name",
                    "team2": "team name",
                    "start_time": "start time in ISO 8601 format",
                    "sport": "sport type",
                    "competition": "competition name"
                }}
            ]
            """),
            ("user", f"Extract match information from the following search results: \n\n {results}")
        ])
        
        response = llm.invoke(prompt.format_messages(results=str(results)))

        try:
            matches = json.loads(response.content)
            
            for match in matches:
                match['start_time'] = datetime.fromisoformat(str(match['start_time']).replace("Z", "+00:00"))
            
            return matches
        except Exception as e:
            raise Exception(f"Failed to process search results: {str(e)}")