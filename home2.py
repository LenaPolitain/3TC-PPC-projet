import socket
import time
from queue import Queue
import sysv_ipc
from multiprocessing import Process
import sys

initial_energy = 5
production_rate = 2
consumption_rate = 3
trade_policy = 1
# qté d'energie à partir de laquelle on veut vendre
MIN_TO_SELL = 5
MIN_TO_BUY = 2
key = 128


def energy_gestion( selling_queue, prod_rate, cons_rate, house_number) :  

    time.sleep(1)
    production_rate = prod_rate
    consumption_rate = cons_rate
    global initial_energy 
    initial_energy = initial_energy - consumption_rate + production_rate
    print("house no : " + str(house_number) + "  -->  " + str(initial_energy))

    # si on veut vendre
    if initial_energy >= MIN_TO_SELL : 
        if trade_policy == 1 :
            print("house no : " + str(house_number) + " I AM SELLING TO ANOTHER HOUSE")
            selling_queue.put(initial_energy)
            print("house no : " + str(house_number) + "  -->  " + str(initial_energy))
        elif trade_policy == 2 : 
            print("house no : " + str(house_number) + " I WANT TO SELL ON THE MARKET") 
            time.sleep(0.5)
            print("house no : " + str(house_number) + "  -->  " + str(initial_energy))
        initial_energy = 2

    # si on est en rade d'énergie 
    if (initial_energy < MIN_TO_BUY) : 
        print("house no : " + str(house_number) + " PROBLEME : bientôt pu d'energie")
        #il faut acheter de l'energie : 
        #d'abord vérifier que personne veut bien en donner : 
        if selling_queue.empty == False : 
            print("house no : " + str(house_number) + " I WANT TO BUY FROM ANOTHER HOUSE")
            message = selling_queue.get()
            initial_energy = initial_energy + message 
            print("house no : " + str(house_number) + "  -->  " + str(initial_energy))
        else :     
            print("house no : " + str(house_number) + " I WANT TO BUY ON THE MARKET")
            time.sleep(0.5)
            initial_energy = initial_energy + MIN_TO_SELL
            print("house no : " + str(house_number) + "  -->  " + str(initial_energy))

  

# home se connecte au serveur de market qui lui donne sa réponse dans un thread personnalisé.
def home(selling_queue, prod_rate, cons_rate, house_number ) : 
    #faire une trade_policy aléatoire entre 1 et 3 
    initial_energy = 10
    while(True) : 
        energy_gestion(selling_queue, prod_rate, cons_rate, house_number)