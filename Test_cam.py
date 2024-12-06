import cv2
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Failed to open camera")
else:
    print("Camera initialized successfully")
    camera.release()