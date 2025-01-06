from phi.agent import Agent
import phi.api
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools 
from phi.tools.duckduckgo import DuckDuckGo
import openai

from phi.playground import Playground, serve_playground_app


import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
phi.api = os.getenv("phi_key")


websearch_agent=Agent(
    name="Web search agent",
    role = "Go into the web and search for the information",
    model=OpenAIChat(id ="gpt-3.5-turbo-0125"),
    tools =[DuckDuckGo()],
    instructions= ["Always include the sources information"],
    show_tools_calls = True,
    markdown= True
)

#Second_agent_financial_agent

finance_agent = Agent(
    name="Finance AI-agent",
    model=OpenAIChat(id ="gpt-3.5-turbo-0125"),
    tools = [YFinanceTools(stock_price=True, analyst_recommendations=True, company_news=True)],
    instructions=["Format your response using markdown and use tables to display data where possible."],
    show_tool_calls=True,
    markdown=True
)

app = Playground(agents= [finance_agent, websearch_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload = True)