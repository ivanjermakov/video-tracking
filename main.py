import VideoProcessor as vp
import VideoTracker as vt

processor = vp.VideoProcessor('test.mp4')
processor.render(False)

tracker = vt.VideoTracker(processor)

tracker.track(processor.selectPoint(), (40, 40), (40, 40))
# tracker.track((435, 994), (50, 50), (10, 10), startFrame=100)
tracker.showTracked()
