import cv2
import base64
import time

def start_cam():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if not cap.isOpened():
        print("Failed to open camera.")
        exit()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame.")
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            with open("image.txt", "w") as f:
                f.write(img_base64)
            time.sleep(3) 

    except KeyboardInterrupt:
        print("Stopped by user.")

    finally:
        cap.release()
        print("Camera released.")

def get_base64():
    try:
        with open("image.txt", "r") as f:
            img_base64 = f.read()
        return img_base64
    except FileNotFoundError:
        return None 

if __name__ == '__main__':
    start_cam()