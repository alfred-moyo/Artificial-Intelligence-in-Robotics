import cv2

# Load the Haar cascade for pure water bottle detection (replace with actual file)
bottle_detector = cv2.CascadeClassifier('classifier/cascade.xml')

# Capture video from the default camera (0 refers to the default webcam)
cap = cv2.VideoCapture(0)

# Continue capturing frames as long as the video is opened
while cap.isOpened():
    # Read the current frame from the video capture object
    _, frame = cap.read()

    # Convert the captured frame to grayscale (Haar cascades work better on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect bottles in the grayscale image
    bottles = bottle_detector.detectMultiScale(gray, 1.1, 4)

    # Iterate through the detected bottles
    for (x, y, w, h) in bottles:
        # Draw a rectangle around each detected bottle in the original frame (color = blue (255,0,0), thickness = 3)
        cv2.rectangle(frame, pt1=(x, y), pt2=(x+w, y+h), color=(255, 0, 0), thickness=3)

    # Display the frame (with rectangles around detected bottles) in a window titled "Bottle Detection"
    cv2.imshow("Bottle Detection", frame)

    # Wait for 1 millisecond for a key press, and if 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object when finished
cap.release()
cv2.destroyAllWindows()
