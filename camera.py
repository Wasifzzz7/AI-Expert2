import cv2
from datetime import datetime

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

def adjust_brightness_contrast(img, brightness=20, contrast=1.2):
    return cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100)
    )

    display_frame = frame.copy()

    if len(faces) > 0:
        display_frame = adjust_brightness_contrast(display_frame, 35, 1.5)
        cv2.putText(display_frame, "Face Detected - Enhancement ON", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(display_frame, "No Face - Normal View", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Smart Face-Aware Camera", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        capture_frame = adjust_brightness_contrast(frame, 30, 1.3)
        cv2.imwrite(filename, capture_frame)
        print(f"Saved: {filename}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    
