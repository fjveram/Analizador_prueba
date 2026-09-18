import subprocess
import re


def hacer_ping(ip):
    """
    Realiza un ping a una dirección IPv4 y devuelve
    el estado y la latencia.
    """

    try:
        resultado = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True,
            text=True,
            encoding="cp850"
        )

        texto = resultado.stdout

        if resultado.returncode != 0:
            return {
                "ip": ip,
                "estado": "OFFLINE",
                "latencia": None
            }

        latencia = re.search(r"tiempo[=<]\s*(\d+)\s*ms", texto)

        if latencia:
            latencia = int(latencia.group(1))
        else:
            latencia = None

        return {
            "ip": ip,
            "estado": "ONLINE",
            "latencia": latencia
        }

    except Exception as error:
        print(f"Error realizando ping: {error}")
        return None

def escanear_red(red):
    
    dispositivos = []
    print(f"Escaneando red: {red}")

    for ip in red.hosts():

        resultado = hacer_ping(str(ip))

        if resultado and resultado["estado"] == "ONLINE":
            dispositivos.append(resultado)

    return dispositivos
def mostrar_dispositivos(dispositivos):
    """
    Muestra los dispositivos que respondieron al escaneo.
    """

    print()
    print("========== DISPOSITIVOS DETECTADOS ==========")
    print()

    if not dispositivos:
        print("No se encontro dispositivos.")
        return

    for dispositivo in dispositivos:
        print(
            f"IP: {dispositivo['ip']} | "
            f"Estado: {dispositivo['estado']} | "
            f"Latencia: {dispositivo['latencia']} ms"
        )

def mostrar_estado(ip):


    resultado = hacer_ping(ip)

    if resultado is None:
        return

    print()
    print("========== NETWORK MONITOR ==========")
    print()
    print(f"IP objetivo: {resultado['ip']}")
    print(f"Estado:      {resultado['estado']}")

    if resultado["latencia"] is not None:
        print(f"Latencia:    {resultado['latencia']} ms")
if __name__ == "__main__":
        mostrar_estado("172.16.1.1")