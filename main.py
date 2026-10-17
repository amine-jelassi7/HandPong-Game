import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk


class HandTrackingApp:
    def __init__(self, window, icon_path="my_icon.ico"):
        self.window = window
        self.window.title("computer vision")

        try:
            self.window.iconbitmap(icon_path)
        except Exception as e:
            print(e)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.cap = cv2.VideoCapture(0)

        self.video_label = tk.Label(window)
        self.video_label.pack()

        self.update_frame()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_frame(self):
        if self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                frame = cv2.flip(frame, 1)
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = self.hands.process(image_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image_rgb,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style(),
                        )

                        h, w, c = image_rgb.shape
                        cx, cy = int(hand_landmarks.landmark[8].x * w), int(
                            hand_landmarks.landmark[8].y * h
                        )

                        cv2.circle(image_rgb, (cx, cy), 12, (255, 0, 255), cv2.FILLED)

                pil_img = Image.fromarray(image_rgb)
                tk_img = ImageTk.PhotoImage(image=pil_img)

                self.video_label.config(image=tk_img)
                self.video_label.image = tk_img

        self.window.after(10, self.update_frame)

    def on_closing(self):
        if self.cap.isOpened():
            self.cap.release()
        self.hands.close()
        self.window.destroy()



if __name__ == "__main__":
    root = tk.Tk()

    app = HandTrackingApp(root, icon_path="my_icon.ico")

    root.mainloop()
