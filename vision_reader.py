import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use gemini-flash-lite-latest - 1500 requests per day!
# Much higher than gemini-2.5-flash (only 20/day)
model = genai.GenerativeModel('gemini-flash-lite-latest')


def read_medical_document(image_file):
    """Read medical document using Gemini Vision"""
    
    # Convert to PIL Image
    image = Image.open(image_file)
    
    prompt = """Analyze this medical document carefully and extract:

1. **Document Type**: (Prescription, Lab Report, etc.)
2. **Patient Information**: (Name, Age, Date if visible)
3. **Doctor/Hospital**: (Name and location)
4. **Medicines Prescribed**: List each with:
   - Medicine name
   - Dosage (e.g., 500mg)
   - Frequency (e.g., twice daily)
   - Duration (e.g., 5 days)
   - Instructions (before/after food)
5. **Diagnosis/Condition**: What is being treated
6. **Warnings/Precautions**: Any warnings mentioned
7. **Follow-up**: When to see doctor again
8. **Additional Notes**: Other important info

Format clearly with headings. If info not visible, say "Not clearly visible"."""

    try:
        response = model.generate_content([prompt, image])
        extracted_text = response.text
        
        # Get raw OCR text
        ocr_response = model.generate_content(["Extract ALL text from this image exactly as it appears.", image])
        raw_text = ocr_response.text
        
        return {
            "success": True,
            "structured_info": extracted_text,
            "raw_text": raw_text,
            "error": None
        }
    
    except Exception as e:
        return {
            "success": False,
            "structured_info": None,
            "raw_text": None,
            "error": str(e)
        }


def extract_key_medicines(structured_info):
    """Extract medicines from structured info"""
    try:
        if "Medicines" in structured_info:
            lines = structured_info.split('\n')
            medicine_section = []
            capturing = False
            
            for line in lines:
                if "Medicines" in line and "**" in line:
                    capturing = True
                    continue
                elif capturing and line.startswith('**') and "Medicines" not in line:
                    break
                elif capturing and line.strip():
                    medicine_section.append(line.strip())
            
            return "\n".join(medicine_section) if medicine_section else "No medicines listed"
        return "No medicines section found"
    except Exception as e:
        return f"Error: {str(e)}"


def get_simple_summary(structured_info):
    """Generate simple summary for text-to-speech"""
    
    prompt = f"""Based on this medical analysis:

{structured_info}

Create a simple 5-sentence summary that can be read aloud. Use plain language, no jargon. Focus on:
- What medicines to take
- When to take them  
- Important warnings
- When to see doctor

Keep it very simple and short."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"