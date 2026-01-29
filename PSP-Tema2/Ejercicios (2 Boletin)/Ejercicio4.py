from multiprocessing import Process, Pipe
import os
from datetime import datetime

# Obtener directorio del script
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))


def proceso_filtrar_peliculas(ruta_fichero, anio, conexion_salida):
    """
    Proceso 1: Lee el fichero de peliculas y envia las del año indicado.

    Args:
        ruta_fichero: Ruta al fichero con las peliculas
        anio: Año a filtrar
        conexion_salida: Conexion del Pipe para enviar peliculas
    """
    print(f"[P1] Buscando peliculas del año {anio}...")

    # Leer el fichero de peliculas
    with open(ruta_fichero, 'r', encoding='utf-8') as fichero:
        for linea in fichero:
            # Separar nombre y año
            partes = linea.strip().split(';')
            nombre = partes[0]
            anio_pelicula = int(partes[1])

            # Enviar solo si coincide el año
            if anio_pelicula == anio:
                print(f"[P1] Enviando: {nombre}")
                conexion_salida.send(nombre)

    # Enviar None para indicar fin
    conexion_salida.send(None)
    conexion_salida.close()
    print("[P1] Finalizado")


def proceso_guardar_peliculas(anio, conexion_entrada):
    """
    Proceso 2: Recibe peliculas y las guarda en un fichero.

    Args:
        anio: Año para nombrar el fichero de salida
        conexion_entrada: Conexion del Pipe para recibir peliculas
    """
    # Crear nombre del fichero de salida
    ruta_salida = os.path.join(DIRECTORIO, f"peliculas{anio}.txt")
    peliculas_guardadas = []

    print(f"[P2] Esperando peliculas para guardar en peliculas{anio}.txt...")

    while True:
        pelicula = conexion_entrada.recv()

        # Si recibe None, termina
        if pelicula is None:
            break

        peliculas_guardadas.append(pelicula)
        print(f"[P2] Recibida: {pelicula}")

    # Guardar peliculas en el fichero
    with open(ruta_salida, 'w', encoding='utf-8') as fichero:
        for pelicula in peliculas_guardadas:
            fichero.write(f"{pelicula}\n")

    conexion_entrada.close()
    print(f"[P2] Guardadas {len(peliculas_guardadas)} peliculas en peliculas{anio}.txt")


if __name__ == "__main__":
    # Obtener año actual
    anio_actual = datetime.now().year

    # Solicitar año al usuario
    while True:
        try:
            anio = int(input("Introduce un año (menor al actual): "))
            if anio < anio_actual:
                break
            else:
                print(f"El año debe ser menor a {anio_actual}")
        except ValueError:
            print("Introduce un número válido")

    # Solicitar ruta del fichero
    ruta = input("Introduce la ruta del fichero de peliculas (o pulsa Enter para usar peliculas.txt): ")
    if ruta == "":
        ruta = os.path.join(DIRECTORIO, "peliculas.txt")

    # Verificar que el fichero existe
    if not os.path.exists(ruta):
        print(f"Error: El fichero {ruta} no existe")
        exit(1)

    print("-" * 40)

    # Crear Pipe para comunicacion entre procesos
    conexion_p1, conexion_p2 = Pipe()

    # Crear los procesos
    p1 = Process(target=proceso_filtrar_peliculas, args=(ruta, anio, conexion_p1))
    p2 = Process(target=proceso_guardar_peliculas, args=(anio, conexion_p2))

    # Lanzar procesos
    p1.start()
    p2.start()

    # Esperar a que terminen
    p1.join()
    p2.join()

    print("-" * 40)
    print("Programa finalizado")
