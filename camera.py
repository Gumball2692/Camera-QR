from time import sleep
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import serial
from threading import Thread
import threading
import time
try:
  ser = serial.Serial('/dev/ttyACM0')
except:
  print("Create serial failed")
i = 0
global bbox
global data
dataImage = "" 
bboxImage = "" 
_ = ""
flagVar = 0
root = Tk()
detector = cv2.QRCodeDetector()
root.geometry("700x700")
root.configure(bg="black")
Label(root, text="Anh Quân", font=("time new roman", 30, "bold"), bg="black", fg = "blue").pack()
Label(root, text="Đọc QR code", font=("time new roman", 30, "bold"), bg="black", fg = "red").pack()
f1 = LabelFrame(root, bg = "red")
f1.pack()
L1 = Label(f1, bg = "red")
L1.pack()
cap = cv2.VideoCapture(2)
def thread_function():
    while True:
        print ("Message from arduino: ")
        msg = b""
        try:
          msg = ser.readline()
        except Exception as e:
          print("serial readline failed")
          raise e 
        print(msg.decode())
def thread_function_2():
    while True:
      if bboxImage is not None and dataImage != "":
        try:
          ser.write(dataImage.encode())
        except:
          print("Serial write failed")        
        time.sleep(5)
if __name__ == "__main__":
  t1 = threading.Thread(target=thread_function)
  t1.start()
  t2 = threading.Thread(target=thread_function_2)
  t2.start()
  while True:
      img = cap.read()[1]
      dataImage, bboxImage, _ = detector.detectAndDecode(img)
      if flagVar == 0:
        flagVar = 1
      img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
      img = ImageTk.PhotoImage(Image.fromarray(img))
      L1['image'] = img
      root.update()
      