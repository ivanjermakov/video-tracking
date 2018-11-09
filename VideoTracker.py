import math

import numpy as np

import VideoProcessor as vp


class VideoTracker:

	def __init__(self, processor):
		self.processor = processor
		self.importanceMask = None
		self.trackPoints = []
		self.startFrame = 0
		self.boxSize = None

	def track(self, point, boxSize, targetSize, startFrame=0):
		self.startFrame = startFrame if startFrame else 0
		self.importanceMask = self._generateImportanceMask(boxSize, targetSize)
		self.boxSize = boxSize
		prevFrame = self.processor.frames[startFrame]
		currFrame = self.processor.frames[startFrame]
		for frame in range(startFrame, self.processor.frames.__len__() - 1):
			point = self._trackNextPoint(prevFrame, currFrame, point, boxSize)
			print(frame, point)
			self.trackPoints.append(point)
			prevFrame = self.processor.frames[frame]
			currFrame = self.processor.frames[frame + 1]

	def showTracked(self):
		self.processor.showTracked(self.trackPoints, self.boxSize, startFrame=self.startFrame)

	def _getSubFrame(self, frame, point, boxSize):
		# TODO: find out the way to keep tracking with point out of bounds
		point = self._clipPoint(point)
		borders = self._generateBoxBorders(point, boxSize)
		cBorders = borders.clip(min=0)
		cBorders = cBorders.astype(np.uint)
		subFrame = frame[cBorders[0][0]:cBorders[0][1], cBorders[1][0]:cBorders[1][1]]
		fixedSubFrame = self._fixSubFrameSize(subFrame, borders, fillValue=-1)
		return fixedSubFrame

	def _clipPoint(self, point):
		p = (np.clip(point[0], 0, self.processor.resolution[1]), np.clip(point[1], 0, self.processor.resolution[0]))
		return p

	def _fixSubFrameSize(self, sub, borders, fillValue=-1):
		borders = borders.astype(np.int)
		w = self.processor.frames[0].shape[1]
		h = self.processor.frames[0].shape[0]

		# TODO: find a better way
		# fix top side
		if borders[0][0] < 0:
			sub = np.vstack((
				np.full((-borders[0][0], sub.shape[1], sub.shape[2]), fillValue),
				sub
			))
		# fix bottom side
		if borders[0][1] > h:
			sub = np.vstack((
				sub,
				np.full((borders[0][1] - h, sub.shape[1], sub.shape[2]), fillValue)
			))
		# fix left side
		if borders[1][0] < 0:
			sub = np.hstack((
				np.full((sub.shape[0], -borders[1][0], sub.shape[2]), fillValue),
				sub
			))
		# fix right side
		if borders[1][1] > w:
			sub = np.hstack((
				sub,
				np.full((sub.shape[0], borders[1][1] - w, sub.shape[2]), fillValue)
			))

		return sub

	def _generateImportanceMask(self, boxSize, targetSize):
		m = boxSize[0]
		n = boxSize[1]
		p = targetSize[0]
		k = targetSize[1]

		mask = np.zeros((m, n))

		for a in range(m):
			for b in range(n):
				mask[a][b] = self._getGradientValue(a, b, m, n, p, k)

		return mask

	def _generateBoxBorders(self, point, boxSize):
		return np.array([[point[0] - (boxSize[0] // 2), point[0] + (boxSize[0] // 2)],
		                 [point[1] - (boxSize[1] // 2), point[1] + (boxSize[1] // 2)]])

	def _getGradientValue(self, a, b, m, n, p, k):
		r = math.hypot(m / 2, n / 2)

		a += 0.5
		b += 0.5

		# TODO: find out a better solution
		# else case to avoid division by zero
		q = abs((m / 2) - a) if m / 2 != a else 0.01
		z = abs((n / 2) - b) if n / 2 != b else 0.01

		isHorizontalC = (q / z) > (p / k)
		c = p / 2 if isHorizontalC else k / 2

		r0 = math.hypot(q, z)

		l = (c * r0) / (q if isHorizontalC else z)

		dr = r0 - l
		v = 1 - (dr / r)

		return v if v < 1 else 1

	# TODO: count not only single prev frame, but also other prev frames
	def _trackNextPoint(self, prevFrame, frame, point, boxSize):
		prevSubFrame = self._getSubFrame(prevFrame, point, boxSize)
		borders = self._generateBoxBorders(point, boxSize)
		possibleSubFrames = []
		for i in range(borders[0][0], borders[0][1]):
			for j in range(borders[1][0], borders[1][1]):
				possibleSubFrames.append(self._getSubFrame(frame, (i, j), boxSize))

		possibleSubFramesSimilarity = [1 - (abs(prevSubFrame - p) / 255) for p in possibleSubFrames]
		# avg similarities from rgb
		possibleSubFramesSimilarity = [np.array(s).mean(axis=2) for s in possibleSubFramesSimilarity]
		# apply importance
		possibleSubFramesSimilarity = list(map(lambda f: f * self.importanceMask, possibleSubFramesSimilarity))
		meanSimilarities = [np.array(s).mean() for s in possibleSubFramesSimilarity]

		rowLength = borders[1][1] - borders[1][0]
		k = meanSimilarities.index(max(meanSimilarities))
		dPoint = (k // rowLength, k % rowLength)
		point = (dPoint[0] + borders[0][0], dPoint[1] + borders[1][0])
		return point
