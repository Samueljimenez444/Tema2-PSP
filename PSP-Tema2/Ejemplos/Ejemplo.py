from multiprocessing import pool
import threading

def square(number):
    return number*number

if __name__ == "main":
    with pool(processes=3) as pool:
        numbers=[1,2,3,4,5]
        
        results = pool.map(square,numbers)
        
        print("Resultados: ", results)