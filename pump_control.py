import sys
import os
import time
import math

# Control de bomba
from bombas.lambda_preciflow_v0 import PumpControl
from bombas.port_config import COM_PORT

# Archivo con funcion de velocidad
from curvas.speed_function import speed_function

# Variables globales
from curvas.speed_function import END_OF_TIMES
from curvas.speed_function import interval

# Clase para duplicar la salida por pantalla y generar un log
class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()


def simulate_speed_function(interval=5):
    """
    Devuelve una lista de pares ordenados (t, speed)
    desde t=0 hasta END_OF_TIMES o hasta que speed > 999.
    """
    results = []
    t = 0

    while t <= END_OF_TIMES:
        speed = speed_function(t)

        if speed > 999:
            break

        results.append((t, speed))
        t += interval

    return results


def print_and_log(text, file):
    print(text)
    file.write(text + "\n")

def format_time(seconds):
    seconds = int(seconds)

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:03d}:{minutes:02d}:{seconds:02d}"

# Main function
def main():

    # Abro el archivo de log y lo vinculo a la salida por terminal
    log_file = open("registro_de_corrida.log", "a", encoding="utf-8")
    sys.stdout = Tee(sys.stdout, log_file)

    print("\n############################################")
    print(f"INICIO DE FUNCIONAMIENTO")

    # Configuración de bomba (Dirección en RS485, sentido de giro)
    pc = PumpControl(address = 1, comport = COM_PORT)
    pc.set_cw_rotation()

    # Pregunta estado actual
    status = pc.get_status()
    print(status)
    print("############################################") 

    # La curva planificada tiene su propio archivo para poder consultarlo
    with open("curva_planificada.log", "w", encoding="utf-8") as f:
        print_and_log("\n############################################", f)
        print_and_log(f"CURVA PLANIFICADA", f)
        print_and_log(f"t=hhh:mm:ss (ssssssssss)  speed=nnn", f)
        # Curva planificada
        data = simulate_speed_function(interval)
        for t, speed in data:
            print_and_log(f"t={format_time(t)} ({t:10d})  speed={speed:6.1f}", f)
        print_and_log("############################################", f) 



    # Curva de trabajo
    # Se usa reloj del sistema para obtener el tiempo desde el inicio

     # Busco por el archivo last_t
    # que guarda el valor del tiempo en el que se quiere empezar la curva
    # Si no lo encuentra, empieza de t=0
    STATE_FILE = "t_inicial.txt"

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            t0 = float(f.read())
    else:
        t0 = 0

    print("\n############################################")
    print(f"Start from: t = {t0}")
    print("############################################") 

    
    try:
        t_run = time.monotonic()
        next_execution = t_run

        while True:
            t = time.monotonic() - t_run + t0

            if (t >= END_OF_TIMES) or (t > data[-1][0]):
                print("\n############################################")
                print("End of run")
                print("############################################")

                pc.set_speed(0)
                time.sleep(5)

                break

            print("\n------------------------------------------------")
            print(f"{format_time(t)} since start")

            speed = int(round(speed_function(t))) % 1000
            pc.set_speed(speed)

            next_execution += interval
            time.sleep(max(0, next_execution - time.monotonic()))
            
    except KeyboardInterrupt:
        print("\nInterrupción detectada (Ctrl + C).")
        print("Cerrando el programa de forma ordenada.")
        pc.set_speed(0)

        time.sleep(5)
        sys.exit(0)



if __name__ == "__main__":
    main()
