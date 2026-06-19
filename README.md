# Pump Control - Control de Bomba Peristaltica

Permite conectarse a una bomba peristáltica que permita conexión por puerto serie y setear su velocidad en función de una
función del tiempo definida por el usuario.

## Tabla de Contenidos
- [Instalación](#instalación)
- [Uso](#uso)
- [Licencia](#licencia)

## Instalación

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

## Logs

- curva_planificada.log: contiene la tabla de pares de tiempo y velocidad que va a seguir la bomba.
- registro_de_corrida.log: es un log de todo lo que hizo el programa. Conservar en caso de falla del programa para debug.

## Licencia

Este proyecto está bajo la Licencia GPL.