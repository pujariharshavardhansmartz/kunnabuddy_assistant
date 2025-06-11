# File: tasks/health_helper.py

import os
import csv
from datetime import datetime

# --- CONFIGURATION ---
HEALTH_LOG_FILE = "kunnabuddy_health_log.csv"
LOG_HEADERS = ["Timestamp", "MetricType", "Value", "Unit"]

def _ensure_log_file_exists():
    """Checks if the log file exists, and creates it with headers if it doesn't."""
    if not os.path.exists(HEALTH_LOG_FILE):
        with open(HEALTH_LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADERS)
        print(f"INFO: Created new health log file: {HEALTH_LOG_FILE}")

def log_health_metric(metric_type, value, unit=""):
    """
    Logs a new health-related metric to the CSV file.
    
    Args:
        metric_type (str): The type of metric (e.g., "water", "run", "calories").
        value (str): The value of the metric (e.g., "500", "5").
        unit (str): The unit for the value (e.g., "ml", "km").
        
    Returns:
        str: A confirmation message.
    """
    try:
        _ensure_log_file_exists()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare the new row of data
        new_row = [timestamp, metric_type.lower(), value, unit.lower()]
        
        with open(HEALTH_LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
            
        confirmation = f"Logged: {metric_type.title()} - {value} {unit}."
        print(f"✅ Health Log: {confirmation}")
        return f"Got it. I've logged that for you."

    except Exception as e:
        error_message = f"Sorry, I couldn't log the health metric. Error: {e}"
        print(f"❌ {error_message}")
        return error_message

def get_health_summary(metric_type, days=7):
    """
    Reads the health log and provides a summary for a specific metric
    over a given number of days. (For now, it will just show recent entries).
    """
    try:
        if not os.path.exists(HEALTH_LOG_FILE):
            return "You haven't logged any health data yet."
        
        recent_entries = []
        with open(HEALTH_LOG_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Simple filter for the requested metric type
                if metric_type.lower() in row["MetricType"].lower():
                    # We can add date filtering here later
                    recent_entries.append(
                        f"- On {row['Timestamp']}, you logged: {row['Value']} {row['Unit']}"
                    )
        
        if not recent_entries:
            return f"I couldn't find any recent entries for '{metric_type}'."
            
        # Get the last 5 entries for a concise summary
        summary = f"Here are your last 5 entries for '{metric_type.title()}':\n"
        summary += "\n".join(recent_entries[-5:])
        
        return summary
        
    except Exception as e:
        error_message = f"Sorry, I couldn't get the health summary. Error: {e}"
        print(f"❌ {error_message}")
        return error_message