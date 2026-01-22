from multiprocessing import Process
import os
import time

def sumar_numeros(numero : int)  -> None:
    print(f"[HIJO] Hola {numero}. PID={os.getpid()}")
    

if __name__ == "__main__":
    print(f"[PADRE] PID={os.getpid()}")
    
    p = Process(target = sumar_numeros,args=(1,))
    inicio = time.perf_counter()
    p.start()
    p.join()
    fin = time.perf_counter()
    tiempo_proceso = fin - inicio
    
    print("[PADRE] El proceso ha terminado")
    print("[PADRE] se ha tardado " , tiempo_proceso)
    
    
    #multiprocessing.Process(target = ..., args = ...)
    #start() join()
    
