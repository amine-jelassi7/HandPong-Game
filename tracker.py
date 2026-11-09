import cv2
import mediapipe as mp


class HandTracker:
    """Handles camera capture and MediaPipe processing."""

    def __init__(self, camera_index=0, max_hands=2, width=1280, height=720):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def process_frame(self):
        if not self.cap.isOpened():
            return None, []

        success, frame = self.cap.read()
        if not success:
            return None, []

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        paddles = []
        h, w, _ = image_rgb.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image_rgb,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

                tip = (
                    int(hand_landmarks.landmark[8].x * w),
                    int(hand_landmarks.landmark[8].y * h),
                )
                wrist = (
                    int(hand_landmarks.landmark[0].x * w),
                    int(hand_landmarks.landmark[0].y * h),
                )

                cv2.line(image_rgb, tip, wrist, (0, 255, 255), 8)
                paddles.append({"tip": tip, "wrist": wrist})

        return image_rgb, paddles

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        self.hands.close()