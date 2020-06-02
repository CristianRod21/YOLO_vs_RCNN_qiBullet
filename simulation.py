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

import pybullet
import pybullet_data
import time
from qibullet import SimulationManager
from qibullet import NaoVirtual
from qibullet import PepperVirtual
from qibullet import RomeoVirtual

def rotate(pepper):
    pepper.move(0, 0, 0.5)
    # time.sleep(0.1745)
    # pepper.move(0,0,0)

cap = cv2.VideoCapture('dang.mp4')
#fps = int(cap.get(60))

host = socket.gethostname()
port = 45678                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


shm = None


sim_manager = SimulationManager()
client = sim_manager.launchSimulation(gui=True)
# client_direct_1 = sim_manager.launchSimulation(gui=False)

pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
print(pybullet_data.getDataPath())
pybullet.loadURDF('plane.urdf')

table = pybullet.loadURDF('table/table.urdf',
         basePosition= [0.5,2,0],
     physicsClientId=client)

item_in_table = pybullet.loadURDF('teddy_vhacd.urdf',
    basePosition= [0.5,2,1],
    globalScaling = 5.0,
    physicsClientId=client)

item_in_table2 = pybullet.loadURDF('bicycle/bike.urdf',
     basePosition= [0.5,2.5,1],
     globalScaling = 0.7,
     physicsClientId=client)

    

#walls2 = pybullet.loadURDF('C:\\Users\\cjrs2\\Downloads\\keras-yolo3\\proyecto_robo\\walls2.urdf',
#     physicsClientId=client)


# nao = sim_manager.spawnNao(
#    client,
#    translation=[0.5,2,1],
#    quaternion=pybullet.getQuaternionFromEuler([0, 0, 3]))
pepper = sim_manager.spawnPepper(
    client,
    translation=[0, -2, 0],
    quaternion=pybullet.getQuaternionFromEuler([0, 0, 1.5]))


#  nao.goToPosture('StandInit', 1)
pepper.goToPosture("Stand", 1)

#  nao.setAngles('HeadPitch', 0.25, 1)    
handle = pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP )
print('Retriving camera frame')
#x = 0
frames = 0

valid_object, object_to_find = find_word.find_word(input("¿Qué objeto desea encontrar?"))
not_found = True

if valid_object:
    while(not_found):
        rotate(pepper)
        t = None
        frame = pepper.getCameraFrame(handle)
        if frames == 0:
            print('Sending initial informantion')
            shm = shared_memory.SharedMemory(create=True, size=frame.nbytes) # name='image_random'
            data=json.dumps({"shape": frame.shape, "name": shm.name, "type": frame.dtype.name})
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
        found_classes = json.loads(t.decode())
        found_classes = found_classes.get("found_objects")

        if(object_to_find in found_classes):
            not_found = False

        frames += 1

    pepper.move(0, 0, 0.5)
    time.sleep(0.1745)
    pepper.move(0,0,0)
    pepper.move(2,0,0)
    time.sleep(4)
    pepper.move(0,0,0)

    # rotate(pepper)
    print("Aquí está el " + object_to_find)
else:
    print("No sé qué es ese objeto")

input("Cualquier tecla para salir")

pepper.unsubscribeCamera(handle)
shm.close() 
shm.unlink()

cap.release()
cv2.destroyAllWindows()


