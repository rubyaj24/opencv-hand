import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Connect to Arduino
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
time.sleep(2)  # Allow time for Arduino to initialize

def send_to_arduino(data):
    """Send data to Arduino via serial communication."""
    arduino.write(str(data).encode())

def count_fingers(landmarks):
    """Count raised fingers based on landmarks."""
    finger_tips = [4, 8, 12, 16, 20]  # Indexes for thumb, index, middle, ring, and pinky tips
    finger_pips = [3, 6, 10, 14, 18]  # Indexes for thumb, index, middle, ring, and pinky PIP joints

    fingers = []
    for tip, pip in zip(finger_tips, finger_pips):
        # Check if the finger tip is above its PIP joint (raised)
        if landmarks[tip].y < landmarks[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    # Adjust thumb logic (different orientation)
    if landmarks[4].x > landmarks[3].x:  # For right hand
        fingers[0] = 1
    else:
        fingers[0] = 0

    return sum(fingers)

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally for natural mirroring
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe
    result = hands.process(rgb_frame)
    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Calculate finger count
            landmarks = hand_landmarks.landmark
            finger_count = count_fingers(landmarks)

            # Display the count
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Send the count to Arduino
            send_to_arduino(finger_count)

    # Show the frame
    cv2.imshow("Hand Gesture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
arduino.close()
