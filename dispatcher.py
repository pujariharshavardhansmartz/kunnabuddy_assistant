# --- UPDATED FILE: tasks/dispatcher.py (Web App Compatible) ---

from .gemini_helper import ask_gemini
from .google_search import google_search
from .shopping_helper import search_shopping
from .system_helper import open_application, find_file
from .memory_helper import remember_info, recall_info, forget_info 
from .file_helper import summarize_file
from .calendar_helper import get_daily_briefing, create_calendar_event

# --- COMMENTED OUT DESKTOP-ONLY FEATURES ---
# from .reminder_helper import set_reminder, get_pending_reminders, start_reminder_thread
# from .finance_helper import get_current_price, set_price_alert, get_active_alerts
# from .health_helper import log_health_metric, get_health_summary
# from .meeting_helper import start_listening, stop_listening_and_transcribe

# Since we commented out the import, we don't start the thread
# start_reminder_thread()

def dispatch_command(command_data, user_prompt):
    command = command_data.get("command")
    print(f"✅ Dispatcher executing command: '{command}'")

    # --- We will keep the logic for now, but the imports are off ---
    # if command == "set_reminder": 
    #     ...
    # elif command == "get_reminders":
    #     ...
    # (And so on for other commented out features)

    # --- ACTIVE WEB-COMPATIBLE COMMANDS ---
    if command == "open_application":
        return "I can't open applications when running in a web browser."
    elif command == "find_file":
        return "I can't search your local file system from a web browser."
    elif command == "create_calendar_event":
        return create_calendar_event(command_data)
    elif command == "get_daily_briefing":
        day = command_data.get("day", "today")
        return get_daily_briefing(day)
    elif command == "summarize_file":
        return "File summarization is not yet supported in the web version."
    elif command == "remember_info":
        key = command_data.get("key")
        value = command_data.get("value")
        return remember_info(key, value)
    elif command == "recall_info":
        key = command_data.get("key")
        return recall_info(key)
    elif command == "forget_info":
        key = command_data.get("key")
        return forget_info(key)
    elif command == "google_search":
        query = command_data.get("query")
        return google_search(query) if query else "What would you like me to search for?"
    elif command == "search_shopping":
        return "Web automation for shopping is disabled in the web version for now."
    else:
        print("INFO: Command not recognized or supported in web mode, falling back to general chat.")
        return ask_gemini(user_prompt)