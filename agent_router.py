# --- File: agent_router.py (COMPLETE AND FINAL) ---

import json
import re
from datetime import datetime
# This import is now CORRECTED (no leading dot)
from gemini_helper import ask_gemini

def determine_command(user_prompt):
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    master_prompt = f"""
    Analyze the user's prompt and generate a JSON object that maps to one of the available tools.
    Current time: {current_time_str}. Your ONLY output should be the JSON object.

    ## Tool Reference:
    - **Function**: "get_daily_briefing", **Parameters**: {{"day": "today" or "tomorrow"}}. **Use for**: Checking calendar/schedule/meetings.
    - **Function**: "create_calendar_event", **Parameters**: {{"summary": "event title", "start_time": "YYYY-MM-DDTHH:MM:SS"}}. **Use for**: Creating/scheduling new events.
    - **Function**: "google_search", **Parameters**: {{"query": "search term"}}. **Use for**: Current events, facts, general knowledge.
    - **Function**: "remember_info", **Parameters**: {{"key": "topic", "value": "information"}}. **Use for**: Storing information.
    - **Function**: "recall_info", **Parameters**: {{"key": "topic"}}. **Use for**: Retrieving stored information.
    - **Function**: "forget_info", **Parameters**: {{"key": "topic"}}. **Use for**: Deleting stored information.
    - **Function**: "general_chat", **Parameters**: {{"prompt": "user's original prompt"}}. **Use for**: Greetings, jokes, poems, or anything that doesn't match another tool.

    ## User Request: "{user_prompt}"

    ## Your JSON Output:
    """
    
    try:
        response_text = ask_gemini(master_prompt)
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
        else:
            print(f"❌ Error: No JSON object found in AI response. Response was: {response_text}")
            return {"command": "general_chat", "params": {"prompt": user_prompt}}

        command_data = json.loads(response_text)
        return command_data
    except Exception as e:
        print(f"❌ Error in router: {e}. Defaulting to general chat.")
        return {"command": "general_chat", "params": {"prompt": user_prompt}}