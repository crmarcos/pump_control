# Numero máximo de segundos para la simulación
END_OF_TIMES = 48*3600
# Intervalo de generación de puntos de la curva y 
# envío de comandos para la bomba
interval = 5 

# Función de la velocidad (en segundos)
def speed_function(t):
    Pmax = 999                  # RPM máxima
    P0 = 100                    # RPM inicial definida por le usuario
    T_horas = 48                # Duración de la curva en horas
    T_segundos = T_horas * 3600 # Duración de la curva en segundos

    # Fórmula que devuelve las RPM para un t dado
    return P0 * (Pmax / P0) ** (t / T_segundos)

    #return 100+0.0000319*t