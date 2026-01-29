from multiprocessing import Process, Queue
import os


def leer_numeros(ruta_fichero, cola):
    """Lee numeros de un fichero y los pone en la cola."""
    print("[LECTOR] Iniciando lectura del fichero...")

    with open(ruta_fichero, 'r') as fichero:
        for linea in fichero:
            numero = int(linea.strip())
            cola.put(numero)
            print(f"[LECTOR] Enviado a la cola: {numero}")

    # Enviar None para indicar fin de datos
    cola.put(None)
    print("[LECTOR] Lectura finalizada, enviado None")


def sumar_numeros(cola):
    """Lee numeros de la cola y los suma."""
    print("[SUMADOR] Esperando numeros...")
    suma = 0

    while True:
        numero = cola.get()

        # Si recibe None, termina
        if numero is None:
            break

        suma += numero
        print(f"[SUMADOR] Recibido: {numero}, suma parcial: {suma}")

    print(f"[SUMADOR] Suma total: {suma}")


if __name__ == "__main__":
    # Obtener ruta del directorio donde esta el script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(directorio, "numeros.txt")

    # Crear la cola para comunicacion
    cola = Queue()

    # Crear los procesos
    proceso_lector = Process(target=leer_numeros, args=(ruta_fichero, cola))
    proceso_sumador = Process(target=sumar_numeros, args=(cola,))

    # Iniciar procesos
    proceso_lector.start()
    proceso_sumador.start()

    # Esperar a que terminen
    proceso_lector.join()
    proceso_sumador.join()

    print("Todos los procesos han terminado")
