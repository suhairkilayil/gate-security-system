# Blynk streaming server and video control
import io
import logging
import socketserver
import threading
import time
import subprocess
from http import server
from threading import Condition
import cv2
from picamera2 import Picamera2
import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH_TOKEN = 'Your_Token_Here'

PAGE = """<html><head><title>Raspberry Pi - Surveillance Camera </title></head>
<body><center><h1>Raspberry Pi - Surveillance Camera </h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center></body></html>"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.condition = Condition()
    def update_frame(self, frame):
        with self.condition:
            self.frame = frame
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": "XRGB8888", "size": (640, 480)}))
picam2.start()
output = StreamingOutput()

def capture_loop():
    while True:
        frame = picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame)
        output.update_frame(jpeg.tobytes())
        time.sleep(0.05)

def run_video_stream():
    capture_thread = threading.Thread(target=capture_loop, daemon=True)
    capture_thread.start()
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    print("Streaming on http://<raspberrypi_ip>:8000")
    server.serve_forever()

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

def run_servo_buzzer():
    try:
        subprocess.run(["python3", "servo_buzzer.py"], check=True)
        print("Executed servo_buzzer.py successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing servo_buzzer.py: {e}")

@blynk.on("V0")
def v0_write_handler(value):
    if int(value[0]) != 0:
        print("Switch ON - Running servo_buzzer.py")
        run_servo_buzzer()
    else:
        print("Switch OFF - No action")

@blynk.on("connected")
def blynk_connected():
    print("Raspberry Pi Connected to New Blynk")

def run_blynk():
    while True:
        blynk.run()

threading.Thread(target=run_video_stream, daemon=True).start()
threading.Thread(target=run_blynk, daemon=True).start()

while True:
    time.sleep(1)
