# File: tasks/audio_controller.py (DEFINITIVE - using soundcard library)

import soundcard as sc
import time

# --- CONFIGURATION ---
# We will find these names dynamically now, which is more robust.
VIRTUAL_CABLE_INPUT_NAME = "CABLE Input"
VIRTUAL_CABLE_OUTPUT_NAME = "CABLE Output"

_original_default_speaker = None
_original_default_mic = None

def switch_to_transcription_mode():
    """
    Saves the current default devices and switches to the virtual cable.
    """
    global _original_default_speaker, _original_default_mic
    print("INFO: Switching to Transcription Audio Mode...")

    try:
        # 1. Save the current default devices
        _original_default_speaker = sc.default_speaker()
        _original_default_mic = sc.default_microphone()
        print(f"INFO: Stored original speaker: '{_original_default_speaker.name}'")
        print(f"INFO: Stored original microphone: '{_original_default_mic.name}'")

        # 2. Find the virtual cable devices by name
        cable_input = sc.get_speaker(VIRTUAL_CABLE_INPUT_NAME, include_loopback=True)
        cable_output = sc.get_microphone(VIRTUAL_CABLE_OUTPUT_NAME, include_loopback=True)

        if not cable_input or not cable_output:
            return "Error: Could not find the necessary VB-CABLE devices."

        # 3. Set the new defaults (This is a feature of the library, may not work on all systems)
        # The soundcard library does not have a cross-platform way to SET the default device.
        # This is a known limitation. We will handle this gracefully.
        print("\n" + "="*50)
        print("ACTION REQUIRED: Automatic switching is not supported by this library.")
        print("Please manually set your default devices for transcription:")
        print(f"  - Playback/Speaker: {VIRTUAL_CABLE_INPUT_NAME}")
        print(f"  - Recording/Microphone: {VIRTUAL_CABLE_OUTPUT_NAME}")
        print("="*50 + "\n")
        
        return "Audio devices must be set manually for transcription."

    except Exception as e:
        return f"An error occurred while trying to switch audio modes: {e}"


def revert_to_normal_mode():
    """
    Guides the user to switch back to their original devices.
    """
    print("INFO: Reverting to Normal Audio Mode...")
    if not _original_default_speaker or not _original_default_mic:
        return "Original devices not stored. Please switch back manually."

    print("\n" + "="*50)
    print("ACTION REQUIRED: Please manually switch your default devices back to normal:")
    print(f"  - Playback/Speaker: '{_original_default_speaker.name}'")
    print(f"  - Recording/Microphone: '{_original_default_mic.name}'")
    print("="*50 + "\n")
    
    return "Audio devices can now be restored to their original settings."