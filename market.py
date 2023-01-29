import socket
import struct
from threading import Thread
import time

energy_price = 0
MAX_CONN = 10
Y = 0.1512
energy_price_t_1 = 0


def energy_price_calcul() : 
    energy_price = energy_price_t_1 * Y
    return energy_price

def socket_creation() : 
    print("Creating the socket")
    HOST = "localhost"
    PORT = 1313

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        number_of_connections = 0
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        while number_of_connections <= MAX_CONN :
            #print("waiting for a connection")
            client_socket, address = server_socket.accept()
            client_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            t = Thread(target = home_interaction, args =(client_socket, address,))
            t.start()
            number_of_connections +=1


def home_interaction(client_socket, address) :
    with client_socket: 
        print("Connected to client: ", address)
        trade_policy = client_socket.recv(1024)
        client_policy = int.from_bytes(trade_policy, "big")
        print("Client's policy is number : " + str(client_policy))
        data = client_socket.recv(1024)
        client_request = data.decode()
        while client_request != "STOP" :
            print(f"le message est {client_request}")
            if(client_request == "BUY") : 
                print("ok la moula")
            data = client_socket.recv(1024)
            client_request = data.decode()
        
        print("Disconnecting from client: ", address) 


def market(current_temp) : 
    print(current_temp.value)
    print(energy_price_calcul())
    socket_creation()