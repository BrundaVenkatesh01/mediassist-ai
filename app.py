import streamlit as st
import os
from datetime import datetime
from vision_reader import read_medical_document, get_simple_summary
from translator import translate_medical_info
from speech_handler import text_to_speech, cleanup_audio
from languages import LANGUAGES, get_text
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🏥",
    layout="centered",  # Centered for mobile
    initial_sidebar_state="collapsed"
)

# ── Session State ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "welcome"  # Start at welcome
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = None
if "results" not in st.session_state:
    st.session_state.results = None
if "medications" not in st.session_state:
    st.session_state.medications = []
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# ── MOBILE-FIRST CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { 
    font-family: 'Poppins', sans-serif; 
    font-size: 20px;
}

.stApp { 
    background: linear-gradient(180deg, #fff5eb 0%, #ffe8d6 100%);
    color: #2d2d2d;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding: 1rem; 
    max-width: 600px; /* Mobile width */
}

/* Welcome Screen */
.welcome-screen {
    text-align: center;
    padding: 3rem 1rem;
}

.welcome-logo {
    font-size: 8rem;
    margin-bottom: 1rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.welcome-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b35, #ff8c42);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 1rem 0;
}

.welcome-subtitle {
    font-size: 1.3rem;
    color: #666;
    margin: 1rem 0 2rem 0;
    line-height: 1.6;
}

/* Language Selection */
.lang-card {
    background: white;
    border: 4px solid #ff8c42;
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.2);
}

.lang-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

.lang-flag {
    font-size: 4rem;
    margin-bottom: 0.5rem;
}

.lang-name {
    font-size: 2rem;
    font-weight: 700;
    color: #ff6b35;
}

.lang-subtitle {
    font-size: 1.2rem;
    color: #666;
    margin-top: 0.5rem;
}

/* Menu Cards */
.menu-card {
    background: linear-gradient(135deg, #4CAF50, #66BB6A);
    color: white;
    border-radius: 25px;
    padding: 2.5rem;
    margin: 1.5rem 0;
    text-align: center;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    transition: all 0.3s;
}

.menu-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(76, 175, 80, 0.5);
}

.menu-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.menu-title {
    font-size: 2rem;
    font-weight: 800;
    margin: 1rem 0;
}

.menu-desc {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Buttons - HUGE for mobile */
div.stButton > button {
    background: linear-gradient(135deg, #ff6b35, #ff8c42) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    padding: 1.5rem 3rem !important;
    width: 100% !important;
    box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4) !important;
    transition: all 0.3s !important;
    margin: 1rem 0 !important;
}

div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.5) !important;
}

/* Back Button */
.back-button {
    position: fixed;
    top: 1rem;
    left: 1rem;
    background: white;
    border: 3px solid #ff8c42;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    z-index: 1000;
}

/* Upload Area */
.upload-zone {
    background: white;
    border: 5px dashed #ff8c42;
    border-radius: 25px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 2rem 0;
}

.upload-icon {
    font-size: 5rem;
    color: #ff8c42;
    margin-bottom: 1rem;
}

.upload-text {
    font-size: 1.5rem;
    font-weight: 600;
    color: #666;
}

/* Results */
.result-box {
    background: white;
    border: 4px solid #4CAF50;
    border-radius: 25px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
}

.result-header {
    font-size: 2rem;
    font-weight: 800;
    color: #4CAF50;
    margin-bottom: 1.5rem;
    border-bottom: 3px solid #4CAF50;
    padding-bottom: 1rem;
}

.result-text {
    font-size: 1.3rem;
    line-height: 2;
    color: #2d2d2d;
    white-space: pre-wrap;
}

/* Page Header */
.page-header {
    text-align: center;
    padding: 2rem 1rem 1rem 1rem;
    margin-bottom: 2rem;
}

.page-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ff6b35;
    margin-bottom: 0.5rem;
}

.page-subtitle {
    font-size: 1.3rem;
    color: #666;
}

/* Audio Player */
audio {
    width: 100%;
    height: 70px;
    margin: 1rem 0;
}

/* Medicine Reminder */
.reminder-card {
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
    border: 4px solid #ff9800;
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
}

.reminder-time {
    font-size: 2.5rem;
    font-weight: 800;
    color: #e65100;
    margin-bottom: 0.5rem;
}

.reminder-medicine {
    font-size: 1.5rem;
    font-weight: 600;
    color: #424242;
}

.reminder-status {
    font-size: 1.3rem;
    font-weight: 700;
    margin-top: 1rem;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: white;
    border: 5px dashed #ff8c42;
    border-radius: 20px;
    padding: 2rem;
}

/* Progress Indicator */
.progress-dots {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
}

.dot {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #ddd;
}

.dot-active {
    background: #ff6b35;
    width: 20px;
    height: 20px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: WELCOME SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "welcome":
    st.markdown("""
    <div class="welcome-screen">
        <div class="welcome-logo">🏥</div>
        <div class="welcome-title">MediAssist AI</div>
        <div class="welcome-subtitle">
            Your Personal<br>
            Healthcare Companion<br><br>
            Read prescriptions<br>
            Track medicines<br>
            Stay healthy
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 GET STARTED"):
        st.session_state.page = "language"
        st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #999; font-size: 1rem;">
        Free • Easy • Safe<br>
        For everyone 👴👵👨👩
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: LANGUAGE SELECTION
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "language":
    
    # Back button
    if st.button("← Back", key="back_from_lang"):
        st.session_state.page = "welcome"
        st.rerun()
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Choose Language</div>
        <div class="page-subtitle">भाषा चुनें • ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Language cards
    if st.button("🇬🇧"):
        st.session_state.selected_lang = "en"
        st.session_state.page = "menu"
        st.rerun()
    st.markdown('<div style="text-align:center; font-size:2rem; font-weight:700; color:#ff6b35; margin:-0.5rem 0 2rem 0;">ENGLISH</div>', unsafe_allow_html=True)
    
    if st.button("🇮🇳"):
        st.session_state.selected_lang = "hi"
        st.session_state.page = "menu"
        st.rerun()
    st.markdown('<div style="text-align:center; font-size:2rem; font-weight:700; color:#ff6b35; margin:-0.5rem 0 2rem 0;">हिंदी (HINDI)</div>', unsafe_allow_html=True)
    
    if st.button("🇮🇳 "):
        st.session_state.selected_lang = "kn"
        st.session_state.page = "menu"
        st.rerun()
    st.markdown('<div style="text-align:center; font-size:2rem; font-weight:700; color:#ff6b35; margin:-0.5rem 0 2rem 0;">ಕನ್ನಡ (KANNADA)</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: MAIN MENU
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "menu":
    lang = st.session_state.selected_lang
    
    # Back button
    if st.button("← Change Language", key="back_from_menu"):
        st.session_state.page = "language"
        st.rerun()
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🏥 MediAssist AI</div>
        <div class="page-subtitle">What would you like to do?</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu options
    if st.button("📸 SCAN PRESCRIPTION"):
        st.session_state.page = "scan"
        st.rerun()
    st.markdown('<div style="text-align:center; color:#666; margin:-0.5rem 0 2rem 0; font-size:1.1rem;">Upload and read your prescription</div>', unsafe_allow_html=True)
    
    if st.button("💊 MY MEDICINES"):
        st.session_state.page = "medicines"
        st.rerun()
    st.markdown('<div style="text-align:center; color:#666; margin:-0.5rem 0 2rem 0; font-size:1.1rem;">View your medication list</div>', unsafe_allow_html=True)
    
    if st.button("🔔 REMINDERS"):
        st.session_state.page = "reminders"
        st.rerun()
    st.markdown('<div style="text-align:center; color:#666; margin:-0.5rem 0 2rem 0; font-size:1.1rem;">See today\'s medicine schedule</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: SCAN PRESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "scan":
    lang = st.session_state.selected_lang
    
    # Back button
    if st.button("← Back to Menu", key="back_from_scan"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📸 Scan Document</div>
        <div class="page-subtitle">Upload prescription or medicine photo</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "📷 Take Photo or Choose File",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        label_visibility="visible"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} image(s) uploaded!")
        
        # Show thumbnails
        cols = st.columns(min(len(uploaded_files), 2))
        for idx, file in enumerate(uploaded_files):
            with cols[idx % 2]:
                st.image(file, use_container_width=True)
        
        if st.button("🔍 ANALYZE NOW", type="primary"):
            all_results = []
            
            progress_bar = st.progress(0)
            for idx, file in enumerate(uploaded_files):
                st.info(f"📖 Reading image {idx+1}/{len(uploaded_files)}...")
                result = read_medical_document(file)
                if result["success"]:
                    all_results.append(result)
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            if all_results:
                combined = "\n\n".join([r['structured_info'] for r in all_results])
                summary = get_simple_summary(combined)
                
                if lang != "en":
                    st.info("🌐 Translating...")
                    summary = translate_medical_info(summary, lang)
                
                audio = text_to_speech(summary, lang)
                
                st.session_state.results = {
                    "summary": summary,
                    "audio": audio
                }
                st.session_state.page = "results"
                st.rerun()
    else:
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">📸</div>
            <div class="upload-text">
                Tap above to upload<br>
                prescription or medicine photo
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "results":
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">✅ Analysis Complete</div>
        <div class="page-subtitle">Here's what we found</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.results:
        st.markdown(f"""
        <div class="result-box">
            <div class="result-header">💡 Summary</div>
            <div class="result-text">{st.session_state.results['summary']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.results.get('audio'):
            st.markdown('<div style="text-align:center; font-size:1.5rem; font-weight:700; color:#ff6b35; margin:2rem 0 1rem 0;">🔊 Listen</div>', unsafe_allow_html=True)
            st.audio(st.session_state.results['audio'])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 SCAN ANOTHER"):
                st.session_state.results = None
                st.session_state.page = "scan"
                st.rerun()
        with col2:
            if st.button("🏠 MENU"):
                st.session_state.results = None
                st.session_state.page = "menu"
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6: MY MEDICINES
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "medicines":
    
    if st.button("← Back to Menu", key="back_from_meds"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">💊 My Medicines</div>
        <div class="page-subtitle">Your medication list</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.medications:
        st.info("📋 No medicines yet. Scan a prescription to add!")
    else:
        for med in st.session_state.medications:
            st.markdown(f"""
            <div class="result-box">
                <div class="result-header">💊 {med['name']}</div>
                <div class="result-text">
                    <b>Dosage:</b> {med.get('dosage', 'Not specified')}<br>
                    <b>When:</b> {med.get('time', 'Not specified')}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7: REMINDERS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "reminders":
    
    if st.button("← Back to Menu", key="back_from_reminders"):
        st.session_state.page = "menu"
        st.rerun()
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🔔 Today's Reminders</div>
        <div class="page-subtitle">Medicine schedule</div>
    </div>
    """, unsafe_allow_html=True)
    
    current_hour = datetime.now().hour
    
    reminders = [
        {"time": "8:00 AM", "medicine": "Blood Pressure", "hour": 8},
        {"time": "2:00 PM", "medicine": "Diabetes Med", "hour": 14},
        {"time": "8:00 PM", "medicine": "Vitamin D", "hour": 20},
    ]
    
    for reminder in reminders:
        taken = current_hour > reminder['hour']
        status_color = "#4CAF50" if taken else "#ff9800"
        status_text = "✅ TAKEN" if taken else "⏰ PENDING"
        
        st.markdown(f"""
        <div class="reminder-card" style="border-color: {status_color};">
            <div class="reminder-time">{reminder['time']}</div>
            <div class="reminder-medicine">💊 {reminder['medicine']}</div>
            <div class="reminder-status" style="color: {status_color};">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)