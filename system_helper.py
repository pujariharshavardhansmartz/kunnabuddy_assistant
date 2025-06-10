# File: tasks/system_helper.py (with App Launcher and File Finder)

import os
import subprocess
import platform

# --- ============================= ---
# ---       APP LAUNCHER            ---
# --- ============================= ---

# We store the full, absolute paths for applications.
# IMPORTANT: Adjust these paths if your installation is different.
APP_MAP = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe", # Standard 64-bit path
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "vscode": r"C:\Users\Harsha\AppData\Local\Programs\Microsoft VS Code\Code.exe", 
    "visual studio code": r"C:\Users\Harsha\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}
# The 'r' before the string means it's a "raw" string.

def open_application(app_name):
    """
    Opens a specified application using a map of known paths.
    """
    print(f"🖥️ Attempting to open application: '{app_name}'")
    
    if platform.system() != "Windows":
        return "Sorry, I can only open applications on a Windows system."

    executable_path = APP_MAP.get(app_name.lower())

    if not executable_path:
        return f"Sorry, I don't have the path for '{app_name}' configured."

    # For simple names like 'notepad.exe', we don't need to check the path.
    # For full paths, we should check if they exist.
    if "\\" in executable_path and not os.path.exists(executable_path):
         return f"I found a path for '{app_name}', but it seems incorrect. Please check the path in system_helper.py."

    try:
        subprocess.Popen([executable_path])
        confirmation = f"I've launched {app_name.title()} for you."
        print(f"✅ {confirmation}")
        return confirmation
        
    except FileNotFoundError:
        return f"Sorry, I couldn't find the application at the path: '{executable_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- ============================= ---
# ---        FILE FINDER            ---
# --- ============================= ---

def find_file(file_name, search_directory="C:\\"):
    """
    Searches for a file within a given directory and its subdirectories.
    
    Args:
        file_name (str): The name of the file to search for (e.g., "report.pdf").
        search_directory (str): The top-level directory to start searching from (e.g., "C:\\Users\\Harsha\\Documents").
                               Defaults to the entire C: drive.
    
    Returns:
        str: The full path to the first found file, or a not-found message.
    """
    print(f"🔎 Searching for '{file_name}' in '{search_directory}'... This may take a while.")
    
    try:
        # os.walk is a powerful generator that "walks" a directory tree.
        for root, dirs, files in os.walk(search_directory):
            if file_name in files:
                found_path = os.path.join(root, file_name)
                print(f"✅ File found at: {found_path}")
                return f"I found the file. It is located at: {found_path}"
    
    except Exception as e:
        return f"An error occurred while searching for the file: {e}"

    # If the loop completes without finding the file
    return f"Sorry, I could not find the file '{file_name}' within the directory '{search_directory}'."