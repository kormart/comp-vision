from	ubuntu:15.04

run	apt-get update
run	apt-get install -y -q wget curl unzip
run	apt-get install -y -q build-essential
run	apt-get install -y -q cmake
run	apt-get install -y -q python2.7 python2.7-dev

run	apt-get install -y -q software-properties-common
run	add-apt-repository -y 'deb http://us.archive.ubuntu.com/ubuntu vivid main restricted universe multiverse'
run	apt-get update
run	apt-get install -y -q libopencv-dev build-essential checkinstall cmake pkg-config yasm libjpeg-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev python-dev python-numpy libtbb-dev libqt4-dev libgtk2.0-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils ffmpeg cmake qt5-default checkinstall

run	mkdir OpenCV && \
	cd OpenCV && \
#	version="$(wget -q -O - http://sourceforge.net/projects/opencvlibrary/files/opencv-unix | egrep -m1 -o '\"[0-9](\.[0-9]+)+' | cut -c2-)"
	version="3.0.0-rc1" && wget -O OpenCV-$version.zip http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/$version/opencv-$version.zip/download && unzip OpenCV-$version.zip && \
	cd opencv-$version && \
	mkdir build && \
 	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON .. && \
	make -j3 install/strip && \
#	checkinstall && \
	sh -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf' && \
 	ldconfig && \
	ln /dev/null /dev/raw1394 && \
	cd / && \
	mv OpenCV/opencv-3.0.0-rc1/samples samples && \
	rm -rf OpenCV && \
 	apt-get remove --purge -y build-essential && apt-get autoclean && apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

env	PYTHONPATH /samples/python2


