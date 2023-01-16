#autor Pizano Pérez Jose Eduardo

import smbus2
import struct
import time
import pyautogui
import os
# Arduino's I2C device address
SLAVE_ADDR = 31 # I2C Address of Arduino 1


# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)
desplazamiento = 50

#La clase cola realizará la función de una cola debido a que no existe en python como tal
class Cola:
    def __init__(self):
        self.items = []


    def agregar(self, item):
        self.items.insert(0,item)

    def avanzar(self):
        return self.items.pop()

    def tam(self):
        return len(self.items)

#Variable que guardara todos los botones presionados por el control remoto        
botones_presionados = Cola()

#petición para leer el boton presionado con comunicacion I2C
def readbotonerature():
    try:
        msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
        i2c.i2c_rdwr(msg)
        data = list(msg)
        pizano = bytes(data)
        boton = struct.unpack('f',pizano)
        boton = boton[0]
        return boton
    except:
        return 0.0
#funcion que realiza acciones dependiendo del boton presionado
def cursor(opcion):
    global desplazamiento
    if  opcion == 1:
        print("Apagar")
        pyautogui.hotkey("ctrl","shift","w")
    elif  opcion == 2:
        
        try:
            os.system("onboard")
            print("Mode")
        except:
            print("Mode2")
    elif  opcion == 3:
        print("Clk")
    elif  opcion == 4:
        print("1")
    elif  opcion == 5:
        print("2")
    elif  opcion == 6:
        print("3")
    elif  opcion == 7:
        print("4")
        desplazamiento = 12
    elif  opcion == 8:
        print("5")
        desplazamiento = 25
    elif  opcion == 9:
        print("6")
        desplazamiento = 50
    elif  opcion == 10:
        print("Loud")
    elif  opcion == 11:
        print("Arriba")
        pos = pyautogui.position()
        pyautogui.moveTo(pos.x,pos.y-desplazamiento)
    elif  opcion == 12:
        print("Eq")
    elif  opcion == 13:
        print("Izquierda")
        pos = pyautogui.position()
        pyautogui.moveTo(pos.x-desplazamiento,pos.y)
    elif  opcion == 14:
        print("Enter")
        pyautogui.click()
    elif  opcion == 15:
        print("Derecha")
        pos = pyautogui.position()
        pyautogui.moveTo(pos.x+desplazamiento,pos.y)
    elif  opcion == 16:
        print("Aps")
    elif  opcion == 17:
        print("Abajo")
        pos = pyautogui.position()
        pyautogui.moveTo(pos.x,pos.y+desplazamiento)
    elif  opcion == 18:
        print("Band")    
          
    else:
        print("Error boton no reconocido")
#verifica si es un flotante el numero que llega para no tener errores
def convertir():
    try:
        num = int(readbotonerature())
        return num
    except:
        return 0
        
#funcion que controla las peticiones y guarda los botones seleccionados para su posterior uso        
def mover():
    try:
        cboton = convertir()
        print("BOTON: "+str(cboton))
        if (cboton != 19):
            botones_presionados.agregar(cboton)
        if (botones_presionados.tam() != 0):
            x = botones_presionados.avanzar()
            cursor(x)
        time.sleep(0.1)
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    while True:
        mover()



