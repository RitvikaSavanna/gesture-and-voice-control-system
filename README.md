
# 🤖 Gesture & Voice Controlled System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![AI](https://img.shields.io/badge/AI-Gesture%20Recognition-purple)
![Status](https://img.shields.io/badge/Status-Working%20Prototype-success)
![License](https://img.shields.io/badge/License-MIT-green)

A real-time **AI-powered gesture and voice control system** that allows users to interact with their computer using **hand gestures and voice commands**. Built using OpenCV, MediaPipe, and custom gesture recognition logic.

---

## 🎯 Features

### ✋ Gesture Recognition

* Detects hand landmarks using MediaPipe
* Recognizes gestures like:

  * Swipe Left / Right
  * Thumbs Up
  * Fist (activation gesture)
* Executes commands based on gestures

### 🖱️ Virtual Mouse Control

* Toggle mouse using gestures
* Move cursor using index finger
* Click/interaction using thumb-index distance

### 🔊 Voice Integration

* Wake word activation (`"apple"`)
* Text-to-speech feedback (`speak()`)
* Voice command system

### 🔐 Smart Activation System

* Prevents accidental triggers
* Requires **gesture hold (fist)** to activate
* Auto-lock after inactivity

### 📜 Scroll Mode

* Gesture-based scrolling
* Separate activation system

### ⚡ Real-Time Performance

* Live webcam processing
* FPS display
* Smooth interaction

---

## 🧠 Core Concepts Used

* Computer Vision (OpenCV)
* Hand Tracking (MediaPipe)
* Gesture Recognition Algorithms
* Voice Processing & TTS
* State Management (activation, locking)
* Real-time event handling

---

## 🗂️ Project Structure

```id="gesture-structure"
project/
│
├── main.py                # Main execution file
├── gesture_logic.py       # Gesture detection logic
├── vision_precision.py    # Mouse control & actions
├── voice_module.py        # Voice commands & TTS
└── requirements.txt
```

---

## ⚙️ Tech Stack

* **Language:** Python
* **Libraries:**

  * OpenCV
  * MediaPipe
  * PyAutoGUI (for mouse control - assumed)
  * SpeechRecognition / TTS (voice module)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash id="clone-gesture"
git clone https://github.com/your-username/gesture-voice-control.git
```

### 2. Install dependencies

```bash id="install-gesture"
pip install -r requirements.txt
```

### 3. Run the project

```bash id="run-gesture"
python main.py
```

---

## 🎮 Controls & Usage

### ✋ Gestures

| Gesture                  | Action          |
| ------------------------ | --------------- |
| ✊ Hold Fist              | Activate system |
| 👉 Index Movement        | Move mouse      |
| 🤏 Pinch (Thumb + Index) | Click           |
| 👍 Thumbs Up             | Exit            |
| 👉➡️ Swipe Right         | Command trigger |
| 👈⬅️ Swipe Left          | Command trigger |

### 🔊 Voice

* Say **"apple"** → Activate voice system
* System gives audio feedback

---

## ⚠️ Limitations

* Requires good lighting for accurate detection
* Single-hand tracking only
* Depends on webcam quality
* Voice accuracy depends on environment noise

---

## 🔮 Future Improvements

* 🧠 ML-based gesture classification
* 🎯 Multi-hand tracking
* 📱 Mobile/IoT integration
* 🗣️ Advanced NLP voice commands
* 🎮 Gesture customization UI
* 🧩 Integration with OS-level automation

---


