import cv2
import mediapipe as mp
import time
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
vol_range = volume.GetVolumeRange()

min_vol = vol_range[0]
max_vol = vol_range[1]

# capture video
cap = cv2.VideoCapture(0)

# intialize mediapipe and hand detection
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

ptime, ctime = 0, 0

while True:
    success, img = cap.read()

    img = cv2.flip(img, 2)  # MIRRORING THE FRAME
    h, w, c = img.shape
    # converting bgr to rgb for mp
    rgbimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgbimg)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)

            # handlms.landmark[4]: Thumb tip X Y Z POSTION
            # handlms.landmark[8]: Index finger tip
            # results.multi_hand_landmarks: Contains multiple detected hands (if any).
            # handlms.landmark: Contains the 21 landmarks for each hand.
            # mp.hands.HandLandmark: Maps indices to meaningful names (e.g., THUMB_TIP).
            # mphands.HAND_CONNECTIONS: Defines the hand skeleton for visualization.

            # cordinates of thumd and index tip
            thumbtip = handlms.landmark[4]
            indextip = handlms.landmark[8]

            # Convert normalized coordinates to pixel values
            x_thumb, y_thumb = int(thumbtip.x*w), int(thumbtip.y*h)
            x_index, y_index = int(indextip.x*w), int(indextip.y*h)
            cx, cy = int((x_thumb+x_index)/2), int((y_thumb+y_index)/2)

            # Draw circles on thumb and index finger
            cv2.circle(img, (x_thumb, y_thumb), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x_index, y_index), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            cv2.line(img, (x_thumb, y_thumb),
                     (x_index, y_index), (255, 0, 255), 4)

            # euclidean distance
            distance = ((x_index-x_thumb)**2 + (y_index-y_thumb)**2)**0.5

            if distance < 30:
                cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

            master_volume = np.interp(distance, [25, 200], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(master_volume, None)

    ctime = time.time()  # Current time
    fps = 1 / (ctime - ptime)  # Calculate FPS
    ptime = ctime  # Update previous time

    # Display FPS on the frame
    cv2.putText(img, str(int(fps)), (10, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Hand Gesture Volume Control', img)
    if cv2.waitKey(1) & 0xff == ord('e'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
