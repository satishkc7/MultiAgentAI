
import typer 
from typing import Optional
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector


import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"]= os.getenv("GROQ_API_KEY")
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://securities.arkansas.gov/wp-content/uploads/2022/06/IPT_Stocks_2015_Arkansas.pdf"],
    vector_db=PgVector(table_name="Stock_info", db_url=db_url)
)

knowledge_base.load()

storage = PgAssistantStorage(table_name="Stock_assistant",db_url= db_url)

def stock_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_sessions: List[str] = storage.get_all_run_ids(user)
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0]

    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge=knowledge_base,
        storage=storage,
        # Show tool calls in the response
        show_tool_calls=True,
        # Enable the agent to read the chat history
        read_chat_history=True,
    
    )
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Session: {run_id}\n")
    else:
        print(f"Continuing Session: {run_id}\n")

    # Runs the agent as a cli app
    assistant.cli_app(markdown=True)


if __name__ == "__main__":
    typer.run(stock_assistant)