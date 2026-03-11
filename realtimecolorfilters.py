import cv2
import numpy as np


def apply_effect(frame, mode, mirror, zoom):
    h, w = frame.shape[:2]
    output = frame.copy()

    if mode == "negative":
        output = cv2.bitwise_not(output)
    elif mode == "blur":
        output = cv2.GaussianBlur(output, (25, 25), 0)
    elif mode == "pixel":
        small = cv2.resize(output, (w // 20, h // 20), interpolation=cv2.INTER_LINEAR)
        output = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    elif mode == "emboss":
        kernel = np.array([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ]) 
        output = cv2.filter2D(output, -1, kernel) + 188
    elif mode == "threshold":
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        _ , th = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        output = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
    elif mode == "thermal":
        gray  = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        output = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # Apply mirror toggle
    if mirror:
        output = cv2.flip(output, 1)

    # Apply zoom toggle
    if zoom:
        cx, cy = w // 2, h // 2
        crop = output[cy-120:cy+120, cx-160:cx+160]
        output = cv2.resize(crop, (w, h))

    return output


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera initialize failed")
        return
    
    mode = None
    mirror = False
    zoom = False

    print("Keys:")
    print("n=Negative | b=Blur | x=Pixel | e=Emboss")
    print("t=Threshold | m=Thermal")
    print("r=Mirror Toggle | z=Zoom Toggle")
    print("o=Original | q=Quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break

        output = apply_effect(frame, mode, mirror, zoom)
        cv2.imshow("Visual Effects Lab", output)

        key = cv2.waitKey(1) & 0xFF

        # Effect selection
        if key == ord('n'):
            mode = "negative"
        elif key == ord('b'):
            mode = "blur"
        elif key == ord('x'):
            mode = "pixel"
        elif key == ord('e'):
            mode = "emboss"
        elif key == ord('t'):
            mode = "threshold"
        elif key == ord('m'):
            mode = "thermal"
        elif key == ord('r'):
            mirror = not mirror
        elif key == ord('z'):
            zoom = not zoom
        elif key == ord('o'):
            mode = None
            mirror = False
            zoom = False
        elif key == ord('q'):
            break

    cap.release()
    cap.destroyAllWindows()


if __name__ == "__main__":
    main()
    
