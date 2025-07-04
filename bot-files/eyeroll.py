import pygame
import random
import math
import time

# ---------- Tunables -------------------------------------------------
SCREEN_W, SCREEN_H   = 600, 300
BG_COLOR             = (30, 30, 30)
EYE_WHITE            = (255, 255, 255)
IRIS_COLOR          = (100, 150, 200)  # Soft blue iris
PUPIL_COLOR         = (0, 0, 0)
HIGHLIGHT_COLOR     = (255, 255, 255, 100)  # Semi-transparent highlight

EYE_RADIUS          = 70
IRIS_RADIUS         = 35
PUPIL_RADIUS        = 22
PUPIL_MOVE_RADIUS   = 24

GAZE_DWELL_MIN, GAZE_DWELL_MAX = 0.6, 1.8
BLINK_INTERVAL_MIN, BLINK_INTERVAL_MAX = 3, 7
BLINK_DURATION      = 0.12
EASING_SPEED        = 6.0  # Slightly slower for smoother motion
FPS                 = 70
# ---------------------------------------------------------------------

class Eye:
    def __init__(self, centre, is_left_eye):
        self.centre = pygame.Vector2(centre)
        self.pupil_pos = pygame.Vector2(centre)
        self.target_pos = pygame.Vector2(centre)
        self.next_shift = 0
        self.is_left_eye = is_left_eye

    def schedule_next_shift(self):
        self.next_shift = time.time() + random.uniform(GAZE_DWELL_MIN, GAZE_DWELL_MAX)

    def pick_new_target(self, other_eye_target=None):
        # Centre-biased target with slight correlation between eyes
        angle = random.uniform(0, 2 * math.pi)
        r = PUPIL_MOVE_RADIUS * (random.random() ** 2)  # Centre-bias
        offset = pygame.Vector2(r * math.cos(angle), r * math.sin(angle))
        self.target_pos = self.centre + offset

        # If other eye's target is provided, bias slightly toward it
        if other_eye_target:
            direction = (other_eye_target - self.centre).normalize() * r * 0.3
            self.target_pos = self.centre + (self.target_pos - self.centre) * 0.7 + direction

        # Ensure pupil stays within bounds
        if (self.target_pos - self.centre).length() > PUPIL_MOVE_RADIUS:
            self.target_pos = self.centre + (self.target_pos - self.centre).normalize() * PUPIL_MOVE_RADIUS

        self.schedule_next_shift()

    def update_pupil(self, dt):
        # Ease-out interpolation for smoother motion
        direction = self.target_pos - self.pupil_pos
        distance = direction.length()
        if distance > 0.1:  # Avoid jitter for tiny movements
            speed = EASING_SPEED * (distance / PUPIL_MOVE_RADIUS)  # Slower when closer
            move = direction * min(1, speed * dt)
            self.pupil_pos += move

        # Clamp pupil position to stay within bounds
        if (self.pupil_pos - self.centre).length() > PUPIL_MOVE_RADIUS:
            self.pupil_pos = self.centre + (self.pupil_pos - self.centre).normalize() * PUPIL_MOVE_RADIUS

    def draw(self, surf, lid_frac):
        # Draw eyeball (anti-aliased)
        pygame.draw.circle(surf, EYE_WHITE, self.centre, EYE_RADIUS)

        # Draw iris with gradient effect
        pygame.draw.circle(surf, IRIS_COLOR, self.centre, IRIS_RADIUS)

        # Draw pupil
        pygame.draw.circle(surf, PUPIL_COLOR, self.pupil_pos, PUPIL_RADIUS)

        # Draw highlight (small glossy dot)
        highlight_pos = self.pupil_pos + pygame.Vector2(-PUPIL_RADIUS * 0.4, -PUPIL_RADIUS * 0.4)
        pygame.draw.circle(surf, HIGHLIGHT_COLOR, highlight_pos, PUPIL_RADIUS * 0.3)

        # Draw eyelids with curved edges
        if lid_frac > 0:
            lid_h = EYE_RADIUS * lid_frac
            x, y = self.centre
            # Top eyelid
            top_points = [
                (x - EYE_RADIUS, y - EYE_RADIUS),
                (x + EYE_RADIUS, y - EYE_RADIUS),
                (x + EYE_RADIUS, y - EYE_RADIUS + lid_h),
                (x - EYE_RADIUS, y - EYE_RADIUS + lid_h)
            ]
            pygame.draw.polygon(surf, BG_COLOR, top_points)
            # Bottom eyelid
            bottom_points = [
                (x - EYE_RADIUS, y + EYE_RADIUS - lid_h),
                (x + EYE_RADIUS, y + EYE_RADIUS - lid_h),
                (x + EYE_RADIUS, y + EYE_RADIUS),
                (x - EYE_RADIUS, y + EYE_RADIUS)
            ]
            pygame.draw.polygon(surf, BG_COLOR, bottom_points)

class EyePair:
    def __init__(self):
        self.left_eye = Eye((SCREEN_W // 3, SCREEN_H // 2), True)
        self.right_eye = Eye((2 * SCREEN_W // 3, SCREEN_H // 2), False)
        self.blink_until = 0
        self.lid_frac = 0.0
        self.left_eye.schedule_next_shift()
        self.right_eye.schedule_next_shift()

    def schedule_blink(self):
        self.blink_until = time.time() + BLINK_DURATION
        self.lid_frac = 0.0

    def update_lids(self, dt):
        if time.time() < self.blink_until:
            phase = (self.blink_until - time.time()) / BLINK_DURATION
            self.lid_frac = 1.0 - abs(phase * 2 - 1)  # Triangle wave
        else:
            self.lid_frac = 0.0

    def update(self, dt, surf):
        # Update gaze with correlation
        if time.time() >= self.left_eye.next_shift:
            self.left_eye.pick_new_target()
            self.right_eye.pick_new_target(self.left_eye.target_pos)
        elif time.time() >= self.right_eye.next_shift:
            self.right_eye.pick_new_target()
            self.left_eye.pick_new_target(self.right_eye.target_pos)

        # Update pupil positions
        self.left_eye.update_pupil(dt)
        self.right_eye.update_pupil(dt)

        # Schedule blinks
        if random.random() < dt / random.uniform(BLINK_INTERVAL_MIN, BLINK_INTERVAL_MAX):
            self.schedule_blink()

        # Update lid animation
        self.update_lids(dt)

        # Draw eyes
        self.left_eye.draw(surf, self.lid_frac)
        self.right_eye.draw(surf, self.lid_frac)

def run_eye_animation():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Realistic Robot Eyes")
    clock = pygame.time.Clock()

    eye_pair = EyePair()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        eye_pair.update(dt, screen)
        pygame.display.flip()

    pygame.quit()
run_eye_animation()