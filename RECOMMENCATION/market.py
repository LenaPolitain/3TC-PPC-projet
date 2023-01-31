import multiprocessing
import threading
from external import *
import signal
import socket
import struct

energy_price = 0
MAX_CONN = 10
end_of_communication = False
socket_pid = 8080
external_pid = 8080
market_pid = 8080

def handler (sig, frame) : 

    global end_of_communication


    if sig == signal.SIGCHLD : 
        print("HURRICANE HAPPENING")
    elif sig == signal.SIGUSR1 : 
        print("PUTIN WAR HAPPPENING")
    elif sig == signal.SIGUSR2 : 
        print("FUEL SHORTAGE HAPPENENING")
    elif sig == signal.SIGINT : 
        print("*****************************************KILLING ALL THE PROCESSES*********************************************")
        os.kill(multiprocessing.current_process().pid, signal.SIGKILL)
        os.kill(multiprocessing.parent_process().pid, signal.SIGKILL)
        os.kill(socket_pid, signal.SIGKILL)
        os.kill(external_pid, signal.SIGKILL)

def socket_creation() : 

    global socket_pid 
    socket_pid = multiprocessing.current_process().pid

    #print(f"Socket PID : {multiprocessing.current_process().pid}")

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
        print(f"Client's policy is number : {client_policy}")
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

    global external_pid 

    #print("Market function")
    #print(f"Market PID : {multiprocessing.current_process().pid}")
    signal.signal(signal.SIGCHLD, handler)
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler)
    pid = multiprocessing.current_process().pid
    #print(f"my pid is {pid}")
    ext = multiprocessing.Process(target=(external), args=(pid,))
    ext.start()
    #external_pid = external.pid

    tcp_socket = multiprocessing.Process(target=(socket_creation), args=())
    tcp_socket.start()

    #maintenant on s'occupe juste de calculer l'energie : 
    while True : 
        time.sleep(1)
        print(f"The price of the energy is : <{energy_price} €> right now")
        energy_price += 1