import os
import sys
import cv2
import call
import time
import wave
import pyaudio
import requests
import subprocess
import tkinter as tk
import numpy as np
from tkinter import *
import drowsiness_detection
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox






face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")








#============================= Open Known Faces File ===========================================
known_faces = ["no_connection"]
data = []
usernames = ['likku']
def request_data():
    global known_faces, data, usernames
    known_faces.clear()
    data.clear()
    try:
        url = 'http://drowsydetection1601.pythonanywhere.com/app_api'
        response = requests.get(url)
        face_encoding = []
        if response.status_code == 200:
            data = response.json()
            for i in data:
                # print("user == ",i['username'])
                # print(type(i['face_encodings']))
                usernames.append(i['username'])
                face_encoding = i['face_encodings']
                face_encoding = np.array(eval(face_encoding))
                known_faces.append(face_encoding)
            # Process the retrieved data as needed
        else:
            print('Error: Failed to retrieve data. Status code:', response.status_code)
    except:
        print("noconnection")
        known_faces = ["no_connection"]
    return known_faces, data
# request_data()
# print(known_faces)
#============================= Open Known Faces File ===========================================








#==================================== Company api ================================================== 
companies = []
def company_api():
    try:
        companies.clear()
        url = 'http://drowsydetection1601.pythonanywhere.com/company_api'
        response = requests.get(url)
        if response.status_code == 200:
            company_data = response.json()
            for i in company_data:
                companies.append(i['company_name'])
        else:
            print('Error: Failed to retrieve data. Status code:', response.status_code)
    except:
        pass
#==================================== Company api ================================================== 






    
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
face_encodings = []
global login

def encoding(face_encoding):
    global data, face_encodings, known_faces
    login = "False"
    user_details = ""
    # Append the face encoding to the list of face encodings
    face_encodings.append(face_encoding)
    print("face_encodeings_length :",len(face_encodings))
    if len(face_encodings) >= 40 and login == "False":
        encodings = np.concatenate(face_encodings[-30:])

        min_list = []

        # Compare the computed face encoding with the stored face encodings for the user
        for encoding in known_faces:
            distances = np.linalg.norm(encodings - encoding, axis=1)
            min_distance = np.min(distances)
            print(min_distance)
            min_list.append(min_distance)
            
        min_dist = min(min_list)        
        min_ind = min_list.index(min_dist)
        print("min_ind :",min_ind)
        # Check if the minimum distance is less than a threshold
        if min_dist <= 4.2:
            user = data[min_ind]
            user_details = str(user['username'])+"-"+str(user['p_code']).split()[-1]+"-"+str(user['number'])
            print("Accessed")
            login = "True"
            logframe.place_forget()
            label.place_forget()
                
            # If the distance is less than the threshold, the user is authenticated
            print("Login Successfully\nWelcome " + user_details)
            messagebox.showinfo("Login Status","Login Suceess\nWelcome %s"%(user_details.split("-")[0]))
            heading.place_forget()
            

    if len(face_encodings) == 50:
        if min_dist > 4.2:
            user_details = ""
            login = "Error"
            # If the distance is less than the threshold, the user is authenticated
            print("User not Registered")
            messagebox.showinfo("Login Status","Login Faild!!!!\nTry Again")
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
alert_count = 0
sec = 15
start_time = time.time()

state = "pause"

# when start button clicks
def state_start():
    global state
    global start_time
    global alert_count
    state = "start"
    alert_count = 0
    start_time = time.time()
    state_start_btn()
    
# when pause button clicks
def state_pause():
    global state
    state = "pause"
    state_pause_btn()


# Left LabelFrame
left_frame = LabelFrame(root, text=" Video Screening ", bd=1, relief="solid")

img_frame = LabelFrame(left_frame, bd=1, relief="solid")

# Left LabelFrame Image
image_label = Label(left_frame)
    
start = Button(img_frame,text="Start",background="green",foreground="white",activebackground="#46923c",activeforeground="white",pady=6,relief="solid",bd=0.3,cursor="hand2",font=("arial bold",10),command=state_start)
start.place(x=10, y=573,width=295)

pause_btn = Button(img_frame,text="Pause",background="crimson",foreground="white",activebackground="#e13b52",activeforeground="white",pady=6,relief="solid",bd=0.3,cursor="hand2",font=("arial bold",10),command=state_pause,state="disabled")
pause_btn.place(x=314, y=573,width=295)

# after start button clicks
def state_start_btn():
    pause_btn.configure(state="normal",background="crimson")
    start.configure(state="disabled",background="#46923c",foreground="white")

# after pause button clicks
def state_pause_btn():
    start.configure(state="normal",text="Continue",background="green")
    pause_btn.configure(state="disabled",background="#e13b52",foreground="white")
#==================================== Video Capturing tkinter ============================================








#==================================== Video Capturing ============================================
faces_list = []
face = 1
eyes_list = []
eye_open = 1
def start_detection(ret,frame,state, user_details):
    
    logframe.place_forget()
    # Left LabelFrame
    left_frame.place(x=10, y=10, width=680, height=680)
    img_frame.place(rely=0.5, width=620, height=620, relx=0.5, anchor=CENTER)
    # Left LabelFrame Image
    image_label.place(relx=0.5, y=307, anchor=CENTER)    


    # Right LabelFrame
    right_frame = LabelFrame(root, text=" Monitoring ", bd=1, relief="solid")
    right_frame.place(x=720, y=10, width=636, height=680)

    face_frame = LabelFrame(right_frame, bd=1, relief="solid")
    face_frame.place(y=21, x=7, width=300, height=300)

    face_label = Label(face_frame)
    face_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    eye_frame = LabelFrame(right_frame, bd=1, relief="solid")
    eye_frame.place(y=21, x=327, width=300, height=300)
    
    eye_label = Label(eye_frame)
    eye_label.place(relx=0.5, rely=0.5, anchor=CENTER)


    values_frame = LabelFrame(right_frame,text=" Prediction " ,bd=1, relief="solid")
    values_frame.place(y=497, width=620, height=313, relx=0.5, anchor=CENTER)
    
    
    prediction = Label(values_frame,font=("arial bold",50))
    prediction.place(relx=.5,rely=.5,anchor=CENTER)
    
    global start_time, alert_count, faces_list, face, eyes_list, eye_open, sec
    if state == "pause":
        frame = cv2.resize(frame, (600,550))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)
    else:
        frame, faces_list, face , eyes_list, eye_open = drowsiness_detection.main(frame, faces_list, eyes_list, eye_label, face_label)
        
        
        if eye_open == 0:
            prediction.configure(text="Eyes Opened",foreground="green")
        elif eye_open == 1:
            prediction.configure(text="Eyes Closed",foreground="red")
        else:
            prediction.configure(text="No Eye Detected",foreground="blue")
        
        
        if len(face) == 0:
            prediction.configure(text="No Face Detected",foreground="blue")
            alert_count, sec = time_check(start_time, faces_list, alert_count, sec, eye_open, user_details)
        elif eye_open == 1:
            alert_count, sec = time_check(start_time, eyes_list, alert_count, sec, eye_open, user_details)
        elif eye_open == None:
            alert_count, sec = time_check(start_time, eyes_list, alert_count, sec, eye_open, user_details)
        else:
            alert_count = 0
            start_time = time.time()


        frame = cv2.resize(frame, (600,550))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)
#==================================== Video Capturing ============================================








#==================================== Alert function ==================================================
def play_alert():
    # set the file name and open the file
    filename = "./media/alarm.wav"
    wf = wave.open(filename, 'rb')

    # instantiate PyAudio
    p = pyaudio.PyAudio()

    # open a stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data and play audio
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # close the stream and terminate PyAudio
    stream.close()
    p.terminate()

    return True
#==================================== Alert function ==================================================








#==================================== Time Check function ============================================
def time_check(start_time, obj_list, alert_count, sec, eye_open, user_details):
    global cap
    br = False
    alert = False
    obj_list_range = obj_list[-11:]
    res = max(set(obj_list_range), key = obj_list_range.count)
    elapsed_time = time.time() - start_time
    print("start_time :",start_time,"---------> elapsed_time :",elapsed_time)

    print("obj_list_range: ",obj_list_range)
    print("res :",res)
    if int((elapsed_time+1)%sec) == 0:
        if eye_open == None:
            messagebox.showwarning("warning","No Eyes Detected") 
        else:
            if res == 0:
                sec = 15
                alert = play_alert()
                if alert:
                    alert_count +=1
                    print("alert_alert:",alert)
                    print("alert_count:",alert_count)
                    obj_list.clear()
                    if alert_count == 2:
                        sec = 15
                        phone_code = user_details.split("-")[1]
                        print("phooooooooooooooooooooooooooooone :",phone_code)
                        mobile_number = user_details.split("-")[2]
                        print(mobile_number)
                        try:
                            calling = call.call_to_user(phone_code,mobile_number)
                            print(calling)
                            if calling == "connection_error":
                                messagebox.showinfo("Network Status", "           No Internet Connection \n\t            or\nMobile number not registered in twillio")
                                cap.release()
                                cv2.destroyAllWindows()
                                root.destroy()
                        except:
                            messagebox.showinfo("Network Status", "error at call function")
                            print("********** error at call function **********")
                    elif alert_count == 3:
                        # br = True
                        cap.release()
                        cv2.destroyAllWindows()
                        root.destroy()
                        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
                        subprocess.call([sys.executable, os.path.realpath(__file__)]+sys.argv[1:])
                        sys.exit()
                else:
                    pass
            else:
                sec = 15
                print("alert_alert:",alert)
                alert_count = 0
    return alert_count, sec
#==================================== Time Check function ============================================








#==================================== Video Display ============================================
# initializing the camera
cap = cv2.VideoCapture(0)

login_status = "False"
user_details, login = ("","")

def video():
    global login_status, user_details, login, state, known_faces
    if len(known_faces) == 0:
        messagebox.showinfo("Users Status", "No User Resistered yet, Please Register")
    elif known_faces[0] == "no_connection":
        request_data()
        if known_faces[0] == "no_connection":
            messagebox.showinfo("Network Status", "No Internet Connection or Server Problem")
        else:
            video()
    else:
        login_btn.place_forget()
        register_btn.place_forget()
        # heading.place_forget()
        logframe.place(relx=.5, y=400, anchor=CENTER,width=518,height=450)
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        if ret:
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            if login_status == "True":
                start_detection(ret, frame, state, user_details)
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







#==================================== Training Data =================================================
training_list = []
def training_data(face_encoding):
    global trained_data, end_loop
    training_list.append(face_encoding)
    # print("face_encodeings_length :",len(training_list))
    if len(training_list) >= 40:
        encodings = np.concatenate(training_list[-30:])
        trained_data = str(face_encoding.tolist())
        end_loop = 'True'
        
    return trained_data, end_loop
#==================================== Training Data ================================================= 







#==================================== Train Data =================================================
# Left LabelFrame
left_reg_frame = Frame(root)

# Right LabelFrame
right_reg_frame = Frame(root)

    
video_label = Label(right_reg_frame)

end_loop = 'Fase'
trained_data = ""
def train_function():
    reg_cap = cv2.VideoCapture(0)
    def train_data():
        global video_label, end_loop, trained_data, train_btn
        ret, frame = reg_cap.read()
        frame = cv2.flip(frame,1)
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
                
                trained_data, end_loop = training_data(face_encoding)
                
            frame = cv2.resize(frame,(530,385))    
            img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        if end_loop == 'True':
            video_label.place_forget()
            train_btn.configure(text="Data Trained", state='disabled',bg='#f09380',fg='white')
            reg_cap.release()
            cv2.destroyAllWindows()
        else:
            root.after(10, train_data)
    train_data()
        
train_btn = Button(left_reg_frame,width=51,pady=7,text='Face Recognition',bg='#f08080',fg='white',cursor="hand2",relief="solid",border=0.3,font=("arial bold",10),activebackground="#f09380",activeforeground="white",command=train_function)
#==================================== Train Data =================================================








#==================================== Register =================================================
def register_function():
    company_api()
    global known_faces, data, companies
    if known_faces == ["no_connection"]:
        request_data()
        if known_faces[0] == "no_connection":
            messagebox.showinfo("Network Status", "No Internet Connection or Server Problem")
        else:
            register_function()
    else:
        global trained_data
        login_btn.place_forget()
        register_btn.place_forget()
        heading.place_forget()
        
        # Left LabelFrame
        left_reg_frame.place(x=10, y=70, width=680, height=570) 
        
        
        reg_heading = Label(left_reg_frame,text="Register",fg='#187bcd',font=("arial",23,'bold'),pady="10")
        reg_heading.place(relx=.5, y=50, anchor=CENTER)
        
        
        # Right LabelFrame
        right_reg_frame.place(x=720, y=70, width=680, height=570)
        
        video_label.place(x=270, rely=.5, anchor=CENTER)
        
        
        
        def register():
            global trained_data, usernames
            validation = 'True'
            username = name.get()
            ph_code = pclicked.get()
            pnumber = number.get()
            ccompany = clicked.get()
            if username == "Username":
                messagebox.showinfo('Validation','Enter Username')
                validation = 'False'
            elif username in usernames:
                messagebox.showinfo('Validation','Username Name Already Exixts')
                validation = 'False'
            elif ph_code == "Phone Code":
                messagebox.showinfo('Validation','Select Phone Code')
                validation = 'False'
            elif pnumber == "Mobile Number":
                messagebox.showinfo('Validation','Enter Mobile Number')
                validation = 'False'
            elif not pnumber.isnumeric():
                messagebox.showinfo('Validation','Enter Valid Mobile Number')
                validation = 'False'
            elif ccompany == "Company / Institutation":
                messagebox.showinfo('Validation','Select Company / Institutation')
                validation = 'False'
            elif len(trained_data) == 0:
                messagebox.showinfo('Validation','Face Recognition not done')
                validation = 'False'
            else:
                if validation == 'True':
                    # Define the base URL
                    base_url = "https://drowsydetection1601.pythonanywhere.com//user_register"
                    # Define the data to be sent
                    data = {'name': username, 'p_code': ph_code, 'number': pnumber, 'company': ccompany, 'face_encodings': trained_data,}

                    # Send the request with data
                    response = requests.post(base_url, data=data)
                    print(response)

                    # Check the response
                    if response.status_code == 200:
                        print("Request was successful.")
                        messagebox.showinfo('Validation','Successfully Registered')
                        request_data()
                        back()
                    else:
                        messagebox.showinfo('Validation','Registration Failed!!')
                        print("Request failed with status code:", response.status_code)
            
        
        # username =====================================================================================
        def on_enter(e):
            username = name.get()
            if username == 'Username':
                name.delete(0,'end')
        def on_leave(e):
            username = name.get()
            if username == '':
                name.insert(0,'Username')
        name = Entry(left_reg_frame,width=50,fg='gray',bg='SystemButtonFace',border=0,font=("arial",11))
        name.place(relx=.5, y=125, anchor=CENTER)
        name.insert(0,'Username')
        name.bind('<FocusIn>',on_enter)
        name.bind('<FocusOut>',on_leave)
        Frame(left_reg_frame,width=415,height=2,bg='black').place(relx=.5, y=140, anchor=CENTER)
        
        
        
        # phone codes =====================================================================================
        codes_list = ['Afghanistan +93', 'Aland Islands +358', 'Albania +355', 'Algeria +213', 'AmericanSamoa +1684', 'Andorra +376', 'Angola +244', 'Anguilla +1264', 'Antarctica +672', 'Antigua and Barbuda +1268', 'Argentina +54', 'Armenia +374', 'Aruba +297', 'Australia +61', 'Austria +43', 'Azerbaijan +994', 'Bahamas +1242', 'Bahrain +973', 'Bangladesh +880', 'Barbados +1246', 'Belarus +375', 'Belgium +32', 'Belize +501', 'Benin +229', 'Bermuda +1441', 'Bhutan +975', 'Bolivia, Plurinational State of +591', 'Bosnia and Herzegovina +387', 'Botswana +267', 'Brazil +55', 'British Indian Ocean Territory +246', 'Brunei Darussalam +673', 'Bulgaria +359', 'Burkina Faso +226', 'Burundi +257', 'Cambodia +855', 'Cameroon +237', 'Canada +1', 'Cape Verde +238', 'Cayman Islands + 345', 'Central African Republic +236', 'Chad +235', 'Chile +56', 'China +86', 'Christmas Island +61', 'Cocos (Keeling) Islands +61', 'Colombia +57', 'Comoros +269', 'Congo +242', 'Congo, The Democratic Republic of the Congo +243', 'Cook Islands +682', 'Costa Rica +506', "Cote d'Ivoire +225", 'Croatia +385', 'Cuba +53', 'Cyprus +357', 'Czech Republic +420', 'Denmark +45', 'Djibouti +253', 'Dominica +1767', 'Dominican Republic +1849', 'Ecuador +593', 'Egypt +20', 'El Salvador +503', 'Equatorial Guinea +240', 'Eritrea +291', 'Estonia +372', 'Ethiopia +251', 'Falkland Islands (Malvinas) +500', 'Faroe Islands +298', 'Fiji +679', 'Finland +358', 'France +33', 'French Guiana +594', 'French Polynesia +689', 'Gabon +241', 'Gambia +220', 'Georgia +995', 'Germany +49', 'Ghana +233', 'Gibraltar +350', 'Greece +30', 'Greenland +299', 'Grenada +1473', 'Guadeloupe +590', 'Guam +1671', 'Guatemala +502', 'Guernsey +44', 'Guinea +224', 'Guinea-Bissau +245', 'Guyana +595', 'Haiti +509', 'Holy See (Vatican City State) +379', 'Honduras +504', 'Hong Kong +852', 'Hungary +36', 'Iceland +354', 'India +91', 'Indonesia +62', 'Iran, Islamic Republic of Persian Gulf +98', 'Iraq +964', 'Ireland +353', 'Isle of Man +44', 'Israel +972', 'Italy +39', 'Jamaica +1876', 'Japan +81', 'Jersey +44', 'Jordan +962', 'Kazakhstan +77', 'Kenya +254', 'Kiribati +686', "Korea, Democratic People's Republic of Korea +850", 'Korea, Republic of South Korea +82', 'Kuwait +965', 'Kyrgyzstan +996', 'Laos +856', 'Latvia +371', 'Lebanon +961', 'Lesotho +266', 'Liberia +231', 'Libyan Arab Jamahiriya +218', 'Liechtenstein +423', 'Lithuania +370', 'Luxembourg +352', 'Macao +853', 'Macedonia +389', 'Madagascar +261', 'Malawi +265', 'Malaysia +60', 'Maldives +960', 'Mali +223', 'Malta +356', 'Marshall Islands +692', 'Martinique +596', 'Mauritania +222', 'Mauritius +230', 'Mayotte +262', 'Mexico +52', 'Micronesia, Federated States of Micronesia +691', 'Moldova +373', 'Monaco +377', 'Mongolia +976', 'Montenegro +382', 'Montserrat +1664', 'Morocco +212', 'Mozambique +258', 'Myanmar +95', 'Namibia +264', 'Nauru +674', 'Nepal +977', 'Netherlands +31', 'Netherlands Antilles +599', 'New Caledonia +687', 'New Zealand +64', 'Nicaragua +505', 'Niger +227', 'Nigeria +234', 'Niue +683', 'Norfolk Island +672', 'Northern Mariana Islands +1670', 'Norway +47', 'Oman +968', 'Pakistan +92', 'Palau +680', 'Palestinian Territory, Occupied +970', 'Panama +507', 'Papua New Guinea +675', 'Paraguay +595', 'Peru +51', 'Philippines +63', 'Pitcairn +872', 'Poland +48', 'Portugal +351', 'Puerto Rico +1939', 'Qatar +974', 'Romania +40', 'Russia +7', 'Rwanda +250', 'Reunion +262', 'Saint Barthelemy +590', 'Saint Helena, Ascension and Tristan Da Cunha +290', 'Saint Kitts and Nevis +1869', 'Saint Lucia +1758', 'Saint Martin +590', 'Saint Pierre and Miquelon +508', 'Saint Vincent and the Grenadines +1784', 'Samoa +685', 'San Marino +378', 'Sao Tome and Principe +239', 'Saudi Arabia +966', 'Senegal +221', 'Serbia +381', 'Seychelles +248', 'Sierra Leone +232', 'Singapore +65', 'Slovakia +421', 'Slovenia +386', 'Solomon Islands +677', 'Somalia +252', 'South Africa +27', 'South Sudan +211', 'South Georgia and the South Sandwich Islands +500', 'Spain +34', 'Sri Lanka +94', 'Sudan +249', 'Suriname +597', 'Svalbard and Jan Mayen +47', 'Swaziland +268', 'Sweden +46', 'Switzerland +41', 'Syrian Arab Republic +963', 'Taiwan +886', 'Tajikistan +992', 'Tanzania, United Republic of Tanzania +255', 'Thailand +66', 'Timor-Leste +670', 'Togo +228', 'Tokelau +690', 'Tonga +676', 'Trinidad and Tobago +1868', 'Tunisia +216', 'Turkey +90', 'Turkmenistan +993', 'Turks and Caicos Islands +1649', 'Tuvalu +688', 'Uganda +256', 'Ukraine +380', 'United Arab Emirates +971', 'United Kingdom +44', 'United States +1', 'Uruguay +598', 'Uzbekistan +998', 'Vanuatu +678', 'Venezuela, Bolivarian Republic of Venezuela +58', 'Vietnam +84', 'Virgin Islands, British +1284', 'Virgin Islands, U.S. +1340', 'Wallis and Futuna +681', 'Yemen +967', 'Zambia +260', 'Zimbabwe +263']
        pclicked =StringVar()
        pclicked.set("Phone Code")
        p_code = OptionMenu(left_reg_frame,pclicked,*codes_list)
        p_code.place(x=130, y=185)
        p_code.configure(width=14,border=0,fg='gray',font=("arial",11))
        Frame(left_reg_frame,width=150,height=2,bg='black').place(x=134, y=215)
        
        
        
        # mobile number =====================================================================================
        def on_enter(e):
            phone = number.get()
            if phone == 'Mobile Number':
                number.delete(0,'end')
        def on_leave(e):
            phone = number.get()
            if phone == '':
                number.insert(0,'Mobile Number')
                
            
        number = Entry(left_reg_frame,width=29,fg='gray',bg='SystemButtonFace',border=0,font=("arial",11))
        number.place(x=306, y=190)
        number.insert(0,'Mobile Number')
        number.bind('<FocusIn>',on_enter)
        number.bind('<FocusOut>',on_leave)
        Frame(left_reg_frame,width=248,height=2,bg='black').place(x=300, y=215)



        # company =====================================================================================
        company_list = companies
        clicked =StringVar()
        clicked.set("Company / Institutation")
        company = OptionMenu(left_reg_frame,clicked,*company_list)
        company.place(relx=.5, y=278, anchor=CENTER)
        company.configure(width=47,border=0,fg='gray',font=("arial",11))
        Frame(left_reg_frame,width=415,height=2,bg='black').place(relx=.5, y=295, anchor=CENTER)


        
        # Train button =====================================================================================        
        train_btn.place(relx=.5, y=370, anchor=CENTER)
        print(trained_data)
        print(len(trained_data))
        
        # register button =====================================================================================
        Button(left_reg_frame,width=51,pady=7,text='Register',bg='#187bcd',fg='white',cursor="hand2",relief="solid",border=0.3,font=("arial bold",10),activebackground="#57a1f8",activeforeground="white",command=register).place(relx=.5, y=455, anchor=CENTER)
        
        # Back button =====================================================================================
        def back():
            left_reg_frame.place_forget()
            right_reg_frame.place_forget()
            register_btn.place(relx=.5 ,y=300, anchor=CENTER)
            login_btn.place(relx=.5 ,y = 370, anchor=CENTER)
            heading.place(relx=.5, y=100, anchor=CENTER)
            clear()
        def clear():
            global trained_data, training_list, end_loop
            name.delete(0,'end')
            name.insert(0,'Username')
            pclicked.set("Phone Code")
            number.delete(0,'end')
            number.insert(0,'Mobile Number')
            clicked.set("Company / Institutation")
            end_loop = 'False'
            trained_data = ""
            training_list.clear()
            train_btn.configure(text="Face Recognition", state='normal',bg='#f08080',fg='white')
            video_label.place(x=270, rely=.5, anchor=CENTER)
            video_label.configure(image="")
        Button(left_reg_frame,text='Clear',fg='#187bcd',bg='SystemButtonFace',border=0,cursor="hand2",font=("arial bold",10),activeforeground="#57a1f8",command=clear).place(relx=.5, y=525, anchor=CENTER)    
        Button(left_reg_frame,text='Back to Home',fg='#187bcd',bg='SystemButtonFace',border=0,cursor="hand2",font=("arial bold",10),activeforeground="#57a1f8",command=back).place(relx=.5, y=550, anchor=CENTER)
#==================================== Register =================================================








#==================================== Buttons =================================================
register_btn = Button(root,text="Register",background="#1167b1",cursor="hand2",foreground="white",width=62, pady=10,relief="solid",border=0.3,activebackground="#187bcd",activeforeground="white",font=("arial bold",10),command=register_function)
register_btn.place(relx=.5 ,y=300, anchor=CENTER)

login_btn = Button(root,text="Login",background="orange",cursor="hand2",foreground="white",width=62, pady=10,relief="solid",border=0.3,activebackground="#ffbf10",activeforeground="white", font=("arial bold",10),command=video)
login_btn.place(relx=.5 ,y = 370, anchor=CENTER)
#==================================== Buttons =================================================

root.mainloop()
