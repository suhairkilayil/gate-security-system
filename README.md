# 🚪 Gate Security System 🔐  
### Smart Multi-Authentication Gate Control Using Raspberry Pi & IoT

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg)

---

## 📌 Introduction

The **Gate Security System** is a smart security solution built on **Raspberry Pi 4B**, integrating:
- 🎭 **Facial Recognition**  
- 🔢 **Keypad-based PIN Authentication**  
- 📱 **IoT-based remote access** via **Blynk App**  

This system provides **automated, secure, and remote-controlled gate access** ideal for **residential buildings**, **offices**, and **gated communities**.

---

## 🎯 Key Features

- 👤 **Face Recognition** using PiCamera & pre-trained face embeddings
- 🔐 **PIN-based Access** via 4x4 matrix keypad
- 📲 **Remote Monitoring** through Blynk with real-time video
- 🔔 **Visitor Bell** for unknown individuals with alert notifications
- 🚨 **Buzzer Feedback** for gate open/close status
- 🔄 **Servo-Controlled Gate** with precise actuation

---

## 🧰 Hardware Components

| Component               | Description                      |
|------------------------|----------------------------------|
| Raspberry Pi 4B        | Main processing unit             |
| Pi Camera Module       | Captures images for recognition  |
| Servo Motor            | Controls gate movement           |
| 4x4 Matrix Keypad      | PIN input                        |
| LCD Display (I2C)      | Feedback for user interactions   |
| Buzzer & Push Buttons  | Alerts and trigger mechanisms    |
| 7805 Voltage Regulator | Stable 5V power supply           |
| Breadboard + Wires     | Prototyping & connections        |

---

## 📁 Project Directory Structure

```bash
gate-security-system/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── docs/
│   ├── Mini_Project_Report.pdf
│   └── images/
│       ├── block_diagram.png
│       ├── face_recognition_output.jpg
│       └── hardware_setup.jpg
├── demo/
│   └── gate_security_demo.mp4
├── hardware/
│   └── circuit_diagram.fritzing
├── code/
│   ├── main.py
│   ├── facial_detection.py
│   ├── pin_lock.py
│   ├── blynk_stream_cntrl.py
│   ├── calling_bell.py
│   ├── servo_buzzer.py
│   └── encodings.pickle
