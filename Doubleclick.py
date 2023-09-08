import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe Drawing module
mp_drawing = mp.solutions.drawing_utils

# Screen width and height (adjust these according to your screen resolution)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Minimum distance between index and middle finger for a double-click
DOUBLE_CLICK_DISTANCE_THRESHOLD = 50

# Video capture from the default camera (0)
cap = cv2.VideoCapture(0)

# Flag to keep track of the last click time
last_click_time = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the index and middle fingers
            index_x, index_y = int(hand_landmarks.landmark[8].x * SCREEN_WIDTH), int(
                hand_landmarks.landmark[8].y * SCREEN_HEIGHT)
            middle_x, middle_y = int(hand_landmarks.landmark[12].x * SCREEN_WIDTH), int(
                hand_landmarks.landmark[12].y * SCREEN_HEIGHT)

            # Calculate the distance between index and middle fingers
            distance = ((index_x - middle_x) ** 2 + (index_y - middle_y) ** 2) ** 0.5

            # Check for a double-click gesture (based on distance and time)
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            if distance < DOUBLE_CLICK_DISTANCE_THRESHOLD and current_time - last_click_time > 1.0:
                pyautogui.doubleClick()
                last_click_time = current_time

            # Draw the hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
