from multiprocessing import Pool
import time


def sumar_hasta(numero):
    """Suma todos los numeros desde 1 hasta el numero dado."""
    suma = 0
    for i in range(1, numero + 1):
        suma += i
    return suma


def ejecutar_con_pool(num_procesos, valores):
    """Ejecuta la suma con un pool de procesos y mide el tiempo."""
    inicio = time.perf_counter()

    with Pool(processes=num_procesos) as pool:
        resultados = pool.map(sumar_hasta, valores)

    fin = time.perf_counter()
    tiempo = fin - inicio

    print(f"Pool con {num_procesos} procesos:")
    for i, valor in enumerate(valores):
        print(f"  Suma hasta {valor}: {resultados[i]}")
    print(f"  Tiempo: {tiempo:.4f} segundos\n")

    return tiempo


if __name__ == "__main__":
    # Valores grandes para notar diferencia de tiempos
    valores = [5000000, 10000000, 15000000, 20000000]

    print("Comparacion de tiempos con diferente numero de procesos\n")

    # Probar con diferentes cantidades de procesos
    tiempos = {}
    for num_procesos in [1, 2, 4, 6]:
        tiempos[num_procesos] = ejecutar_con_pool(num_procesos, valores)

    # Mostrar resumen comparativo
    print("RESUMEN:")
    for num_procesos, tiempo in tiempos.items():
        print(f"  {num_procesos} proceso(s): {tiempo:.4f} segundos")

    print("\nTodos los procesos han terminado")
