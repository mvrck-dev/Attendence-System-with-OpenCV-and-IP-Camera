import os
import cv2 as cv
import numpy as np
import pandas as pd  # Import pandas
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Function to choose laptop camera
def start_laptop_camera(id):
    print("Starting Laptop Camera...")
    camera = cv.VideoCapture(0)
    face_classifier = cv.CascadeClassifier('Classifiers/haarface.xml')
    
    photos_taken = 0

    while True:
        _, img = camera.read()
        grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            face_region = grey[y:y + h, x:x + w]
            if cv.waitKey(1) & 0xFF == ord('s') and np.average(face_region) > 50:
                face_img = cv.resize(face_region, (220, 220))
                img_name = f'face.{id}.{datetime.now().microsecond}.jpeg'
                cv.imwrite(f'faces/{id}/{img_name}', face_img)
                photos_taken += 1
                print(f'{photos_taken} -> Photos taken!')

        cv.imshow('Face', img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv.destroyAllWindows()

# Function to choose IP camera
def start_ip_camera(id):
    print("Starting IP Camera...")

    rtsp_url = 'rtsp://admin:admin123@192.168.128.10:554/avstream/channel=1/stream=1-substream.sdp'
    cap = cv.VideoCapture(rtsp_url)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video stream.")
        return

    face_classifier = cv.CascadeClassifier('Classifiers/haarface.xml')
    photos_taken = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to retrieve frame.")
            break

        grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            face_region = grey[y:y + h, x:x + w]
            if cv.waitKey(1) & 0xFF == ord('s') and np.average(face_region) > 50:
                face_img = cv.resize(face_region, (220, 220))
                img_name = f'face.{id}.{datetime.now().microsecond}.jpeg'
                cv.imwrite(f'faces/{id}/{img_name}', face_img)
                photos_taken += 1
                print(f'{photos_taken} -> Photos taken!')

        cv.imshow('IP Camera Live Feed', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def capture_photos():
    ID_NAMES_FILE = 'id-names.csv'

    # Create the file and directory if they don't exist
    if not os.path.exists(ID_NAMES_FILE):
        id_names = pd.DataFrame(columns=['id', 'name'])
        id_names.to_csv(ID_NAMES_FILE, index=False)
    else:
        id_names = pd.read_csv(ID_NAMES_FILE)

    if not os.path.exists('faces'):
        os.makedirs('faces')

    print('Welcome!')
    print('\nPlease put in your ID.')
    print('If this is your first time choose a random ID between 1-10000')

    id = int(input('ID: '))
    name = ''

    if id in id_names['id'].values:
        name = id_names[id_names['id'] == id]['name'].item()
        print(f'Welcome Back {name}!!')
    else:
        name = input('Enter your name: ')
        new_entry = pd.DataFrame([{'id': id, 'name': name}])
        id_names = pd.concat([id_names, new_entry], ignore_index=True)
        os.makedirs(f'faces/{id}', exist_ok=True)
        id_names.to_csv(ID_NAMES_FILE, index=False)

    print("\nLet's capture!")
    print("Now this is where you begin taking photos. Once you see a rectangle around your face, press the 's' key to capture a picture.", end=" ")
    print("It is recommended to take at least 20-25 pictures, from different angles, in different poses, with and without specs.")
    input("\nPress ENTER to start when you're ready, and press the 'q' key to quit when you're done!")

    start_laptop_camera(id)  # You can also replace with start_ip_camera() for IP camera

# Tkinter GUI setup
def open_menu():
    root = tk.Tk()
    root.title("Camera Selection Menu")
    root.geometry("300x200")

    def on_select_camera_type(camera_type):
        if camera_type == "Laptop":
            capture_photos()  # Call the method for laptop camera
        elif camera_type == "IP Camera":
            start_ip_camera()  # Call the method for IP camera

    label = tk.Label(root, text="Choose Camera Type", font=('Helvetica', 14))
    label.pack(pady=20)

    laptop_button = tk.Button(root, text="Laptop Camera", width=20, command=lambda: on_select_camera_type("Laptop"))
    laptop_button.pack(pady=10)

    ip_camera_button = tk.Button(root, text="IP Camera", width=20, command=lambda: on_select_camera_type("IP Camera"))
    ip_camera_button.pack(pady=10)

    root.mainloop()

# Run the menu
open_menu()
