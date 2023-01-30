from multiprocessing import Process, Value, Queue
from market import *
from weather import * 
from home import *

NUM_HOUSES = 3


if __name__ == "__main__" : 

    current_temperature = Value('i', 20) 
    selling_queue = Queue()
    market = Process(target= market, args=())
    weather = Process(target = weather, args = (current_temperature,))

    houses = [Process(target = home, args = (i, selling_queue,)) for i in range(NUM_HOUSES)]

    market.start()
    weather.start()

    for i in houses : 
        i.start()