import tkinter as tk
from PIL import Image, ImageTk

from tracker import HandTracker
from game import PongGame
from settings_ui import SettingsWindow


class HandTrackingApp:
    def __init__(self, window, settings, icon_path="my_icon.ico"):
        self.window = window
        self.window.title("HandPong")
        self.window.configure(bg="#1e1e1e")
        self.window.geometry("1340x840")

        try:
            self.window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon loading error: {e}")

        GAME_W, GAME_H = 1280, 720

        self.tracker = HandTracker(width=GAME_W, height=GAME_H)
        self.game = PongGame(
            width=GAME_W,
            height=GAME_H,
            ball_speed=settings["speed"],
            ball_size=settings["size"],
            winning_score=settings["winning_score"],
        )

        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.update_frame()

    def setup_ui(self):
        self.score_frame = tk.Frame(self.window, bg="#2d2d2d", pady=12)
        self.score_frame.pack(side=tk.TOP, fill=tk.X)

        self.score_p1_label = tk.Label(
            self.score_frame,
            text="Player 1: 0",
            font=("Helvetica", 22, "bold"),
            fg="#00FF00",
            bg="#2d2d2d",
        )
        self.score_p1_label.pack(side=tk.LEFT, padx=60)

        self.title_label = tk.Label(
            self.score_frame,
            text="HANDPONG",
            font=("Helvetica", 24, "bold"),
            fg="#FFFFFF",
            bg="#2d2d2d",
        )
        self.title_label.pack(side=tk.LEFT, expand=True)

        self.score_p2_label = tk.Label(
            self.score_frame,
            text="Player 2: 0",
            font=("Helvetica", 22, "bold"),
            fg="#FF00FF",
            bg="#2d2d2d",
        )
        self.score_p2_label.pack(side=tk.RIGHT, padx=60)

        self.game_frame = tk.Frame(self.window, bg="#000000", bd=4, relief=tk.RIDGE)
        self.game_frame.pack(side=tk.TOP, padx=15, pady=15)

        self.video_label = tk.Label(self.game_frame, bg="#000000")
        self.video_label.pack()

    def update_frame(self):
        image_rgb, paddles = self.tracker.process_frame()

        if image_rgb is not None:
            self.game.update(paddles)
            image_rgb = self.game.draw_elements(image_rgb)

            self.score_p1_label.config(text=f"Player 1: {self.game.score_p1}")
            self.score_p2_label.config(text=f"Player 2: {self.game.score_p2}")

            pil_img = Image.fromarray(image_rgb)
            tk_img = ImageTk.PhotoImage(image=pil_img)
            self.video_label.config(image=tk_img)
            self.video_label.image = tk_img

        self.window.after(16, self.update_frame)

    def on_closing(self):
        self.tracker.release()
        self.window.destroy()


if __name__ == "__main__":
    settings_root = tk.Tk()
    setup_app = SettingsWindow(settings_root)
    settings_root.mainloop()

    if setup_app.settings:
        game_root = tk.Tk()
        app = HandTrackingApp(game_root, setup_app.settings)
        game_root.mainloop()