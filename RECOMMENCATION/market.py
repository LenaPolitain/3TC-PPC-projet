import multiprocessing
import threading
from external import *
import signal
import socket
import struct
from string import printable

energy_price = 0.0
global NUM_HOUSES
external_event = False

def newPrice(current_temp) :
    atenuation_coeff = 0.99
    modulating_coeff_int = 0.001
    modulating_coeff_ext = 0.01
    global energy_price

    if (external_event) :
        energy_price = atenuation_coeff*energy_price + modulating_coeff_int*current_temp + modulating_coeff_ext
    else :
        energy_price = atenuation_coeff*energy_price + modulating_coeff_int*current_temp

def handler (sig, frame) :

    global end_of_communication
    global socket_pid
    global external_pid
    global external_event

    if sig == signal.SIGCHLD :
        print(" ")
        print("HURRICANE HAPPENING")
        print(" ")
        external_event = True
    elif sig == signal.SIGUSR1 :
        print(" ")
        print("PUTIN WAR HAPPPENING")
        print(" ")
        external_event = True
    elif sig == signal.SIGUSR2 :
        print(" ")
        print("FUEL SHORTAGE HAPPENENING")
        print(" ")
        external_event = True

    # here : to make sure that every process is killed
    elif sig == signal.SIGINT :
        print(" ")
        print(" ")
        print("KILLING ALL THE PROCESSES :")
        print(" ")
        print(" ")
        active = multiprocessing.active_children()
        for child in active:
            print(f"killing : {child}")
            child.kill()
        os.kill(multiprocessing.parent_process().pid, signal.SIGINT)
        os.kill(multiprocessing.current_process().pid, signal.SIGKILL)

def socket_creation(current_temp, everybody_connected) :

    #print(f"Socket PID : {multiprocessing.current_process().pid}")

    #print("Creating the socket")
    HOST = "localhost"
    PORT = 1313

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        number_of_connections = 0
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

        sockets = [threading.Thread for i in range(NUM_HOUSES)]

        while number_of_connections < NUM_HOUSES :
            #print("waiting for a connection")
            client_socket, address = server_socket.accept()
            client_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            sockets[number_of_connections] = threading.Thread(target = home_interaction, args =(client_socket, address, current_temp,))
            sockets[number_of_connections].start()
            number_of_connections +=1

        everybody_connected.value = True

        for h in sockets :
            h.join()

def home_interaction(client_socket, address, current_temp) :
    #with client_socket:
    trade_policy = client_socket.recv(1024)
    client_policy = int.from_bytes(trade_policy, "big")
    print(f"*************** Connected to client : {address}. Client's policy is number : {client_policy} **********************")
    while current_temp.value != 10000 :
        data = client_socket.recv(1024)
        client_request = data.decode()
        client_request = str(client_request)
        # on enlève les espaces indésirables
        client_request = client_request.strip()
        # on enlève les char spéciaux
        client_request = ''.join(char for char in client_request if char in printable)

        if client_request == "BUY" :
            print("FROM MARKET : someone just bought me energy")
        elif client_request == "SELL" :
            print("FROM MARKET : someone just sold me energy")
    print("Disconnecting from client: ", address)
    client_socket.close()

def market(current_temp, number_of_houses, everybody_connected) :

    global NUM_HOUSES
    NUM_HOUSES = number_of_houses

    #print("Market function")
    #print(f"Market PID : {multiprocessing.current_process().pid}")
    signal.signal(signal.SIGCHLD, handler)
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    signal.signal(signal.SIGINT, handler)

    pid = multiprocessing.current_process().pid

    ext = multiprocessing.Process(target=(external), args=(pid, current_temp, everybody_connected,))
    ext.start()

    tcp_socket = threading.Thread(target=(socket_creation), args=(current_temp, everybody_connected,))
    tcp_socket.start()

    ext.join()
    tcp_socket.join()

    #maintenant on s'occupe juste de calculer l'energie :
    while True :
        time.sleep(1)
        print(f"The price of the energy is : <{energy_price} €> right now")
        newPrice(current_temp)
