from multiprocessing import Process, Queue
import os


def leer_rangos(ruta_fichero, cola):
    """Lee pares de numeros de un fichero y los pone en la cola."""
    print("[LECTOR] Iniciando lectura del fichero...")

    with open(ruta_fichero, 'r') as fichero:
        for linea in fichero:
            partes = linea.strip().split()
            valor1 = int(partes[0])
            valor2 = int(partes[1])
            cola.put((valor1, valor2))
            print(f"[LECTOR] Enviado a la cola: ({valor1}, {valor2})")

    # Enviar None para indicar fin de datos
    cola.put(None)
    print("[LECTOR] Lectura finalizada, enviado None")


def sumar_rangos(cola):
    """Lee pares de numeros de la cola y suma los valores entre ellos."""
    print("[SUMADOR] Esperando rangos...")

    while True:
        datos = cola.get()

        # Si recibe None, termina
        if datos is None:
            break

        valor1, valor2 = datos
        menor = min(valor1, valor2)
        mayor = max(valor1, valor2)

        suma = 0
        for i in range(menor, mayor + 1):
            suma += i

        print(f"[SUMADOR] Suma desde {valor1} hasta {valor2}: {suma}")

    print("[SUMADOR] Finalizado")


if __name__ == "__main__":
    # Obtener ruta del directorio donde esta el script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(directorio, "rangos.txt")

    # Crear la cola para comunicacion
    cola = Queue()

    # Crear los procesos
    proceso_lector = Process(target=leer_rangos, args=(ruta_fichero, cola))
    proceso_sumador = Process(target=sumar_rangos, args=(cola,))

    # Iniciar procesos
    proceso_lector.start()
    proceso_sumador.start()

    # Esperar a que terminen
    proceso_lector.join()
    proceso_sumador.join()

    print("Todos los procesos han terminado")
