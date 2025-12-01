import json
from google import genai
from typing import Optional
from google.genai import types
from .sub_agents.head_analyst_agent import head_analyst
from .sub_agents.data_analyst_agent import data_analyst
from .sub_agents.medical_analyst_agent import medical_analyst
from .sub_agents.data_researcher_agent import data_researcher
from google.adk.agents.callback_context import CallbackContext
from .sub_agents.performance_analyst_agent import performance_analyst

client = genai.Client()

class CallBackConfig:

    AGENT_REGISTRY = {
        "head_analyst": head_analyst,
        "medical_analyst": medical_analyst,
        "data_researcher": data_researcher,
        "performance_analyst": performance_analyst
    }

    def run_general_agent(user_query: str) -> str:
        """
        This represents a restricted general agent that handles off-topic queries.
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction="""
                    RESTRICTIONS: 
                    1. Sports Analytics Focused: Replies should be strictly limited to sports-related topics.
                    2. General Knowledge Only: No analysis of videos or technical coding tasks.
                    3. Concise Replies: Keep responses brief and to the point.
                    4. Out-of-Domain: If the query is not related to sports analytics, no reply will be given, and the assistant will politely refrain from responding.
                """
            ),
            contents=[user_query]
        )
        return response.text

    def relevance_and_planning_callback(callback_context: CallbackContext) -> Optional[types.Content]:
        """
        1. Checks if query is Relevant.
        2. If Relevant, decides WHICH sub-agents are needed and saves to State.
        """

        callback_context.state["video_analysis"] = ""
        callback_context.state["stats_analysis"] = ""
        callback_context.state["physio_analysis"] = ""
        callback_context.state["tactical_analysis"] = ""
        callback_context.state["qualitative_analysis"] = ""
        callback_context.state["biomechanics_analysis"] = ""
        callback_context.state["medical_history_analysis"] = ""
        callback_context.state["analysis_report"] = ""

        user_msg = getattr(callback_context, "user_content", None)
        user_text = user_msg.parts[0].text if user_msg and user_msg.parts else ""
        
        print(f"\n[Planner] Analyzing: {user_text}")

        descriptions = "\n".join([f"- {name}" for name in CallBackConfig.AGENT_REGISTRY.keys()])

        prompt = f"""
            You are the Orchestrator.
            User Query: "{user_text}"
            
            Available Agents: {descriptions}
            
            Instructions:
            1. If query is NOT about sports/analysis, return status="BLOCKED".
            2. If query IS relevant, return status="OK" and the list of agents needed.
            
            Output JSON:
            {{
                "status": "OK" or "BLOCKED",
                "response": "Error message if blocked",
                "agents": ["data_researcher", "head_analyst"] 
            }}
        """

        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        plan = json.loads(resp.text)

        if plan.get("status") == "BLOCKED":
            general_response_text = CallBackConfig.run_general_agent(user_text)
            return types.Content(
                role="model",
                parts=[types.Part(text=f"{general_response_text}")]
            )

        required_agents = plan.get("agents", [])

        callback_context.state["active_agents"] = required_agents

        print(f"[Planner] 📝 Plan approved. Active Agents: {required_agents}")
        return None

    def relevance_check_callback(callback_context: CallbackContext) -> Optional[types.Content]:
        """
        Checks if the query is related to the 'Video Analysis' domain.
        If NOT, it routes the query to the General Agent and skips the Main Agent.
        """

        callback_context.state["video_analysis"] = ""
        callback_context.state["stats_analysis"] = ""
        callback_context.state["tactical_analysis"] = ""
        callback_context.state["qualitative_analysis"] = ""

        agent_name = callback_context.agent_name
        user_content = getattr(callback_context, "user_content", None)
        
        user_text = ""
        if user_content and user_content.parts:
            for part in user_content.parts:
                if part.text:
                    user_text += part.text + " "
        
        user_text = user_text.strip()

        if not user_text:
            return None

        classification_resp = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                temperature=0.0,
                system_instruction="""
                    You are a classifier. Your specific domain is: SPORTS ANALYSIS.
                    Analyze the user input.
                    If the input is asking to analyze a video, describe a scene, or discuss visual data, output 'RELATED'.
                    If the input is general conversation, math, history, or greeting, output 'NOT_RELATED'.
                    Output ONLY the label.
                """
            ),
            contents=[user_text]
        )
        
        decision = classification_resp.text.strip().upper()

        if "NOT_RELATED" in decision:
            
            general_response_text = CallBackConfig.run_general_agent(user_text)
            
            return types.Content(
                role="model",
                parts=[types.Part(text=f"{general_response_text}")]
            )
        else:
            return None

