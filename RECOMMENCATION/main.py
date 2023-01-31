from multiprocessing import Process, Value, Queue
from market import *
from weather import * 
from home import *

NUM_HOUSES = 3


if __name__ == "__main__" : 

    #print(f"Main PID : {multiprocessing.current_process().pid}")
    current_temperature = Value('i', 20) 
    selling_queue = Queue()

    market = Process(target= market, args=())
    market.start()
    print("Simulation is starting ...")
    for i in range(10) : 
        print(".")
        time.sleep(0.1)

    weather = Process(target = weather, args = (current_temperature,))
    weather.start()

    houses = [Process(target = home, args = (i, selling_queue,)) for i in range(NUM_HOUSES)]
    for i in houses : 
        i.start()
        time.sleep(1)