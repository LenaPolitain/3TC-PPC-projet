import random
import time

initial_energy = 10
production_rate = 2
consumption_rate = 3
trade_policy = 0
MIN_TO_SELL = 5
MIN_TO_BUY = 2

# selling queue fonctionnelle mais problèmes ds le côté économique 

def home(id, selling_queue) :
    
    global initial_energy 
    trade_policy = random.randint(1, 2)

    while True :

        initial_energy = initial_energy - consumption_rate + production_rate

        # si on veut vendre
        if initial_energy >= MIN_TO_SELL : 
            if trade_policy == 1 :
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : put {initial_energy-MIN_TO_BUY} enery in the queue")
                selling_queue.put(initial_energy-MIN_TO_BUY)
            elif trade_policy == 2 : 
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : put {initial_energy-MIN_TO_BUY} energy on the market") 
            initial_energy = MIN_TO_BUY

        # si on est en rade d'énergie 
        if (initial_energy < MIN_TO_BUY) : 
            try :  
                message = selling_queue.get()
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : got {message} energy from the queue")
                initial_energy = initial_energy + message
            except:     
                print(f"House number {id} with trade policy {trade_policy} and {initial_energy} energy left : got {MIN_TO_BUY} enery from the market") 
        
        time.sleep(3)