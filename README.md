# 🏓 HandPong Game

An interactive, gesture-controlled Computer Vision Ping Pong game built with **Python**, **OpenCV**, **MediaPipe**, and **Tkinter**. Control your paddle in real time using your hand movements caught on your webcam!

---

## Features

- **Gesture Control**: Uses MediaPipe Hand Tracking to map your hand (wrist to index finger tip) into an active dynamic paddle in real time.
- **Improved Collision Physics**: Calculates true point-to-line-segment distance to prevent tunneling and sticky collisions.
- **Spark Particle Effects**: Custom particle system generates explosive spark bursts on paddle impacts.
- **Pre-Game Settings Menu**: Interactive configuration launcher for customizing ball speed, ball size, and target winning score.
- **HD Widescreen Interface**: Runs at 1280x720 camera capture with a structured Tkinter GUI container layout (separated scoreboard and game canvas).
- **Clean Modular Architecture**: Fully decoupled into dedicated modules for tracking, physics/rendering, setup UI, and runtime execution.

---

## 📁 Project Structure

```text
cyber_smash/
├── tracker.py       # Camera feed acquisition & MediaPipe landmark processing
├── game.py          # Ball physics, line-segment collision detection & particle engine
├── settings_ui.py   # Launcher setup window for customizing game parameters
├── main.py          # Master application controller and GUI mainloop
└── README.md        # Project documentation
```

---

##  Prerequisites & Installation

Ensure you have **Python 3.8+** installed on your system.

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/amine-jelassi7/HandPong-Game.git
   cd HandPong-Game
   ```

2. **Install required dependencies**:
   ```bash
   pip install opencv-python mediapipe pillow
   ```

---

##  How to Run

Execute `main.py` from your terminal or IDE:

```bash
python main.py
```

### Gameplay Workflow
1. The **GAME SETUP** window appears.
2. Adjust your preferred **Ball Speed**, **Ball Size (Radius)**, and **Winning Score**.
3. Click **START GAME**.
4. Position yourself in front of the webcam, raise one or two hands, and enjoy!

---

##  How to Play

- **Paddles**: Move your hand in view of the camera. The app tracks your **wrist** and **index finger tip**, drawing a vibrant yellow paddle line segment between them.
- **Bouncing & Angling**: Hitting the ball near the ends of your hand paddle angles the bounce trajectory dynamically.
- **Scoring**: Prevent the ball from slipping past your side of the screen while attempting to score against your opponent.
- **Game Over**: When Player 1 or Player 2 reaches the target score, a winner banner displays over the video feed.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
