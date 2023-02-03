import os
from datetime import datetime
import pyttsx3
import speech_recognition as sr
import openai
from neuralintents import GenericAssistant
import json
import nltk
import sys
import prediction
# initialize text, make it global
global text
text = None
quit_out = False


def listen_to_user():
    # initialize the recognizer
    r = sr.Recognizer()

    # listen for input
    with sr.Microphone() as source:
        print("listening...")
        audio = r.listen(source, phrase_time_limit=5)

    # recognize the speech
    try:
        global text
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print(
            "Error requesting results from Google Speech Recognition service; {0}".format(e))


def speak(text):

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_time():
    global current_time
    current_time = datetime.now().strftime("%H:%M:%S")


get_time()


def get_date():
    from datetime import date
    global current_date
    current_date = date.today().strftime("%Y-%m-%d")


get_date()


def get_weather():
    import requests
    global current_weather
    api_key = "b22bc55d67020f9b057f44cf6b3f15b8"
    city = "Abuja"

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    weather_data = requests.get(weather_url).json()
    current_temp = weather_data['main']['temp']
    current_weather = weather_data['weather'][0]['description']


get_weather()


def intro(user):

    global person

    person = user
    user_dialouge = "Hello, " + user
    speak(user_dialouge)


def get_started():
    global user
    text = 'Before we get started, what can i refer to you as?'
    speak(text)
    listen_to_user()


def database():

    qa_database = {
        "what is the time": f"The current time is {current_time}.",
        "what is the date": f"The current date is {current_date}.",
        "what is the weather": f"The current weather is {current_weather}.",
        "what is your name": f"My name is Cyber assistant",
        "what is your purpose": f"My purpose is to assist you with your needs.",
        "bye": quit,
        "stop": quit,
        "i want to quit": quit,
        "good bye ": quit,
        "i want to exit": quit,
        "i have to go": quit,
        "i have no more questions for you": quit,
        "that will be all": quit
        # "i have no more questions for you": f'I am glad to have been of help to you {person}',
    }
    return qa_database


def quit():
    global quit_out
    speak('I am glad to have been of help to you')
    quit_out = True


def return_answer(question):
    # Replace {current_time}, {current_date}, and {current_weather} with the actual values
    question = question.lower()
    print(question)
    qa_database = database()

    if question in qa_database:

        try:
            qa_database[question]()

        except:
            text = qa_database[question]

        speak(text)
    # elif assistant.request(question):
    #    text = assistant.request(question)
    #    print('neuralintents')
    #    print(text)
    elif questions(question):
        print('open ai answered successfully')

    else:
        text = "I'm sorry, I don't understand your question."
        speak(text)


# questions


def questions(question):
    openai.api_key = "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"
    # enter the open ai func and ask it a question directly instead of retrieving the question again

    #prompt = 'Ask me anything you want: '
    # speak(prompt)
    # listen_to_user()
    print(question)
    completions = openai.Completion.create(
        prompt=text, engine='text-davinci-002', max_tokens=100)

    completion = completions.choices[0].text
    print(completion)
    speak(completion)
    return True


mappings = {
    "exit": quit,
}

#assistant = GenericAssistant(intents='intents.json', intent_methods=mappings)
# assistant.train_model()
# assistant.save_model()
#model = load_model(chatbot_model.model)

while not prediction.predict():
    print('predict again')
else:
        
    get_started()
    while text is None:
        speak("Sorry, I did not get that")
        get_started()
    else:
        intro(text)


    while quit_out != True:
        print(quit_out)
        listen_to_user()
        try:
            print(return_answer(text))
        except:
            print("The value of text has no value")
    else:
        print('eri wants to stop here')
        raise SystemExit
