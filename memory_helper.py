# --- NEW FILE: tasks/memory_helper.py ---

import os
import json
from datetime import datetime

MEMORY_FILE = "kunnabuddy_memory.json"

def _load_memory():
    """Loads the memory dictionary from the JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If file is empty or corrupted, start with an empty memory
        return {}

def _save_memory(memory_data):
    """Saves the memory dictionary to the JSON file."""
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory_data, f, indent=4)
    except IOError as e:
        print(f"❌ Error saving memory file: {e}")

def remember_info(key, value):
    """Saves a piece of information (a key-value pair) to memory."""
    if not key or not value:
        return "I need both a topic and the information you want me to remember about it."
    
    print(f"🧠 Remembering: '{key}' -> '{value}'")
    memories = _load_memory()
    memories[key.lower()] = {
        "value": value,
        "timestamp": datetime.now().isoformat()
    }
    _save_memory(memories)
    return f"Okay, I've remembered that '{key}' is '{value}'."

def recall_info(key):
    """Recalls a piece of information from memory based on its key."""
    if not key:
        return "What topic do you want me to recall information about?"

    print(f"🧠 Recalling info for: '{key}'")
    memories = _load_memory()
    
    retrieved_item = memories.get(key.lower())
    
    if retrieved_item:
        value = retrieved_item.get("value")
        return f"I remember you told me that '{key}' is '{value}'."
    else:
        return f"I don't have any specific memory stored for '{key}'."

def forget_info(key):
    """Forgets (deletes) a piece of information from memory."""
    if not key:
        return "What topic should I forget?"
        
    print(f"🧠 Forgetting info for: '{key}'")
    memories = _load_memory()
    
    if key.lower() in memories:
        del memories[key.lower()]
        _save_memory(memories)
        return f"Okay, I have forgotten what I knew about '{key}'."
    else:
        return f"I don't have a memory for '{key}', so there's nothing to forget."