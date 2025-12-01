from google.adk.agents import ParallelAgent
from sports_analyst.config import AgentConfig
from .stats_researcher_agent import stats_researcher
from .information_researcher_agent import information_researcher

data_researcher = ParallelAgent(
    name="data_researcher",
    sub_agents=[stats_researcher, information_researcher],
    before_agent_callback = AgentConfig.conditional_execution_callback
)