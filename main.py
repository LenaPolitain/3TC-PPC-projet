from multiprocessing import Process, Array
import threading
import os 
import time 
import socket 
import sys
from queue import Queue

# variables globales pour la shared memory : weather
# dictionnaire de couples de trucs méteo
meteo_size = 12
shared_meteo = Array('L', meteo_size) 




def home() : 
    print("home")

def market() :
    print("market")

def weather(meteo) : 
    print("weather")



if __name__ == "__main___" : 
    home = Process(target = home, args=())
    market = Process(target= market, args=())
    weather = Process(target = weather, args = (shared_meteo,))
    home.start() 
    market.start()
    weather.start()
    home.join() 
    market.join()
    weather.join()