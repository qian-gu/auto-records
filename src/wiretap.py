#!/usr/bin/env python
from sys import byteorder
from array import array
from struct import pack
from pathlib import Path

import pyaudio
import wave
from datetime import datetime

THRESHOLD = 500
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30

RECORD_PATH = './records/'


def list_device():
    print('-------------- record device list --------------')
    audio = pyaudio.PyAudio()
    info = audio.get_host_api_info_by_index(0)
    device_num = info.get('deviceCount')
    for i in range(0, device_num):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')):
            print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    print('------------------------------------------------')


def wiretap():
    # prepare
    Path(RECORD_PATH).mkdir(exist_ok=True)
    list_device()
    # working
    try:
        while(1):
            # continous recoding
            sample_width, snd_data = record()
            # skip logfile to save storage
            print(max(abs(i) for i in snd_data))
            if is_silent(snd_data):
                continue
            else:
                filename = RECORD_PATH + datetime.now().isoformat('-') + '.wav'
                data = dsp(snd_data)
                save_to_file(filename, sample_width, data)
    except Exception as e:
        print(str(e))
        print('Breaking...')


def record():
    """
    Record a 30s tape and return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the start and end, and pads with
    0.5 seconds of blank sound to make sure VLC et al can play it without
    getting choppped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    # record
    r = array('h')
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        snd_data = array('h', stream.read(CHUNK))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)
    print(type(r))
    sample_width = p.get_sample_size(FORMAT)
    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, r


def dsp(snd_data):
    # Digital Signal Processing
    r = normalize(snd_data)
    r = trim(r)
    return r


def save_to_file(filename, sample_width, data):
    data = pack('<' + ('h'*len(data)), *data)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def is_silent(snd_data):
    "Return 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def trim(snd_data):
    return snd_data


if __name__ == '__main__':
    print("Start working...")
    wiretap()
    print("Done")
