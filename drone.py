import os 
from time import sleep


os.system("bash start_tello.sh")
sleep(1)
os.system("bash tello_takeoff.sh")


