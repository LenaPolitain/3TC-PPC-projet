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
from home2 import *
import sysv_ipc
key = 128

# variables globales pour la shared memory : weather
# dictionnaire de couples de trucs méteo
meteo_size = 12



if __name__ == "__main__" : 

    print("hello")
    current_temperature = Value('i', 20) 
    #home = Process(target = home, args=())
    selling_queue = Queue()
    home1 = Process(target = home, args=(selling_queue, 5, 1, 1,))
    home2 = Process(target = home, args=(selling_queue, 2, 3, 2,))
    home3 = Process(target = home, args=(selling_queue, 2, 3, 3,))
    home1.start()
    home2.start()
    home3.start()