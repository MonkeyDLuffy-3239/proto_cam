import cv2
from flask import Flask, Response

app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)  # Try 1, 2, or other indices if 0 doesn't work
if not camera.isOpened():
    print("Error: Could not access the camera. Check camera index and permissions.")
    exit()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            print("Error: Failed to read frame from camera.")
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame.")
                break
            frame = buffer.tobytes()
            # Yield frame as byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
        <html>
            <head><title>Live Camera Feed</title></head>
            <body>
                <h1>Live Camera Feed</h1>
                <img src="/video_feed">
            </body>
        </html>
    '''

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error: {e}")
