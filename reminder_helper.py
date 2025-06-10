import schedule, time, threading
from .speaker import say_text

_pending_reminders = []

def _run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_reminder_thread():
    thread = threading.Thread(target=_run_scheduler)
    thread.daemon = True
    thread.start()

def _trigger_reminder(message):
    print(f"\n🔔 REMINDER: {message}")
    say_text(f"Hey, this is your reminder: {message}")
    _pending_reminders.pop(0)
    return schedule.CancelJob

def set_reminder(time_value, time_unit, message):
    try:
        val = int(time_value)
        job = None
        if "minute" in time_unit: job = schedule.every(val).minutes
        elif "second" in time_unit: job = schedule.every(val).seconds
        elif "hour" in time_unit: job = schedule.every(val).hours
        else: return f"Unknown time unit: {time_unit}."
        
        job.do(_trigger_reminder, message=message)
        reminder_text = f"'{message}' in {val} {time_unit}"
        _pending_reminders.append(reminder_text)
        return f"Okay, reminder set: {reminder_text}"
    except Exception as e: return f"Error setting reminder: {e}"

def get_pending_reminders():
    if not _pending_reminders: return "No pending reminders."
    return "Pending reminders:\n" + "\n".join(f"- {r}" for r in _pending_reminders)