#-*- coding: utf-8 -*-
import signal, os, time
from picamera import PiCamera
from threading import Lock

lck = Lock()
resolution = "1920x1080" # 설정 변수 예

def signal_handler(signum, frame):
    print 'Signal handler called with signal', signum
    lck.acquire()
    # TODO: ipcam_config.py 가 새로 저장한 설정을 읽어서 설정 변수를 변경한다.
    lck.release()

signal.signal(signal.SIGUSR1, signal_handler)

# TODO: 이 프로세스의 PID를 특정 파일에 저장하여, 시그널을 보낼 프로그램(ipcam_config.py)이 PID를 알 수 있도록 한다.
print 'PID:', os.getpid()

camera = PiCamera()

while True:
    lck.acquire()
    # TODO: 변경된 설정을 반영한다.
    lck.release()
    # TODO: 적당한 간격으로 캡쳐 한다.
    camera.capture('foo.jpg')
    time.sleep(5)

