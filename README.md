# Pump Control - Control de Bomba Peristáltica

Permite conectarse a una bomba peristáltica que permita conexión por puerto serie y setear su velocidad en función de una
función del tiempo definida por el usuario.

## Tabla de Contenidos

- [Instalación](#instalación)
  - [Prerequisitos](#prerequisitos)
  - [Copia de repositorio y dependencias](#copia-de-repositorio-y-dependencias)
- [Uso](#uso)
  - [1. Seteo de puerto](#1-seteo-de-puerto)
  - [2. Definición de la función de velocidad e intervalo de comandos](#2-definición-de-la-función-de-velocidad-e-intervalo-de-comandos)
  - [3. Ejecución del script](#3-ejecución-del-script)
  - [4. Detención y relanzamiento del programa](#4-detención-y-relanzamiento-del-programa)
- [Logs](#logs)
- [Licencia](#licencia)


## Instalación
### Prerequisitos
Tener instalados los siguientes programas:
- Python
- Git

### Copia de repositorio y dependencias
1. Clona el repositorio:
   ```bash
   git clone https://github.com/crmarcos/pump_control.git
   ```
2. Instala las dependencias:
   ```bash
   pip install pyserial
   ```

## Uso

Los archivos que debe modificar el usuario son los siguientes:
- bombas\port_config.py: define el puerto serie donde está conectada la bomba.
- curvas\speed_function.py: define los parámetros de generación de la curva, el intervalo entre actualizaciones de velocidad y el tiempo máximo de simulación.
- t_inicial.txt: define el tiempo en segundos desde donde se desea que empiece a enviar comandos. Útil en caso de que se tenga que reiniciar el programa y la curva ya esté avanzada.

### 1. Seteo de puerto
Dentro del archivo **bombas\port_config.py**, modificar el valor de la variable **COM_PORT** al puerto que corresponda. **COMX** en windows, **/dev/ttyX** en linux, donde **X** lo otorga el sistema.

```bash
COM_PORT = "COM3"
```

### 2. Definición de la función de velocidad e intervalo de comandos
Dentro del archivo **curvas\speed_function.py**, se encuentra la función **speed_function()** que debe ser escrita por el usuario para definir la velocidad de la bomba en función del tiempo. La función es arbitraria, puede ser una única expresión o puede ser definida por tramos.

```bash
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
```

### 3. Ejecución del script
Ir al mismo nivel donde se encuentra el archivo **pump_control.py** y ejecutar:

```bash
py .\pump_control.py
```

En una primera instancia se va a intentar comunicarse con la bomba.
Luego se van a generar los puntos de la curva en función de los parámetros seteados.
Por último va a empezar a correr el tiempo de ejecución y los comandos van a ser enviados a intervalos regulares.

Ejemplo de salida por pantalla:

```bash
############################################
INICIO DE FUNCIONAMIENTO

Setear bomba en address: 1
      Setear velocidad a 0
      Setear sentido  a r
      Comando enviado:b'#0102r000E8\r'

Pedido de Estado:b'#0102G2D\r'
Received: '<0201r00001\r'
{'address': 1, 'speed': '000', 'rotation': 'r'}
############################################

############################################
CURVA PLANIFICADA
t=hhh:mm:ss (ssssssssss)  speed=nnn
t=000:00:00 (         0)  speed= 100.0
t=000:00:05 (         5)  speed= 100.0
t=000:00:10 (        10)  speed= 100.0
... más puntos por acá
t=047:59:50 (    172790)  speed= 998.9
t=047:59:55 (    172795)  speed= 998.9
t=048:00:00 (    172800)  speed= 999.0
############################################

############################################
Start from: t = 0.0
############################################

------------------------------------------------
000:00:00 since start

Setear bomba en address: 1
      Setear velocidad a 100
      Setear sentido  a r
      Comando enviado:b'#0102r100E9\r'

Interrupción detectada (Ctrl + C).
Cerrando el programa de forma ordenada.

Setear bomba en address: 1
      Setear velocidad a 0
      Setear sentido  a r
      Comando enviado:b'#0102r000E8\r'

... más comandos enviados acá

############################################
End of run
############################################

```

### 4. Detención y relanzamiento del programa
El programa se puede detener en cualquier momento presionando **CTRL+C**.
Si la bomba queda girando por una terminación incorrecta del programa, volver a relanzarlo para que la velocidad sea 0 y detenerlo nuevamente presionando **CTRL+C**. Si eso no funciona, desconectar la bomba.

Si se desea relanzarlo desde un punto particular de la curva,
hay que modificar el archivo **t_inicial.txt** indicando en su interior el tiempo en segundos desde donde se requiere que se retome la curva.

Para empezar desde el comienzo de la curva:
```bash
0.0
```

Para empezar desde t = 300.0 segundos:
```bash
300.0
```

Este valor debe ser indicado con un decimal después de la coma.

## Logs

- curva_planificada.log: contiene la tabla de pares de tiempo y velocidad que va a seguir la bomba.
- registro_de_corrida.log: es un log de todo lo que hizo el programa. Conservar en caso de falla del programa para debug.

## Licencia

Este proyecto está bajo la Licencia GPLv3.
