import cv2
import math
import random


class Particle:
    """Represents a single spark particle generated on impact."""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-10, 10)
        self.lifetime = random.randint(12, 22)
        self.age = 0
        self.size = random.randint(4, 9)
        self.color = random.choice(
            [(0, 255, 255), (0, 165, 255), (255, 255, 0), (255, 200, 100)]
        )

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        if self.size > 1:
            self.size -= 0.25

    def is_dead(self):
        return self.age >= self.lifetime

    def draw(self, frame_rgb):
        cv2.circle(
            frame_rgb,
            (int(self.x), int(self.y)),
            int(self.size),
            self.color,
            cv2.FILLED,
        )


class PongGame:
    """Manages game physics using custom user settings."""

    def __init__(self, width=1280, height=720, ball_speed=10, ball_size=20, winning_score=5):
        self.width = width
        self.height = height
        self.base_speed = ball_speed
        self.ball_radius = ball_size
        self.winning_score = winning_score

        self.ball_pos = [width // 2, height // 2]
        self.ball_vel = [self.base_speed, max(4, int(self.base_speed * 0.6))]
        self.score_p1 = 0
        self.score_p2 = 0
        self.max_speed = self.base_speed * 1.8
        self.particles = []
        self.game_over = False
        self.winner_text = ""

    def update(self, paddles):
        if self.game_over:
            return

        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]

        # Wall bounces
        if (
            self.ball_pos[1] - self.ball_radius <= 0
            or self.ball_pos[1] + self.ball_radius >= self.height
        ):
            self.ball_vel[1] *= -1

        # Out-of-bounds score check
        if self.ball_pos[0] < 0:
            self.score_p2 += 1
            self.check_winner()
            self.reset_ball()
        elif self.ball_pos[0] > self.width:
            self.score_p1 += 1
            self.check_winner()
            self.reset_ball()

        # Hand Paddle Collision
        for paddle in paddles:
            p1, p2 = paddle["tip"], paddle["wrist"]
            dist, closest_point = self.point_to_line_dist(self.ball_pos, p1, p2)

            if dist <= self.ball_radius + 12:
                self.ball_vel[0] *= -1

                paddle_center_y = (p1[1] + p2[1]) / 2
                offset = (self.ball_pos[1] - paddle_center_y) / 50.0
                self.ball_vel[1] = max(
                    -self.max_speed, min(self.max_speed, self.ball_vel[1] + offset)
                )

                if self.ball_vel[0] > 0:
                    self.ball_pos[0] += 8
                else:
                    self.ball_pos[0] -= 8

                self.spawn_sparks(closest_point[0], closest_point[1], count=25)
                break

        for p in self.particles[:]:
            p.update()
            if p.is_dead():
                self.particles.remove(p)

    def check_winner(self):
        if self.score_p1 >= self.winning_score:
            self.game_over = True
            self.winner_text = "PLAYER 1 WINS!"
        elif self.score_p2 >= self.winning_score:
            self.game_over = True
            self.winner_text = "PLAYER 2 WINS!"

    def spawn_sparks(self, x, y, count=25):
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def reset_ball(self):
        self.ball_pos = [self.width // 2, self.height // 2]
        self.ball_vel[0] = self.base_speed if self.ball_vel[0] < 0 else -self.base_speed

    def draw_elements(self, frame_rgb):
        if self.game_over:
            cv2.putText(
                frame_rgb,
                self.winner_text,
                (self.width // 2 - 250, self.height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                2.0,
                (0, 255, 255),
                4,
            )
            return frame_rgb

        cv2.circle(
            frame_rgb,
            (int(self.ball_pos[0]), int(self.ball_pos[1])),
            self.ball_radius,
            (0, 255, 0),
            cv2.FILLED,
        )

        for p in self.particles:
            p.draw(frame_rgb)

        return frame_rgb

    @staticmethod
    def point_to_line_dist(pt, p1, p2):
        x, y = pt
        x1, y1 = p1
        x2, y2 = p2

        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(x - x1, y - y1), (x1, y1)

        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return math.hypot(x - closest_x, y - closest_y), (closest_x, closest_y)