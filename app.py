import os
import shutil
import cv2
import numpy as np

from flask import Flask, request, render_template, Response
from ultralytics import YOLO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == "POST":
        if 'file' in request.files:
            # save the input file to uploads folder
            f = request.files['file']
            if f.filename == '':
                return render_template('index.html', error_message="Error: Select an image to upload.")
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'static','uploads',f.filename)
            # print("upload folder is", filepath)
            f.save(filepath)
            rel_path = os.path.join('static','uploads',f.filename)

            # model
            # model = YOLO('best.pt')
            model = YOLO('best-yolo8-tiny.pt')
            results = model.predict(rel_path,save=True)

            # getting the predict image
            folder_path = 'runs/detect'
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path,x)))
            directory = folder_path + '/' + latest_subfolder
            latest_file = os.path.join(directory,f.filename)
            # print('latest file path: ', latest_file)
            
            # move image to static
            static_path = os.path.join('static', 'detect', f.filename)
            shutil.move(latest_file,static_path)

            shutil.rmtree(folder_path)
    return render_template('image.html', filepath=static_path)

@app.route('/real')
def cam():
    return render_template('cam.html')

def generate_frames():
    for i in range(10):
        camera = cv2.VideoCapture(i)
        if camera.read()[0]:
            break
    else:
        camera = cv2.VideoCapture(0)
        
    model = YOLO('best-yolo8-tiny.pt')
    while True:
        ret, frame = camera.read()
        if ret == False:
            continue
        # encode the frame in JPEG format

        # encodedImage = cv2.imencode(".jpg", frame)
        # yield (b'--frame\r\n'
        # b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

        results = model(frame)
        for res in results:
            res_plotted = res.plot()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', res_plotted)[1].tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)