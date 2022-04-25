FROM python:3.9

# Add the code
COPY src /app
WORKDIR /app

# Install opencv req
RUN apt update; apt install -y libgl1

# Install yolov5
RUN git clone https://github.com/ultralytics/yolov5
RUN pip3 install -r yolov5/requirements.txt
RUN python3 -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)"

# Make sure the socket can work
EXPOSE 6141

# Start the socket
CMD ["python3", "-u", "container_socket.py"]
