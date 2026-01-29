from multiprocessing import Process, Pool
import random
import os

# Obtener directorio del script
DIRECTORIO = os.path.dirname(os.path.abspath(__file__))


def proceso_generar_notas(ruta_fichero):
    """
    Proceso 1: Genera 6 notas aleatorias (1-10 con decimales) y las guarda en un fichero.

    Args:
        ruta_fichero: Ruta donde guardar las notas
    """
    with open(ruta_fichero, 'w') as fichero:
        for _ in range(6):
            # Generar nota aleatoria con 2 decimales
            nota = round(random.uniform(1, 10), 2)
            fichero.write(f"{nota}\n")


def proceso_calcular_media(args):
    """
    Proceso 2: Lee las notas de un fichero y calcula la media.
    Guarda la media en medias.txt junto al nombre del alumno.

    Args:
        args: Tupla con (ruta_fichero_notas, nombre_alumno)
    """
    ruta_fichero, nombre_alumno = args

    # Leer las notas del fichero
    with open(ruta_fichero, 'r') as fichero:
        notas = [float(linea.strip()) for linea in fichero]

    # Calcular la media
    media = round(sum(notas) / len(notas), 2)

    # Escribir en medias.txt (modo append)
    ruta_medias = os.path.join(DIRECTORIO, "medias.txt")
    with open(ruta_medias, 'a') as fichero:
        fichero.write(f"{media} {nombre_alumno}\n")


def proceso_nota_maxima():
    """
    Proceso 3: Lee medias.txt y encuentra la nota maxima.
    Imprime el alumno con la mejor nota.
    """
    ruta_medias = os.path.join(DIRECTORIO, "medias.txt")

    nota_maxima = 0
    alumno_ganador = ""

    # Leer todas las medias
    with open(ruta_medias, 'r') as fichero:
        for linea in fichero:
            partes = linea.strip().split(' ')
            nota = float(partes[0])
            nombre = partes[1]

            # Actualizar si es mayor
            if nota > nota_maxima:
                nota_maxima = nota
                alumno_ganador = nombre

    # Mostrar resultado
    print("=" * 40)
    print(f"MEJOR ALUMNO: {alumno_ganador}")
    print(f"NOTA MEDIA: {nota_maxima}")
    print("=" * 40)


if __name__ == "__main__":
    # Limpiar medias.txt si existe
    ruta_medias = os.path.join(DIRECTORIO, "medias.txt")
    if os.path.exists(ruta_medias):
        os.remove(ruta_medias)

    # ============================================
    # PASO 1: Generar notas de 10 alumnos (Pool)
    # ============================================
    print("[MAIN] Generando notas de 10 alumnos...")

    # Crear lista de rutas de ficheros
    rutas_alumnos = [os.path.join(DIRECTORIO, f"Alumno{i}.txt") for i in range(1, 11)]

    # Lanzar 10 procesos concurrentes con Pool
    with Pool(processes=10) as pool:
        pool.map(proceso_generar_notas, rutas_alumnos)

    print("[MAIN] Notas generadas correctamente")

    # ============================================
    # PASO 2: Calcular medias (bucle for)
    # ============================================
    print("[MAIN] Calculando medias...")

    # Preparar argumentos: (ruta_fichero, nombre_alumno)
    argumentos = [(ruta, f"Alumno{i}") for i, ruta in enumerate(rutas_alumnos, 1)]

    # Crear y lanzar procesos con bucle for
    procesos = []
    for args in argumentos:
        p = Process(target=proceso_calcular_media, args=(args,))
        procesos.append(p)
        p.start()

    # Esperar a que todos terminen
    for p in procesos:
        p.join()

    print("[MAIN] Medias calculadas correctamente")

    # ============================================
    # PASO 3: Obtener nota maxima
    # ============================================
    print("[MAIN] Buscando mejor alumno...")

    p3 = Process(target=proceso_nota_maxima)
    p3.start()
    p3.join()

    print("[MAIN] Programa finalizado")
