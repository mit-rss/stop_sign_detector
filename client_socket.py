#!/usr/bin/env python3

import socket
import pickle
import struct
import numpy as np
import cv2
# import rospy

HOST = '127.0.0.1'
PORT = 6141
ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

class StopSignDetector:

    def __init__(self, s):
        self.s = s
        # Initialize ROS and subscribe
        # self.sub = rospy.Subscriber("/zed/zed_node/rgb/image_rect_color", Image, img_callback)

    def ros_msg_detect(self, img_msg):
        # Convert to RGB CV image
        np_img = np.frombuffer(img_msg.data, dtype=np.uint8).reshape(img_msg.height, img_msg.width, -1)
        self.img_detect(np_img[:,:,:-1])

    def file_detect(self, path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        self.img_detect(img)

    def img_detect(self, img):
        # Resize the image so the max side length is 640
        aspect_ratio = img.shape[0]/img.shape[1]
        img = cv2.resize(img, (640, int(640*aspect_ratio)))

        # Convert the data to a JPG so its smaller
        _, frame = cv2.imencode('.jpg', img, ENCODE_PARAM)

        # Dump the data to a pickle and
        # send it over the socket
        data = pickle.dumps(frame, 0)
        size = len(data)
        self.s.sendall(struct.pack(">L", size) + data)

        # Wait for the result
        data = self.s.recv(1024)

        # Publish the result as a ROS message
        print(data)

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to socket!")

        # rospy.init_node("stop_sign_detector")

        ssd = StopSignDetector(s)

        while True:
            ssd.file_detect('/Users/theia/Pictures/li_sunrise.jpg')
        # rospy.spin()
