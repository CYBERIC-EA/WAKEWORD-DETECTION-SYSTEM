import sounddevice as sd
from scipy.io.wavfile import write


def record_audio_and_save(save_path, n_times=100):
    input("To start audio recording press Enter:")
    for i in range(199, 206):
        fs = 44100
        seconds = 2
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write(save_path + str(i) + ".wav", fs, myrecording)

        #input(f"Press to record next or to stop press ctrl + C {i + 1} / {n_times} ")
        input(f"Press to record next or to stop press ctrl + C {i + 1} / 160 ")


def record_background_and_save(save_path, n_times=100):

    input("To start recording background sounds press Enter:")
    for i in range(199, 206):
        fs = 44100
        seconds = 2
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write(save_path + str(i) + ".wav", fs, myrecording)
        print(f" currently recoded : {i + 1 / n_times } times")


#print('You can record the wake word below: \n ')
#record_audio_and_save("wakeword implementation\\audio_data/")

print("Recording the background sounds below: \n")
record_background_and_save("wakeword implementation\\background_sound/")
