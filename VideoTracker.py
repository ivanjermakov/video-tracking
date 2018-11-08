import math

import numpy as np

import VideoProcessor as vp


class VideoTracker:

	def __init__(self, processor):
		self.processor = processor

	def track(self, point, boxSize, targetSize, frame=0):
		currFrame = self.processor.frames[frame]
		boxBorders = np.array([[point[1] - (boxSize[1] // 2), point[1] + (boxSize[1] // 2)],
		                       [point[0] - (boxSize[0] // 2), point[0] + (boxSize[0] // 2)]])
		subFrame = self._getSubFrame(currFrame, boxBorders)
		importanceMask = self._generateImportanceMask(boxSize, targetSize)
		vp.showAsImage(subFrame, resizeRate=(4, 4))
		pass

	def _getSubFrame(self, frame, borders):
		clippedBorders = borders.clip(min=0)
		subFrame = frame[clippedBorders[0][0]:clippedBorders[0][1], clippedBorders[1][0]:clippedBorders[1][1]]
		return self._fixSubFrameSize(subFrame, borders, fillValue=-1)

	def _fixSubFrameSize(self, sub, borders, fillValue=-1):
		w = self.processor.frames[0].shape[1]
		h = self.processor.frames[0].shape[0]

		# TODO: find a better way
		# fix top side
		if borders[0][0] < 0:
			sub = np.vstack((
				np.full((-borders[0][0], sub.shape[1]), fillValue),
				sub
			))
		# fix bottom side
		if borders[0][1] > h:
			sub = np.vstack((
				sub,
				np.full((borders[0][1] - h, sub.shape[1]), fillValue)
			))
		# fix left side
		if borders[1][0] < 0:
			sub = np.hstack((
				np.full((sub.shape[0], -borders[1][0]), fillValue),
				sub
			))
		# fix right side
		if borders[1][1] > w:
			sub = np.hstack((
				sub,
				np.full((sub.shape[0], borders[1][1] - w), fillValue)
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

		print(mask)
		# mask = np.fromfunction(lambda a, b: self._getGradientValue(a, b, m, n, p, k), (m, n))
		return mask

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
