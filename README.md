# VLC Hand Gesture Controller 🎥✋

A computer vision project that lets you control VLC Media Player using **hand gestures** through your webcam. Built using Python, OpenCV, MediaPipe, and VLC Python bindings.

---

## 🚀 Features

- 👋 **Hand Detection** via webcam  
- 🎵 **Play/Pause** using 0 or 1 finger  
- ⏭️ **Next Track** with 2 fingers  
- ⏮️ **Previous Track** with 3 fingers  
- 🔉 **Decrease Volume** with 4 fingers  
- 🔊 **Increase Volume** with 5 fingers  
- 📊 **Live UI** showing current command and finger count

---

## 🧠 How it Works

This project uses:
- **MediaPipe** to detect and track your hand
- **OpenCV** to access your webcam and draw on the screen
- **VLC Python** API to control the VLC player
- **Custom gesture recognition logic** to detect number of fingers shown



---

## 📸 Demo

Each number of fingers maps to a specific command (see below).

| Fingers | Action           |
|--------:|------------------|
| 0       | Pause            |
| 1       | Play             |
| 2       | Next Track       |
| 3       | Previous Track   |
| 4       | Volume Down 🔉   |
| 5       | Volume Up 🔊     |
 
> Make sure your hand is fully visible in front of the webcam.

---

## 🛠️ Setup Instructions

### ✅ Step 1: Clone the Repo

```bash
git clone https://github.com/JAFFER1272HUSSAIN/VLC-Hand-Gesture-Controller.git
cd VLC-Hand-Gesture-Controller
```

### ✅ Step 2: Install Dependencies
Make sure you have Python 3.7+ installed.
```bash
pip install -r requirements.txt
```

--- 

## 🎯 Run the App
Run the Python script:
```bash
python hand_gesture_vlc.py
```
---

## 🧩 Dependencies
All dependencies are listed in requirements.txt, but in short:

- opencv-python

- mediapipe

- python-vlc

- numpy

---

## ❓ Troubleshooting
### Media not playing?
Ensure VLC is installed and the DLL path is correct.

Verify media files exist inside the media/ folder.
### Webcam not detected?
Close any app using the webcam.

Ensure camera permissions are allowed.
### Gestures not working?
Use good lighting.

Keep your hand within the camera frame.

---

## 👨‍💻 Author
Name: Rana Jaffer Hussain

Email: jaffer1272hussain@gmail.com

GitHub: https://github.com/JAFFER1272HUSSAIN

---
