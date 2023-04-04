from flask import Flask, render_template, request, Response
from API import DataBase
import FaceRecognition
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
db = DataBase()


def generate_frames():

    camera = cv2.VideoCapture(0)
    FaceRecognition.train()
    while True:

        success, frame = camera.read()
        if not success:
            break

        frame = FaceRecognition.test(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        name = request.form['username']
        acn = request.form['aadhar']
        mn = request.form['mobile']
        im = request.files['image']

        name = str(name)
        acn = int(acn)
        mn = int(mn)

        db = DataBase()
        db.insert_record(name, acn, mn, secure_filename(im.filename))
        im.save("./train/" + secure_filename(im.filename))

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
