import face_recognition
import cv2
import numpy as np
import subprocess
from picamera2 import Picamera2
import time
import pickle
import os
import signal

print("[INFO] Loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

def initialize_camera():
    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
        picam2.start()
        return picam2
    except Exception as e:
        print(f"[ERROR] Failed to initialize camera: {e}")
        exit(1)

picam2 = initialize_camera()
cv_scaler = 4
face_locations = []
face_encodings = []
face_names = []

def process_frame(frame):
    global face_locations, face_encodings, face_names
    resized_frame = cv2.resize(frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            trigger_gate()
            terminate_recognition()
        face_names.append(name)
    return frame

def trigger_gate():
    print("[INFO] Recognized face detected, opening gate...")
    subprocess.run(["python3", "servo_buzzer.py"])

def terminate_recognition():
    print("[INFO] Face recognition process terminating...")
    os.kill(os.getpid(), signal.SIGTERM)

try:
    while True:
        frame = picam2.capture_array()
        processed_frame = process_frame(frame)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= cv_scaler
            right *= cv_scaler
            bottom *= cv_scaler
            left *= cv_scaler
            cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
            cv2.rectangle(frame, (left - 3, top - 35), (right + 3, top), (244, 42, 3), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == ord("q"):
            break
except KeyboardInterrupt:
    print("[INFO] Exiting...")
finally:
    print("[INFO] Releasing camera and closing windows...")
    cv2.destroyAllWindows()
    picam2.stop()
