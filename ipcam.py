#-*- coding: utf-8 -*-
from flask import Flask, send_file, render_template, request
import os, signal
from ipcam_config import save_config, load_config

app = Flask(__name__)

@app.route('/')
def index():
    cfg_dict = load_config()
    return render_template('config.html', annotate_text=cfg_dict['annotate'],
        resolution=cfg_dict['resolution']) # config.html은 templates/config.html 에 위치해야 함.


def read_capture_pid():
    with open('capture.pid', 'r') as f:
        line = f.readline()
        return int(line)
    return -1


@app.route('/config')
def config():
    resolution = request.args.get('resolution', '')
    annotate = request.args.get('annotate', '')
    print resolution, annotate
        
    # TODO: resolution, annotate 설정을 특정 파일에 저장한다. 저장 방법은 xml이나 pickle 등을 사용
    save_config(resolution, annotate)

    # 캡쳐 프로그램이 설정을 다시 읽도록 SIGUSR1 시그널을 보낸다.
    cap_pid = read_capture_pid()
    if cap_pid > 0:
        os.kill(cap_pid, signal.SIGUSR1)
        return 'OK'
    else:
        return 'Failed! - no capture.py is running'


@app.route('/capture')
def capture():
    return send_file('foo.jpg') # 캡쳐 프로그램이 캡쳐한 파일 전송

if __name__ == '__main__':
    app.run('0.0.0.0')

