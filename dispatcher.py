# --- File: dispatcher.py (COMPLETE AND CORRECTED) ---

# These imports are now correct and match the available functions
from gemini_helper import ask_gemini
from google_search import google_search
# The broken 'create_calendar_event' import is now REMOVED
from calendar_helper import get_daily_briefing
from memory_helper import remember_info, recall_info, forget_info

def dispatch_command(command_data, user_prompt):
    """
    Executes the command determined by the agent_router.
    This version is now in sync with all other helper files.
    """
    command = command_data.get("command")
    params = command_data.get("params", {})
    
    print(f"Executing command: {command} with params: {params}")

    try:
        if command == "google_search":
            return google_search(params.get("query"))
        
        elif command == "get_daily_briefing":
            return get_daily_briefing(params.get("day", "today"))
            
        # The entire block for the broken function is now REMOVED
        # elif command == "create_calendar_event": ...

        elif command == "remember_info":
            return remember_info(params.get("key"), params.get("value"))
            
        elif command == "recall_info":
            return recall_info(params.get("key"))
            
        elif command == "forget_info":
            return forget_info(params.get("key"))

        elif command == "general_chat":
            return ask_gemini(user_prompt)
            
        else:
            # Fallback for any unknown commands
            return ask_gemini(f"The command '{command}' is unknown. Please answer this user prompt directly: {user_prompt}")
            
    except Exception as e:
        print(f"❌ Error during command dispatch: {e}")
        return f"I'm sorry, an error occurred while I was trying to perform that action: {e}"