#autor: Pizano Pérez José Eduardo
Este proyecto es un centro multimedia para la raspberry pi 

Este proyecto solo puede ser realizado con los siguientes materiales
•	Raspberry pi 4
•	Memoria MicroSD de 8 GB o superior
•	Monitor con entrada HDMI
•	Mouse y teclado con cables USB 
•	Cable HDMI a microHDMI
•	Una fuente de alimentación de 5V@1A con adaptador USB tipo C
•	Control remoto
•	Un módulo ky-022
•	Arduino Uno
•	Protoboard 
•	Cables varios.
•	Extensión puerto GPIO a protoboard para Raspberry
•	USB con contenido multimedia

Los codigos necesarios estan presentes en 
https://github.com/JoseEduardoPizano/Proyecto-Multimedia.git

Dependiendo del Control remoto es necesario modificar el archivo control.ino ubicado en 
src/control para las señales que mande el control

Las librerias a utilizar son
•	Tkinter
•	De tkinter tkk y PhotoImage
•	Pygame
•	Webview 
•	Time
•	Os
•	Threading
•	Smbus2
•	Struct
•	Pyautogui
•	De Pil importaremos Image y ImageTk
•	De tkinter.messagebox importaremos showinfo y showerror
•	De mutagen.mp3 importaremos MP3

Los comandos en consola necesarios son 
•	pip install Pillow
•	pip install functools
•	pip install pygame
•	pip install mutagen
•	pip install smbus2
•	pip install pyautogui
sudo apt-get install python-rpi.gpio python3-rpi.gpio



