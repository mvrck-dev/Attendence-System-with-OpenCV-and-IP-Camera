import pandas as pd
import numpy as np
import cv2 as cv

# Load IDs and Names from the CSV file
id_names = pd.read_csv('id-names.csv')
id_names = id_names[['id', 'name']]

# Load the Haar Cascade classifier for face detection
faceClassifier = cv.CascadeClassifier('Classifiers/haarface.xml')

# Initialize the LBPH face recognizer
lbph = cv.face.LBPHFaceRecognizer_create(threshold=500)
lbph.read('Classifiers/TrainedLBPH.yml')

# Start the camera
camera = cv.VideoCapture(0)

# Set the threshold for trust score to determine if the recognition is valid
RECOGNITION_THRESHOLD = 30  # You can adjust this value based on your use case

while cv.waitKey(1) & 0xFF != ord('q'):
    _, img = camera.read()
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceClassifier.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Iterate through detected faces
    for x, y, w, h in faces:
        faceRegion = grey[y:y + h, x:x + w]
        faceRegion = cv.resize(faceRegion, (220, 220))

        # Recognize the face using LBPH
        label, trust = lbph.predict(faceRegion)
        
        # If the recognition confidence is above the threshold, display the name
        if trust < RECOGNITION_THRESHOLD:
            try:
                name = id_names[id_names['id'] == label]['name'].item()
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.putText(img, name, (x, y + h + 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            except:
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.putText(img, "Unknown", (x, y + h + 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        else:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.putText(img, "Unknown", (x, y + h + 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

    # Display the image with the detected faces and names
    cv.imshow('Recognize', img)

# Release the camera and close the OpenCV windows
camera.release()
cv.destroyAllWindows()
