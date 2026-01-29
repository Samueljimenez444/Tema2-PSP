from multiprocessing import Pool
import os


def contar_vocal(vocal):
    """
    Cuenta cuantas veces aparece una vocal en el fichero.

    Args:
        vocal: La vocal a buscar (a, e, i, o, u)

    Returns:
        Tupla con la vocal y su cantidad
    """
    # Obtener ruta del fichero de texto
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(directorio, "texto.txt")

    # Leer el contenido del fichero
    with open(ruta_fichero, 'r', encoding='utf-8') as fichero:
        contenido = fichero.read().lower()  # Convertir a minusculas

    # Contar la vocal
    cantidad = contenido.count(vocal)

    return (vocal, cantidad)


if __name__ == "__main__":
    # Lista de vocales a buscar
    vocales = ['a', 'e', 'i', 'o', 'u']

    # Crear pool con 5 procesos (uno por vocal)
    with Pool(processes=5) as pool:
        # Ejecutar en paralelo para cada vocal
        resultados = pool.map(contar_vocal, vocales)

    # Mostrar resultados
    print("Conteo de vocales en el fichero:")
    print("-" * 30)
    for vocal, cantidad in resultados:
        print(f"Vocal '{vocal}': {cantidad} veces")

    # Mostrar total
    total = sum(cantidad for _, cantidad in resultados)
    print("-" * 30)
    print(f"Total de vocales: {total}")
