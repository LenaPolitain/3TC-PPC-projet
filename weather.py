import time 
import random 
from multiprocessing import Value


# la temperature croit ou décroit de facon random toutes les secondes

mod_temp = 0.001

def weather(current_temp) : 
    while True : 
        aleatoire = random.choice([True, False])
        if aleatoire == True : 
            current_temp.value = current_temp.value + 1
        else : 
            current_temp.value = current_temp.value - 1
        time.sleep(1)