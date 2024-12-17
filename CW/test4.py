# Import necessary libraries
import cv2 as cv
import threading
from tkinter import Tk, Label, Button, StringVar
from PIL import Image, ImageTk
import time
from Arm_Lib import Arm_Device

# Initialize the robotic arm
Arm = Arm_Device()
joints_0 = [90, 135, 20, 25, 90, 30]
Arm.Arm_serial_servo_write6_array(joints_0, 1000)

# Positions for different actions for Book 1
p_left = [180, 100 , -80, 140, 90]
p_left2 = [180, 180, 10, 20, 90]  # Left position
p_right = [0, 80, 50, 50, 90]   # Right position
p_top = [90, 80, 50, 50, 90]    # Top (transition) position
p_rest = [90, 90, 90, 0, 90]    # Rest position

# Positions for different actions for Book 2
p_leftBook2 = [150, 100 , -80, 140, 90]
p_left2Book2 = [150, 180, 10, 20, 90]  # Left position
p_rightBook2 = [0, 80, 50, 50, 90]   # Right position
p_topBook2 = [90, 80, 50, 50, 90]    # Top (transition) position
p_restBook2 = [90, 90, 90, 0, 90]    # Rest position

# Control the clamp (servo 6)
def arm_clamp_block(enable):
    if enable == 0:  # Release
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:  # Clamp
        Arm.Arm_serial_servo_write(6, 120, 400)
    time.sleep(0.5)

# Move the arm to specified positions
def arm_move(p, s_time=500):
    for i in range(5):
        id = i + 1
        if id == 5:
            time.sleep(0.1)
            Arm.Arm_serial_servo_write(id, p[i], int(s_time * 1.2))
        elif id == 1:
            Arm.Arm_serial_servo_write(id, p[i], int(3 * s_time / 4))
        else:
            Arm.Arm_serial_servo_write(id, p[i], int(s_time))
        time.sleep(0.01)
    time.sleep(s_time / 1000)

arm_moving = False

# Function to move object from left to right for book1
def move_object_left_to_rightBook1():
    global arm_moving
    
    if arm_moving:
        return
    
    arm_moving = True
    
    try:
        # Move to left position to pick object
        arm_clamp_block(0)  # Open clamp
        arm_move(p_left2, 2000)
        arm_move(p_left, 2000)  # Move to left position
        arm_clamp_block(1)  # Clamp object

        # Transition to top position
        arm_move(p_left2, 2000)

        # Move to right position
        arm_move(p_right, 2000)

        # Release object
        arm_clamp_block(0)

        # Return to rest position
        arm_move(p_top, 2000)
        arm_move(p_rest, 2000)
        
    finally:
        arm_moving = False
        

# Function to move object from left to right for book2
def move_object_left_to_rightBook2():
    global arm_moving
    
    if arm_moving:
        return
    
    arm_moving = True
    
    try:
        # Move to left position to pick object
        arm_clamp_block(0)  # Open clamp
        arm_move(p_left2Book2, 2000)
        arm_move(p_leftBook2, 2000)  # Move to left position
        arm_clamp_block(1)  # Clamp object

        # Transition to top position
        arm_move(p_left2Book2, 2000)

        # Move to right position
        arm_move(p_rightBook2, 2000)

        # Release object
        arm_clamp_block(0)

        # Return to rest position
        arm_move(p_topBook2, 2000)
        arm_move(p_restBook2, 2000)
        
    finally:
        arm_moving = False



# Tkinter setup
root = Tk()
root.title("QR Code Scanner")

# Tkinter variables
img_label = Label(root)
img_label.pack()

status_var = StringVar()
status_var.set("Status: Running")
status_label = Label(root, textvariable=status_var)
status_label.pack()

def exit_program():
    global model
    model = 'Exit'
    status_var.set("Status: Exiting...")
    root.quit()

exit_button = Button(root, text="Exit", command=exit_program, bg="red", fg="white", height=2, width=10)
exit_button.pack()

# Camera thread function
def camera():
    global model

    # Open the camera
    capture = cv.VideoCapture(0)

    # Initialize QRCodeDetector
    qr_detector = cv.QRCodeDetector()
    
    processed_qr = None
    last_processed_time = 0  # Track the last processed QR code time
    cooldown_period = 2  # Cooldown period in second

    while capture.isOpened():
        try:
            ret, img = capture.read()
            if not ret:
                break

            img = cv.resize(img, (640, 480))

            # Detect QR code in the image
            data, bbox, _ = qr_detector.detectAndDecode(img)
            if bbox is not None:
                bbox = bbox.astype(int)  # Ensure coordinates are integers
                
                # Draw bounding box around the QR code
                for i in range(len(bbox)):
                    pt1 = tuple(bbox[i][0])
                    pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
                    cv.line(img, pt1, pt2, (0, 255, 0), 2)

                # Display QR code data on the image
                if data:
                    cv.putText(img, data, (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    
                    # Check if the QR code is new and within the cooldown period
                    current_time = time.time()
                    if data != processed_qr:
                        processed_qr = data
                        last_processed_time = time.time()
                        
                        # Check if the QR code matches Wikipedia or Qrco
                        if "wikipedia.org" in data:  
                            move_object_left_to_rightBook1()
                        elif "qrco.de" in data:
                            move_object_left_to_rightBook2()
                            
                            
                else:
                    processed_qr = None

            if model == 'Exit':
                capture.release()
                break

            # Convert the frame to an image Tkinter can display
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)
            img_label.imgtk = img_tk
            img_label.configure(image=img_tk)

        except KeyboardInterrupt:
            capture.release()
            break

    capture.release()
    cv.destroyAllWindows()

# Global variable to manage program state
model = 'General'

# Run the camera in a separate thread
camera_thread = threading.Thread(target=camera, daemon=True)
camera_thread.start()

# Run the Tkinter main loop
root.mainloop()

del Arm  # Release DOFBOT object



