import signal
import random
import time

def external (pid_market) :
    while True :
        print("What is happening to the Market ?")
        #evenement = input()
        frequency = 1
        evenement = random.randint(1, 4)
        time.sleep(frequency)

        if evenement == 1 :
            print("HURRICANE")
            signal.kill(pid_market, signal.sigint)
        elif evenement == 2 : 
            print("PUTIN MAKES A WAR")
            signal.kill(pid_market, signal.sigusr1)
        elif evenement == 3 : 
            print("FUEL SHORTAGE")
            signal.kill(pid_market, signal.sigusr2)
        elif evenement == 4 : 
            print("BUTTERFLY EFFECT")
            signal.kill(pid_market, signal.sigkill)
        else : 
            print("L'evenement que vous avez demandé n'existe pas")

pid_market = 8321
external(pid_market)