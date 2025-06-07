# 🤖 Junior AI Assistant

Junior is a powerful desktop-based AI assistant built in Python, designed to help with everyday tasks using voice commands. It integrates OpenAI, Spotify, WolframAlpha, Google Calendar, Face Recognition, and much more — all from your own system.

---

## ✨ Features

- 🎙️ Voice Commands via Speech Recognition  
- 🗣️ Text-to-Speech with pyttsx3  
- 🌤️ Weather Updates  
- 🔋 Battery Monitoring  
- 🎵 Spotify Music Playback  
- 🧠 GPT-based Chat Integration (via OpenAI API)  
- 🔒 Face Recognition Login (OpenCV)  
- 📧 Email Sending  
- 📂 PDF & Image Text Reader (OCR)  
- 🔍 Web Search via PyWhatKit  
- 📅 Google Calendar Integration  
- 🧮 WolframAlpha Query Handling  
- 🖥️ System Controls (Shutdown, Restart, Screenshot, Lock)  
- 📜 Memory Log for Questions and Answers  

---

## 📁 Project Structure

```bash
junior-ai-assistant/
├── main.py                     # Main script with all functionalities
├── haarcascade_frontalface_default.xml
├── trained_model.yml           # Face recognition model (needs to be trained separately)
├── label_map.json              # Face label mappings
├── junior_memory.json          # Assistant memory file
├── requirements.txt            # List of dependencies
└── README.md
```

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/YourUsername/junior-ai-assistant.git
cd junior-ai-assistant
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Set Up API Keys**

Update the following placeholders in `main.py`:

```python
openai.api_key = 'your-openai-api-key'
WOLFRAMALPHA_APP_ID = 'your-wolframalpha-app-id'

SPOTIPY_CLIENT_ID = 'your-spotify-client-id'
SPOTIPY_CLIENT_SECRET = 'your-spotify-client-secret'
SPOTIPY_REDIRECT_URI = 'your-spotify-redirect-uri'
```

4. **Tesseract OCR Setup**

Install Tesseract for image text reading:  
- On Windows: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)  
- On Linux:  
```bash
sudo apt install tesseract-ocr
```

---

## 📸 Face Recognition Setup

1. Train your face recognizer using OpenCV LBPH.
2. Save the trained model as `trained_model.yml`.
3. Create `label_map.json` like:

```json
{ "0": "YourName" }
```

---

## 🗣️ How to Use

Run the assistant:

```bash
python main.py
```

The assistant will:
- Recognize your face for login.
- Greet you based on time.
- Start listening for voice commands.

---

## 🧠 Example Voice Commands

- “Play Shape of You”  
- “What’s the weather?”  
- “Check battery”  
- “Read PDF”  
- “Search Python tutorial”  
- “Shutdown the system”  
- “Send email”  
- “Open YouTube”  
- “Who is Elon Musk?”

---

## 🔐 Disclaimer

This project uses multiple APIs and services. Do **NOT expose your real API keys or passwords** in any public repository.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Made with ❤️ by [Srajan Jain](https://github.com/TheSrajanJain)
