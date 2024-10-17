#Quen 2
import os
import numpy as np
import cv2

# Function to retrieve the first image from the specified folder
def get_image_from_folder(folder_path):
    files = os.listdir(folder_path)
    images = [f for f in files if f.endswith(('jpg', 'jpeg', 'png'))]

    if len(images) == 0:
        print("No images found in the folder.")
        return None

    image_path = os.path.join(folder_path, images[0])
    print(f"Using image: {image_path}")
    return image_path


# Specify the folder where images are located
folder_path = 'path_to_your_folder'  # Change this to the actual folder path
image_path = get_image_from_folder('images')

if image_path:
    # Load pre-trained classifiers for face, eye, and mouth detection
    face_detector1 = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    mouth_detector = cv2.CascadeClassifier('haarcascade/haarcascade_mcs_mouth.xml')  # Mouth detection

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces_result = face_detector1.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces_result:
        # Draw rectangle around face
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Define regions of interest for eyes and mouth within the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]


        # Detect mouth (since the mouth is usually in the lower third of the face, adjust the region of interest)
        roi_gray_mouth = gray[y + int(h / 2):y + h, x:x + w]  # Mouth is generally in the lower half of the face
        roi_color_mouth = img[y + int(h / 2):y + h, x:x + w]
        mouths = mouth_detector.detectMultiScale(roi_gray_mouth, 1.3, 5)

        for (mx, my, mw, mh) in mouths:
            # Draw a green rectangle around the detected mouth
            cv2.rectangle(roi_color_mouth, (mx, my), (mx + mw, my + mh), (0, 255, 0), 2)
            break  # Optional: Break after detecting the first mouth

    # Display the image with detected faces, eyes, and mouth
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No image selected.")
