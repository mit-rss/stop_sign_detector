import os
import torch
import numpy as np

class StopSignDetector:
  def __init__(self, threshold=0.5, label='stop sign'):
    self.model = torch.hub.load('yolov5', 'yolov5n', source='local')
    self.threshold = threshold
    self.label = label

  def predict(self, img):
    results = self.model(img)
    df = results.pandas().xyxy[0]
    confidences = df[df['confidence'] > self.threshold]
    stop_signs = confidences[confidences['name'] == self.label]

    if len(stop_signs):
      # Extract the bounding box
      stop_sign = stop_signs.head(1)
      coords = stop_sign.xmin, stop_sign.ymin, stop_sign.xmax, stop_sign.ymax
      return [coord.values[0] for coord in coords]
    else:
      return None
