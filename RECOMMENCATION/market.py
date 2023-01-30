import multiprocessing
import threading
from external import *
import signal
import socket
import struct

energy_price = 0
MAX_CONN = 10
end_of_communication = False

def handler (sig, frame) : 

    global end_of_communication

    if sig == signal.SIGCHLD : 
        print("HURRICANE HAPPENING")
    elif sig == signal.SIGUSR1 : 
        print("PUTIN WAR HAPPPENING")
    elif sig == signal.SIGUSR2 : 
        print("FUEL SHORTAGE HAPPENENING")
    elif sig == signal.SIGKILL : 
        end_of_communication = True

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
            t = threading.Thread(target = home_interaction, args =(client_socket, address,))
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
        while end_of_communication == False :
            data = client_socket.recv(1024)
            client_request = data.decode()
            if(client_request == "BUY") : 
                print("FROM MARKET : someone just bought me energy")
            elif(client_request == "SELL") : 
                print("FROM MARKET : someone just sold me energy")
        print("Disconnecting from client: ", address) 

def market() :
    print("Market function")
    signal.signal(signal.SIGCHLD, handler)
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler)
    pid = multiprocessing.current_process().pid
    print(f"my pid is {pid}")
    ext = multiprocessing.Process(target=(external), args=(pid,))
    ext.start()
    tcp_socket = multiprocessing.Process(target=(socket_creation), args=())
    tcp_socket.start()

    #maintenant on s'occupe juste de calculer l'energie : 
    while True : 
        time.sleep(1)
        print(f"The price of the energy is : <{energy_price} €> right now")
        energy_price += 1