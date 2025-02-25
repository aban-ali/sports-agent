from Typing import Dict, Optional
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class QueryState(BaseModel):
    query: str
    response: Dict = {}
    error: Optional[str]

class QueryParser:
    def __init__(self,model ="sonar"):
        self.llm = ChatOpenAI(temperature=0, model=model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system","You are a sports query parser. Extract the sport type and time frame from user queries."),
            ("user","Extract sport type (football/cricket/volleyball) and time frame (today/tomorrow/week) from: \
                {query} \
                    \n Return the answer strictly in yaml format as follows - \n\
                    sport:tennis \
                    time:2025-04-25")
        ])
    def parse(self,state: QueryState) -> QueryState:
        try:
            response=self.llm.invoke(
                self.prompt.format_messages(query=state["query"])
            )
            values=response.strip().split("\n")
            print(values)
            res={}
            for val in values:
                if ':' in val:
                    key,value=val.split(':')
                    res[key.strip().lower()]=value.strip().lower()
        except Exception as e:
            state["error"] = f"Failed to parse the query \n {str(e)}"
            return state