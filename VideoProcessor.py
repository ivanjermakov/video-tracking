import cv2
import numpy as np


def showAsImage(frame, resizeRate=(1, 1)):
	frame = frame.astype(np.uint8)
	frame = cv2.resize(frame, (0, 0), fx=resizeRate[0], fy=resizeRate[1])
	cv2.imshow('frame', frame)
	cv2.waitKey(0)


class VideoProcessor:

	def __init__(self, path):
		self._DEFAULT_VIDEO_FOLDER = 'video/'

		self.path = path

		self.mousePos = (0, 0)
		self.waitForMouseClick = False

		self.frames = []

		self.resolution = None

	def render(self, show=True, resizeRate=(1, 1)):
		cap = cv2.VideoCapture(self._DEFAULT_VIDEO_FOLDER + self.path)
		self.resolution = (cap.get(3), cap.get(4))
		while cap.isOpened():
			ret, frame = cap.read()
			if not ret:
				break
			frame = cv2.resize(frame, (0, 0), fx=resizeRate[0], fy=resizeRate[1])
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			self.frames.append(frame)
			if show:
				cv2.imshow('video', frame)
				while True:
					key = cv2.waitKeyEx(0)
					if key == 2555904:
						break
					if key & 0xFF == ord('q'):
						exit(-1)
		cap.release()
		cv2.destroyAllWindows()

	def selectPoint(self, frame=0):
		cv2.namedWindow('select point')
		cv2.setMouseCallback('select point', self._mouseCallback)
		self.waitForMouseClick = True
		while self.waitForMouseClick:
			cv2.imshow('select point', self.frames[frame])
			cv2.waitKey(1)
		return self.mousePos

	def _mouseCallback(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONUP:
			self.mousePos = (x, y)
			self.waitForMouseClick = False
