import os
import cv2
import call
import time
import math
import wave
import pyaudio
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array








face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("./haarcascade/eye.xml")
close_eye_cascade = cv2.CascadeClassifier("./haarcascade/cascade.xml")
model = load_model("./files/dnn_model.h5")
print(model)
faces = []
eyes = []








# ====================================== Face Detect Fuction ====================================
def detect_face(frame, faces_list, eyes_list):
    predicted_class = 1
    face = face_cascade.detectMultiScale(frame, 1.3, 5)

    if len(face)>0:
        faces_list.append(1)
    else:
        faces_list.append(0)
        
    for (x, y, w, h) in face:
        
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract the region of interest (ROI) which is the face area
            roi_face = frame[y:y+h, x:x+w]
            cv2.imshow("roi",roi_face)

            # Detect eyes and extract
            eye = eye_cascade.detectMultiScale(roi_face, 1.1, 3)
            if len(eye)>0:
                predicted_class = detect_eyes(roi_face, eye)
            else:
                eye = close_eye_cascade.detectMultiScale(roi_face, 1.1, 3)
                predicted_class = detect_eyes(roi_face, eye)

            if predicted_class == 0:
                eyes_list.append(1)
            else:
                eyes_list.append(0)


            
    return faces_list, face, eyes_list, predicted_class
# ====================================== Face Detect Fuction ====================================








# =================================== Detect Eyes and Predict Fuction =============================
def detect_eyes(roi_face, eye):
    # Iterate over each detected eye
    for (ex, ey, ew, eh) in eye:
        # Draw a rectangle around the eye
        #cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Check if the eye is on the left or right side of the face
        roi_eye = roi_face[ey:ey+eh, ex:ex+ew]

        cv2.imshow("roi_frame",roi_eye)

        # Resize the face region to match the input shape of the model
        roi_eye = cv2.resize(roi_eye, (64, 64))
        
        # Convert the face region to a numpy array
        roi_array = img_to_array(roi_eye)
        
        # Reshape the numpy array to match the input shape of the model
        roi_array = roi_array.reshape(1, 64, 64, 1)
        
        # Make a prediction using the model
        prediction = model.predict(roi_array)
        
        # Get the predicted class index
        predicted_class = np.argmax(prediction)
        print("predicted_class :", predicted_class)

        # Draw a rectangle around the detected face
        cv2.rectangle(roi_face, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
        
        # Draw a label for the predicted class on the frame
        label = "Open Eyes" if predicted_class == 0 else "Closed Eyes"
        cv2.putText(roi_face, label, (ex, ey-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 2)

        return predicted_class
# =================================== Detect Eyes and Predict Fuction =============================








# ========================================== Main Function =====================================
def main(frame, faces_list, eyes_list):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_list, face , eyes_list, eye_open = detect_face(frame, faces_list, eyes_list)
        
    return frame, faces_list, face , eyes_list, eye_open
# ========================================== Main Function =====================================
