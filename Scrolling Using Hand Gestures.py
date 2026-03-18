import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=1)

control_active = False
scroll_speed = 40

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands and control_active:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        if fingers == [1, 1, 1, 1, 1]:
            pyautogui.scroll(scroll_speed)

        elif fingers == [0, 0, 0, 0, 0]:
            pyautogui.scroll(-scroll_speed)

    status = "ACTIVE" if control_active else "PAUSED"

    cv2.rectangle(img,(10, 10), (520, 90), (0, 0, 0), -1)

    cv2.putText(img, "HAND SCROLL CONTROL", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.putText(img, f"STATUS: {status}", (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    
    cv2.imshow("Hand Gesture Scroll Control", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        control_active = True
    elif key == ord('p'):
        control_active = False
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()            
