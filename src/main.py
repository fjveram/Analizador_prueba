import ip_analyzer


def main():
    configuracion = ip_analyzer.obtener_configuracion_red()

    if configuracion is None:
        return

    ip_analyzer.analizar_red(
        configuracion["ip"],
        configuracion["mascara"],
        configuracion["gateway"]
    )


if __name__ == "__main__":
    main()