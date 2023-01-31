from multiprocessing import Process, Value, Queue
from market import *
from weather import * 
from home import *

NUM_HOUSES = 3
TIME_MAX = 20

def handler (sig, frame) : 

    if sig == signal.SIGINT : 
        active = multiprocessing.active_children()
        for child in active:
            print(f"killing : {child}")
            child.kill()
        os.kill(multiprocessing.current_process().pid, signal.SIGKILL)


if __name__ == "__main__" : 

    #print(f"Main PID : {multiprocessing.current_process().pid}")
    current_temperature = Value('i', 20) 
    selling_queue = Queue()
    signal.signal(signal.SIGINT, handler)

    market = Process(target= market, args=(current_temperature,))
    market.start()
    print("Simulation is starting ...")
    for i in range(10) : 
        print(".")
        time.sleep(0.1)

    weather = Process(target = weather, args = (current_temperature, TIME_MAX,))
    weather.start()

    houses = [Process(target = home, args = (i, selling_queue, current_temperature,)) for i in range(NUM_HOUSES)]
    for i in houses : 
        i.start()
        time.sleep(1)

    market.join()
    weather.join()
    for i in houses : 
        i.join()