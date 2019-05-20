# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:56:08 2019

@author: YURU
"""
import aubio
import numpy as np
import pyaudio
import time
import argparse
import queue
import music21

#輸入音訊
parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
args = parser.parse_args()

if args.input is None:
    print("讀取輸入音源: ")
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("裝置 %i: %s" % (i, p.get_device_info_by_index(i).get('name')))
    print("--由裝置 1 輸入")
    
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1, rate=44100, input=True,
                input_device_index=args.input, frames_per_buffer=4096)
time.sleep(1)

pDetection = aubio.pitch("default", 2048, 2048//2, 44100)
pDetection.set_unit("Hz")
pDetection.set_silence(-40)

q = queue.Queue()

def getCurrentNote(volume_thresh=0.01, printOut=False):
    current_pitch = music21.pitch.Pitch()
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        samples = np.fromstring(data, dtype=aubio.float_type)
        pitch = pDetection(samples)[0]
        volume = np.sum(samples**2)/len(samples) * 100
        if pitch and volume > volume_thresh:
            current_pitch.frequency = pitch
        else:
            continue
        if printOut:
            print(current_pitch)        
        else:
            current = current_pitch.nameWithOctave
            q.put({'Note': current, 'Cents': current_pitch.microtone.cents})
            
if __name__ == '__main__':
    getCurrentNote(volume_thresh=0.001, printOut=True)