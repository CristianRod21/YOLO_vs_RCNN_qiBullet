import cv2
import numpy as np
from multiprocessing import shared_memory
import cv2
import socket
import json
from sys import getsizeof

import find_word

import sys
import time
import os

import pybullet
import pybullet_data
import time
from qibullet import SimulationManager
from qibullet import NaoVirtual
from qibullet import PepperVirtual
from qibullet import RomeoVirtual
from gtts import gTTS 
from playsound import playsound
from enum import Enum


X_MIN = 0
Y_MIN = 1
X_MAX = 2
Y_MAX = 3
 


def rotate(pepper):
    pepper.move(0, 0, 0.5)
    # time.sleep(0.1745)
    # pepper.move(0,0,0)

 

def reading_from_string(text_to_read, filename, language='es', slow_audio_speed=False):
    audio_created = gTTS(text=text_to_read, lang=language,
                         slow=slow_audio_speed)
    audio_created.save(filename)
    playsound(filename)
    os.remove(filename)


cap = cv2.VideoCapture('dang.mp4')
#fps = int(cap.get(60))

host = socket.gethostname()
port = 45678                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

language = 'es'
shm = None


#Starting index
object_filename = "object.mp3"
filename = "speech.mp3"

sim_manager = SimulationManager()
client = sim_manager.launchSimulation(gui=True)
# client_direct_1 = sim_manager.launchSimulation(gui=False)

pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
print(pybullet_data.getDataPath())
f_plane = pybullet.loadURDF('plane.urdf')
textUid = pybullet.loadTexture('enviroment/wood.png')
pybullet.changeVisualShape(f_plane, -1, textureUniqueId=textUid)



plane = pybullet.loadURDF('enviroment/room.urdf', globalScaling=3, basePosition=[0,0,-7])
texUid = pybullet.loadTexture("enviroment/wall_2.png")
pybullet.changeVisualShape(plane, -1, textureUniqueId=texUid)


table = pybullet.loadURDF('table/table.urdf',
 basePosition= [0,5,0],
physicsClientId=client)
table_2 = pybullet.loadURDF('table/table.urdf',
 basePosition= [5,0,0],
 baseOrientation=pybullet.getQuaternionFromEuler([0, 0, 1.5]),
 physicsClientId=client)
table_3 = pybullet.loadURDF('table/table.urdf',
 basePosition= [-5,0,0],
 baseOrientation=pybullet.getQuaternionFromEuler([0, 0, -1.5]),
 physicsClientId=client)
table_4 = pybullet.loadURDF('table/table.urdf',
 basePosition= [0,-5,0],
 physicsClientId=client)


item_in_table_1 = pybullet.loadURDF('enviroment/water_bottle.urdf',
    basePosition= [-0.5,5,0.6],
    globalScaling = 3.0,
    physicsClientId=client)

item_in_table_1 = pybullet.loadURDF('teddy_vhacd.urdf',
basePosition= [0,5,0.6],
globalScaling = 6.0,
 baseOrientation=pybullet.getQuaternionFromEuler([2,0 , 0]),
physicsClientId=client)


item_in_table2 =  pybullet.loadURDF('enviroment/laptop.urdf',
    basePosition= [-5,0,0.7],
    baseOrientation=pybullet.getQuaternionFromEuler([2, 0, 3]),
    globalScaling = 3.5,
    physicsClientId=client)

item_in_table3 =  pybullet.loadURDF('enviroment/knife.urdf',
    basePosition= [0,-5,0.7],
    baseOrientation=pybullet.getQuaternionFromEuler([2, 0, 3]),
    globalScaling = 0.1,
    physicsClientId=client)


item_in_table4 =  pybullet.loadURDF('enviroment/cat.urdf',
    basePosition= [5,0,0.7],
    baseOrientation=pybullet.getQuaternionFromEuler([0, 0, -1.5]),
    globalScaling = 0.3,
    physicsClientId=client)
    

#walls2 = pybullet.loadURDF('C:\\Users\\cjrs2\\Downloads\\keras-yolo3\\proyecto_robo\\walls2.urdf',
#     physicsClientId=client)


# nao = sim_manager.spawnNao(
#    client,
#    translation=[0.5,2,1],
#    quaternion=pybullet.getQuaternionFromEuler([0, 0, 3]))
pepper = sim_manager.spawnPepper(
    client,
    translation=[0, 0, 0],
    quaternion=pybullet.getQuaternionFromEuler([0, 0, 1.5]))


#  nao.goToPosture('StandInit', 1)
pepper.goToPosture("Stand", 1)



#  nao.setAngles('HeadPitch', 0.25, 1)    
handle = pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP )
print('Retriving camera frame')
resolution = pepper.getCameraResolution(handle)
#print("Resolution: " + str(resolution.width) + "x" + str(resolution.height))
mid_frame = resolution.width / 2
#x = 0
frames = 0


text_to_read = "¿Qué objeto desea encontrar?"
reading_from_string(text_to_read, object_filename)
original_text = input(text_to_read)
valid_object, object_to_find = find_word.find_word(original_text)
object_found = False
coords = []
if valid_object:
    while(not(object_found)):
        t = None
        frame = pepper.getCameraFrame(handle)
        if frames == 0:
            print('Sending initial informantion')
            shm = shared_memory.SharedMemory(create=True, size=frame.nbytes) # name='image_random'
            data=json.dumps({"shape": frame.shape, "name": shm.name, "type": frame.dtype.name, "object":object_to_find})
            s.send(data.encode())
            
            #data = s.recv(1024)
            #s.close()
            #print('Received', data)
        # Now create a NumPy array backed by shared memory
        b = np.ndarray(frame.shape, dtype=frame.dtype, buffer=shm.buf)
        b[:] = frame[:]  # Copy the original data into shared memory
        print('Sending')
        s.send(bytes("1",'utf8'))
        t = s.recv(1024)
        found_info = json.loads(t.decode())
        object_found = found_info.get("was_found")
        if object_found:
            coords = found_info.get("coords")
            right_distance_from_middle = abs(coords[X_MAX] - mid_frame)
            left_distance_from_middle = abs(coords[X_MIN] - mid_frame)
            # Este 20 es solo un threshold para que se posicione como debe, se puede cambiar si parece que no está bien
            if abs(right_distance_from_middle - left_distance_from_middle) > 20:
                object_found = False

        frames += 1
        rotate(pepper)

    print(coords)
    width = coords[ X_MAX ]  - coords[ X_MIN ]
    height = coords[ Y_MAX ] - coords[ Y_MIN]

    # https://github.com/paul-pias/Object-Detection-and-Distance-Measurement
    distance = ((2 * 3.14 * 180) / (width + height * 360) * 1000 + 3) /39.37

    print("El objeto se encuentra a una distancia de " + str(distance))
    pepper_speed = 1

    movement_time = (distance/pepper_speed) * 5

    print("Voy a caminar por " + str(movement_time) + "s")
    pepper.move(pepper_speed, 0, 0)
    print("Voy a caminar, miher")
    time.sleep(movement_time)
    print("A mimir")
    pepper.move(0,0,0)
    current_angle = pepper.getAnglesPosition(['RShoulderPitch'])
    # print("Mi brazo derecho está en " + str(current_angle))

    # rotate(pepper)
    pepper.setAngles('RShoulderPitch', 2.08 - current_angle, 1)
    text_to_read = "Aquí está el " + original_text
    reading_from_string(text_to_read, filename)
    print(text_to_read)
else:
    text_to_read = "No sé qué es ese objeto"
    reading_from_string(text_to_read, filename)
    print(text_to_read)

input("Cualquier tecla para salir")

pepper.unsubscribeCamera(handle)
shm.close() 
shm.unlink()

cap.release()
cv2.destroyAllWindows()


