from multiprocessing import Process, Pipe
import os


def leer_rangos(ruta_fichero, conexion):
    """Lee pares de numeros de un fichero y los envia por la tuberia."""
    print("[LECTOR] Iniciando lectura del fichero...")

    with open(ruta_fichero, 'r') as fichero:
        for linea in fichero:
            partes = linea.strip().split()
            valor1 = int(partes[0])
            valor2 = int(partes[1])
            conexion.send((valor1, valor2))
            print(f"[LECTOR] Enviado: ({valor1}, {valor2})")

    # Enviar None para indicar fin de datos
    conexion.send(None)
    print("[LECTOR] Lectura finalizada, enviado None")
    conexion.close()


def sumar_rangos(conexion):
    """Recibe pares de numeros de la tuberia y suma los valores entre ellos."""
    print("[SUMADOR] Esperando rangos...")

    while True:
        datos = conexion.recv()

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
    conexion.close()


if __name__ == "__main__":
    # Obtener ruta del directorio donde esta el script
    directorio = os.path.dirname(os.path.abspath(__file__))
    ruta_fichero = os.path.join(directorio, "rangos.txt")

    # Crear la tuberia (dos extremos)
    conexion_lector, conexion_sumador = Pipe()

    # Crear los procesos
    proceso_lector = Process(target=leer_rangos, args=(ruta_fichero, conexion_lector))
    proceso_sumador = Process(target=sumar_rangos, args=(conexion_sumador,))

    # Iniciar procesos
    proceso_lector.start()
    proceso_sumador.start()

    # Esperar a que terminen
    proceso_lector.join()
    proceso_sumador.join()

    print("Todos los procesos han terminado")
