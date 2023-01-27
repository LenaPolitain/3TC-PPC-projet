import time 
import random 
from multiprocessing import Value

mod_temp = 0.001

def weather(current_temp) : 
    time.sleep(1)
    current_temp.value = random.randint(10, 35)