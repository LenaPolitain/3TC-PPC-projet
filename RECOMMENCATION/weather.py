#**************** La fonction weather fait croitre ou décroitre la température aléatoirement de 1 toutes les secondes

import random
import time
import multiprocessing

def weather(current_temp, temps_max) :
    #print(f"Weather PID : {multiprocessing.current_process().pid}")
    start = time.time()
    execution = 0

    while execution < temps_max : 
        aleatoire = random.choice([True, False])
        if aleatoire == True : 
            current_temp.value = current_temp.value + 1
        else : 
            current_temp.value = current_temp.value - 1
        time.sleep(1)
        end = time.time()
        execution = end - start

    current_temp.value = 10000
    print(" ")
    print(" ")
    print("TIME REACHED END OF SIMULATION")
    print(" ")
    print(" ")
