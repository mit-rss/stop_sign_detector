# Stop Sign Detector

This repo specifies a docker image that can run on your car that encapsulates the [YOLO](https://github.com/ultralytics/yolov5) object detection architecture.
A "bridge" script takes pipes images from your ZED camera into this image and republishes the bounding boxes it receives as ROS messages.

SSH into your car then clone this repo and build it. This can take a little while and might require some extra space (see below) but it only needs to be done once:

    cd stop_sign_detector
    sudo docker build -t stop_sign_detector .

Once it's built, start the detector:

    sudo docker run --rm -p 6141:6141 -ti stop_sign_detector

Once its running, launch your ZED camera and start the bridge to send ROS images to the detector:

    ./bridge.py

Point your camera towards a stop sign (a screenshot works).
If you visualize at the `stop_sign_debug` topic in `rviz`, you'll see it bounded by a blue rectangle.
The coordinates of that rectangle, (xmin, ymin, xmax, ymax), are published to `stop_sign_bbox`

## Freeing Space

If you need more space to build the image delete the following:

    /var/cache/apt
    /home/racecar/.ros/log
    /home/racecar/.local/lib/python3.6/site-packages/tensorflow
    /usr/lib/libreoffice
    /usr/lib/thunderbird
    /usr/src/tensorrt/data/mnist
    /usr/src/tensorrt/python/data/resnet50

If you still don't have enough space run `ncdu /` to find large files.
