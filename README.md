comp-vision
===========
This describes how to set-up a computer vision server in python using the OpenCV library, on a Marathon/Mesos and NixOS platform.

## client side for video streaming
The computer vision server expects an rtsp/rtp video stream. Using vlc like this produces such stream from a camera

    cvlc v4l2:// :v4l2-dev=/dev/video0 :v4l2-width=640 :v4l2-height=320 :v4l2-fps=15 --sout="#transcode{vcodec=mp4v,vb=800,scale=1,acodec=mp4a,ab=128,channels=2,samplerate=44100}:rtp{sdp=rtsp://:8080/test.sdp}" -I dummy
    
Using H.264 is also possible, just replace "mp4v" with "h264".

## nix stuff
Have this in configuration.nix

    environment.systemPackages = with pkgs; [
      wget
      python
      opencv
    ];

Plus usual Mesos and Marathon services.

## making opencv stuff available for python app
The python app below uses the libraries: numpy and opencv. I manually created two sym links to make Marathon manifest simpler

    numpy-lib -> /nix/store/kc3rvyqky78jcfsp6c2hyyfxdgffnvc2-python2.7-numpy-1.7.1/lib/python2.7/site-packages
    opencv-python-lib -> /nix/store/x75azbh2qfipna4s8ybas33q1kvgjszi-opencv-2.4.7/lib/python2.7/site-packages


## marathon manifest
Application is started with the manifest file mara_video.json, using Marathon API like this

    curl -X POST -H "Content-Type: application/json" http://10.0.1.101:8081/v2/apps -d@mara_video.json

I serve the python app from a web server at 10.0.1.161, you have to put in your own in the manifest.

## python application 
The server application is in file server-stream-track.py
Note that first line in .py needs to have the Nix path to python.

    #!/run/current-system/sw/bin/python

