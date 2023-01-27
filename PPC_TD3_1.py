import multiprocessing
from multiprocessing import Pipe
from multiprocessing import Process

def reverse(conn, x) :
    reversed_x = x[::-1]
    conn.send(reversed_x)
    conn.close()

if __name__ == "__main__" :
    parent_conn, child_conn = Pipe()
    print("Say something : ")
    x = input() 
    while x != "stop" :
        p = Process(target = reverse, args =(child_conn, x,))
        p.start()
        print(parent_conn.recv())
        print("Say something else : ")
        x = input() 
    p.join()