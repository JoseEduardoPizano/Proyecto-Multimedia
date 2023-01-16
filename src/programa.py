#Autor: Pizano Pérez José Eduardo
#Programa multimedia
#Es necesario el Uso de una Raspberry, un arduino y un modulo IR
#import tkinter


import tkinter as tk
from tkinter import ttk
#import webview
import webbrowser
from PIL import Image,ImageTk
from tkinter import PhotoImage
from functools import partial
import time
#from tkvideo import tkvideo
import dir as buscar
import pygame
import os
#from tkinter import HORIZONTAL,SUNKEN, W
try:
    from mutagen.mp3 import MP3
except:
    raise ValueError('Instale la libreria mutagen con: pip install mutagen')
    from mutagen.mp3 import MP3
import threading
from tkinter.messagebox import showinfo, showerror
if os.name != 'nt': #sistema Windows
    import cursor
    import pyudev
    import pyautogui

#variables que nos indican si se inserto una memoria USB despues de cargar el programa.
memoria = "remove"
memoria_antes = "remove"

#Ayuda a los ciclos While a permanecer activos
ventana_cerrar = True

class Ventanavideo(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana = self
        self.width= self.winfo_screenwidth()
        self.height= self.winfo_screenheight() 
        
        self.tam_boton_x = int(self.height/8)
        self.tam_boton_y = self.tam_boton_x 
        
        self.config(width=self.width, height= self.height)
        self.title("Ventana secundaria")
        
        self.ruta = buscar.buscar("video")
        self.lista = ["Option 1", "Option 2", "Option 3", "Option 4"]
        
        # seleccionado en OptionMenu
        self.value_inside = tk.StringVar(self.ventana)
          
        # Establecer el valor predeterminado de la variable
        self.value_inside.set("Select an Option")
        
        self.label1= tk.Label(self)
        #label.pack()
        self.label1.place(relx=.55, rely=.5, anchor='center')
          
        # Create the optionmenu widget and passing 
        # the options_list and value_inside to it.
        self.question_menu = tk.OptionMenu(self.ventana, self.value_inside, *self.lista)
        self.question_menu.place(relx=.1, rely=.05, anchor='center')

          
         ##Boton de play
        self.im1=Image.open('/home/pizano/Desktop/Proyecto/iconos/play.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_play = ImageTk.PhotoImage(self.im1,master=self) #se utiliza el master para corregir el error de seleccionar una photo random
        self.boton=tk.Button(self, image=self.foto_play, command=self.print_answers)
        self.boton.place(relx=.10, rely=.2, anchor='center')#grid(column=1, row=2)
                
                
        ##Boton de pausa
        self.im2=Image.open('/home/pizano/Desktop/Proyecto/iconos/stop.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_pause = ImageTk.PhotoImage(self.im2,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton1=tk.Button(self, image=self.foto_pause, command=self.print_answers)
        self.boton1.place(relx=.10, rely=.35, anchor='center')#grid(column=2, row=2)
        
        #submit_button = tk.Button(self.ventana, text='Submit', command=self.print_answers)
        #submit_button.place(x=75, y=75)
        
        '''self.boton_cerrar = ttk.Button(
            self,
            text="Cerrar ventana",
            command=self.destroy
        )
        self.boton_cerrar.place(x=75, y=75)'''
        
        
        self.focus()
        self.grab_set()
        
        
    def print_answers(self):
        print("Hola desde aqui")
        print("Selected Option: {}".format(self.value_inside.get()))
               
    #def play(self):
        #pygame.init()
        #AnchuraMaxima=self.width-400
        #AlturaMaxima=self.height-200
        #player = tkvideo("merlina.mp4", self.label1, loop = 1, size = (1800,720))
        #player.play() 
        #pygame.quit()

class VentanaMusica(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ventana = self
        
        #Obtener el largo y ancho de la pantalla
        self.width= self.winfo_screenwidth()
        self.height= self.winfo_screenheight() 
        
        #Obtener un tamaño aproximado para asignar a los botones
        self.tam_boton_x = int(self.height/8)
        self.tam_boton_y = self.tam_boton_x 
        
        #Redimencionar la ventana
        self.config(width=self.width, height= self.height)
        
        #Variables necesarias para navegar entre canciones
        self.cancion=""
        self.listaCanciones=[]
        self.contador = 0
        self.cantidad = 0
        self.nombre_cancion_titulo = ""

        pygame.mixer.init()
        self.pausado=False
        self.nombre_cancion=""     
        
        #Ruta absoluta de la carpeta Iconos en Raspberry
        ruta="/home/pizano/Desktop/Proyecto/iconos/"
        self.des = self.ventana.after(1000, self.ReproducirCancion)
        
        
        ##Boton de play
        self.im1=Image.open(ruta+'play.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_play = ImageTk.PhotoImage(self.im1,master=self) #se utiliza el master para corregir el error de seleccionar una photo random
        self.boton=tk.Button(self, image=self.foto_play, command=self.ReproducirCancion)
        self.boton.place(relx=.10, rely=.2, anchor='center')#grid(column=1, row=2)
                
                
        ##Boton de pausa
        self.im2=Image.open(ruta+'pause.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_pause = ImageTk.PhotoImage(self.im2,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton1=tk.Button(self, image=self.foto_pause, command=self.PausarCancion)
        self.boton1.place(relx=.10, rely=.35, anchor='center')#grid(column=2, row=2)

        ##Boton de stop
        self.im3=Image.open(ruta+'stop.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_stop = ImageTk.PhotoImage(self.im3,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton2=tk.Button(self, image=self.foto_stop, command=self.DetenerCancion)
        self.boton2.place(relx=.10, rely=.5, anchor='center')#grid(column=3, row=2) 

        ##Boton de prev
        self.im4=Image.open(ruta+'prev_music.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_prev = ImageTk.PhotoImage(self.im4,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton3=tk.Button(self, image=self.foto_prev, command=self.PrevCancion)
        self.boton3.place(relx=.10, rely=.65, anchor='center')#grid(column=4, row=2) 
        
        ##Boton de next
        self.im5=Image.open(ruta+'next_music.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.foto_next = ImageTk.PhotoImage(self.im5,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton4=tk.Button(self, image=self.foto_next, command=self.NextCancion)
        self.boton4.place(relx=.10, rely=.8, anchor='center')#grid(column=5, row=2) 
        
        
        #Selección de la cancion a reproducir de la carpeta Canciones
        self.listaCanciones= buscar.buscar("sonido")
        self.cantidad = len(self.listaCanciones)


        #Descripción del total de canción y tiempo transcurrido
        self.lengthlabel = tk.Label(self, text='Duración total de la canción: --:--')
        self.lengthlabel.place(relx=.0, rely=.1)
        

        #Titulo
        self.barra=tk.Label(self, text="Reproductor de música", font="Times 12 italic")
        self.barra.place(relx=.0, rely=.0)

        self.protocol("WM_DELETE_WINDOW", self.cierre)        

        #Titulo cancion
        self.buscar_nombre()
        self.titulo_cancion=tk.Label(self, text=self.nombre_cancion_titulo, font="Times 35 italic")
        self.titulo_cancion.place(relx=.7, rely=.05, anchor='center')
        
        
        self.im6=Image.open(ruta+'music.png')
        self.foto_music = ImageTk.PhotoImage(self.im6,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
         
        self.imagen_musica= tk.Label(self,image= self.foto_music)
        #self.imagen_musica.pack()
        self.imagen_musica.place(relx=.7, rely=.5, anchor='center')
        
        self.focus()
        self.grab_set()
        
    def ReproducirCancion(self):

        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
        else:
            try:
                self.DetenerCancion() 
                nombre_cancion=self.listaCanciones[self.contador]
                pygame.mixer.music.load(nombre_cancion) 
                pygame.mixer.music.play() 
                self.mostrar_detalles(nombre_cancion)
            except:
                showerror('Archivo no encontrado', ' El reproductor no encontro ninguna canción en la ruta. Por favor verificar nuevamente.')
                print("Error")

    def PausarCancion(self):            
        self.pausado = True
        if self.pausado: 
            self.ventana.after_cancel(self.des)
            pygame.mixer.music.pause()      


    def cierre(self):
        self.DetenerCancion()
        self.destroy()   

    def barra_volumen(val):
        volumen = int(val) / 100
        pygame.mixer.music.set_volume(volumen)


    def DetenerCancion(self):
        self.ventana.after_cancel(self.des)
        pygame.mixer.music.stop()
        
    def NextCancion(self): 
        if self.contador == ((self.cantidad)-1):
            self.contador = 0
        else:
            self.contador = (self.contador) + 1
        self.DetenerCancion()
        
        print("Reproducir por Next")
        self.ventana.after_cancel(self.des)
        self.ReproducirCancion()
    
    def PrevCancion(self):
        if self.contador == 0:
            self.contador = ((self.cantidad)-1)
        else:
            self.contador = (self.contador) - 1
        self.DetenerCancion()
        
        print("Reproducir por Prev")
        self.ventana.after_cancel(self.des)
        self.ReproducirCancion()
        
    def mostrar_detalles(self,reproducir_cancion):
        nombre_cancion = os.path.splitext(reproducir_cancion)
        if nombre_cancion[1] == '.mp3':
            audio = MP3(reproducir_cancion)
            Duracion_total = audio.info.length
        else:
            a = pygame.mixer.Sound(NextCancion)
            Duracion_total = a.get_length()   
        mins, secs = divmod(Duracion_total, 60)        
        mins1 = round(mins)
        secs1 = round(secs)  
        timeformat = '{:02d}:{:02d}'.format(mins1, secs1)
        #self.barra['text']= reproducir_cancion
        self.lengthlabel['text'] = "Duración total de la canción" + ' - ' + timeformat
        self.buscar_nombre()
        self.titulo_cancion['text'] = self.nombre_cancion_titulo
        t = (((60*mins1)+secs1)*1000) + 2000
        print(t)
        self.des = self.ventana.after(t, self.NextCancion)
        #t1 = threading.Thread(target=self.comenzar_conteo, args=(mins1,secs1))
        #t1.start()
        
          

    def buscar_nombre(self):
        nombre_cancion_aux = self.listaCanciones[self.contador]
        punto = nombre_cancion_aux.find('.')
        diagonal = nombre_cancion_aux.rfind('/') + 1
        self.nombre_cancion_titulo = self.listaCanciones[self.contador][diagonal:punto]

       
    def comenzar_conteo(self, minutos,segundos):
        current_time = 0
        t = (60*minutos)+segundos
        #print(t)
        while current_time <= t and pygame.mixer.music.get_busy():
            if self.pausado:
                continue
            else:
                #mins, secs = divmod(current_time, 60)
                #mins = round(mins)
                #secs = round(secs)
                time.sleep(1)
                current_time += 1
                #print(current_time)
        time.sleep(2)
        self.NextCancion()
        
      
        
        
        


class VentanaSecundaria(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        
        #busqueda de todas las imagenes en la memoria USB
        self.imagenes = buscar.buscar("imagen")
        #print(self.imagenes)
        #tamaño de la lista de imagenes
        self.cantidad = len( self.imagenes)
        self.contador = 0
        
        #dimencionar el tamaño de la ventana 
        super().__init__(*args, **kwargs)
        self.ventana = self
        self.width= self.winfo_screenwidth()
        self.height= self.winfo_screenheight() 
        
        #after nos ayuda a poner las fotos en modo presentación 
        self.des = self.ventana.after(5000, self.siguiente)

        #obtenemos dimenciones para las imagenes y para el tamaño de los botones
        self.imagenAnchuraMaxima=self.height-1000
        self.imagenAlturaMaxima=self.width-100
        self.tam_boton_x = int(self.height/8)
        self.tam_boton_y = self.tam_boton_x 
        
        #dimencionamos la ventana
        self.config(width=self.width, height= self.height)
        self.title("Ventana secundaria")
        
        #self.boton_cerrar = ttk.Button(self, text="Cerrar ventana", command=self.destroy)
        #self.boton_cerrar.place(x=0, y=0)
        
        #Contenedor label para la imagen 
        archivo_imagen =  self.imagenes[self.contador]    
        
        #abrimos el primer archivo
        self.img1=Image.open(archivo_imagen)
        self.img1.thumbnail((self.width,self.height))
        self.img1 = ImageTk.PhotoImage(self.img1,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        
        #creamos un label que contenga nuestras imagenes 
        self.label= tk.Label(self,image= self.img1)
        self.label.pack()
        self.label.place(relx=.5, rely=.5, anchor='center') #posición relativa centrada

        #Boton retroceder
        self.img_prev = Image.open('/home/pizano/Desktop/Proyecto/iconos/prev2.png').resize((self.tam_boton_x, self.tam_boton_y)) # Redimension (Alto, Ancho)
        self.img_prev = ImageTk.PhotoImage(self.img_prev,master=self)
        self.boton_prev = tk.Button(self, image=self.img_prev,height = (self.tam_boton_x+30), width = (self.tam_boton_y+50), compound="top",command=self.anterior)
        self.boton_prev.place(relx=.1, rely=.5, anchor='center')

        #Boton siguiente
        self.img_next = Image.open('/home/pizano/Desktop/Proyecto/iconos/next2.png').resize((self.tam_boton_x, self.tam_boton_y)) # Redimension (Alto, Ancho)
        self.img_next = ImageTk.PhotoImage(self.img_next,master=self)
        self.boton_next = tk.Button(self, image=self.img_next,height = (self.tam_boton_x+30), width = (self.tam_boton_y+50), compound="top",command=self.siguiente)
        self.boton_next.place(relx=.9, rely=.5, anchor='center')
        

        self.focus()
        self.grab_set()
        
    #cambiamos la imagen dependiendo del contador    
    def cambiarImagen(self):
        archivo_imagen = self.imagenes[self.contador]
        img = Image.open(archivo_imagen)
        img.thumbnail((self.width,self.height))
        tkimage = ImageTk.PhotoImage(img)      
        self.label.configure(image=tkimage)
        self.label.image=tkimage
    
    #movemos el contador a la siguiente imagen
    def siguiente(self):
        if self.contador == (self.cantidad-1):
            self.contador = 0
        else:
            self.contador = self.contador + 1
        self.cambiarImagen()
        self.ventana.after_cancel(self.des)
        self.des = self.ventana.after(5000, self.siguiente)
    
    #movemos el cantador a la anterior imagen
    def anterior(self):
        if self.contador == 0:
           self.contador = (self.cantidad-1)
        else:
            self.contador = self.contador - 1
        self.cambiarImagen() 
        self.ventana.after_cancel(self.des)
        self.des = self.ventana.after(5000, self.siguiente)
        

        
        
        
class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        #URL de nuestras paginas de streaming 
        self.streaming = {'Amazon_Video': ['/home/pizano/Desktop/Proyecto/iconos/Amazon_Video.png','https://www.primevideo.com/',0.1,0.25],
             'Netflix': ['/home/pizano/Desktop/Proyecto/iconos/Netflix.png','https://www.netflix.com/mx/',0.35,0.25],
             'Youtube': ['/home/pizano/Desktop/Proyecto/iconos/Youtube.png','https://www.youtube.com/',0.60,0.25],
             'Disney': ['/home/pizano/Desktop/Proyecto/iconos/Disney.png','https://www.disneyplus.com/es-mx',0.85,0.25],
             'Spotify': ['/home/pizano/Desktop/Proyecto/iconos/Spotify.png','https://open.spotify.com/',0.10,0.75],
             'Cloudflare': ['/home/pizano/Desktop/Proyecto/iconos/Cloudflare.png','https://www.cloudflare.com/es-es/',0.25,0.75],
             'unnamed': ['/home/pizano/Desktop/Proyecto/iconos/unnamed.png','https://www.deezer.com/mx/',0.40,0.75],
             'Multimedia': ['/home/pizano/Desktop/Proyecto/iconos/Multimedia.png','https://www.google.com/',0.75,0.75]
            }
        
        #dimencionamos nuestra ventana 
        super().__init__(*args, **kwargs)
        self.ventana = self
        #self.config(width=400, height=300)
        self.width1=  4096#self.winfo_screenwidth()  
        self.height1=  2160#self.winfo_screenheight()
        print(self.width1,self.height1)
        self.tam_boton_x = int(self.height1/4)
        self.tam_boton_y = int(self.height1/4)
        #print("ventana/boton"+str(self.height1/200))
  
        self.title("PAGINA PRINCIPAL")
        self['bg'] = '#000'
        # self.geometry('300x200')
        # self.attributes('-fullscreen', True) 
        # self.geometry("960x600")
        # self.overrideredirect(True) 
         
        self.geometry("%dx%d" % (self.width1, self.height1))
        
        ##Boton para Amazon video
        self.img1=Image.open(self.streaming['Amazon_Video'][0]).resize((self.tam_boton_x, self.tam_boton_y))
        self.img1 = ImageTk.PhotoImage(self.img1,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton1 = tk.Button(self, image=self.img1,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"Amazon_Video"))#command= lambda:self.pagina_Web("Amazon_Video"))
        self.boton1.place(relx=.1, rely=.25, anchor='center')
        
        ##Boton para Netflix
        self.img2=Image.open(self.streaming['Netflix'][0]).resize((self.tam_boton_x, self.tam_boton_y))
        self.img2 = ImageTk.PhotoImage(self.img2,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton2 = tk.Button(self, image=self.img2,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"Netflix"))
        self.boton2.place(relx=.35, rely=.25, anchor='center')
        
        ##Boton para Youtube
        self.img3=Image.open(self.streaming['Youtube'][0]).resize((self.tam_boton_x, self.tam_boton_y))
        self.img3 = ImageTk.PhotoImage(self.img3,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton3 = tk.Button(self, image=self.img3,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"Youtube"))
        self.boton3.place(relx=.60, rely=.25, anchor='center')
        
        ##Boton para Disney
        self.img4=Image.open(self.streaming['Disney'][0]).resize((self.tam_boton_x, self.tam_boton_y))
        self.img4 = ImageTk.PhotoImage(self.img4,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton4 = tk.Button(self, image=self.img4,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"Disney"))
        self.boton4.place(relx=.85, rely=.25, anchor='center')
        
        
        
        #self.tam_boton_x = 150
        #self.tam_boton_y = 150
        
        ##Boton para Spotify
        self.img6=Image.open(self.streaming['Spotify'][0]).resize((self.tam_boton_x, self.tam_boton_y))
        self.img6 = ImageTk.PhotoImage(self.img6,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton6 = tk.Button(self, image=self.img6,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"Spotify"))
        self.boton6.place(relx=.10, rely=.75, anchor='center')
        
        '''
        self.img7=Image.open('/home/pizano/Desktop/Proyecto/iconos/Amazon_Video.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.img7 = ImageTk.PhotoImage(self.img7,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton7 = tk.Button(self, image=self.img7,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"Amazon_Video"))
        self.boton7.place(relx=.25, rely=.75, anchor='center')
        '''
        ##Boton para unnamed
        self.img8=Image.open(self.streaming['unnamed'][0]).resize((self.tam_boton_x, self.tam_boton_y))
        self.img8 = ImageTk.PhotoImage(self.img8,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton8 = tk.Button(self, image=self.img8,height = self.tam_boton_x, width = self.tam_boton_y,command=partial(self.pagina_Web,"unnamed"))
        self.boton8.place(relx=.40, rely=.75, anchor='center')
        
        self.tam_boton_x = int(self.tam_boton_x/2)
        self.tam_boton_y = int(self.tam_boton_y/2)
        
        ##Boton para Reproductor de musica
        self.img9=Image.open('/home/pizano/Desktop/Proyecto/iconos/Musica.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.img9 = ImageTk.PhotoImage(self.img9,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton9 = tk.Button(self, image=self.img9,height = self.tam_boton_x, width = self.tam_boton_y,command=self.abrir_ventana_musica)
        self.boton9.place(relx=.60, rely=.75, anchor='center')
        
        ##Boton para Reproductor de video 
        self.img10=Image.open('/home/pizano/Desktop/Proyecto/iconos/Video.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.img10 = ImageTk.PhotoImage(self.img10,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton10 = tk.Button(self, image=self.img10,height = self.tam_boton_x, width = self.tam_boton_y,command=self.abrir_ventana_videos)
        self.boton10.place(relx=.75, rely=.75, anchor='center')
        
        ##Boton para Imagen
        self.img11=Image.open('/home/pizano/Desktop/Proyecto/iconos/Imagen.png').resize((self.tam_boton_x, self.tam_boton_y))
        self.img11 = ImageTk.PhotoImage(self.img11,master=self)#se utiliza el master para corregir el error de seleccionar una photo random
        self.boton11 = tk.Button(self, image=self.img11,height = self.tam_boton_x, width = self.tam_boton_y,command=self.abrir_ventana_imagenes)
        self.boton11.place(relx=.90, rely=.75, anchor='center')
        self.des = self.ventana.after(500, self.estadoBotones)
        #self.estadoBotones()
        
    #funciones para abrir las diferentes ventanas
    def abrir_ventana_imagenes(self):
        #self.ventana.after_cancel(self.des)
        self.ventana_secundaria = VentanaSecundaria()
    
    def abrir_ventana_musica(self):
        #self.ventana.after_cancel(self.des)
        self.VentanaMusica = VentanaMusica()
        
    def abrir_ventana_videos(self):
        #self.ventana.after_cancel(self.des)
        self.ventanaVideo = Ventanavideo()
                
    def estadoBotones(self):
        global memoria
        global memoria_antes
        tipos_bool = buscar.contenidos()
        print(tipos_bool)
        #activamos o no los botones multimedia si existe una USB conectada 
        #y si esta tiene alguno de estos archivos
        if (tipos_bool["sonido"] == False):
            self.boton9['state'] = tk.DISABLED
        else:
            self.boton9['state'] = tk.NORMAL
            
        if (tipos_bool["video"] == False):
            self.boton10['state'] = tk.DISABLED
        else:
            self.boton10['state'] = tk.NORMAL
            
        if (tipos_bool["imagen"] == False):
            self.boton11['state'] = tk.DISABLED
        else:
            self.boton11['state'] = tk.NORMAL
        #print("memoria:"+memoria+" memoria antes:"+memoria_antes)
        #verificamos si una memoria USB fue conectada
        if (memoria_antes!=memoria):
            memoria_antes = memoria
            #print("memoria:"+memoria+" memoria antes:"+memoria_antes)
            if (tipos_bool["sonido"] == True and tipos_bool["video"] == False and tipos_bool["imagen"] == False):
                self.abrir_ventana_musica()
            if (tipos_bool["sonido"] == False and tipos_bool["video"] == True and tipos_bool["imagen"] == False):
                self.abrir_ventana_videos()
            if (tipos_bool["sonido"] == False and tipos_bool["video"] == False and tipos_bool["imagen"] == True):
                print("_AQUI")
                self.abrir_ventana_imagenes()
            if (tipos_bool["sonido"] == True or tipos_bool["video"] == True or tipos_bool["imagen"] == True):
                print("HOLA")
                #showinfo(message="Se activaron los botones con contenido multimedia", title="USB insertada")
        #despues de 3 segundos verificamos el estado de los botones   
        self.des = self.ventana.after(3000, self.estadoBotones)
        
        
        
        
    def WEB2(url):
        cmd = "chromium --kiosk --app="+url
        os.system(cmd)
    
    #abrir paginas web   
    def pagina_Web(self,nombre):
        '''cmd = "chromium --kiosk --app="+self.streaming[nombre][1]
        #cmd = "/user/bin/chromium-browser --start--fullscream www.google.de"
        os.system(cmd)'''

        
        try:
            webbrowser.get("chromium").open_new(self.streaming[nombre][1])
        except:
            webbrowser.open(self.streaming[nombre][1],new=1,autoraise=True)
        #time.sleep(6)
        #pyautogui.click()
        time.sleep(8)
        pyautogui.hotkey("f11") # ponemos en Full screen el navegador 
        '''

        print(nombre) 
        window = webview.create_window('Geeks for Geeks', self.streaming[nombre][1],fullscreen=False) 
        webview.start()'''
    
    def imprimir():
        print("HOLA")
        



def ventanas():
    ventana_principal = VentanaPrincipal()
    while ventana_cerrar: #modificar al cerrar pestañas
        if os.name != 'nt':
            cursor.mover()
        #sustitutos de main.loop()    
        ventana_principal.update_idletasks()
        ventana_principal.update()

def USB():
    global memoria
    if os.name == 'nt': #sistema Windows
        while ventana_cerrar:
            print("Hola") 
    else:
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')
        while ventana_cerrar:            
            for device in iter(monitor.poll, None):
                if 'ID_FS_TYPE' in device:
                    memoria = device.action #si la memoria se inserta o quita
                    print('{0} partition {1}'.format(device.action, device.get('ID_FS_LABEL')))
                

#hilo para las ventanas
t1 = threading.Thread(target=ventanas)
t1.start()
#hilo para reconocer la inserción de una USB
t2 = threading.Thread(target=USB)
t2.start()