import cv2

def load_face_tracker():
    return cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

def initialize_camera(camera_index=0):
    return cv2.VideoCapture(camera_index)

def preprocess_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def detect_faces(detector, gray_frame):
    faces = detector.detectMultiScale(
        gray_frame,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30,30)
    )
    return faces

def draw_faces(frame, faces):
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cx = x + w//2
        cy = y + h//2
        cv2.circle(frame, (cx, cy), 4, (0,0,255), -1)

    return frame

def display_people_count(frame, count):
    text = f"People in Frame: {count}"

    cv2.putText(
        frame,
        text,
        (10,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,0,0),
        2
    )

def run_people_counter():

    tracker = load_face_tracker()
    camera = initialize_camera()

    while True:

        ret, frame = camera.read()
        if not ret:
            break

        gray = preprocess_frame(frame)

        faces = detect_faces(tracker, gray)

        frame = draw_faces(frame, faces)

        people_count = len(faces)

        display_people_count(frame, people_count)

        cv2.imshow("Real-Time Face Tracking & People Count", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_people_counter()
