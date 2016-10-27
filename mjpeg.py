from flask import Flask, render_template, Response, redirect
from picamera import PiCamera
import io


camera = PiCamera()
camera.resolution = (320, 240)

app = Flask(__name__)


def get_frame():
    stream = io.BytesIO()
    camera.capture(stream, 'jpeg', use_video_port=True)
    stream.seek(0)
    return stream.read()


@app.route('/')
def index():
    return redirect('/video_feed')


def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0') #, threaded=True)

