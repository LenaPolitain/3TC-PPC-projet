import socket
import time
from queue import Queue
import sysv_ipc
from multiprocessing import Process

initial_energy = 10
production_rate = 2
consumption_rate = 3
trade_policy = 1
# qté d'energie à partir de laquelle on veut vendre
MIN_TO_SELL = 5
MIN_TO_BUY = 2
key = 128


def energy_gestion(server_socket, selling_queue) :  

    time.sleep(1)
    global initial_energy 
    initial_energy = initial_energy - consumption_rate + production_rate
    print(initial_energy)

    # si on veut vendre
    if initial_energy >= MIN_TO_SELL : 
        if trade_policy == 1 :
            #selling_queue.send(initial_energy)
            print("bonjour")
        elif trade_policy == 2 : 
            server_socket.sendall("I WANT TO SELL".encode) 
            time.sleep(0.5)
            server_socket.sendall(initial_energy.encode())
        initial_energy = 0

    # si on est en rade d'énergie 
    if (initial_energy <= MIN_TO_BUY) : 
        print("PROBLEME : bientôt pu d'energie")
        #il faut acheter de l'energie : 
        #d'abord vérifier que personne veut bien en donner : 
        try :  
            #message = selling_queue.receive()
            initial_energy = initial_energy + 3
            server_socket.sendall("STOP".encode())
        except:     
            server_socket.sendall("BUY".encode())
            time.sleep(0.5)
            server_socket.sendall(MIN_TO_SELL.encode())
            initial_energy = initial_energy + MIN_TO_SELL
            server_socket.sendall("STOP".encode())

  

# home se connecte au serveur de market qui lui donne sa réponse dans un thread personnalisé.
def home(selling_queue) : 
    #faire une trade_policy aléatoire entre 1 et 3 
    initial_energy = 10

    HOST = "localhost"
    PORT = 1313
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, PORT))
        trade_policy_bytes = trade_policy.to_bytes(2, 'big')
        server_socket.sendall(trade_policy_bytes)
        while(True) : 
            energy_gestion(server_socket, selling_queue)



#selling_queue est la queue dans laquelle on vent ou on achete son energie d'autres maisons
selling_queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
home(selling_queue)