from typing import Optional
from google.genai import types
from google.adk.agents.callback_context import CallbackContext

class AgentConfig:

    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

    def conditional_execution_callback(callback_context: CallbackContext) -> Optional[types.Content]:
        """
        Checks Session State. If this agent isn't in 'active_agents', SKIP it.
        """
        current_agent = callback_context.agent_name
        active_list = callback_context.state.get("active_agents", [])

        if active_list and current_agent not in active_list:
            return types.Content(role="model", parts=[types.Part(text=f"[{current_agent} was skipped]")])

        return None
    
    def require_video_input_callback(callback_context: CallbackContext) -> Optional[types.Content]:
        """
        Dynamically inspects the incoming user message to ensure a video is present.
        """

        user_input = getattr(callback_context, "user_content", None)
        
        has_video = False

        if user_input and user_input.parts:
            for part in user_input.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("video/"):
                    has_video = True
                    break
                if part.file_data and part.file_data.mime_type.startswith("video/"):
                    has_video = True
                    break
                if part.text and "[VIDEO]" in part.text: 
                    has_video = True 

        if has_video:
            return None
        else:
            callback_context.state["video_analysis"] = ""

            return types.Content(
                role="model",
                parts=[types.Part(text="⚠️ I can only analyze video inputs. Please upload a video file.")]
            )
