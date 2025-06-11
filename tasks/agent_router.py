# --- UPDATED FILE: tasks/agent_router.py (with Meeting Tools) ---

from .gemini_helper import ask_gemini
import json
from datetime import datetime, timedelta

def determine_command(user_prompt):
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    master_prompt = f"""
    You are a specialized AI routing system. Your job is to analyze the user's prompt and generate a clean JSON object that maps to an available tool.
    The current date and time is {current_time_str}.

    ## Available Tools and their JSON format:

    1.  **start_listening**: Begins recording system audio for transcription. Use this at the start of a meeting.
        - **JSON**: {{"command": "start_listening"}}

    2.  **stop_listening**: Stops recording system audio and generates a transcript and summary. Use this at the end of a meeting.
        - **JSON**: {{"command": "stop_listening"}}
        
    3.  **get_stock_price**: Fetches the current price of a stock or cryptocurrency.
        - **Required keys**: "ticker"
        - **Example**: "what is the price of microsoft stock" -> {{"command": "get_stock_price", "ticker": "MSFT"}}

    4.  **log_health_metric**: Logs a user-reported health metric.
        - **Required keys**: "metric_type", "value", "unit"
        - **Example**: "i drank 500ml of water" -> {{"command": "log_health_metric", "metric_type": "water", "value": "500", "unit": "ml"}}

    5.  **get_health_summary**: Retrieves a summary of logged health data.
        - **Required keys**: "metric_type"
        - **Example**: "show me my water intake" -> {{"command": "get_health_summary", "metric_type": "water"}}

    6.  **set_reminder**: Sets a future reminder.
        - **Required keys**: "time_value", "time_unit", "message"
        - **Example**: "remind me in 5 minutes" -> {{"command": "set_reminder", "time_value": 5, "time_unit": "minutes", "message": "Follow up"}}

    7.  **google_search**: Use for general knowledge questions.
        - **Required keys**: "query"
        - **Example**: {{"command": "google_search", "query": "latest news on AI"}}
        
    8.  **general_chat**: For any request that does not match the tools above.
        - **Required keys**: "prompt"
        - **Example**: {{"command": "general_chat", "prompt": "tell me a joke"}}

    ## User Request Analysis
    **User's request**: "{user_prompt}"
    **Your JSON output**:
    """
    
    try:
        print("🤔 KunnaBuddy is thinking...")
        response_text = ask_gemini(master_prompt)
        
        if '```' in response_text:
            response_text = response_text.split('```')[1]
            if response_text.lower().strip().startswith('json'):
                response_text = response_text.strip()[4:].strip()

        print(f"🧠 Raw AI Response: {response_text}")
        command_data = json.loads(response_text)
        return command_data
    except Exception as e:
        print(f"❌ Error in router: {e}. Defaulting to general chat.")
        return {"command": "general_chat", "prompt": user_prompt}