# --- File: dispatcher.py (COMPLETE AND FINAL) ---

# All imports are correct
from gemini_helper import ask_gemini
from google_search import google_search
from calendar_helper import get_daily_briefing, create_calendar_event
from memory_helper import remember_info, recall_info, forget_info

def dispatch_command(command_data, user_prompt):
    command = command_data.get("command")
    params = command_data.get("params", {})
    
    try:
        if command == "google_search":
            return google_search(params.get("query"))
        
        elif command == "get_daily_briefing":
            return get_daily_briefing(params.get("day", "today"))
            
        elif command == "create_calendar_event":
            return create_calendar_event(params.get("summary"), params.get("start_time"))

        elif command == "remember_info":
            return remember_info(params.get("key"), params.get("value"))
            
        elif command == "recall_info":
            return recall_info(params.get("key"))
            
        elif command == "forget_info":
            return forget_info(params.get("key"))

        elif command == "general_chat":
            return ask_gemini(user_prompt)
            
        else:
            return ask_gemini(f"The command '{command}' is unknown. Please answer this user prompt directly: {user_prompt}")
            
    except Exception as e:
        return f"An error occurred while performing the action: {e}"