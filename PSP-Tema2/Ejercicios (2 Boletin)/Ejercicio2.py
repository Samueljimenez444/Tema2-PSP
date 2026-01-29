from multiprocessing import Process, Pipe
import random


def obtener_clase_ip(ip):
    """
    Determina la clase de una direccion IP segun su primer octeto.

    Args:
        ip: Direccion IP como string (ej: "192.168.1.1")

    Returns:
        Clase de la IP (A, B, C) o None si no pertenece a ninguna
    """
    # Obtener el primer octeto
    primer_octeto = int(ip.split('.')[0])

    # Determinar la clase segun el rango del primer octeto
    if 1 <= primer_octeto <= 126:
        return 'A'
    elif 128 <= primer_octeto <= 191:
        return 'B'
    elif 192 <= primer_octeto <= 223:
        return 'C'
    else:
        return None


def proceso_generador(conexion_salida):
    """
    Proceso 1: Genera 10 direcciones IP aleatorias y las envia.
    """
    print("[P1] Generando 10 direcciones IP aleatorias...")

    for _ in range(10):
        # Generar IP aleatoria (4 octetos de 0-255)
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        print(f"[P1] Generada: {ip}")
        conexion_salida.send(ip)

    # Enviar None para indicar fin
    conexion_salida.send(None)
    conexion_salida.close()
    print("[P1] Finalizado")


def proceso_filtrador(conexion_entrada, conexion_salida):
    """
    Proceso 2: Filtra las IPs y envia solo las de clase A, B o C.
    """
    print("[P2] Esperando IPs para filtrar...")

    while True:
        ip = conexion_entrada.recv()

        # Si recibe None, termina
        if ip is None:
            break

        # Comprobar si es clase A, B o C
        clase = obtener_clase_ip(ip)
        if clase is not None:
            print(f"[P2] IP {ip} es clase {clase}, enviando...")
            conexion_salida.send(ip)
        else:
            print(f"[P2] IP {ip} descartada (no es clase A, B o C)")

    # Enviar None para indicar fin
    conexion_salida.send(None)
    conexion_entrada.close()
    conexion_salida.close()
    print("[P2] Finalizado")


def proceso_impresor(conexion_entrada):
    """
    Proceso 3: Recibe las IPs filtradas y muestra su clase.
    """
    print("[P3] Esperando IPs filtradas...")
    print("-" * 40)

    while True:
        ip = conexion_entrada.recv()

        # Si recibe None, termina
        if ip is None:
            break

        # Obtener clase y mostrar
        clase = obtener_clase_ip(ip)
        print(f"[P3] IP: {ip} -> Clase {clase}")

    print("-" * 40)
    conexion_entrada.close()
    print("[P3] Finalizado")


if __name__ == "__main__":
    # Crear tuberias para comunicacion entre procesos
    # Pipe 1: Proceso 1 -> Proceso 2
    pipe1_entrada, pipe1_salida = Pipe()

    # Pipe 2: Proceso 2 -> Proceso 3
    pipe2_entrada, pipe2_salida = Pipe()

    # Crear los procesos
    p1 = Process(target=proceso_generador, args=(pipe1_entrada,))
    p2 = Process(target=proceso_filtrador, args=(pipe1_salida, pipe2_entrada))
    p3 = Process(target=proceso_impresor, args=(pipe2_salida,))

    # Lanzar procesos en orden
    p1.start()
    p2.start()
    p3.start()

    # Esperar a que terminen
    p1.join()
    p2.join()
    p3.join()

    print("Todos los procesos han terminado")
