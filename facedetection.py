import cv2

def load_face_detector():
    return cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

def initialize_camera(camera_index=0):
    return cv2.VideoCapture(camera_index)

def preprocess_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def detect_faces(detector, gray_frame):
    return detector.detectMultiscale(
        gray_frame,
        scaleFactor=1.3,
        minNeighbors=5
    )

def draw_faces(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def display_face_count(frame, count):
    cv2.putText(
        frame,
        f"Faces Detected: {count}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

def run_face_detection():
    face_detector = load_face_detector()
    camera = initialize_camera()

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        gray = preprocess_frame(frame)
        faces = detect_faces(face_detector, gray)

        frame = draw_faces(frame, faces)    
        display_face_count(frame, len(faces))

        cv2.imshow("Real-Time Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_face_detection()


