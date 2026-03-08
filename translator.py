from deep_translator import GoogleTranslator
import time

def translate_text(text, target_lang="hi"):
    """
    Translate text to target language using deep-translator.
    
    Args:
        text: Text to translate
        target_lang: Target language code (hi, kn, en)
    
    Returns:
        Translated text
    """
    if not text or target_lang == "en":
        return text
    
    try:
        # deep-translator is more stable than googletrans
        translator = GoogleTranslator(source='auto', target=target_lang)
        result = translator.translate(text)
        return result
    
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original if translation fails


def translate_medical_info(structured_info, target_lang="hi"):
    """
    Translate the entire structured medical information.
    For long texts, we split into chunks to avoid limits.
    """
    if target_lang == "en":
        return structured_info
    
    try:
        # Split into smaller chunks (max 5000 chars per chunk)
        max_chunk_size = 4500
        chunks = []
        
        # Split by paragraphs first
        paragraphs = structured_info.split('\n\n')
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk)
        
        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            if chunk.strip():
                translated = translate_text(chunk, target_lang)
                translated_chunks.append(translated)
                time.sleep(0.5)  # Be gentle with API
        
        return '\n\n'.join(translated_chunks)
    
    except Exception as e:
        print(f"Error translating medical info: {e}")
        return structured_info


def detect_language(text):
    """
    Detect what language the text is in.
    """
    try:
        from deep_translator import single_detection
        lang = single_detection(text, api_key=None)
        return lang
    except:
        return "unknown"


# Medical term mapping for better accuracy
MEDICAL_TERMS = {
    "prescription": {"hi": "नुस्खा", "kn": "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್"},
    "tablet": {"hi": "गोली", "kn": "ಮಾತ್ರೆ"},
    "capsule": {"hi": "कैप्सूल", "kn": "ಕ್ಯಾಪ್ಸುಲ್"},
    "mg": {"hi": "मिलीग्राम", "kn": "ಮಿಲಿಗ್ರಾಂ"},
    "ml": {"hi": "मिलीलीटर", "kn": "ಮಿಲಿಲೀಟರ್"},
    "morning": {"hi": "सुबह", "kn": "ಬೆಳಿಗ್ಗೆ"},
    "evening": {"hi": "शाम", "kn": "ಸಂಜೆ"},
    "night": {"hi": "रात", "kn": "ರಾತ್ರಿ"},
    "daily": {"hi": "रोजाना", "kn": "ಪ್ರತಿದಿನ"},
    "twice": {"hi": "दो बार", "kn": "ಎರಡು ಬಾರಿ"},
    "before food": {"hi": "खाने से पहले", "kn": "ಊಟದ ಮೊದಲು"},
    "after food": {"hi": "खाने के बाद", "kn": "ಊಟದ ನಂತರ"},
}

def enhance_medical_translation(text, target_lang):
    """
    Improve translation by replacing common medical terms with
    accurate translations from our glossary.
    """
    translated = translate_text(text, target_lang)
    
    # Replace common medical terms with our curated translations
    for eng_term, translations in MEDICAL_TERMS.items():
        if target_lang in translations:
            # Case-insensitive replacement
            translated = translated.replace(eng_term, translations[target_lang])
            translated = translated.replace(eng_term.capitalize(), translations[target_lang])
    
    return translated