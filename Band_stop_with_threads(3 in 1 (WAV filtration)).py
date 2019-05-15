from math       import sin, pi 
import numpy as np

import librosa
import soundfile as sf

import threading
##--------------------------------------------
##-------------import submodules--------------
##--------------------------------------------
import global_values as g_v
import filterr       as fl
import generatorr    as gn

##--------data extraction------
g_v.voltage, g_v.f_d = librosa.load('..\\Separated_filter_with_threads\\wav\\Clean_file.wav', duration = g_v.T)
##--------adding noise--------
g_v.voltage = g_v.voltage + 0.250*(np.sin(2*np.pi*g_v.f_s_1*g_v.t) + 
               np.sin(2*np.pi*g_v.f_s_2*g_v.t) + 
               np.sin(2*np.pi*g_v.f_s_3*g_v.t) +
               np.sin(2*np.pi*g_v.f_s_4*g_v.t) + 
               np.sin(2*np.pi*g_v.f_s_5*g_v.t) + 
               np.sin(2*np.pi*g_v.f_s_6*g_v.t))
##-------save as WAV----------
sf.write('..\\Separated_filter_with_threads\\wav\\Signal_with_noise.wav', g_v.voltage, g_v.f_d, subtype = 'PCM_24')

##--------------------------------------------
##--------------create threads----------------
##--------------------------------------------

generator_thread = threading.Thread(target = gn.generator)
filter_thread    = threading.Thread(target = fl.filter_controller, daemon = True)
generator_thread.start() 
filter_thread.start()

##---set the first event--------
g_v.e1.set()

##--waiting for the end of threads---
generator_thread.join()

#--------save WAV file---------
output = np.array(g_v.filt_volt)
sf.write('..\\Separated_filter_with_threads\\wav\\Matlab_simulation.wav', output, g_v.f_d, subtype = 'PCM_24')