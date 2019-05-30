# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:56:08 2019

@author: YURU
"""
import aubio
import numpy as np
import pyaudio
import time
import queue
import music21

class voiceControl:
    def __init__(self):
        #輸入音訊
        print("讀取輸入音源: ")  
        self.p = pyaudio.PyAudio()  #輸入源
        self.stream = self.p.open(format=pyaudio.paFloat32,  #讀入
                        channels=1, rate=44100, input=True,
                        input_device_index=None, frames_per_buffer=4096)
        time.sleep(1)
        
        self.pDetection = aubio.pitch("default", 2048, 2048//2, 44100)  #aubio.pitch(method, buf_size, hop_size, samplerate)
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-40)
        
        self.q = queue.Queue()
        self.end = False

    def getCurrentNote(self,volume_thresh=0.01, printOut=False):
        current_pitch = music21.pitch.Pitch()
        while True:
            if self.end == True:
                print('close')
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
                break
            data = self.stream.read(1024, exception_on_overflow=False)
            samples = np.fromstring(data, dtype=aubio.float_type)
            pitch = self.pDetection(samples)[0]
            volume = np.sum(samples**2)/len(samples) * 100
            if pitch and volume > volume_thresh:
                current_pitch.frequency = pitch
            else:
                continue
            if printOut:
                print(current_pitch)        
            else:
                current = current_pitch.nameWithOctave
                self.q.put({'Note': current, 'Cents': current_pitch.microtone.cents,'Pitch':current_pitch})
            
if __name__ == '__main__':
    vc = voiceControl()
    vc.getCurrentNote(volume_thresh=0.001, printOut=True)
    
    

