import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

prev_index_tip_x = None
swipe_threshold = 50
cap = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
        hand_landmarks = results.multi_hand_landmarks[0]

        index_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]

        if prev_index_tip_x is None:
            prev_index_tip_x = index_tip_x
        tip_distance = index_tip_x - prev_index_tip_x
        if tip_distance > swipe_threshold:
            pyautogui.press("right") 
        elif tip_distance < -swipe_threshold:
            pyautogui.press("left")
        prev_index_tip_x = index_tip_x
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow("Hand Swipe Presentation Control", frame) 
    if cv2.waitKey(1) & 0xff==ord(' '):
        break
cap.release()
cv2.destroyAllWindows()
