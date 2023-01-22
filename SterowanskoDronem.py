from multiprocessing.process import current_process
import numpy as np
import os
import rclpy
from numpy.distutils.command.config import config
from rclpy.node import Node
from std_msgs.msg import  String
from geometry_msgs.msg import Twist
import  time

class SterowanieDronem(Node):
	subscription = None
	def __init__(self):
		super().__init__('SterowanskoDronem')
		self.subscription = self.create_subscription(String,
		'/Pileczka', self.Sterowanie_callback, 1)
		self.subscription
		self.count_rotate_CW=0
		self.count_rotate_STOP=0
		self.ball_was_seen = 0
		self.land  = 0
		self.golower = 0
		self.count_go_stop = 0
		#os.system("bash tello_Go_LOWER.sh")
		#time.sleep(2)
		self.was_spining_CW = 0
		self.was_spining_CCW = 0
		self.start = 1

	def Sterowanie_callback(self, msg):

		mes_w = msg.data.index('w')
		mes_x = msg.data.index('x')
		mes_y = msg.data.index('y')
		x = int(msg.data[mes_x+1:mes_y])
		y = int(msg.data[mes_y+1:mes_w])
		area_wall = int(msg.data[mes_w + 1:len(msg.data)])
		area = int(msg.data[1:mes_x])
		self.get_logger().info('I heard: %d %d %d %d' % (area, x,y,area_wall))
		print("Start %d"%(self.start))
		if area > 0:
			self.ball_was_seen = 1
		else:
			self.ball_was_seen = 0
		if self.ball_was_seen == 0:
			print(self.ball_was_seen)
			if self.count_go_stop == 0:
				if area_wall > 39*1000:
					self.count_go_stop += 1

					#os.system("bash tello_Rotate_STOP.sh")
					os.system("ros2 topic pub --once /drone1/cmd_vel geometry_msgs/msg/Twist \"{linear: {x: 0.05, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}\"")
					###### Pytanie czy przechodzimy na te komendy na stalo ???????
					time.sleep(2)
					#os.system("bash tello_Go_FORWARD.sh")
					os.system("ros2 topic pub --once /drone1/cmd_vel geometry_msgs/msg/Twist \"{linear: {x: 0.05, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}\"")


			if self.was_spining_CW == 0 and self.start ==1:
				if area_wall < 34*1000:
					#self.was_spining_CW +=1
					self.was_spining_CCW = 0
					self.count_go_stop = 0
					os.system("bash tello_Go_STOP.sh")
					time.sleep(1)
					os.system("bash tello_Rotate_CW.sh")

			if self.was_spining_CCW == 0 and self.start ==0:
					if area_wall < 34*1000:
						self.was_spining_CCW +=1
						self.was_spining_CW =0
						self.count_go_stop = 0
						os.system("bash tello_Go_STOP.sh")
						time.sleep(1)
						os.system("bash tello_Rotate_CCW.sh")
		else:
			print(self.ball_was_seen)
			if self.land == 0:
				if (self.golower == 0):
					print("Lece bo chce")
					os.system("bash tello_Go_LOWER.sh")

					os.system("bash tello_Rotate_STOP.sh")
					self.golower += 1
					#if area_wall > 39*1000:
					#	os.system("bash tello_Go_FORWARD.sh")
						#if area > 700:
						#	os.system("bash tello_Rotate_STOP.sh")
						#	os.system("bash tello_land.sh")


					"""				if area > 0 and self.count_rotate_STOP == 0:
										self.count_rotate_STOP += 1
										self.count_rotate_CW = 0
										os.system("bash tello_Rotate_STOP.sh")
										os.system("bash tello_Go_FORWARD.sh")
									if x > 450 and x < 500:
										os.system("bash tello_Go_FORWARD.sh")
										os.system("bash tello_Rotate_STOP.sh")
										if area == 0:
											os.system("bash tello_land.sh")
									if x < 440 and self.count_rotate_CW == 0:
										self.count_rotate_STOP = 0
										self.count_rotate_CW += 1
										os.system("bash tello_Rotate_CW.sh")
										os.system("bash tello_Rotate_STOP.sh")
									if x > 520 and self.count_rotate_CCW == 0:
										self.count_rotate_STOP = 0
										self.count_rotate_CCW += 1
										os.system("bash tello_Rotate_CCW.sh")
										os.system("bash tello_Rotate_STOP.sh")"""


					#elif self.ball_was_seen == 1:
					#	self.ball_was_seen = 0
					#	os.system("bash tello_Go_STOP.sh")
					#	time.sleep(1)
					#	os.system("bash tello_land.sh")
					#	self.land = 1


def main(args=None):
	rclpy.init()
	SD = SterowanieDronem()
	rclpy.spin(SD)
	SD.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()

"""if self.land == 0:
	if area > 0 and self.count_rotate_STOP==0:
		self.count_rotate_STOP += 1
		self.count_rotate_CW = 0
		os.system("bash tello_Rotate_STOP.sh")
		os.system("bash tello_Go_FORWARD.sh")
		if(self.golower==0):
			os.system("bash tello_Go_LOWER.sh")
			os.system("bash tello_Rotate_STOP.sh")
			self.golower+=1
	elif area==0 and self.count_rotate_CW==0:
		if self.ball_was_seen ==0:
			self.count_rotate_STOP =0
			self.count_rotate_CW += 1
			os.system("bash tello_Rotate_CW.sh")

		elif self.ball_was_seen ==1:
			self.ball_was_seen = 0
			os.system("bash tello_Go_STOP.sh")
			time.sleep(1)
			os.system("bash tello_land.sh")
			self.land=1"""
