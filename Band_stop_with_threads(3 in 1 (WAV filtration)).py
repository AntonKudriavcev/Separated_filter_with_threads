from math       import sin, pi 

import numpy as np

import librosa

import soundfile as sf

import threading
##--------------------------------------------------------
##------------------signal settings-----------------------
##--------------------------------------------------------
f_s_1 = 25
f_s_2 = 50
f_s_3 = 100
f_s_4 = 200
f_s_5 = 400
f_s_6 = 800

A   = 1
##--------------------------------------------------------
##------------------sample settings-----------------------
##--------------------------------------------------------
f_d = 22050
T   = 10.0
dt  = 1/f_d
t   = np.linspace(0.1, T, int(T*f_d), endpoint = False) # time variable
##----------------------------------------------------------
##-------------coefficient for first stage------------------
##----------------------------------------------------------
##section #1
a_coef_1_1 = [0.525828543039357776,
             -1.99315287833078858,
              0.997244104076249416]
b_coef_1_1 = [1,
             -1.99631885323521785,
              1] 
##section #2
a_coef_1_2 = [0.98514378788174306,
             -1.9665278007775604,
              0.971680540810641924]
b_coef_1_2 = [1,
             -1.99759749798163111,
              1] 
##section #3
a_coef_1_3 = [1.7899432111289777,
             -0.885200010264396653,
              0]
b_coef_1_3 = [1,
             -1,
              0] 
##----------------------------------------------------------
##-------------coefficient for second stage-----------------
##----------------------------------------------------------
##section #1
a_coef_2_1 = [0.780545597983568928,
             -1.98454172327042144,
              0.998468983060898374]
b_coef_2_1 = [1,
             -1.98640637335991888,
              1] 
##section #2
a_coef_2_2 = [0.780545597983568928,
             -1.98653531191395594,
              0.998576070222813805]
b_coef_2_2 = [1,
             -1.98764535316191138,
              1] 
##section #3
a_coef_2_3 = [1.62751709363638364,
             -1.97321776696518358,
              0.986087001680641895]
b_coef_2_3 = [1,
             -1.98704061332200621,
              1] 
##----------------------------------------------------------
##-------------coefficient for third stage------------------
##----------------------------------------------------------
##section #1
a_coef_3_1 = [0.780545597983568817,
             -1.94490255673515455,
              0.998496105813971191]
b_coef_3_1 = [1,
             -1.94703027431694564,
              1] 
##section #2
a_coef_3_2 = [0.780545597983568817,
             -1.94870398482269636,
              0.998548945297613622]
b_coef_3_2 = [1,
             -1.94949292626011861,
              1] 
##section #3
a_coef_3_3 = [1.6275170936363812,
             -1.93472288180304686,
              0.986087001680639008]
b_coef_3_3 = [1,
             -1.94827606259531683,
              1] 

##----------delay line for first stage-----------
##section #1
z_1_1 = 3*[0]
z_1_2 = 3*[0]
z_1_3 = 3*[0]
##----------delay line for second stage-----------
##section #2
z_2_1 = 3*[0]
z_2_2 = 3*[0]
z_2_3 = 3*[0]
##----------delay line for thrid stage-----------
##section #3
z_3_1 = 3*[0]
z_3_2 = 3*[0]
z_3_3 = 3*[0]
##------------general list----------
Z = [[z_1_1,z_1_2,z_1_3], [z_2_1,z_2_2,z_2_3], [z_3_1,z_3_2,z_3_3]]
##-----------list for filt_volt--------------
filt_volt = []
y = 0
##--------thread for signal generaton--------
def generator(event_for_wait, event_for_set):
  global X
  for i in range (len(voltage)):
    event_for_wait.wait()
    # print('generator thread is started')
    event_for_wait.clear()
    X = voltage[i]
    # print(i , X)
    event_for_set.set()
    # print('generator thread is finished')

##------------thread for filter-------------
def filter_controller(event_for_wait, event_for_set):
  global X
  global y
  while 1:
    event_for_wait.wait()
    event_for_wait.clear()
    # print('filter thread is started')
  ##--------------------------------------------
  ##----filtration for every single section-----
  ##--------------------------------------------
    X = filter(1, 1, a_coef_1_1, b_coef_1_1, 2, X)
    X = filter(1, 2, a_coef_1_2, b_coef_1_2, 2, X)
    X = filter(1, 3, a_coef_1_3, b_coef_1_3, 1, X)

    X = filter(2, 1, a_coef_2_1, b_coef_2_1, 2, X)
    X = filter(2, 2, a_coef_2_2, b_coef_2_2, 2, X)
    X = filter(2, 3, a_coef_2_3, b_coef_2_3, 2, X)

    X = filter(3, 1, a_coef_3_1, b_coef_3_1, 2, X)
    X = filter(3, 2, a_coef_3_2, b_coef_3_2, 2, X)
    X = filter(3, 3, a_coef_3_3, b_coef_3_3, 2, X)
    filt_volt.append(y)
    y = 0
    event_for_set.set()
    # print('filter thread is finished')
##--------------------------------------------------------
##--------------------filtering part----------------------
##-------------------------------------------------------
def filter(stage_n, sec_n, a_coef, b_coef, n_coef, input_data):
  global Z
  global y
  for m in range(n_coef, 0, -1):
      Z[stage_n - 1][sec_n - 1][m] = Z[stage_n - 1][sec_n - 1][m - 1]

  Z[stage_n - 1][sec_n - 1][0] = input_data*a_coef[0]

  for j in range (1, n_coef + 1, 1): 
      Z[stage_n - 1][sec_n - 1][0] += -Z[stage_n - 1][sec_n - 1][j]*a_coef[j]

  for k in range (0, n_coef + 1, 1):
      y += Z[stage_n - 1][sec_n - 1][k]*b_coef[k]
  return X


##--------data extraction------
voltage, f_d = librosa.load('..\\Separated filter with threads\\wav\\Clean_file.wav', duration = T)
##--------adding noise--------
voltage = voltage + 0.250*(np.sin(2*np.pi*f_s_1*t) + 
               np.sin(2*np.pi*f_s_2*t) + 
               np.sin(2*np.pi*f_s_3*t) +
               np.sin(2*np.pi*f_s_4*t) + 
               np.sin(2*np.pi*f_s_5*t) + 
               np.sin(2*np.pi*f_s_6*t))
##-------save as WAV----------
sf.write('..\\Separated filter with threads\\wav\\Signal_with_noise.wav', voltage, f_d, subtype = 'PCM_24')

##-----set events for threads--------
e1 = threading.Event()
e2 = threading.Event()

##-----create threads-------
generator_thread = threading.Thread(target = generator, args = (e1, e2))
filter_thread    = threading.Thread(target = filter_controller, daemon = True, args = (e2, e1))
generator_thread.start() 
filter_thread.start()

##---set the first event--------
e1.set()

##--waiting for the end of threads---
generator_thread.join()

#--------save WAV file---------
output = np.array(filt_volt)
sf.write('..\\Separated filter with threads\\wav\\Matlab_simulation.wav', output, f_d, subtype = 'PCM_24')
