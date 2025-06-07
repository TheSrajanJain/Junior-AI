# Junior AI Assistant - Full Version with OpenCV Face Recognition

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ctypes
import pyautogui
import cv2
import json
import time
import requests
import threading
import smtplib
import psutil
import pytesseract
import pdfplumber
import fitz  # PyMuPDF
import pywhatkit
import wolframalpha
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Calendar
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Text-to-Speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# API Keys
openai.api_key = 'YourOpenAI_API_Key'
WOLFRAMALPHA_APP_ID = 'Your_WolframAlpha_App_ID'

# Spotify API Setup
SPOTIPY_CLIENT_ID = 'Your_Spotify_Client_ID'
SPOTIPY_CLIENT_SECRET = 'Your_Spotify_Client_Secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state"
))

MEMORY_FILE = 'junior_memory.json'

# Helpers
def speak(text):
    print(f"Junior: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        return r.recognize_google(audio, language='en-in').lower()
    except:
        speak("Sorry, please repeat that.")
        return "None"

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        answer = response.choices[0].message['content']
        save_to_memory(prompt, answer)
        return answer
    except:
        return "Error contacting OpenAI."

def save_to_memory(question, answer):
    try:
        memory = {}
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                memory = json.load(f)
        memory[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = {"Q": question, "A": answer}
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f, indent=4)
    except Exception as e:
        print(f"Memory Save Error: {e}")

def wish_me():
    hour = datetime.datetime.now().hour
    greet = "Good Morning" if 0 <= hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    speak(f"{greet}! I am Junior. How can I assist you today?")

def get_weather():
    try:
        city = 'Your_City_Name'
        url = f"https://wttr.in/{city}?format=3"
        weather = requests.get(url).text
        speak(weather)
    except:
        speak("Unable to fetch weather.")

def check_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Battery is at {percent} percent.")

def play_spotify(song):
    try:
        results = sp.search(q=song, limit=1)
        song_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[song_uri])
        speak(f"Playing {song} on Spotify.")
    except:
        speak("Unable to play song.")

def read_pdf(path):
    try:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        speak(text[:500])
    except:
        speak("Unable to read PDF.")

def read_image_text(path):
    try:
        text = pytesseract.image_to_string(path)
        speak(text[:500])
    except:
        speak("Failed to read image text.")

def system_control(command):
    if 'shutdown' in command:
        os.system("shutdown /s /t 1")
    elif 'restart' in command:
        os.system("shutdown /r /t 1")
    elif 'lock' in command:
        ctypes.windll.user32.LockWorkStation()
    elif 'screenshot' in command:
        pyautogui.screenshot().save('screenshot.png')
        speak("Screenshot saved.")

def send_email():
    try:
        sender = 'YourEmail@example.com'
        password = 'YourEmailPassword'
        to = input("Recipient Email: ")
        subject = input("Subject: ")
        content = input("Content: ")
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        speak("Email sent successfully.")
    except:
        speak("Failed to send email.")

def ask_wolfram(query):
    try:
        client = wolframalpha.Client(WOLFRAMALPHA_APP_ID)
        res = client.query(query)
        answer = next(res.results).text
        speak(answer)
    except:
        speak("I couldn't fetch an answer from WolframAlpha.")

def face_login():
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read('trained_model.yml')
    with open('label_map.json', 'r') as f:
        label_map = json.load(f)

    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            label, confidence = model.predict(roi)
            if confidence < 70:
                name = label_map[str(label)]
                speak(f"Welcome back, {name}!")
                cap.release()
                cv2.destroyAllWindows()
                return
            else:
                speak("Face not recognized.")
        if cv2.waitKey(1) == 13:
            break

def handle_query(query):
    if 'play' in query:
        song = query.replace('play', '').strip()
        play_spotify(song)
    elif 'weather' in query:
        get_weather()
    elif 'battery' in query:
        check_battery()
    elif 'screenshot' in query or 'shutdown' in query or 'restart' in query or 'lock' in query:
        system_control(query)
    elif 'email' in query:
        send_email()
    elif 'read pdf' in query:
        path = input("Enter PDF file path: ")
        read_pdf(path)
    elif 'read image' in query:
        path = input("Enter image path: ")
        read_image_text(path)
    elif 'who is' in query or 'what is' in query:
        ask_wolfram(query)
    elif 'search' in query:
        query = query.replace('search', '').strip()
        pywhatkit.search(query)
    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")
    elif 'open google' in query:
        webbrowser.open("https://google.com")
    elif 'open chat gpt' in query:
        webbrowser.open("https://chat.openai.com")
    elif 'sing your favorite song' in query:
        speak("Sure, Let me play my favorite song!")
        webbrowser.open("https://www.youtube.com/watch?v=sySlY1XKlhM")
    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        exit()
    else:
        response = chat_with_gpt(query)
        speak(response)

if __name__ == "__main__":
    face_login()
    wish_me()
    while True:
        query = take_command()
        if query != "None":
            handle_query(query)
