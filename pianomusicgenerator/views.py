from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import sounddevice as sd
import time
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 1200  # Duration of recording

start_time = 0
stop_time = 0
counter = 0
my_recording = 0
is_recording = False

def index(request):
    template = loader.get_template('home.html')
    context = {
        
    }
    return HttpResponse(template.render(context, request))


def composition(request):
    template = loader.get_template('composition.html')
    name = request.GET['name']
    context = {
        "name": name
    }
    return HttpResponse(template.render(context, request))


def recording(request):
    global counter
    global is_recording
    global my_recording

    template = loader.get_template('recording.html')
    name = request.GET['name']
    context = {
        "name": name
    }

    counterIncrement()

    if counter % 2 == 1:
        is_recording = True
        setStartTime()
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    if counter % 2 == 0:
        is_recording = False
        setStopTime()
        write_to_file = True

    while is_recording == True:
        continue

    recording_time = stop_time - start_time
    my_recording = my_recording[0 : int(recording_time * fs)]
    name = 'my_recording_' + str(int(start_time)) + '.wav'
    write(name, fs, my_recording)  # Save as WAV file
    counter = 0
    my_recording = 0

    return HttpResponse(template.render(context, request)) 


def setStartTime():
    global start_time
    start_time = time.time()

def setStopTime():
    global stop_time
    stop_time = time.time()

def counterIncrement():
    global counter
    counter = counter + 1