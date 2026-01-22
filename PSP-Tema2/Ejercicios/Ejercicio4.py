from multiprocessing import Process, Pipe
import os


def leer_numeros(ruta_fichero, conexion):
    """Lee numeros de un fichero y los envia por la tuberia."""
    print("[LECTOR] Iniciando lectura del fichero...")

    with open(ruta_fichero, 'r') as fichero:
        for linea in fichero:
            numero = int(linea.strip())
            conexion.send(numero)
            print(f"[LECTOR] Enviado: {numero}")

    # Enviar None para indicar fin de datos
    conexion.send(None)
    print("[LECTOR] Lectura finalizada, enviado None")
    conexion.close()


def sumar_numeros(conexion):
    """Recibe numeros de la tuberia y los suma."""
    print("[SUMADOR] Esperando numeros...")
    suma = 0

    while True:
        numero = conexion.recv()

        # Si recibe None, termina
        if numero is None:
            break

        suma += numero
        print(f"[SUMADOR] Recibido: {numero}, suma parcial: {suma}")

    print(f"[SUMADOR] Suma total: {suma}")
    conexion.close()


if __name__ == "__main__":
    # Obtener ruta del directorio donde esta el script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(directorio, "numeros.txt")

    # Crear la tuberia (dos extremos)
    conexion_lector, conexion_sumador = Pipe()

    # Crear los procesos
    proceso_lector = Process(target=leer_numeros, args=(ruta_fichero, conexion_lector))
    proceso_sumador = Process(target=sumar_numeros, args=(conexion_sumador,))

    # Iniciar procesos
    proceso_lector.start()
    proceso_sumador.start()

    # Esperar a que terminen
    proceso_lector.join()
    proceso_sumador.join()

    print("Todos los procesos han terminado")
