#########################
##  MAKE SURE to change the model in runModel.py
##  to the one you want, because this script makes a call ther
#########################
import pygame
import sys
from runModel import predict

# === Config ===
DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HOURS = list(range(1, 24))  # 6 AM to 11 PM

# === Replace with your actual model prediction function ===
def predict_percent(hour, day):
    am_pm = 0 if hour < 12 else 1
    hr_12 = hour % 12
    if hr_12 == 0:
        hr_12 = 12  # make 12AM/PM clearer
    return predict(hr_12, am_pm, day)
    # # 🔁 Placeholder value

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Gym Busyness by Hour")

font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GRAY = (200, 200, 200)

selected_day = 0

def draw_graph():
    screen.fill(WHITE)

    title = title_font.render(f"Predicted Gym Busyness – {DAY_NAMES[selected_day]}", True, BLACK)
    screen.blit(title, (300, 20))

    max_height = 300
    bar_width = 30
    spacing = 10
    start_x = 50
    bottom_y = 400

    for i, hour in enumerate(HOURS):
        pred = predict_percent(hour, selected_day)
        bar_height = int((pred / 100.0) * max_height)
        x = start_x + i * (bar_width + spacing)
        y = bottom_y - bar_height

        # Draw bar
        pygame.draw.rect(screen, BLUE, (x, y, bar_width, bar_height))

        # Draw value
        label = font.render(f"{int(pred)}%", True, BLACK)
        screen.blit(label, (x, y - 20))

        # Hour label
        hour_label = font.render(f"{hour}", True, BLACK)
        screen.blit(hour_label, (x, bottom_y + 5))

    # Draw left/right buttons
    pygame.draw.rect(screen, GRAY, (50, 450, 150, 30))
    pygame.draw.rect(screen, GRAY, (800, 450, 150, 30))
    screen.blit(font.render("← Previous Day", True, BLACK), (60, 455))
    screen.blit(font.render("Next Day →", True, BLACK), (820, 455))

    pygame.display.flip()

while True:
    draw_graph()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 50 <= x <= 200 and 450 <= y <= 480:
                selected_day = (selected_day - 1) % 7
            elif 800 <= x <= 950 and 450 <= y <= 480:
                selected_day = (selected_day + 1) % 7

    clock.tick(30)
