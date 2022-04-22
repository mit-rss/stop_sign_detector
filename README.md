
    sudo docker build -t stop_detector .
    docker run --rm -p 6141:6141 -ti stop_detector
