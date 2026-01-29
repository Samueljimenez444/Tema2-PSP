from multiprocessing import Pool


def sumar_entre(valor1, valor2):
    """Suma todos los numeros entre dos valores, incluyendo ambos."""
    menor = min(valor1, valor2)
    mayor = max(valor1, valor2)

    suma = 0
    for i in range(menor, mayor + 1):
        suma += i

    print(f"La suma desde {valor1} hasta {valor2} es: {suma}")
    return suma


if __name__ == "__main__":
    # Pares de valores para cada proceso
    rangos = [
        (1, 10),
        (50, 20),
        (100, 200),
        (75, 25),
    ]

    # Usar Pool con starmap para funciones con multiples argumentos
    with Pool(processes=4) as pool:
        resultados = pool.starmap(sumar_entre, rangos)

    print(f"\nResultados: {resultados}")
    print("Todos los procesos han terminado")
