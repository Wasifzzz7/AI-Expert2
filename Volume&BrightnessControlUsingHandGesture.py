import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import screen_brightness_control as sbc

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

mode = "VOLUME"
control_active = False

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands and control_active:
        hand = hands(0)
        lmList = hand["lmList"]

        x1, y1 = lmList[4][0], lmList[4][1]
        x2, y2 = lmList[8][0], lmList[8][1]

        length = math.hypot(x2 - x1, y2 - y1)

        if mode == "VOLUME":
            vol = np.interp(length, [30, 200], [volMin, volMax])
            volume.SetMasterVolumeLevel(vol, None)

        elif mode == "BRIGHTNESS":
            bright = int(np.interp(length, [30, 200], [0, 100]))
            sbc.set_brightness(bright)

    status = "ACTIVE" if control_active else "PAUSED"

    cv2.rectangle(img, (10, 10), (520, 90), (0, 0, 0), -1)
    cv2.putText(img, f"MODE: {mode}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(img, f"STATUS: {status}", (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    
    cv2.imshow("Hand Gesture Control System", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('v'):
        mode = "VOLUME"
    elif key == ord('b'):
        mode = "BRIGHTNESS"
    elif key == ord('s'):
        control_active = True
    elif key == ord('p'):
        control_active = False  
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
      
