from multiprocessing import Process


def sumar_entre(valor1, valor2):
    """Suma todos los numeros entre dos valores, incluyendo ambos."""
    # Determinar el menor y mayor para manejar cualquier orden
    menor = min(valor1, valor2)
    mayor = max(valor1, valor2)

    suma = 0
    for i in range(menor, mayor + 1):
        suma += i

    print(f"La suma desde {valor1} hasta {valor2} es: {suma}")


if __name__ == "__main__":
    # Pares de valores para cada proceso (algunos invertidos)
    rangos = [
        (1, 10),
        (50, 20),     # Invertido: el primero es mayor
        (100, 200),
        (75, 25),     # Invertido: el primero es mayor
    ]

    # Crear lista de procesos
    procesos = []

    # Crear y arrancar cada proceso
    for valor1, valor2 in rangos:
        proceso = Process(target=sumar_entre, args=(valor1, valor2))
        procesos.append(proceso)
        proceso.start()

    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()

    print("Todos los procesos han terminado")
