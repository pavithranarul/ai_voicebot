import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import subprocess
import sys
import wave
import datetime

def install_missing_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def save_audio(audio_data):
    filename = f"audio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_data.get_wav_data())
    print(f"Audio saved as {filename}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)  # Increased to 15 seconds
        save_audio(audio)  # Save the recorded audio
    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Check your internet connection.")
        return ""

conversation_history = []

def chat_with_gpt(prompt):
    global conversation_history
    genai.configure(api_key="api_key")
    model = genai.GenerativeModel("gemini-pro")
    conversation_history.append({"role": "user", "content": prompt})
    response = model.generate_content("\n".join([entry["content"] for entry in conversation_history]), stream=False)
    response_text = response.text if hasattr(response, "text") else "I'm not sure, could you clarify?"
    conversation_history.append({"role": "assistant", "content": response_text})
    return response_text

def main():
    speak("Hey! What's up?")
    while True:
        user_input = listen()
        if user_input.lower() in ["exit", "quit", "stop"]:
            speak("Alright, talk to you later!")
            break
        if user_input:
            response = chat_with_gpt(user_input)
            print("Bot:", response)
            speak(response)

if __name__ == "__main__":
    main()
