#Quen 3

import cv2

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# Capture video from the default camera (0 refers to the default webcam)
cap = cv2.VideoCapture(0)

# Continue capturing frames as long as the video is opened
while cap.isOpened():
    # Read the current frame from the video capture object
    _, frame = cap.read()

    # Convert the captured frame to grayscale (many detection algorithms work better on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image using the face detector
    # '1.1' - scale factor and '4' - min number of neighbors for each rectangle to be retained
    faces = face_detector.detectMultiScale(gray, 1.1, 4)

    # Iterate through the detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around each face in the original frame (color = blue (255,0,0), thickness = 3)
        cv2.rectangle(frame, pt1=(x, y), pt2=(x+w, y+h), color=(255, 0, 0), thickness=3)

        # Extract the region of interest (ROI) from the grayscale and colored frames for the detected face
        roi_gray = gray[y:y+h, x:x+w]   # ROI for the face in grayscale
        roi_color = frame[y:y+h, x:x+w] # ROI for the face in the colored frame

        # Detect eyes within the face region (using the eye detector on the grayscale face region)
        eyes = eye_detector.detectMultiScale(roi_gray)

        # Iterate through the detected eyes
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around each detected eye in the colored face ROI (color = green (0,255,0), thickness = 5)
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 5)

    # Display the frame (with rectangles around faces and eyes) in a window titled "window"
    cv2.imshow("window", frame)

    # Wait for 1 millisecond for a key press, and if 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object when finished
frame.release()