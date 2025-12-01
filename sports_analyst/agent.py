from google.adk.runners import Runner
from google.adk.agents import SequentialAgent
from google.adk.sessions import DatabaseSessionService
from .sub_agents.head_analyst_agent import head_analyst
from sports_analyst.callback_config import CallBackConfig
from google.adk.apps.app import App, EventsCompactionConfig
from .sub_agents.data_researcher_agent import data_researcher
from .sub_agents.medical_analyst_agent import medical_analyst
from .sub_agents.performance_analyst_agent import performance_analyst

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[data_researcher, performance_analyst, medical_analyst, head_analyst],
    before_agent_callback = CallBackConfig.relevance_and_planning_callback
)

app = App(
    name="sports_analyst",
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,
        overlap_size=1
    )
)

db_url = "sqlite:///my_agent_data.db" # Local SQLite Database
session_service = DatabaseSessionService(db_url=db_url)

runner = Runner(
    app=app, session_service=session_service
)