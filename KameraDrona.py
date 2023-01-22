from multiprocessing.process import current_process
import numpy as np
import cv2
import rclpy
from numpy.distutils.command.config import config
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2 as cv
class KameraDrona(Node):
	subscription = None
	def __init__(self):
		super().__init__('KameraDrona')
		self.subscription = self.create_subscription(Image,
		'drone1/image_raw', self.KameraDrona_callback, 10)
		self.publisher = self.create_publisher(String,'Pileczka',1)

		self.timer = self.create_timer(0.1,self.timer_callback)
		self.br = CvBridge()
		self.value_of_area_ball = 0
		self.center_point = [0,0]
		self.value_of_area_wall = 0
	def KameraDrona_callback(self, data):



		## Pobranie obrazu kamery z drona
		current_frame = self.br.imgmsg_to_cv2(data)
		## Konwersja BGR TO
		current_frame = cv.cvtColor(current_frame,cv.COLOR_BGR2RGB)


		lower_wall = np.array([14,0,0])
		upper_wall = np.array([180,255,172])

		lower_ball = np.array([90, 50, 50])
		upper_ball = np.array([120, 255, 255])

		hsv = cv.cvtColor(current_frame,cv.COLOR_RGB2HSV)

		mask_ball = cv2.inRange(hsv, lower_ball, upper_ball)
		mask_wall = cv2.inRange(hsv, lower_wall, upper_wall)

		result_ball = cv2.bitwise_and(current_frame, current_frame, mask=mask_ball)
		result_wall = cv2.bitwise_and(current_frame, current_frame,mask=mask_wall)

		ball_blur = cv2.GaussianBlur(result_ball, (13, 13), 2)
		ball_blurr = cv2.GaussianBlur(result_wall, (69, 69), 4)
		blur_ball = cv2.Canny(ball_blur,100,200)
		blur_wall = cv2.Canny(ball_blurr,0,50,2)
		cv2.imshow('xD',blur_wall)


		_, contours_ball , _ = cv2.findContours(blur_ball,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
		_,contours_wall, _ = cv2.findContours(blur_wall, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

		#WYznaczenie konturu piłeczki oraz jej srodka
		if len(contours_ball)>0:
			cnt = contours_ball[0]
			(x, y), radius = cv.minEnclosingCircle(cnt)
			center = (int(x), int(y))
			self.center_point[0] = int(x)
			self.center_point[1] = int(y)
			radius = int(radius)
			cv.circle(current_frame, center, radius, (0, 255, 0), 2)
			cv.circle(current_frame, center, 1, (0, 255, 0), 1)
		else:
			self.center_point[0] = 0
			self.center_point[1] = 0
		cv2.drawContours(current_frame, contours_wall, -1, (0, 255, 0), 1)

		##Wyznaczenie krwaedzi koloru zielonego w celu obliczenia pola/ odleglosc od sciany
		if len(contours_wall)>0:
			for i in range(0,len(contours_wall)):
				cnt = contours_wall[i]

				(x,y,w,h) = cv2.boundingRect(cnt)


				cv.rectangle(current_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				area_wall = np.zeros(current_frame.shape, dtype=np.uint16)
				wall_contour = cv2.drawContours(area_wall,contours_wall,-1,(255,0,255),10)
				self.value_of_area_wall = np.count_nonzero(area_wall[mask_wall == 255])

		cv2.imshow('Camera', current_frame)
		area_ball = np.zeros(current_frame.shape, dtype=np.uint16)


		area_contour_ball = cv2.drawContours(area_ball,contours_ball,-1,(255,0,0),4)


		self.value_of_area_ball = np.count_nonzero(area_ball[mask_ball == 255])




		cv.waitKey(1)
	def timer_callback(self):

		msg = String()
		msg.data = "p%dx%dy%dw%d" % (self.value_of_area_ball, self.center_point[0],self.center_point[1],self.value_of_area_wall)
		self.publisher.publish(msg)
		self.get_logger().info(msg.data)

def main(args=None):
	rclpy.init()
	KD = KameraDrona()
	rclpy.spin(KD)
	KD.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()

