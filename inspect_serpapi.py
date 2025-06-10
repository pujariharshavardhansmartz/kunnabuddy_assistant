# File: inspect_serpapi.py
import serpapi
import inspect

print("--- Inspecting the 'serpapi' library ---")

# Get all members (classes, functions, etc.) of the serpapi module
members = inspect.getmembers(serpapi)

found_class = False
print("\nPossible Client/Search classes found:")
for name, member_type in members:
    # We are looking for a class that might be the client
    if inspect.isclass(member_type):
        print(f"- Found class: {name}")
        # Common names for API clients
        if "search" in name.lower() or "client" in name.lower():
            print(f"  ^^^ This is a likely candidate!")
            found_class = True

if not found_class:
    print("\nCould not automatically identify a likely candidate class.")
    print("Please check the library's documentation for the correct class to use.")

print("\n--- Full Directory of 'serpapi' ---")
print(dir(serpapi))