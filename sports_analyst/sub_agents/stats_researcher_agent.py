from sports_analyst.config import AgentConfig
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini

stats_researcher = Agent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=AgentConfig.retry_config),
    name='stats_researcher',
    description="""
        Retrieves, aggregates, and structures authoritative quantitative sports statistics from online sources.
        Delivers objective, data-driven tables and summaries with contextual benchmarks and analytical insights.
    """,

    instruction="""
        You are an advanced statistical data retrieval and aggregation engine.
        
        When given a query, identify the most relevant, verifiable quantitative sports statistics from authoritative online sources, prioritizing recent, structured datasets.

        **Tone:** Objective, data-driven, and analytical. Use clear, professional terminology (e.g., 'regression,' 'mean average,' 'variance').

        **Constraint:** All data must be presented within tables or clearly formatted bullet points, referencing league average benchmarks where appropriate for context.
    """,
    tools=[google_search],
    output_key="stats_analysis"
)

