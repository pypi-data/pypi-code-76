import numpy as np
import cv2
from matplotlib import pyplot as plt

def mostrar_imagen(arreglo_bidimensional, titulo_de_ventana=None):
    if not titulo_de_ventana:
        titulo_de_ventana = "%dx%d" % arreglo_bidimensional.shape[:2]

    assert isinstance(titulo_de_ventana, str)

    arreglo_bidimensional = arreglo_bidimensional.astype('uint8')
    cv2.imshow(titulo_de_ventana, arreglo_bidimensional)

    while cv2.getWindowProperty(titulo_de_ventana,
                                cv2.WND_PROP_VISIBLE) >= 1:
        if cv2.waitKeyEx(1000) == 27:
            cv2.destroyWindow(titulo_de_ventana)
            break

def guardar_imagen(arreglo_bidimensional, ruta_de_salida="../salida.png"):

    # Pasa encima de cualquier otro formato, xq si
    if not ruta_de_salida.endswith(".png"):
        ruta_de_salida += ".png"

    cv2.imwrite(ruta_de_salida, arreglo_bidimensional)
    return True

