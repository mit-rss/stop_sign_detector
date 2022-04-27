# Stop Sign Detector

This repo specifies a docker container, capable of running directly on your car, that encapsulates the [YOLO](https://github.com/ultralytics/yolov5) object detection architecture.
A "bridge" script pipes images from your ZED camera into the docker container and republishes the bounding boxes it receives as ROS messages.

SSH into your car then clone this repo and build it. This can take a little while and might require some extra space (see below) but it only needs to be done once. Your car needs to be connected to the internet to build (make sure you can `ping google.com`).

    cd stop_sign_detector
    sudo docker build -t stop_sign_detector .

Once it's built, first run a `roscore` one terminal then start the detector:

    sudo docker run --rm -p 6141:6141 -ti stop_sign_detector

Once the detector says "socket open and listening" run the bridge:

    ./bridge.py
    
They should both say "connected". Note that if you kill the bridge you'll also need to restart the docker container.
    
Then launch your ZED camera:

    roslaunch zed_wrapper zed.launch
    
Point your camera towards a stop sign (a screenshot works).
If you visualize the `stop_sign_debug` topic in `rviz`, you'll see your camera feed and the stop sign bounded by a blue rectangle.
The coordinates of that rectangle, (xmin, ymin, xmax, ymax), are published to `stop_sign_bbox` --- subscribe to this topic to build control logic around the detector!

## Freeing Space

If you need more space, delete the following:

    /var/cache/apt
    /home/racecar/.ros/log
    /home/racecar/.local/lib/python3.6/site-packages/tensorflow
    /usr/lib/libreoffice
    /usr/lib/thunderbird
    /usr/src/tensorrt/data/mnist
    /usr/src/tensorrt/python/data/resnet50
    
If your install failed for any reason you can also try clearning the docker cache:

    docker system prune -a

If you still don't have enough space run `ncdu /` to find large files. \~don't delete your kernel pls\~
