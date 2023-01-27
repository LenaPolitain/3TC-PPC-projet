from multiprocessing import Process, Value
import threading
import os 
import time 
import socket 
import sys
from queue import Queue
#from home import *
from market import *
from weather import *

# variables globales pour la shared memory : weather
# dictionnaire de couples de trucs méteo
meteo_size = 12



if __name__ == "__main__" : 

    print("hello")
    current_temperature = Value('i', 0) 
    #home = Process(target = home, args=())
    market = Process(target= market, args=(current_temperature,))
    weather = Process(target = weather, args = (current_temperature,))
    #home.start()
    market.start()
    weather.start()
    #print(current_temperature.value)
    #time.sleep(3)
    #print(current_temperature.value)
    #home.join()
    weather.join()