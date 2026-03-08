from gtts import gTTS
import os
import tempfile

def text_to_speech(text, lang_code="en"):
    """
    Convert text to speech audio file.
    
    Args:
        text: Text to convert to speech
        lang_code: Language code (en, hi, kn)
    
    Returns:
        Path to generated audio file
    """
    try:
        # Create temp file for audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        audio_path = temp_file.name
        temp_file.close()
        
        # Generate speech
        # gTTS language codes: en, hi, kn
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(audio_path)
        
        return audio_path
    
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return None


def create_audio_summary(structured_info, simple_summary, lang_code="en"):
    """
    Create an audio file from the simple summary.
    This is what gets played when user clicks "Read Aloud"
    """
    # Use the simple summary for audio (easier to understand when listening)
    audio_path = text_to_speech(simple_summary, lang_code)
    return audio_path


def cleanup_audio(audio_path):
    """
    Delete temporary audio file after use.
    """
    try:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
    except Exception as e:
        print(f"Error cleaning up audio: {e}")