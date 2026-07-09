import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, min_detec_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=min_detec_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def findHandsLandMarks(self, image, draw=True):
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        all_hands = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                h, w, _ = image.shape
                hand_data = []
                for id, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_data.append((id, cx, cy))
                all_hands.append(hand_data)
                if draw:
                    self.mp_draw.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS)
        return all_hands