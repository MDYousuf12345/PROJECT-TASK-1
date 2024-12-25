import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import threading
import webbrowser

def takecommand():
    """Capture audio command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm locked in, Sir.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            print("waiting for your command sir..")
            query = r.recognize_google(audio, language='en-us')
            print(f"You Said: {query}\n")
            return query
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except Exception as e:
            print(f"I'm Sorry, Sir, I missed that. Error: {e}")
        return "None"

query=takecommand().lower()

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)  # Range: 0.0 to 1.0

# Lock for thread-safe speech
speak_lock = threading.Lock()

def speak(audio):
    """Speak function runs with a lock to avoid overlapping."""
    with speak_lock:
        engine.say(audio)
        engine.runAndWait()


def searchGoogle(query):
    if "google" in query.lower():
        query = query.lower().replace("google", "").strip()
        speak("This is the information I gathered based on your command, Sir.")
        
        try:
            # Perform a Google search (opens in the browser)
            pywhatkit.search(query)
            
            # Fetch a summary from Wikipedia
            result = wikipedia.summary(query, sentences=2)
            print(result)  # Print the result to the console
            speak(result)  # Speak the result
        except wikipedia.exceptions.DisambiguationError as e:
            speak("The query is too broad. Please be more specific.")
            print("Disambiguation error:", e)
        except wikipedia.exceptions.PageError:
            speak("I couldn't find any relevant information on Wikipedia.")
            print("Page error: No result found.")
        except Exception as e:
            speak("An error occurred while searching.")
            print("Error:", e)


def searchYoutube(query):
    if "youtube" in query:
        speak("This the information gathered based on your command, Sir ")
        query=query.replace("jarvis","")
        query=query.replace("youtube search","")
        query=query.replace("youtube","")
        web="https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Here you go , Sir")

def searchWikipedia(query):
    if "wikipedia" in query:
         speak("This the information gathered based on your command from wikipedia, Sir ")
         query=query.replace("wikipedia","")
         query=query.replace("search wikipedia","")
         query=query.replace("jarvis","")
         results=wikipedia.summary(query,sentences=2)
         speak("based on research from wikipedia this is what i found, sir")
         print(results)
         speak(results)            
