import ip_analyzer
import network_monitor


def main():
    configuracion = ip_analyzer.obtener_configuracion_red()

    if configuracion is None:
        return

    informacion_red = ip_analyzer.analizar_red(
        configuracion["ip"],
        configuracion["mascara"],
        configuracion["gateway"]
    )

    if informacion_red is None:
        return

    network_monitor.mostrar_estado(
        configuracion["gateway"]
    )
    dispositivos = network_monitor.escanear_red(
        informacion_red["red"]
    )

    network_monitor.mostrar_dispositivos(
        dispositivos
    )


if __name__ == "__main__":
    main()