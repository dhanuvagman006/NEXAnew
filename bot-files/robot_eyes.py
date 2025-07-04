import pygame
import sys
import math
import os

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Robot Eyes - Scaled PNGs")
clock = pygame.time.Clock()

# Emotion and animation
emotion = "normal"
time_counter = 0

# Eye image directory
EYE_DIR = "eyes/4x"
SCALE = 0.3  # 👈 Adjust this to change eye size

# Load and scale image
def load_png(path, scale=1.0):
    image = pygame.image.load(path).convert_alpha()
    size = (int(image.get_width() * scale), int(image.get_height() * scale))
    return pygame.transform.smoothscale(image, size)

# Load all emotions
emotions = ["normal", "happy", "loving","sad", "angry"]
eye_images = {}

for emo in emotions:
    try:
        left_img = load_png(os.path.join(EYE_DIR, f"{emo}_left.png"), SCALE)
        right_img = load_png(os.path.join(EYE_DIR, f"{emo}_right.png"), SCALE)
        eye_images[emo] = {"left": left_img, "right": right_img}
    except Exception as e:
        print(f"Error loading {emo} images: {e}")
        sys.exit()

# Adjust center positions based on new size
image_width = eye_images["normal"]["left"].get_width()
image_height = eye_images["normal"]["left"].get_height()

left_eye_center = (350, 350)
right_eye_center = (650, 350)

# Wiggle function
def get_wiggle_offset(t, strength=6, speed=0.03):
    return (
        math.sin(t * speed) * strength,
        math.cos(t * speed * 0.8) * strength
    )

# Main loop
running = True
while running:
    screen.fill((20, 20, 20))  # Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                emotion = "normal"
            elif event.key == pygame.K_h:
                emotion = "happy"
            elif event.key == pygame.K_l:
                emotion = "loving"
            elif event.key == pygame.K_s:
                emotion = "sad"
            elif event.key == pygame.K_a:
                emotion = "angry"

    # Animate
    dx, dy = get_wiggle_offset(time_counter)
    eyes = eye_images[emotion]

    screen.blit(eyes["left"], eyes["left"].get_rect(center=(left_eye_center[0] + dx, left_eye_center[1] + dy)))
    screen.blit(eyes["right"], eyes["right"].get_rect(center=(right_eye_center[0] + dx, right_eye_center[1] + dy)))

    pygame.display.flip()
    clock.tick(60)
    time_counter += 1

# Exit
pygame.quit()
sys.exit()
