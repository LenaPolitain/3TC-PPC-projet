import multiprocessing
from external import *
import signal


def handler (sig, frame) : 
    if sig == signal.SIGCHLD : 
        print("HURRICANE HAPPENING")
    elif sig == signal.SIGUSR1 : 
        print("PUTIN WAR HAPPPENING")
    elif sig == signal.SIGUSR2 : 
        print("FUEL SHORTAGE HAPPENENING")

def market() :
    print("Market function")
    signal.signal(signal.SIGCHLD, handler)
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    pid = multiprocessing.current_process().pid
    print(f"my pid is {pid}")
    e = multiprocessing.Process(target=(external), args=(pid,))
    e.start()