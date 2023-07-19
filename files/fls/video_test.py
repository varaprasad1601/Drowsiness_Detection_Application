import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import math
import numpy as np
import tkinter.messagebox as messagebox

root = tk.Tk()
root.geometry("1920x1080")
frame = Frame(root)
frame.place(relx=.5, y=320, anchor=CENTER)

label = Label(frame,width=500, height=500)
label.pack()
cap = cv2.VideoCapture(0) 
    
def play_video():
    ret, frame = cap.read()
    if ret: 
        frame = cv2.resize(frame,(500,500))    
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    root.after(10, play_video)



root.mainloop()