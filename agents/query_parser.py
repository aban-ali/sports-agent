from typing import Dict, Optional
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config.config import Config

class QueryState(BaseModel):
    query: str
    parsed_query: Dict = {}
    error: Optional[str] = None

class QueryParser:
    def __init__(self,model ="sonar"):
        self.llm = ChatOpenAI(temperature=0, model=model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system","You are a sports query parser. Extract the sport type and time frame from user queries."),
            ("user","Extract sport type (football/cricket/volleyball) and time frame (convert it in yyyy-mm-dd format) from: \
                {query} \
                    \n Return the answer strictly in format as follows - \n\
                    sport:tennis \
                    timeframe:2025-04-25")
        ])
    def parse(self,state):
        try:
            response=self.llm.invoke(
                self.prompt.format_messages(query=state.query)
            )
            values=response.content.strip().split("\n")
            res={}
            for val in values:
                if ':' in val:
                    key,value=val.split(':')
                    res[key.strip().lower()]=value.strip().lower()
            state.parsed_query = res
            print("In Query Parser")
            print(state)
            return state
        except Exception as e:
            state["error"] = f"Failed to parse the query \n {str(e)}"
            return state