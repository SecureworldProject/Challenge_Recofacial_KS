# Challenge_Recofacial_KS
ChallengeMM recognized by a regular user with low level of intrusion

# DESCRIPCION y FIABILIDAD:
Reco_Facial_KS es un challenge multimedia que cuenta con dos modos de funcionamiento: 
1. Modo Parental, comprueba que el usuario es una persona adulta con la que se ha entrenado el modelo previamente.
2. Modo no parental, comprueba si el usuario es un usuario habitual (empleado de la empresa), lo hace mediante
reconocimiento facial, resultando 1 si es un usuario habitual, sino puede dar valores de 0 (si el challenge 
no se ejecuta por falta de cámara del pc, o si no detecta ningún rostro en la captura),
también puede dar valores de 2 a 12 si el rostro detectado es desconocido, alcanzando una cardinalidad igual a 13. Este challenge
tiene una fiabilidad alta porque el usuario debe precionar 5 teclas con un tiempo mínimo de diferencia entre ellas para que se capture 
la imagen, con el objetivo de intentar garantizar que el usuario no pueda presentar una foto a la cámara haciendo que tenga las manos ocupadas.
Este challenlle se ejecutará sin tener interacción con el usuario, o sea, de forma silenciosa en el tiempo establecido para su ejecución previamente.
Esperará que el usuario tecleé y luego de teclear 5 teclas tomará la foto por la webcam. 

# FUNCIONAMIENTO:
Este challenge requiere un proceso inicial de entrenamiento del modelo, esto se hace con el archivo crear_BD.py, donde se realiza
una captura de un video en streaming si el usuario cuenta con webcam en el pc. Se capturan 300 fotos y se almacenan en una carpeta 
con el nombre del usuario, para con estas entrenar el modelo de machine learning (LBPHFaceRecognizer) y almacenarlo.

El challenge se encuentra en el fichero Reco_Facial_KS.py donde se toma una captura después que el usuario presiona 5 teclas seguidas y 
se pasa al modelo almacenado, devolviendo este un parámetro de nivel de confianza que estará entre 0 y 70 si es un usuario conocido por el modelo. 
Retornando 1 si el valor de confianza está en ese rango. La clave resultante para el modo parental será 0 ó 1, y en el modo no parental
estará desde 0 hasta 12, siendo 1 el valor correcto en ambos casos. 

#Modelos de IA de opencv para reconocimiento Facial:
https://docs.opencv.org/4.2.0/da/d60/tutorial_face_main.html#tutorial_face_eigenfaces

Modelo utilizado: LBPHFaceRecognizer
https://docs.opencv.org/3.4/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html

# REQUISITOS:
Tener cámara en pc. 
Entrenar el modelo antes de usar el challenge, en el lugar de trabajo habitual y con la iluminación habitual. 

La variable de entorno SECUREMIRROR_CAPTURES debe existir.

Librerías utilizadas:
pygame para obtener el tiempo entre la pulsación de una y otra tecla.
pynput para controlar/escuchar las pulsaciones en el teclado. https://pypi.org/project/pynput/

Opencv para extraer información de videos tanto en streaming como almacenados y modelos de IA para reconocimiento facial.    
https://www.geeksforgeeks.org/opencv-python-tutorial

para instalar la libreria openCV simplemente:

pip3 install opencv-python

IMPORTANTE Si se muestra el  error: AttributeError: module 'cv2' has no attribute 'face' hacer lo siguiente:
pip install opencv-contrib-python

IMPORTANTE: tras instalar opencv, la dll python3.dll de instalacion de python cambia, debes darle acceso al programa que haga uso de este challenge ubicandola en un directorio al que pueda acceder

para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial

# Configuración para validar el challenge:

El valor del campo "FileName" debe ser "challenge_loader_python.dll". Dentro del campo "Props" debe haber varios pares clave-valor:

"module_python": Debe contener el nombre del archivo del módulo de python  (sin incluir ".py"). En este caso: "Reco_Facial".

"validity_time": el tiempo de validez del challenge en segundos (entero).

"refresh_time": el tiempo en segundos (entero) entre ejecuciones automáticas del challenge.

"modo": determina el modo de ejecución. El modo parental se selecciona si su valor es "parental". De lo contrario, se utiliza el modo no parental.

Otros campos como "Description" y "Requirements" son opcionales e informativos.

# EJEMPLO:
Ejemplo de configuración del challenge para el modo parental:

{ 	"FileName": "challenge_loader_python.dll",
	
	"Props": {
		"module_python": "Reco_Facial_KS",
		"validity_time": 3600,
		"refresh_time": 3000,
		"mode": "parental",
		
	},
	"Requirements": "webcam"
}

A continuación se presenta una configuración en modo no parental, para el caso de uso en empresas. 

{	"FileName": "challenge_loader_python.dll",
	
	"Props": {
		"module_python": "Reco_Facial_KS",
		"validity_time": 3600,
		"refresh_time": 3000,
		"mode": "normal",
		
	},
	"Requirements": "webcam"
}


