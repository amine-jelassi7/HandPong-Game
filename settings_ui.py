import tkinter as tk


class SettingsWindow:
    """Start screen dialog to configure game parameters before launching."""

    def __init__(self, root):
        self.root = root
        self.root.title("CyberSmash Setup")
        self.root.geometry("450x480")
        self.root.configure(bg="#1e1e1e")

        self.settings = None

        tk.Label(
            root,
            text="GAME SETUP",
            font=("Helvetica", 20, "bold"),
            fg="#00FF00",
            bg="#1e1e1e",
        ).pack(pady=20)

        tk.Label(root, text="Ball Speed:", font=("Helvetica", 12), fg="#FFFFFF", bg="#1e1e1e").pack()
        self.speed_slider = tk.Scale(
            root, from_=5, to=25, orient=tk.HORIZONTAL, bg="#2d2d2d", fg="#00FF00", length=300
        )
        self.speed_slider.set(12)
        self.speed_slider.pack(pady=10)

        tk.Label(root, text="Ball Size (Radius):", font=("Helvetica", 12), fg="#FFFFFF", bg="#1e1e1e").pack()
        self.size_slider = tk.Scale(
            root, from_=10, to=40, orient=tk.HORIZONTAL, bg="#2d2d2d", fg="#00FF00", length=300
        )
        self.size_slider.set(20)
        self.size_slider.pack(pady=10)

        tk.Label(root, text="Winning Score:", font=("Helvetica", 12), fg="#FFFFFF", bg="#1e1e1e").pack()
        self.score_slider = tk.Scale(
            root, from_=1, to=15, orient=tk.HORIZONTAL, bg="#2d2d2d", fg="#00FF00", length=300
        )
        self.score_slider.set(5)
        self.score_slider.pack(pady=10)

        tk.Button(
            root,
            text="START GAME",
            font=("Helvetica", 14, "bold"),
            bg="#00FF00",
            fg="#000000",
            padx=20,
            pady=10,
            command=self.on_start,
        ).pack(pady=25)

    def on_start(self):
        self.settings = {
            "speed": self.speed_slider.get(),
            "size": self.size_slider.get(),
            "winning_score": self.score_slider.get(),
        }
        self.root.destroy()