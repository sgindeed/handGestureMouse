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

# Scrolling sensitivity (you can adjust this value)
SCROLL_SENSITIVITY = 10

# Video capture from the default camera (0)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the thumb and index finger
            thumb_x, thumb_y = int(hand_landmarks.landmark[4].x * SCREEN_WIDTH), int(
                hand_landmarks.landmark[4].y * SCREEN_HEIGHT)
            index_x, index_y = int(hand_landmarks.landmark[8].x * SCREEN_WIDTH), int(
                hand_landmarks.landmark[8].y * SCREEN_HEIGHT)

            # Detect scrolling gesture (up or down)
            if thumb_y < index_y:
                pyautogui.scroll(SCROLL_SENSITIVITY)
            elif thumb_y > index_y:
                pyautogui.scroll(-SCROLL_SENSITIVITY)

            # Draw the hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow("Hand Gesture Scrolling", frame)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
