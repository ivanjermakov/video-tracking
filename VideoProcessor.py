import cv2


class VideoProcessor:

	def __init__(self, path):
		self._DEFAULT_VIDEO_FOLDER = 'video/'

		self.path = path
		self.mousePos = (0, 0)
		self.waitForMouseClick = False
		self.frames = []

	def render(self, show=True):
		cap = cv2.VideoCapture(self._DEFAULT_VIDEO_FOLDER + self.path)
		while cap.isOpened():
			ret, frame = cap.read()
			if not ret:
				break
			# frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
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
		cv2.destroyAllWindows()
		return self.mousePos

	def _mouseCallback(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONUP:
			print('MOUSECLICK!')
			self.mousePos = (x, y)
			self.waitForMouseClick = False
