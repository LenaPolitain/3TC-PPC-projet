import socket
import time
from queue import Queue
import sysv_ipc
from multiprocessing import Process
import sys

initial_energy = 0
production_rate = 2
consumption_rate = 3
trade_policy = 1
# qté d'energie à partir de laquelle on veut vendre
MIN_TO_SELL = 5
MIN_TO_BUY = 2
key = 128


def energy_gestion(selling_queue, prod_rate, cons_rate) :  

    time.sleep(1)
    production_rate = prod_rate
    consumption_rate = cons_rate
    global initial_energy 
    initial_energy = initial_energy - consumption_rate + production_rate
    print(initial_energy)

    # si on veut vendre
    if initial_energy >= MIN_TO_SELL : 
        if trade_policy == 1 :
            print("I AM SELLING TO ANOTHER HOUSE")
            selling_queue.send(initial_energy)
            print(initial_energy)
        elif trade_policy == 2 : 
            print("I WANT TO SELL ON THE MARKET") 
            time.sleep(0.5)
            print(initial_energy)
        initial_energy = 0

    # si on est en rade d'énergie 
    if (initial_energy <= MIN_TO_BUY) : 
        print("PROBLEME : bientôt pu d'energie")
        #il faut acheter de l'energie : 
        #d'abord vérifier que personne veut bien en donner : 
        try :  
            print("I WANT TO BUY FROM ANOTHER HOUSE")
            message = selling_queue.receive()
            initial_energy = initial_energy + message 
            print(initial_energy)
        except:     
            print("I WANT TO BUY ON THE MARKET".encode())
            time.sleep(0.5)
            initial_energy = initial_energy + MIN_TO_SELL
            print(initial_energy)
    selling_queue.remove()

  

# home se connecte au serveur de market qui lui donne sa réponse dans un thread personnalisé.
def home(selling_queue, prod_rate, cons_rate ) : 
    #faire une trade_policy aléatoire entre 1 et 3 
    initial_energy = 10
    while(True) : 
        energy_gestion(selling_queue, prod_rate, cons_rate)



#selling_queue est la queue dans laquelle on vent ou on achete son energie d'autres maisons
selling_queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
home(selling_queue, int(sys.argv[1]), int(sys.argv[2]))