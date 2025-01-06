from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools 
from phi.tools.duckduckgo import DuckDuckGo
import openai



import os
from dotenv import load_dotenv
load_dotenv()

api_key=os.environ.get("GROQ_API_KEY")

# OPENAI_API_KEY='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'

#First_agent_Web_search_agent
websearch_agent=Agent(
    name="Web search agent",
    role = "Go into the web and search for the information",
    model=Groq(id ="llama-3.2-1b-preview"),
    tools =[DuckDuckGo()],
    instructions= ["Always include the sources information"],
    show_tools_calls = True,
    markdown= True
)

#Second_agent_financial_agent

finance_agent = Agent(
    name="Finance AI-agent",
    model=Groq(id ="llama-3.2-1b-preview"),
    tools = [YFinanceTools(stock_price=True, analyst_recommendations=True, company_news=True)],
    instructions=["Format your response using markdown and use tables to display data where possible."],
    show_tool_calls=True,
    markdown=True
)


multi_AI_agent = Agent(
    model=Groq(id ="llama-3.2-1b-preview"),
    team = [websearch_agent, finance_agent],
    instructions = ["Always include the sources","Use table to display the data"],
    show_tool_calls=True,
    markdown=True
)

multi_AI_agent.print_response("Sumamrize Analyst recommendation and share the latest news for Gold future", stream = True)