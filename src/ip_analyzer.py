
import ipaddress
import subprocess
import re


def obtener_configuracion_red():
    """
    Obtiene automáticamente la IP, máscara y puerta de enlace
    de la interfaz que Windows utiliza actualmente.
    """

    try:
        resultado = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            encoding="cp850"
        )

        texto = resultado.stdout

        # Buscar la puerta de enlace predeterminada
        gateway = re.search(
            r"Puerta de enlace predeterminada[ .]*:\s*(\d+\.\d+\.\d+\.\d+)",
            texto
        )

        if not gateway:
            print("No se pudo detectar la puerta de enlace.")
            return None

        gateway = gateway.group(1)

        # Buscar el bloque de configuración que contiene el gateway
        bloques = re.split(r"\n\s*\n", texto)

        for bloque in bloques:

            if gateway not in bloque:
                continue

            ip = re.search(
                r"Dirección IPv4[ .]*:\s*(\d+\.\d+\.\d+\.\d+)",
                bloque
            )

            mascara = re.search(
                r"Máscara de subred[ .]*:\s*(\d+\.\d+\.\d+\.\d+)",
                bloque
            )

            if ip and mascara:
                return {
                    "ip": ip.group(1),
                    "mascara": mascara.group(1),
                    "gateway": gateway
                }

        print("No se pudo identificar la configuración de la interfaz.")
        return None

    except Exception as error:
        print(f"Error al obtener la configuración de red: {error}")
        return None


def analizar_red(ip, mascara, gateway):
    """
    Calcula la información de la red a partir de la IP
    y la máscara detectadas.
    """

    try:
        interfaz = ipaddress.ip_interface(f"{ip}/{mascara}")
        red = interfaz.network

        print()
        print("========================================")
        print("          NETWORK ANALYZER")
        print("========================================")

        print()
        print("CONFIGURACIÓN ACTUAL")
        print("----------------------------------------")
        print(f"IP local:        {interfaz.ip}")
        print(f"Máscara:         {red.netmask}")
        print(f"Gateway:         {gateway}")

        print()
        print("========== RED ACTUAL ==========")
        print(f"Red:             {red.network_address}/{red.prefixlen}")
        print(f"Broadcast:       {red.broadcast_address}")

        if red.num_addresses > 2:
            hosts = list(red.hosts())

            print(f"Primer host:     {hosts[0]}")
            print(f"Último host:     {hosts[-1]}")
            print(f"Número de hosts: {len(hosts)}")
        else:
            print(f"Número de hosts: {red.num_addresses}")

    except ValueError:
        print("La configuración IPv4 detectada no es válida.")


def main():
    """
    Punto de entrada principal del analizador.
    """

    configuracion = obtener_configuracion_red()

    if configuracion is None:
        return

    analizar_red(
        configuracion["ip"],
        configuracion["mascara"],
        configuracion["gateway"]
    )


if __name__ == "__main__":
    main()

