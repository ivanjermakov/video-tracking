import VideoProcessor as vp
import VideoTracker as vt

processor = vp.VideoProcessor('test.mp4')
processor.render(False)

tracker = vt.VideoTracker(processor)
print(tracker)

print(processor.selectPoint())
