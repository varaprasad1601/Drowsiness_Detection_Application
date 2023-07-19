import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import math
import numpy as np
import tkinter.messagebox as messagebox


known_faces = {}
names_list = []

# Load the known face encodings from the file
with open("./known_faces.txt", "r") as f:
    for line in f:
        # Split the line into the name and face encoding
        name, face_encoding = line.strip().split(",", 1)
        # Convert the face encoding from a string to a numpy array
        face_encoding = np.array(eval(face_encoding))
        # Add the face encoding to the dictionary
        known_faces[name] = face_encoding
        names_list.append(name)
print(names_list)

if len(names_list) == 0:
    messagebox.showinfo("Users Status", "No User Resistered yet, Please Register")
else:
    face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")

    root = tk.Tk()
    root.geometry("1920x1080")
    frame = Frame(root)
    frame.place(relx=.5, y=320, anchor=CENTER)

    label = Label(frame,width=500, height=500)
    label.pack()
    cap = cv2.VideoCapture(0)    


    global face_encodings
    face_encodings = []

    def encoding(face_encoding):
        user_details = ""
        global login
        login = "False"
        
        # Append the face encoding to the list of face encodings
        face_encodings.append(face_encoding)
        print("face_encodeings_length :",len(face_encodings))
        if len(face_encodings) >= 20:
            encodings = np.concatenate(face_encodings[-5:])

            user_count = 0
            min_list = []

            for user in names_list:
            # Compare the computed face encoding with the stored face encodings for the user
                if user in known_faces:
                    distances = np.linalg.norm(encodings - known_faces[user], axis=1)
                    min_distance = np.min(distances)
                    print(min_distance)
                    min_list.append(min_distance)
            
            min_dist = min(min_list)        
            min_ind = min_list.index(min_dist)
            print("min_ind :",min_ind)
            # Check if the minimum distance is less than a threshold
            if int(min_dist) <= 5:
                user_count = 1
                user_details = names_list[min_ind]
                print("Accessed")
                login = "True"
                # If the distance is less than the threshold, the user is authenticated
                # print("Login Successfully\nWelcome " + user_details)
                # messagebox.showinfo("Login Status","Login Suceess\nWelcome %s"%(user_details))

        if len(face_encodings) == 30:
            if int(min_dist) > 5:
                login = "Error"
                # If the distance is less than the threshold, the user is authenticated
                # print("User not Registered")
                # messagebox.showinfo("Login Status","User Not Registered\nPlease Register")
            else:
                # If the distance is greater than or equal to the threshold, the user is not authenticated
                login = "False"
                # print("Login Failed!!!")
                # messagebox.showinfo("Login Status","Login Faild!!!!\nTry Again")
            face_encodings.clear()
            
        return user_details, login
            
            


    def video():
        user_details, login = ("","")
        ret, frame = cap.read()
        if ret:
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Convert the frame from BGR color to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                face_roi = gray[y:y+h, x:x+w]

                # Resize the face ROI to a fixed size
                face_roi = cv2.resize(face_roi, (32, 32))

                # Normalize the face ROI pixel values to be between 0 and 1
                face_roi = face_roi / 255.0

                # Reshape the face ROI into a 1D numpy array
                face_encoding = face_roi.reshape(1, -1)
                user_details, login = encoding(face_encoding)
                
                print("user_details, login :",user_details, login)
                
            frame = cv2.resize(frame,(500,500))    
            img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        root.after(10, video)
        return user_details, login
    video()



    start_btn = Button(root,text="Start",background="orange",foreground="white",width=62, pady=10,relief="solid",border=0.3, font=("arial bold",10))
    start_btn.place(relx=.5 ,y=620, anchor=CENTER)

    root.mainloop()
