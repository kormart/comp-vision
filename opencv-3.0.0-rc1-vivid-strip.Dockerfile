from	opencv-3.0.0-rc1-vivid

run	ln /dev/null /dev/raw1394

run	cd / && \
	mv OpenCV/opencv-3.0.0-rc1/samples samples && \
	rm -rf OpenCV

env	PYTHONPATH /samples/python2

