import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image, ImageTk








face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("./haarcascade/eye.xml")
close_eye_cascade = cv2.CascadeClassifier("./haarcascade/cascade.xml")
model = load_model("./files/dnn_model.h5")
print(model)
faces = []
eyes = []








# ====================================== Face Detect Fuction ====================================
def detect_face(frame, faces_list, eyes_list, eye_label, face_label):
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
        
        face_img = cv2.resize(roi_face, (300, 300))
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        face_img = Image.fromarray(face_img)
        face_imgtk = ImageTk.PhotoImage(image=face_img)
        face_label.img1tk = face_imgtk
        face_label.configure(image=face_imgtk)
        # cv2.imshow("roi",roi_face)

        # Detect eyes and extract
        eye = eye_cascade.detectMultiScale(roi_face, 1.1, 3)
        if len(eye)>0:
            predicted_class = detect_eyes(roi_face, eye, eye_label)
        else:
            eye = close_eye_cascade.detectMultiScale(roi_face, 1.1, 3)
            predicted_class = detect_eyes(roi_face, eye, eye_label)
            
            
        if predicted_class == 0:
            eyes_list.append(1)
        else:
            eyes_list.append(0)
            
    return faces_list, face, eyes_list, predicted_class
# ====================================== Face Detect Fuction ====================================








# =================================== Detect Eyes and Predict Fuction =============================
def detect_eyes(roi_face, eye, eye_label):
    # Iterate over each detected eye
    for (ex, ey, ew, eh) in eye:
        # Draw a rectangle around the eye
        #cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Check if the eye is on the left or right side of the face
        roi_eye = roi_face[ey:ey+eh, ex:ex+ew]
        
        eye_img = cv2.resize(roi_eye, (300, 300))
        eye_img1 = cv2.cvtColor(eye_img, cv2.COLOR_BGR2RGB)
        eye_img1 = Image.fromarray(eye_img1)
        eye_img1tk = ImageTk.PhotoImage(image=eye_img1)
        eye_label.eye_img1tk = eye_img1tk
        eye_label.configure(image=eye_img1tk)

        # cv2.imshow("roi_frame",roi_eye)

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
        cv2.putText(roi_face, label, (ex, ey-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

        return predicted_class
# =================================== Detect Eyes and Predict Fuction =============================








# ========================================== Main Function =====================================
def main(frame, faces_list, eyes_list, eye_label, face_label):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_list, face , eyes_list, eye_open = detect_face(frame, faces_list, eyes_list, eye_label, face_label)
        
    return frame, faces_list, face , eyes_list, eye_open
# ========================================== Main Function =====================================
