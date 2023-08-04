
import mediapipe as mp
import cv2
import numpy as np
import uuid
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#Getting webcam feed
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.85, min_tracking_confidence=0.85) as hands:
    while cap.isOpened():
        ret, frame = cap.read() #Reading each frame from the webcam

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convert the BGR Image feed to RGB

        # image = cv2.flip(image, 1)

        image.flags.writeable = False

        results = hands.process(image)
        
        image.flags.writeable = True
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=3, circle_radius=2),
                                         )

        cv2.imshow('Hand Tracking', image) #Rendering the image to the screen

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()