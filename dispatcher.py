# --- File: dispatcher.py (COMPLETE AND FINAL) ---

# All these imports are now CORRECTED (no leading dots)
from gemini_helper import ask_gemini
from google_search import google_search
from calendar_helper import get_daily_briefing, create_calendar_event
from memory_helper import remember_info, recall_info, forget_info

def dispatch_command(command_data, user_prompt):
    """
    Executes the command determined by the agent_router.
    This version is for the cloud and only includes cloud-compatible tools.
    """
    command = command_data.get("command")
    params = command_data.get("params", {})
    
    print(f"Executing command: {command} with params: {params}")

    try:
        if command == "google_search":
            query = params.get("query")
            return google_search(query)
        
        elif command == "get_daily_briefing":
            day = params.get("day", "today")
            return get_daily_briefing(day)
            
        elif command == "create_calendar_event":
            summary = params.get("summary")
            start_time = params.get("start_time")
            if not summary or not start_time:
                return "To create an event, I need a title and a start time."
            return create_calendar_event(summary, start_time)

        elif command == "remember_info":
            key = params.get("key")
            value = params.get("value")
            return remember_info(key, value)
            
        elif command == "recall_info":
            key = params.get("key")
            return recall_info(key)
            
        elif command == "forget_info":
            key = params.get("key")
            return forget_info(key)

        elif command == "general_chat":
            return ask_gemini(user_prompt)
            
        else:
            return f"I received an unknown command: {command}. I'll try to answer directly. " + ask_gemini(user_prompt)
            
    except Exception as e:
        print(f"❌ Error during command dispatch: {e}")
        return f"I'm sorry, an error occurred while I was trying to perform that action: {e}"