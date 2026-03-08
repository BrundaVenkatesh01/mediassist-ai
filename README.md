# 🏥 MediAssist AI

**Your Personal Healthcare Companion**

An AI-powered multilingual healthcare assistant that helps people understand medical documents, track medications, and stay healthy. Built with accessibility in mind for elderly users and people with disabilities.

🌐 **Live Demo:** [Coming Soon]

---

## ✨ Features

### 📸 Smart Document Reading
- Upload prescription or medicine photos
- AI reads and explains in simple language
- Multi-image support for verification
- Cross-checks prescription vs actual medicine

### 🌍 Multilingual Support
- **English** - Full support
- **हिंदी (Hindi)** - Complete translation
- **ಕನ್ನಡ (Kannada)** - Native support
- Text-to-speech in all languages

### 💊 Medication Management
- Track all your medicines
- Dosage and timing information
- Visual medication cards
- Easy-to-read format

### 🔔 Smart Reminders
- Daily medication schedule
- Morning, Afternoon, Evening timing
- ✅ Taken / ⏰ Pending status
- Large, clear display

### ♿ Accessibility First
- Large buttons & text (2-3x normal size)
- High contrast warm colors
- Voice output (text-to-speech)
- Simple mode for elderly users
- Mobile-optimized flow

### 🎨 Elder-Friendly Design
- Warm orange/cream color scheme
- Easy on aging eyes
- One task per page
- HUGE touch targets
- Clear visual hierarchy

---

## 🚀 Tech Stack

- **Frontend:** Streamlit
- **AI/ML:** Google Gemini 2.5 Flash (Vision AI)
- **Translation:** Deep Translator
- **Text-to-Speech:** gTTS
- **Language:** Python 3.10+

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key (free at aistudio.google.com)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mediassist-ai.git
   cd mediassist-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - App will open at `http://localhost:8501`

---

## 🎯 How It Works

### 1. Welcome Screen
Beautiful landing page with "Get Started" button

### 2. Choose Language
Select from English, Hindi, or Kannada

### 3. Main Menu
Three clear options:
- 📸 Scan Prescription
- 💊 My Medicines
- 🔔 Reminders

### 4. Upload & Scan
- Take photo or upload image
- AI analyzes with Gemini Vision
- Extracts medicines, dosage, timing
- Translates to selected language

### 5. Results
- Simple explanation in plain language
- Text-to-speech audio
- Full details available
- Easy navigation

---

## 🌟 Use Cases

### For Elderly Users
- Read prescriptions they can't see clearly
- Hear medicine instructions read aloud
- Large buttons easy to tap
- Simple, one-step-at-a-time flow

### For Caregivers
- Verify correct medicines
- Track medication schedules
- Cross-check prescription vs pills
- Multi-language support for diverse families

### For Visually Impaired
- Complete text-to-speech support
- High contrast design
- Screen reader compatible
- Audio-first experience available

### For Non-English Speakers
- Full Hindi and Kannada translation
- Medical term glossary
- Native language audio
- Cultural accessibility

---

## 🛠️ Project Structure

```
mediassist-ai/
├── app.py                 # Main Streamlit application
├── vision_reader.py       # Gemini Vision integration
├── translator.py          # Multi-language translation
├── speech_handler.py      # Text-to-speech functionality
├── languages.py           # Language configs & glossary
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

---

## 🔒 Privacy & Security

- ✅ No data is stored permanently
- ✅ Images processed in real-time only
- ✅ API calls are secure (HTTPS)
- ✅ No personal health data collected
- ✅ Complies with medical data privacy standards

---

## 🚧 Roadmap

### Planned Features
- [ ] Voice commands (speak to upload)
- [ ] Drug interaction database
- [ ] Medication calendar export
- [ ] Emergency contact integration
- [ ] More languages (Tamil, Malayalam, Telugu)
- [ ] OCR for scanned documents
- [ ] Offline mode
- [ ] Mobile app (Flutter)

---

## 🤝 Contributing

Contributions are welcome! This project aims to help people access healthcare more easily.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Google Gemini** - Vision AI capabilities
- **Streamlit** - Beautiful web framework
- **Open source community** - Amazing tools and libraries

---

## 💡 Why This Project?

Healthcare accessibility is a fundamental right. Yet millions struggle to:
- Read medical documents in unfamiliar languages
- Understand complex prescriptions
- Track medications effectively
- Verify they have the correct medicine

**MediAssist AI** bridges this gap using AI technology, making healthcare more accessible, especially for:
- 🧓 Elderly populations
- ♿ People with disabilities  
- 🌍 Non-English speakers
- 👨‍👩‍👧 Families caring for loved ones

---

## 📞 Contact

**Brunda Venkatesh**
- GitHub: [@BrundaVenkatesh01](https://github.com/BrundaVenkatesh01)
- Email: brundave01@gmail.com

---

## ⭐ Show Your Support

If this project helps you or someone you know, please give it a star! It helps others discover this tool.

---

**Built with ❤️ for accessible healthcare**
