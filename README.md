Run this to initialize the yolo model and socket:

    sudo docker build -t stop_detector .
    sudo docker run --rm -p 6141:6141 -ti stop_detector

Once its running, run this to send images over the socket and receive a bounding box:

    ./client_socket.py
