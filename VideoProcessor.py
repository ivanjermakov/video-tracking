import cv2
import numpy as np


class VideoProcessor:

	def __init__(self, path, show=False):
		self._DEFAULT_VIDEO_FOLDER = 'video/'

		self.show = show
		self.path = path
		self.frames = []

		if show:
			self.render(show)
		else:
			cap = cv2.VideoCapture(self._DEFAULT_VIDEO_FOLDER + self.path)
			while cap.isOpened():
				ret, frame = cap.read()
				if not ret:
					break
				frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				self.frames.append(frame)
			cap.release()
			cv2.destroyAllWindows()

	def render(self, show=True):
		cap = cv2.VideoCapture(self._DEFAULT_VIDEO_FOLDER + self.path)
		while cap.isOpened():
			ret, frame = cap.read()
			if not ret:
				break
			frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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


def hexToRgb(hex):
	return np.array(tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4)))


def rgbToHex(rgb):
	return int('0x' + f'{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}', 0)

