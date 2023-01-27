import socket
import time

initial_energy = 10
production_rate = 2
consumption_rate = 3
trade_policy = 1
# qté d'energie à partir de laquelle on veut vendre
MIN_TO_SELL = 5


def energy_gestion(server_socket) :  

    time.sleep(1)
    global initial_energy 
    initial_energy = initial_energy - consumption_rate + production_rate
    print(initial_energy)
    if (initial_energy <= 0) : 
        print("PROBLEME : pu d'energie")
        #il faut acheter de l'energie : 
        #d'abord vérifier que personne veut bien en donner : 
        server_socket.sendall("BUY".encode())

  

# home se connecte au serveur de market qui lui donne sa réponse dans un thread personnalisé.
def home() : 
    #faire une trade_policy aléatoire entre 1 et 3 
    initial_energy = 10
    HOST = "localhost"
    PORT = 1313
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, PORT))
        trade_policy_bytes = trade_policy.to_bytes(2, 'big')
        server_socket.sendall(trade_policy_bytes)
        while(True) : 
            energy_gestion(server_socket)

home()
