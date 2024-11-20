# Hand Gesture Volume Control

This project demonstrates how to use hand gestures to control the system volume. It combines computer vision and hand landmark detection using MediaPipe with audio control via Pycaw.

---

## Features

- Detects the position of thumb and index fingertips using a webcam.
- Calculates the distance between thumb and index fingertips.
- Maps the distance to system volume levels using Pycaw.
- Real-time visualization of gestures, including circles and lines connecting the fingertips.
- Dynamic feedback with frame-per-second (FPS) display.

---

## How It Works

1. **Hand Detection**:
   - MediaPipe is used to detect 21 hand landmarks.
   - Thumb tip (`landmark[4]`) and Index tip (`landmark[8]`) coordinates are extracted.

2. **Distance Calculation**:
   - The Euclidean distance between the thumb and index fingertips is calculated.

3. **Volume Mapping**:
   - The distance is mapped to system volume levels using `np.interp`.

4. **System Volume Adjustment**:
   - Pycaw is used to adjust the system volume based on the calculated distance.

5. **Visual Feedback**:
   - Circles and lines are drawn on the video feed for better user interaction.

---

## Prerequisites

- Python 3.7+
- Webcam

---

## Installation

1. Clone this repository or download the code.
2. Install the dependencies by running:
   ```bash
   pip install -r requirements.txt
