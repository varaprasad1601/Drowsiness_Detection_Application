import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import math
import numpy as np
import tkinter.messagebox as messagebox
import webbrowser
import drowsiness_detection






face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")







#============================= Open Known Faces File ===========================================
known_faces = {}
names_list = []

# Load the known face encodings from the file
with open("./files/known_faces.txt", "r") as f:
    for line in f:
        # Split the line into the name and face encoding
        name, face_encoding = line.strip().split(",", 1)
        # Convert the face encoding from a string to a numpy array
        face_encoding = np.array(eval(face_encoding))
        # Add the face encoding to the dictionary
        known_faces[name] = face_encoding
        names_list.append(name)
print(names_list)
#============================= Open Known Faces File ===========================================







    
#==================================== Tkinter ================================================== 
root = tk.Tk()
root.title("Drowsiness Detection System")
logo = PhotoImage(file="./media/icon.png")
root.iconphoto(False,logo)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.geometry("%dx%d+0+0"%(width,height))
logframe = LabelFrame(root,bd=1,relief="solid")

label = Label(logframe,width=500, height=438)
label.place(relx=.5, rely=.5, anchor=CENTER)
    
heading = Label(root,text="Drowsiness Detection System",font=("arial bold",30),pady="10")
heading.place(relx=.5, y=100, anchor=CENTER)
#==================================== Tkinter ================================================== 








#==================================== Encoding Face ============================================
global face_encodings
face_encodings = []
global login

def encoding(face_encoding):
    login = "False"
    user_details = ""
    # Append the face encoding to the list of face encodings
    face_encodings.append(face_encoding)
    print("face_encodeings_length :",len(face_encodings))
    if len(face_encodings) >= 20:
        encodings = np.concatenate(face_encodings[-5:])

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
            user_details = names_list[min_ind]
            print("Accessed")
            login = "True"
            logframe.place_forget()
            label.place_forget()
            # cap.release()
                
            # If the distance is less than the threshold, the user is authenticated
            print("Login Successfully\nWelcome " + user_details)
            messagebox.showinfo("Login Status","Login Suceess\nWelcome %s"%(user_details))
            heading.place_forget()
            
            # greetings = Label(root,text="Welcome",font=("cambria",30),pady="40")
            # greetings.place(relx=.5, y=250, anchor=CENTER)
            # user_name = Label(root,text=user_details.split("-")[0],font=("Frunch",15),pady="10")
            # user_name.place(relx=.5, y=300, anchor=CENTER)
            # Frunch Youthome cambria
            
            
            
#==================================== Detection Function =================================================
            # def hide_show():
            #     continue_btn.place_forget()
            #     greetings.place_forget()
            #     user_name.place_forget()
            #     heading.place_forget()
#==================================== Detection Function =================================================
            
            
            
            # continue_btn = Button(root,text="Start Detection",background="green",foreground="white",relief="solid",border=0.3,font=("arial bold",10),activebackground="#46923c",activeforeground="white",pady=10,width=62,command=hide_show)
            # continue_btn.place(relx=.5, y=420, anchor=CENTER)

    if len(face_encodings) == 30:
        if int(min_dist) > 5:
            user_details = ""
            login = "Error"
            # If the distance is less than the threshold, the user is authenticated
            print("User not Registered")
            messagebox.showinfo("Login Status","User Not Registered\nPlease Register")
        else:
            # If the distance is greater than or equal to the threshold, the user is not authenticated
            user_details = ""
            login = "False"
            print("Login Failed!!!")
            messagebox.showinfo("Login Status","Login Faild!!!!\nTry Again")
        face_encodings.clear()
            
    return user_details, login
#==================================== Encoding Face ============================================









#==================================== Video Capturing tkinter ============================================
# Left LabelFrame
left_frame = LabelFrame(root, text=" Video Screening ", bd=1, relief="solid")

img_frame = LabelFrame(left_frame, bd=1, relief="solid")

# Left LabelFrame Image
image_label = Label(left_frame)
    
continue_btn = Button(img_frame,text="Continue",background="green",foreground="white",activebackground="#46923c",activeforeground="white",pady=6,relief="solid",bd=0.3,cursor="hand2",font=("arial bold",10))
continue_btn.place(x=10, y=573,width=295)

pause_btn = Button(img_frame,text="Pause",background="crimson",foreground="white",activebackground="#e13b52",activeforeground="white",pady=6,relief="solid",bd=0.3,cursor="hand2",font=("arial bold",10))
pause_btn.place(x=314, y=573,width=295)
#==================================== Video Capturing tkinter ============================================









#==================================== Video Capturing ============================================
def start_detection(ret,frame):
    # Left LabelFrame
    left_frame.place(x=10, y=10, width=680, height=680)
    img_frame.place(rely=0.5, width=620, height=620, relx=0.5, anchor=CENTER)
    # Left LabelFrame Image
    image_label.place(relx=0.5, y=307, anchor=CENTER)    


    # Right LabelFrame
    right_frame = LabelFrame(root, text=" Monitoring ", bd=1, relief="solid")
    right_frame.place(x=720, y=10, width=636, height=680)

    eye_frame = LabelFrame(right_frame, bd=1, relief="solid")
    eye_frame.place(y=21, x=7, width=300, height=300)

    eye_label = Label(eye_frame)
    eye_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    prediction_frame = LabelFrame(right_frame, bd=1, relief="solid")
    prediction_frame.place(y=21, x=327, width=300, height=300)

    values_frame = LabelFrame(right_frame,text=" Prediction " ,bd=1, relief="solid")
    values_frame.place(y=497, width=620, height=313, relx=0.5, anchor=CENTER)
    
    drowsiness_detection.main(frame)
    
    if ret:
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            org_frame = frame
            roi = frame[y:y+h, x:x+w]
            roi_img = cv2.resize(roi, (300, 300))
            img1 = cv2.cvtColor(roi_img, cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(img1)
            img1tk = ImageTk.PhotoImage(image=img1)
            eye_label.img1tk = img1tk
            eye_label.configure(image=img1tk)
            cv2.rectangle(org_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        frame = cv2.resize(frame, (600, 550))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)
#==================================== Video Capturing ============================================









#==================================== Video Display ============================================
# initializing the camera
cap = cv2.VideoCapture(0)

login_status = "False"
def video():
    logframe.place(relx=.5, y=400, anchor=CENTER,width=518,height=450)
    global login_status
    if len(names_list) == 0:
        messagebox.showinfo("Users Status", "No User Resistered yet, Please Register")
    else:
        login_btn.place_forget()
        register_btn.place_forget()
        # heading.place_forget()
        user_details, login = ("","")
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        if ret:
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            if login_status == "True":
                start_detection(ret,frame)
            else:
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
                    login_status = login
                    print("false login status ===============",login_status)
                    print("user_details, login :",user_details, login)
                    
           
            frame = cv2.resize(frame,(500,432))    
            img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            
        if login_status == "True":
            root.after(10, video)
        else:
            root.after(10, video)
#==================================== Video Display ============================================








#==================================== Register =================================================
def register_function():
    webbrowser.open("https://irctctrainticketextracter.pythonanywhere.com/")
#==================================== Register =================================================








#==================================== Buttons =================================================
register_btn = Button(root,text="Register",background="#1167b1",cursor="hand2",foreground="white",width=62, pady=10,relief="solid",border=0.3,activebackground="#187bcd",activeforeground="white",font=("arial bold",10),command=register_function)
register_btn.place(relx=.5 ,y=300, anchor=CENTER)

login_btn = Button(root,text="Login",background="orange",cursor="hand2",foreground="white",width=62, pady=10,relief="solid",border=0.3,activebackground="#ffbf10",activeforeground="white", font=("arial bold",10),command=video)
login_btn.place(relx=.5 ,y = 370, anchor=CENTER)
#==================================== Buttons =================================================

root.mainloop()