import sys
import time
import serial

# Pump Control Class
class PumpControl:
    
    def __init__(self, comport = "COM4", address = 0, speed = 0, rotation = "l"):
        self.comport = comport   # Com port number
        self.address = address   # 0 a 99
        self.speed = speed       # 0 a 999
        self.rotation = rotation # "l" o "r"


    def send_command(self):
        print(f"\nSetear bomba en address: {self.address}")
        print(f"      Setear velocidad a {self.speed}")
        print(f"      Setear sentido  a {self.rotation}")
        
        #Port init
        try:
            ser = serial.Serial(self.comport, baudrate=2400,bytesize=serial.EIGHTBITS, parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_ONE,timeout=10)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            exit()
        time.sleep(0.1)
        ser.flush()

        # Command
        cmd = f"#{self.address:02d}02{self.rotation}{self.speed:03d}"
        cs = sum(ord(c) for c in cmd) % 256

        cmd = f"{cmd}{cs:02X}\r"
        
        print("      Comando enviado:" + f"{cmd.encode()}")

        #Port writing
        ser.write(cmd.encode());

    def get_status(self):
        
        #Port init
        try:
            ser = serial.Serial(self.comport, baudrate=2400,bytesize=serial.EIGHTBITS, parity=serial.PARITY_ODD,stopbits=serial.STOPBITS_ONE,timeout=10)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            exit()
        time.sleep(0.1)
        ser.flush()

        # Command
        cmd = f"#{self.address:02d}02G"
        cs = sum(ord(c) for c in cmd) % 256

        cmd = f"{cmd}{cs:02X}\r"

        print("\nPedido de Estado:" + f"{cmd.encode()}")

        #Port writing
        ser.write(cmd.encode());
        time.sleep(0.1)
        
        # 1. Read raw bytes until \r is found
        raw_data = ser.read_until(b'\r')
        
        # 2. Convert bytes to string (optional)
        decoded_string = raw_data.decode('utf-8')
        status_speed = decoded_string[6:9]
        status_rotation = decoded_string[5:6]

        print(f"Received: {repr(decoded_string)}")

        return {"address": self.address , "speed": status_speed, "rotation": status_rotation} 

        

    def set_speed(self, speed):
        # Chequeo que speed sea entre 0 y 999
        if (speed >= 0) and (speed <= 999):
            self.speed = speed
        else:
            print("!!!!!! Valor de speed no válido !!!!! ")
        self.send_command()

    def set_cw_rotation(self):
        self.rotation = "r"
        self.send_command()

    def set_ccw_rotation(self):
        self.rotation = "l"
        self.send_command()