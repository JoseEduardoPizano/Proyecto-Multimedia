#Pizano Pérez José Eduardo
import os

# Condicional que nos indica el SO en el que nos encontramos
url = ''
if os.name == 'nt': #sistema Windows
    url = 'C:/Users/lalop/OneDrive/Escritorio/Proyecto'
elif os.name == 'nt': #sistemas POSIX y distribuciones de Linux
    url = ''
else:
    url = '/media/pizano'

#extensiones por tipo
tipo = {
    "imagen":["jpeg","jpg","png","gif","rgb","pbm","pgm","ppm","tiff","rast","xbm","bmp","webp"],
    "sonido":["mp3","acc","wma","rec","wav","cda"],
    "video": ["mp4","mpeg","wmm","3gp","avi"]#,"vcd","svcd"]
}


#busqueda en carpeta principal y subcarpetas de la memoria
def buscar(formato):
    archivos = []
    for carpeta in os.walk(url):
        #print(f'En {carpeta[0]} tenemos {len(carpeta[2])} ficheros:')
        for fichero in carpeta[2]:
            #print(f' - {fichero}')
            for t in tipo[formato]:
                if fichero.endswith(t):
                    archivos.append(carpeta[0].replace("\\", "/")+'/'+fichero)
                    break
    return archivos   
    
#Si encuentra al menos un archivo nos indica que existe y se sale de la función     
def contenido(formato):
    archivos = []
    for carpeta in os.walk(url):
        for fichero in carpeta[2]:
            for t in tipo[formato]:
                if fichero.endswith(t):
                    #if ("video"==formato):
                        #print(carpeta[0]+fichero)
                    return True
    return False
#verifica la existencia de los tres tipos de archivos, 
#si es False entonces no existe ningun archivo si es True almenos tenemos un archivo
def contenidos():
    tipos_bool= {"sonido":False,"imagen":False,"video":False}
    tipos_bool["imagen"] = contenido("imagen")
    tipos_bool["sonido"] = contenido("sonido")
    tipos_bool["video"]  = contenido("video")
    return tipos_bool
    
if __name__ == '__main__':
    print(buscar("imagen"))