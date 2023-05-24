import pygame
from pygame.locals import *
from pynput import keyboard as kb
import cv2
import os
#from keytime import time
#from keytime import timekey
import lock

# Variables globales
# ------------------
props_dict = {}
timekey=[]  


def time(tecla):
    if tecla:
            timekey.append(pygame.time.get_ticks())
            if len(timekey) >= 5: 
                return False


def init(props):
    global props_dict
    print("Python: Enter in init")

    # Props es un diccionario
    props_dict = props
    resultado = executeChallenge()
    if (resultado[1]>0):
        return 0
    else:
        return -1



def executeChallenge():
    print("Python: Enter in  executeChallenge")
    pygame.init()
    
    timekey.clear()
    kb.Listener(time).run()

    
    # Mecanismo de lock BEGIN
    # -----------------------
    lock.lockIN("Reco_Facial_Ks")
    
    if ((timekey[4]-timekey[3])<1000):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        
    else:
         # Mecanismo de lock END
         #----------------------
         lock.lockOUT("Reco_Facial_Ks")
         key_size = 0
         result =(NULL, key_size)
         print ("result:",result)
         
         return result
    
    
    print("Starting execute")
    #for key in os.environ: print(key, ':', os.environ[key])
    dataPath = os.environ['SECUREMIRROR_CAPTURES']

    print ("storage folder is :",dataPath)

    #dataPath = 'B:/Doctorado/Challenges/Data' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath + "/" + "Data")
    print('imagePaths=', imagePaths)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Leyendo el modelo
    face_recognizer.read(dataPath+ "/" + 'modeloLBPHFace.xml')

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    print("MODELO LEÍDO")

    res=0

    try:
        ret,frame = cap.read()
    except:
        print("CHALLENGE_RECO_FACIAL_KS --> Error: cannot get frame from camera")
        result = (NULL, key_size)
        print("CHALLENGE_RECO_FACIAL --> result:", result)
        return result

    if ret == False:
        cap.release()
        cv2.destroyAllWindows()
        lock.lockOUT("Reco_Facial_KS")
        key_size = 0
        result = (NULL, key_size)
        print("CHALLENGE_RECO_FACIAL_KS --> result:", result)
        return result

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)
    auxFrame = gray.copy()
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)
        cv2.putText(frame, '{}'.format(result), (x,y-5), 1, 1.3, (255,255,0), 1, cv2.LINE_AA)
        print(result)

        # LBPHFace
        if result[1] > 0 and result[1] <= 70:
            cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x,y-25), 2, 1.1, (0,255,0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.imshow('frame', frame)
            #cv2.waitKey(0) #Se comenta para que la ventana cierre automáticamente
            res = result[1]
            #print(resultado)
        elif result[1] <= 0 or result[1] > 70:
            cv2.putText(frame, 'Desconocido', (x,y-20), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
            cv2.imshow('frame', frame)
            #cv2.waitKey(0) #Se comenta para que la ventana cierre automáticamente
            res = result[1]

    #cierre 
    #cv2.destroyAllWindows() #Se comenta para que se vea la imagen antes de cerrar la ventana de reconocimiento


    # Mecanismo de lock END
    #----------------------
    lock.lockOUT("Reco_Facial_Ks")

    # Get the mode from the properties dictionary (global variable)
    mode = props_dict["mode"]

    # Construcción de la respuesta
    if mode == "parental":
        if res > 0 and res <= 70:   resp= 1
        else: 
                                    resp= 0
        
    else:   # Modo no parental
        
        if res<=0:                  resp = 0
        elif res>0 and res<=70:     resp = 1
        elif res>70 and res<=75:    resp = 2
        elif res>75 and res<=80:    resp = 3
        elif res>80 and res<=85:    resp = 4
        elif res>85 and res<=90:    resp = 5
        elif res>90 and res<=95:    resp = 6
        elif res>95 and res<=100:   resp = 7
        elif res>100 and res<=105:  resp = 8
        elif res>105 and res<=110:  resp = 9
        elif res>110 and res<=115:  resp = 10
        elif res>115 and res<=120:  resp = 11
        elif res>120:               resp = 12

   


    cad = "%d"%(resp)
    key = bytes(cad, 'utf-8')
    key_size = len(key)
    result = (key, key_size)
    print("result:", result)
    return result


if __name__ == "__main__":
    midict = {"mode": "normal"}
    print(init(midict))
    #executeChallenge()
