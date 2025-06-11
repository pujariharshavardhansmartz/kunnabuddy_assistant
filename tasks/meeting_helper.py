# File: tasks/meeting_helper.py (DEFINITIVE - with AI Summarization)

import os, time, re, whisper, sounddevice as sd, numpy as np, tempfile, datetime, threading
from scipy.io.wavfile import write
from .gemini_helper import ask_gemini # <-- NEW IMPORT

# --- WHISPER MODEL (UNCHANGED) ---
SAMPLE_RATE, MODEL_SIZE = 16000, "base.en"
print("INFO: Loading transcription model...")
model = whisper.load_model(MODEL_SIZE)
print("✅ Transcription model loaded.")

# --- Global variables for threaded recording (UNCHANGED) ---
_is_listening = False
_recording_thread = None
_audio_chunks = []

def _record_audio_thread():
    def audio_callback(indata, frames, time, status):
        if _is_listening: _audio_chunks.append(indata.copy())
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback, dtype='float32'):
        while _is_listening: sd.sleep(100)

def start_listening():
    global _is_listening, _audio_chunks, _recording_thread
    if _is_listening: return "I am already listening."

    print("\n" + "="*60)
    print("ACTION REQUIRED: Please ensure your audio devices are set for transcription:")
    print("  - Playback Device: CABLE Input")
    print("  - Recording Device: CABLE Output")
    print("="*60 + "\n")
    
    _is_listening = True
    _audio_chunks = []
    _recording_thread = threading.Thread(target=_record_audio_thread)
    _recording_thread.start()
    return "I am ready to listen. I will start recording when you play audio."

def stop_listening_and_transcribe():
    global _is_listening, _audio_chunks, _recording_thread
    if not _is_listening: return "I wasn't listening."

    _is_listening = False
    _recording_thread.join()

    if not _audio_chunks:
        return "I didn't hear anything to transcribe. Please check your audio setup."

    print("INFO: Concatenating recorded audio...")
    recorded_audio = np.concatenate(_audio_chunks, axis=0)
    
    temp_filename = ""
    try:
        audio_int16 = np.int16(recorded_audio * 32767)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            temp_filename = tmp.name
            write(temp_filename, SAMPLE_RATE, audio_int16)
        
        # --- STEP 1: Get the full transcript ---
        print("INFO: Sending audio to Whisper for transcription...")
        result = model.transcribe(temp_filename, without_timestamps=True)
        transcript = result['text'].strip()
        
        if not transcript:
            return "Transcription resulted in an empty text. Nothing to summarize."

        # --- NEW STEP 2: Summarize the transcript with Gemini ---
        print("INFO: Sending transcript to Gemini for summarization...")
        summarization_prompt = f"""
        You are an expert meeting summarizer. Your task is to analyze the following meeting transcript and provide a concise summary.
        Focus on identifying the key decisions made, the main action items assigned (and who they were assigned to, if mentioned), and any open questions or topics for future discussion.
        
        Present the summary in a clear, easy-to-read format.

        MEETING TRANSCRIPT:
        ---
        {transcript}
        ---

        EXECUTIVE SUMMARY:
        """
        
        summary = ask_gemini(summarization_prompt)
        # --- END OF NEW STEP ---

        # --- STEP 3: Save BOTH the summary and the full transcript ---
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fn = f"Meeting_Summary_{ts}.txt"
        
        with open(fn, "w", encoding="utf-8") as f:
            f.write("==============================\n")
            f.write("    AI-Generated Summary\n")
            f.write("==============================\n\n")
            f.write(summary)
            f.write("\n\n\n==============================\n")
            f.write("      Full Transcript\n")
            f.write("==============================\n\n")
            f.write(transcript)
            
        print(f"✅ Summary and transcript saved to {fn}")
        
        print("\n" + "="*60)
        print("ACTION REQUIRED: Please switch your audio devices back to normal.")
        print("="*60 + "\n")
        
        return f"Meeting summary and full transcript have been saved to the file: {fn}."
        
    except Exception as e:
        return f"An error occurred during transcription or summarization: {e}"
    finally:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)