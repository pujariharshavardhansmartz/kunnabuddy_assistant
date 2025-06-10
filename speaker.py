# --- UPDATED FILE: tasks/speaker.py (with Stop Function) ---

import pygame
from gtts import gTTS
import io
import threading

# Global flag to check if audio is currently playing
_is_speaking = False

def stop_speaking():
    """
    Public function to forcefully stop any currently playing speech.
    """
    global _is_speaking
    if _is_speaking:
        print("INFO: Received stop command. Halting audio playback.")
        pygame.mixer.music.stop()
        _is_speaking = False

def _play_audio(fp):
    """Internal function that will run on a separate thread to play the audio."""
    global _is_speaking
    try:
        _is_speaking = True
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"❌ Error during audio playback: {e}")
    finally:
        # Check if the audio finished naturally (wasn't stopped)
        if _is_speaking:
             _is_speaking = False
        fp.close()

def say_text_non_blocking(text):
    """
    Generates speech and plays it in a non-blocking background thread.
    The main program can continue running while the audio plays.
    """
    global _is_speaking
    if not text or not text.strip():
        print("INFO: No text provided to speak.")
        return

    if _is_speaking:
        print("INFO: Speech is already in progress. New request ignored.")
        return

    print(f"🔊 KunnaBuddy speaking (in background)...")
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        playback_thread = threading.Thread(target=_play_audio, args=(fp,))
        playback_thread.daemon = True
        playback_thread.start()

    except Exception as e:
        print(f"❌ Error in text-to-speech generation: {e}")

def say_text(text):
    """The original blocking version of the function."""
    print(f"🔊 KunnaBuddy speaking (blocking)...")
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"❌ Error in text-to-speech: {e}")