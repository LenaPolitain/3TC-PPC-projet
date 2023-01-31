#**************** La fonction weather fait croitre ou décroitre la température aléatoirement de 1 toutes les secondes

import random
import time
import multiprocessing

def weather(current_temp) :
    #print(f"Weather PID : {multiprocessing.current_process().pid}")
    while True : 
        aleatoire = random.choice([True, False])
        if aleatoire == True : 
            current_temp.value = current_temp.value + 1
        else : 
            current_temp.value = current_temp.value - 1
        time.sleep(1)