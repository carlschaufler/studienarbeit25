from flask import Flask, Response, render_template
import cv2
import os
from ultralytics import YOLO
import sys
from bandZero import moveBandByStepsforward, moveBandByStepsBackward, moveBandBySteps_Auto

app = Flask(__name__)

def lieferband():
    print("laufe 10 schritte vorwärts")


modelPath = "best_ncnn_model"
if not os.path.exists(modelPath):
    print('ERROR: Make sure your model is in the same folder under model.pt.')
    sys.exit(0)

mode = "automated"

model = YOLO(modelPath, task='detect')
labels = model.names
cameraPos = 0

videoWidth = 1920
videoHeight = 1080

cap = cv2.VideoCapture(cameraPos)
cap.set(3, videoWidth)
cap.set(4, videoHeight)


def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model(frame, verbose=False)
            detections = results[0].boxes
            batteriesDetected = 0

            for i in range(len(detections)):
                xyxy_tensor = detections[i].xyxy.cpu()
                xyxy = xyxy_tensor.numpy().squeeze()
                xmin, ymin, xmax, ymax = xyxy.astype(int)
                classidx = int(detections[i].cls.item())
                classname = labels[classidx]
                conf = detections[i].conf.item()

                if conf > 0.8:
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (220, 20, 20), 2)
                    label = f'{classname}: {int(conf*100)}%'
                    cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    batteriesDetected += 1

            
            if batteriesDetected == 0 and mode == "automated":
                moveBandBySteps_Auto(10)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', mode=mode)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mode')
def swap_mode():
    global mode
    if mode == "automated":
        mode = "manual"
    else:
        mode = "automated"
    
    return {'mode': mode}

@app.route('/bandforward')
def move_band_forward():
    if mode == "manual":
        moveBandByStepsforward(100)
        return {'error': "", 'worked': True}
    else:
        return {'error': "Band befindet sich im automatisierten Modus. Wechseln Sie zum manuellen Modus um das Band zu bewegen. ", 'worked': False}

@app.route('/bandbackward')
def move_band_backward():
    if mode == "manual":
        moveBandByStepsBackward(100)
        return {'error': "", 'worked': True}
    else:
        return {'error': "Band befindet sich im automatisierten Modus. Wechseln Sie zum manuellen Modus um das Band zu bewegen. ", 'worked': False}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
