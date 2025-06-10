# --- UPDATED FILE: main.py (with Interrupt Handling) ---

import os
from dotenv import load_dotenv
load_dotenv()

import pygame
# We now import the new stop_speaking function as well
from tasks.speaker import say_text_non_blocking, say_text, stop_speaking 
from tasks.listener import listen_for_command
from tasks.agent_router import determine_command
from tasks.dispatcher import dispatch_command 

pygame.mixer.init()

def main():
    print("\n--- Welcome to KunnaBuddy ---")
    
    mode = ""
    while mode not in ["1", "2"]:
        print("Please select your mode:")
        print("1: Text Mode (Type commands)")
        print("2: Voice Mode (Speak commands)")
        mode = input("Enter your choice (1 or 2): ").strip()
    
    if mode == "1":
        print("\n--- KunnaBuddy is Ready! (Text Mode) ---")
    else:
        print("\n--- KunnaBuddy is Ready! (Voice Mode) ---")
        say_text("Voice mode activated. How can I help you?")

    print("(Say/Type 'stop' to interrupt me, or 'exit'/'quit' to end the session)")
    print("-" * 30)

    while True:
        try:
            user_prompt = ""
            if mode == "1":
                user_prompt = input("🤖 You (Text): ").strip().lower()
            else:
                print("🎤 Listening...")
                user_prompt = listen_for_command()
                if user_prompt: 
                    print(f"🗣️ You (Voice): {user_prompt}")
                else:
                    continue
            
            # --- THE FIX: Check for interrupt and exit commands first ---
            if user_prompt in ['exit', 'quit']:
                say_text("Shutting down. Goodbye!")
                break
                
            if user_prompt == 'stop':
                stop_speaking()
                print("INFO: Playback stopped.")
                continue # Immediately ask for the next command

            if not user_prompt: 
                continue

            # --- REGULAR COMMAND PROCESSING ---
            command_data = determine_command(user_prompt)
            result = dispatch_command(command_data, user_prompt)
            
            print(f"\n✅ Task Result:\n{result}")
            say_text_non_blocking(result)

        except Exception as e:
            error_msg = f"A critical error occurred in the main loop: {e}"
            print(f"🚨 {error_msg}")
            say_text_non_blocking("I've run into an unexpected error. Let's try that again.")
        finally:
            print("-" * 30)

if __name__ == "__main__":
    main()