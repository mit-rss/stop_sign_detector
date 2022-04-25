#!/usr/bin/env python2

import socket
import pickle
import struct
import numpy as np
from cv_bridge import CvBridge
import cv2
import json
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray

HOST = '127.0.0.1'
PORT = 6141
ENCODE_PARAM = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

class StopSignDetector:

    def __init__(self, s):
        self.s = s
        # Initialize ROS and subscribe
        self.br = CvBridge()
        self.debug_pub = rospy.Publisher('stop_sign_debug', Image, queue_size=1)
        self.bbox_pub = rospy.Publisher('stop_sign_bbox', Float32MultiArray, queue_size=1)
        self.sub = rospy.Subscriber("/zed/zed_node/rgb/image_rect_color", Image, self.ros_msg_detect, queue_size=1, buff_size=99999999)

    def ros_msg_detect(self, img_msg):
        np_img = np.frombuffer(img_msg.data, dtype=np.uint8).reshape(img_msg.height, img_msg.width, -1)
        self.img_detect(np_img[:,:,:-1])

    def file_detect(self, path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        self.img_detect(img)

    def img_detect(self, img):
        # Resize the image so the max side length is 640
        scale = 640./max(img.shape[0], img.shape[1])
        img_scaled = cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))

        # Convert the data to a JPG so its smaller
        _, frame = cv2.imencode('.jpg', img_scaled, ENCODE_PARAM)

        # Dump the data to a pickle and
        # send it over the socket
        data = pickle.dumps(frame, 0)
        size = len(data)
        self.s.sendall(struct.pack(">L", size) + data)

        # Wait for the result
        bbox_msg = Float32MultiArray()
        bbox = json.loads(self.s.recv(4096).decode())

        if bbox:
            # Scale the bounding box back up
            bbox = [int(x/scale) for x in bbox]
            bbox_msg.data = bbox

            # Draw a rectangle on the image to republish
            img = img.astype(np.uint8)
            img = cv2.rectangle(img,
                    (bbox[0], bbox[1]),
                    (bbox[2], bbox[3]),
                    (255, 0, 0), 2)

        self.bbox_pub.publish(bbox_msg)
        self.debug_pub.publish(self.br.cv2_to_imgmsg(img))

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connected to socket!")

    rospy.init_node("stop_sign_detector")
    ssd = StopSignDetector(s)
    rospy.spin()
