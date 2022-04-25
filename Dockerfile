FROM ultralytics/yolov5:latest-cpu

# Preload the model
RUN git clone https://github.com/ultralytics/yolov5
RUN python3 -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)"

# Add the code
COPY src /usr/src/app/

# Make sure the socket can work
EXPOSE 6141

# Start the socket
CMD ["python3", "-u", "container_socket.py"]
