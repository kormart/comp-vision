#!/usr/bin/python
'''
	orig author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import cv2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time
import numpy as np
import video
from common import anorm2, draw_str

capture=None

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
        	self.track_len = 10
        	self.detect_interval = 5
        	self.tracks = []
        	self.cam = cv2.VideoCapture(video_src)
        	self.frame_idx = 0
		print self.path
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					rc,img = self.cam.read()
					if not rc:
						continue
#					imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            				frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            				vis = img.copy()

            				if len(self.tracks) > 0:
                				img0, img1 = self.prev_gray, frame_gray
                				p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                				p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                				p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                				d = abs(p0-p0r).reshape(-1, 2).max(-1)
                				good = d < 1
                				new_tracks = []
                				for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    					if not good_flag:
                        					continue
                    					tr.append((x, y))
                    					if len(tr) > self.track_len:
                        					del tr[0]
                    					new_tracks.append(tr)
                    					cv2.circle(vis, (x, y), 3, (0, 255, 255), -1)
                				self.tracks = new_tracks
                				cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 255), 3)
                				draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))
		
            				if self.frame_idx % self.detect_interval == 0:
                				mask = np.zeros_like(frame_gray)
                				mask[:] = 255
                				for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    					cv2.circle(mask, (x, y), 5, 0, -1)
                				p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                				if p is not None:
                    					for x, y in np.float32(p).reshape(-1, 2):
                        					self.tracks.append([(x, y)])


            				self.frame_idx += 1
            				self.prev_gray = frame_gray
					r, buf = cv2.imencode(".jpg",vis)
					self.wfile.write("--jpgboundary\r\n")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(len(buf)))
					self.end_headers()
					self.wfile.write(bytearray(buf))
					self.wfile.write('\r\n')
#					time.sleep(0.1)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html') or self.path=="/":
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return

def main():
	global video_src
    	import sys
    	try: video_src = sys.argv[2]
    	except: video_src = 0

	try:
		server = HTTPServer(('',int(sys.argv[1])),CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()
