import numpy as np

import VideoProcessor as vp


class VideoTracker:

	def __init__(self, processor):
		self.processor = processor

	def track(self, point, frameSize, frame=0):
		currFrame = self.processor.frames[frame]
		borders = np.array([[point[1] - (frameSize[1] // 2), point[1] + (frameSize[1] // 2)],
		                    [point[0] - (frameSize[0] // 2), point[0] + (frameSize[0] // 2)]])
		subFrame = self._getSubFrame(currFrame, borders)
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
