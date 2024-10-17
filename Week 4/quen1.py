#Quen 1
import os
import numpy as np
import cv2


# Function to retrieve the first image from the specified folder
def get_image_from_folder(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    # Filter the files, keeping only images (with jpg, jpeg, or png extensions)
    images = [f for f in files if f.endswith(('jpg', 'jpeg', 'png'))]

    # If there are no images in the folder, print a message and return None
    if len(images) == 0:
        print("No images found in the folder.")
        return None

    # If images exist, pick the first one (can be modified for user input to select)
    image_path = os.path.join(folder_path, images[0])
    print(f"Using image: {image_path}")  # Output which image is being used
    return image_path


# Specify the folder where images are located
folder_path = 'images'
image_path = get_image_from_folder(folder_path)

if image_path:
    # Load pre-trained classifiers for face and eye detection
    face_detector1 = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')  # Face detection
    eye_detector1 = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')

    # Read the selected image
    img = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces_result = face_detector1.detectMultiScale(gray, 1.3, 5)

    # Loop through each detected face (returns the coordinates of face rectangles)
    for (x, y, w, h) in faces_result:
        # Draw a rectangle around each detected face (color = blue (255,0,0), thickness = 2)
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Define regions of interest (ROI) to focus on the face area for eye detection
        roi_gray = gray[y:y + h, x:x + w]  # Grayscale face area
        roi_color = img[y:y + h, x:x + w]  # Color face area

        # Detect eyes within the face region
        eyes = eye_detector1.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # Draw rectangles around the detected eyes (color = green (0,255,0), thickness = 2)
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("No image selected.")
