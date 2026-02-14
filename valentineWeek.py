import pygame
import random
import math
import sys
import os

# ---------- CONFIG ----------
WIDTH, HEIGHT = 900, 600
FPS = 60
HEART_COUNT = 30

# ---------- INITIALIZE PYGAME ----------
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except Exception as e:
    print("Mixer init failed:", e)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Valentine's Week Proposal")
clock = pygame.time.Clock()

# ---------- LOAD MUSIC (PORTABLE) ----------
script_dir = os.path.dirname(os.path.abspath(__file__))
music_file = os.path.join(script_dir, "love_song.ogg")  # Relative path to script

if os.path.exists(music_file):
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except Exception as e:
        print("Error playing music:", e)
else:
    print("Music file not found! Please put love_song.ogg in the same folder as the script.")

# ---------- LOAD FONTS ----------
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 42, bold=True)
small_font = pygame.font.SysFont("Segoe UI Emoji", 24, bold=True)

# ---------- COLORS ----------
BG_COLOR = (20, 10, 40)
HEART_COLORS = [
    (255, 105, 180),
    (255, 20, 147),
    (255, 182, 193),
    (255, 255, 100)
]

# ---------- HEART CLASS ----------
class Heart:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = random.randint(HEIGHT, HEIGHT+300)
        self.size = random.randint(12, 20)
        self.speed = random.uniform(0.8, 2)
        self.color = random.choice(HEART_COLORS)
        self.phase = random.uniform(0, 2*math.pi)
        self.sway = random.uniform(0.5, 1.5)

    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.phase) * self.sway
        self.phase += 0.05
        if self.y < -50:
            self.y = HEIGHT + random.randint(50, 200)
            self.x = random.randint(50, WIDTH-50)

    def draw(self, surface):
        scale = self.size / 10
        points = []
        for t in range(0, 360, 2):
            rad = math.radians(t)
            x = 16*math.sin(rad)**3
            y = 13*math.cos(rad) - 5*math.cos(2*rad) - 2*math.cos(3*rad) - math.cos(4*rad)
            points.append((self.x + x*scale, self.y - y*scale))
        pygame.draw.polygon(surface, self.color, points)

hearts = [Heart() for _ in range(HEART_COUNT)]

# ---------- VALENTINE WEEK DATA ----------
days = [
    ("Rose Day 🌹", "I promise to always bring you smiles and joy"),
    ("Chocolate Day 🍫", "I promise to share sweet moments with you"),
    ("Teddy Day 🧸", "I promise to always comfort you and be there"),
    ("Promise Day 💌", "I promise to be honest and loyal to you"),
    ("Valentine's Day 💖", "Will you be my Valentine?")
]
day_index = 0

# ---------- CELEBRATION ----------
celebrating = False
celebration_hearts = []

class CelebrationHeart:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = random.randint(50, HEIGHT-50)
        self.size = random.randint(10, 25)
        self.color = random.choice(HEART_COLORS)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)
        self.gravity = 0.05

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# ---------- NO MESSAGE VARS ----------
no_messages = [
    "Please say Yes ❤️ ... try again!",
    "I really want you to say Yes ❤️ ... please!",
    "I can't give up, please say Yes ❤️ ... 😢",
    "You're my everything ❤️ ... just say Yes!",
    "Please say Yes ❤️ ... try again!",
    "I really want you to say Yes ❤️ ... please!",
    "I can't give up, please say Yes ❤️ ... 😢",
    "You're my everything ❤️ ... just say Yes!",
    "Please say Yes ❤️ ... try again!",
    "I really want you to say Yes ❤️ ... please!",
    "I can't give up, please say Yes ❤️ ... 😢",
    "You're my everything ❤️ ... just say Yes!",
    "Please, my heart is yours ❤️ ... YES!"
]
no_index = 0
no_pressed = False

# ---------- MAIN LOOP ----------
running = True
response_pending = False

while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    # Draw floating hearts
    for heart in hearts:
        heart.update()
        heart.draw(screen)

    # Celebration animation
    if celebrating:
        for c in celebration_hearts:
            c.update()
            c.draw(screen)
        text_surface = emoji_font.render("I LOVE YOU ❤️", True, (255, 50, 180))
        screen.blit(text_surface, (WIDTH//2 - 150, HEIGHT//2 - 50))
    else:
        day, message = days[day_index]
        day_surface = emoji_font.render(day, True, (255,182,193))
        screen.blit(day_surface, (WIDTH//2 - 180, HEIGHT//2 - 80))

        msg_surface = small_font.render(message, True, (255,200,200))
        screen.blit(msg_surface, (WIDTH//2 - 220, HEIGHT//2))

        if day_index == len(days)-1:
            prompt_surface = small_font.render("Press Y for Yes ❤️ or N for No 💔", True, (255,255,255))
            screen.blit(prompt_surface, (WIDTH//2 - 180, HEIGHT//2 + 50))
            response_pending = True

            if no_pressed:
                retry_surface = small_font.render(no_messages[no_index], True, (255,200,50))
                screen.blit(retry_surface, (WIDTH//2 - 180, HEIGHT//2 + 90))
        else:
            continue_surface = small_font.render("Press any key for next day...", True, (200,200,200))
            screen.blit(continue_surface, (WIDTH//2 - 140, HEIGHT//2 + 50))

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if celebrating:
                continue
            if day_index < len(days)-1:
                day_index += 1
            elif response_pending:
                if event.key == pygame.K_y:
                    celebrating = True
                    for _ in range(50):
                        celebration_hearts.append(CelebrationHeart())
                    no_pressed = False
                    no_index = 0
                elif event.key == pygame.K_n:
                    no_pressed = True
                    no_index = min(no_index + 1, len(no_messages)-1)

pygame.quit()
try:
    pygame.mixer.music.stop()
except:
    pass
sys.exit()
