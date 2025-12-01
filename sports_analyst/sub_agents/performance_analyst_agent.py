from google.adk.agents import ParallelAgent
from sports_analyst.config import AgentConfig
from .video_analyst_agent import video_analyst
from .tactical_analyst_agent import tactical_analyst

performance_analyst = ParallelAgent(
    name="performance_analyst",
    description="""
        Integrates video and tactical analysis to evaluate athletic performance comprehensively.
        Delivers synchronized insights on movement quality, strategy, and in-game decision-making.
    """,
    sub_agents=[video_analyst, tactical_analyst],
    before_agent_callback = AgentConfig.conditional_execution_callback
)

