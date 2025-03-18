import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import sys
import requests
import json

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# To-do list storage
todo_list = []

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user based on the current time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Krishna, paarth. I'm here to help. What can I do for you?")

# Function to take voice commands from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Say that again please, paarth...")
        return "None"
    return query.lower()

# Function to send email
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Use environment variables or a config file for credentials
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry paarth. I am not able to send this email")

# Function to get weather information
def getWeather(city):
    try:
        api_key = "xyz"  # Replace with your actual OpenWeatherMap API key
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()

        if response.status_code == 200 and "main" in data:
            main = data["main"]
            weather = data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]
            weather_report = f"The temperature in {city} is {temperature} degrees Celsius with {description}. The humidity is {humidity} percent."
            return weather_report
        elif response.status_code == 404:
            return "City not found. Please check the city name and try again."
        else:
            return "Unable to get weather information at the moment. Please try again later."
    except Exception as e:
        print(e)
        return "There was an error retrieving the weather information."    

# Functions for to-do list management
def addTodoItem(item):
    todo_list.append(item)
    speak(f"Added {item} to your to-do list.")

def showTodoList():
    if not todo_list:
        speak("Your to-do list is empty.")
    else:
        speak("Your to-do list items are:")
        for idx, item in enumerate(todo_list, start=1):
            speak(f"{idx}. {item}")

def removeTodoItem(index):
    try:
        removed_item = todo_list.pop(index - 1)
        speak(f"Removed {removed_item} from your to-do list.")
    except IndexError:
        speak("Invalid item number. Please try again.")


# Function to search Wikipedia
def searchWikipedia(query):
    try:
        if query.strip() == "":
            speak("Please provide a valid query to search on Wikipedia.")
            return
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results.encode(sys.stdout.encoding, errors='ignore').decode(sys.stdout.encoding))
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Your query may refer to multiple pages: {e.options}")
    except wikipedia.exceptions.PageError:
        speak("No page matches your query.")
    except wikipedia.exceptions.WikipediaException as e:
        speak(f"An error occurred while searching Wikipedia: {e}")


# Main function to handle different commands
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
#wikipedia
        if 'wikipedia' in query or 'open wikipedia' in query:
            query = query.replace("wikipedia", "").strip()
            if not query:
                speak("What do you want to know from Wikipedia?")
                query = takeCommand()
            searchWikipedia(query)
#youtube
        elif 'open youtube' in query or 'youtube' in query:
            webbrowser.open("https://www.youtube.com/")
#google
        elif 'open google' in query or 'google' in query:
            speak("What do you want to search on Google?")
            search_query = takeCommand()
            if search_query != 'none':
                search_url = f"https://www.google.com/search?q={search_query}"
                speak(f"Here are the Google search results for {search_query}.")
                webbrowser.open(search_url)
#whatsapp
        elif 'open whatsapp' in query or 'whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com/")
#music
        elif 'play music' in query or 'music' in query or 'open spotify' in query:
            speak("Sure, would you like to search for a specific song or artist?")
            search_query = takeCommand()
            if search_query != 'none':
                search_url = f"https://open.spotify.com/search/{search_query}"
                speak(f"Here's the Spotify search results for {search_query}. Please play the song from the Spotify interface.")
                webbrowser.open(search_url)
#time
        elif 'the time' in query or 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sure, the time is {strTime}")
#date
        elif 'the date' in query:
            currentDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Sure, today's date is {currentDate}")
#email
        elif 'email to you' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "othersEmail@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry paarth. I am not able to send this email")
#weather
        elif 'weather' in query:
            speak("Please tell me the city name.")
            city = takeCommand()
            if city != 'none':
                weather_report = getWeather(city)
                speak(weather_report)
                print(weather_report)
#add to do
        elif 'add to do' in query or 'add task' in query:
            speak("What task do you want to add?")
            task = takeCommand()
            if task != 'none':
                addTodoItem(task)
#show to do
        elif 'show to do list' in query or 'show tasks' in query:
            showTodoList()
#remove to do
        elif 'remove to do' in query or 'remove task' in query:
            speak("Please tell me the task number to remove.")
            try:
                task_number = int(takeCommand())
                removeTodoItem(task_number)
            except ValueError:
                speak("I didn't understand the task number. Please try again.")
#thanks
        elif 'thank you' in query or 'thank' in query or 'goodbye' in query or 'thanks' in query:
            speak("You're welcome. Goodbye, paarth")
            sys.exit()
