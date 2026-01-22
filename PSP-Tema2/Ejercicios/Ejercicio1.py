from multiprocessing import Process


def sumar_hasta(numero):
    """Suma todos los numeros desde 1 hasta el numero dado."""
    suma = 0
    for i in range(1, numero + 1):
        suma += i
    print(f"La suma desde 1 hasta {numero} es: {suma}")


if __name__ == "__main__":
    # Valores para cada proceso
    valores = [10, 20, 50, 100]

    # Crear lista de procesos
    procesos = []

    # Crear y arrancar cada proceso
    for valor in valores:
        proceso = Process(target=sumar_hasta, args=(valor,))
        procesos.append(proceso)
        proceso.start()

    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()

    print("Todos los procesos han terminado")
