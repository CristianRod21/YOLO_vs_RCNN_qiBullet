
from npsocket import SocketNumpyArray
import cv2
import sys
import pybullet
import pybullet_data
import time
from qibullet import SimulationManager
from qibullet import NaoVirtual
from qibullet import PepperVirtual
from qibullet import RomeoVirtual

import time

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


sock_sender = SocketNumpyArray()
sock_sender.initialize_sender('localhost', 9995)

#  nao.setAngles('HeadPitch', 0.25, 1)    
handle = pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP )

print('Retriving camera frame')
#x = 0
frames = 0
# while True:
while True:
	start_time = time.time()
	frame = pepper.getCameraFrame(handle)
	print('sending frame')
	sock_sender.send_numpy_array(frame)
pepper.unsuscribeCamera(PepperVirtual.ID_CAMERA_TOP)
