import cv2
import tensorflow as tf
from deepface import DeepFace
import requests

def send_emotion_to_backend(emotion):
    try:
        response = requests.post("http://localhost:5000/emotion", json={"emotion": emotion})
        response.raise_for_status() 
        if response.text:
            print("Songs:", response.json())
        else:
            print("Empty response from backend")
    except Exception as e:
        print("Error sending emotion to backend:", e)

count = 0
cap=cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    try :
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')

        emotion = analysis[0]['dominant_emotion']
        print("Detected Emotion:", emotion)

        send_emotion_to_backend(emotion)
    
    except Exception as e:
        print("Error:", e)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if count == 10:
        break
    count += 1
cap.release()
cv2.destroyAllWindows()
