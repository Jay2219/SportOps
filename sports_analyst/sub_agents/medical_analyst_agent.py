from .physio_agent import physio_agent
from google.adk.agents import SequentialAgent
from sports_analyst.config import AgentConfig
from .biomechanics_agent import biomechanics_agent
from .medical_historian_agent import medical_historian

medical_analyst = SequentialAgent(
    name="medical_analyst",
    sub_agents=[biomechanics_agent, medical_historian, physio_agent],
    before_agent_callback = AgentConfig.conditional_execution_callback
)