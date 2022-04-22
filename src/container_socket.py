#!/usr/bin/env python3

import socket
import struct
import pickle
import cv2
# from stop_sign_detector import StopSignDetector

print("Loading model...")

# stop_sign_detector = StopSignDetector()

print("Model loaded")

HOST = '0.0.0.0'
PORT = 6141

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Socket open and listening")

    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)

        data = b""
        payload_size = struct.calcsize(">L")
        while True:
            # Get an image
            while len(data) < payload_size:
                data += conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            print("got image")
            bgr_img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
            print("decoded")

            # Perform prediction and send the bounding box back
            conn.sendall(b'image received')
