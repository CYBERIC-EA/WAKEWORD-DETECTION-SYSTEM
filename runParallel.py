###### IMPORTS ###################
import threading
import time
import sounddevice as sd
import librosa
import numpy as np
import pyttsx3
from keras.models import load_model

#### SETTING UP TEXT TO SPEECH ###
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty(
    'voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.endLoop()


##### CONSTANTS ################
fs = 24000
seconds = 3

model = load_model("wakeword implementation\saved_model/WWD.h5")

##### LISTENING THREAD #########


def listener():
    while True:
        print('listening...')
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        mfcc = librosa.feature.mfcc(y=myrecording.ravel(), sr=fs, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        prediction_thread(mfcc_processed)
        time.sleep(1)


def voice_thread():
    listen_thread = threading.Thread(target=listener, name="ListeningFunction")
    listen_thread.start()

##### PREDICTION THREAD #############


def prediction(y):
    prediction = model.predict(np.expand_dims(y, axis=0))
    if prediction[:, 1] > 0.96:
        if engine._inLoop:
            engine.endLoop()

        print("succesfully predicted that alpha has been called")
        speak("Hello, What can I do for you?")

    time.sleep(0.1)


def prediction_thread(y):
    pred_thread = threading.Thread(
        target=prediction, name="PredictFunction", args=(y,))
    pred_thread.start()


voice_thread()
