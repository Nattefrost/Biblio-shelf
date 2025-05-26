import torch
import cv2
from pyzbar import pyzbar
import time
import json


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

def serialize_codes_to_file(list_unique_barcodes):
  if len(list_unique_barcodes) == 0:
     pass
  else:
    with open('barcode_reader/barcodes.txt', 'a', encoding='utf-8') as f:
      for bcode in list_unique_barcodes:
        f.write("%s\n" % bcode)
      


def scan_barcode(device_id=0):
  scanned_barcodes = set()
  device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
  model = torch.hub.load('ultralytics/yolov5', 'custom', path='barcode_reader/model.pt').to(device)

  cap = cv2.VideoCapture(device_id, cv2.CAP_DSHOW)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  while cap.isOpened():
    _, frame = cap.read()
    results = model(frame)
    detections = results.pandas().xyxy[0]

    # Extract the coordinates, class id, and confidence for each detection
    for i, detection in detections.iterrows():
      x1, y1, x2, y2 = detection[['xmin', 'ymin', 'xmax', 'ymax']]
      x1, y1, x2, y2 = [round(num) for num in [x1, y1, x2, y2]]

      class_id = detection['class']
      confidence = detection['confidence']
      #print(f'Detection {i}: class {class_id}, confidence {confidence}, bbox [{x1}, {y1}, {x2}, {y2}]')

      # Draw bounding box on input image
      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

      # Put label text on bounding box
      label = f'{"Barcode"} {confidence:.2f}'
      label_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
      cv2.rectangle(frame, (x1, y1), (x1 + label_size[0], y1 - label_size[1] - baseline), (0, 255, 0), cv2.FILLED)
      cv2.putText(frame, label, (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
      
      # Crop image to bounding box of first detected object
      cropped_img = frame[y1:y2, x1:x2]
      gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
      barcodes = pyzbar.decode(gray)
      data_captured = False
      #print(barcodes)
      for barcode in barcodes:
        data = barcode.data.decode("utf-8")
        # Put barcode data on bounding box
        data_size, baseline = cv2.getTextSize(data, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (x1, y2), (x1 + data_size[0], y2 + data_size[1]), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, data, (x1, y2 + data_size[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        print("DATA => {}".format(data))
        scanned_barcodes.add(data)


    # Display annotated image
    cv2.imshow('Result', frame)
    # Close cam window if 'escape is pressed
    k = cv2.waitKey(27) 
    if k == 27:
      cv2.destroyAllWindows()
      scanned_barcodes_list = serialize_sets(scanned_barcodes)
      serialize_codes_to_file(scanned_barcodes_list)
      break



if __name__ == '__main__':
  scan_barcode()
