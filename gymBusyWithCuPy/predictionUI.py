import pygame
import sys
from runModel  import predict

pygame.init()
screen = pygame.display.set_mode((750, 500))
pygame.display.set_caption("Gym Busy % Predictor")

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARKGRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
ACTIVE_COLOR = (255, 255, 150)

input_boxes = []
input_texts = ["", "", ""]
labels = ["Hour (0-11):", "AM (0) / PM (1):", "Day (0=Mon to 6=Sun):"]
active_index = -1

for i in range(3):
    input_boxes.append(pygame.Rect(350, 50 + i * 70, 140, 40))

button = pygame.Rect(150, 280, 200, 50)
result = ""

def draw():
    screen.fill(WHITE)
    for i in range(3):
        label_surf = small_font.render(labels[i], True, BLACK)
        screen.blit(label_surf, (50, 60 + i * 70))

        color = ACTIVE_COLOR if i == active_index else GRAY
        pygame.draw.rect(screen, color, input_boxes[i])

        text_surface = font.render(input_texts[i], True, BLACK)
        screen.blit(text_surface, (input_boxes[i].x + 5, input_boxes[i].y + 5))


#   draw prediction clicker button here if you want, it will do it automatically otherwise
    #pygame.draw.rect(screen, BLUE, button)
    #screen.blit(font.render("Predict", True, WHITE), (button.x + 40, button.y + 10))

    result_surf = font.render(result, True, DARKGRAY)
    screen.blit(result_surf, (50, 350))

    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            active_index = -1
            for i, box in enumerate(input_boxes):
                if box.collidepoint(event.pos):
                    active_index = i
                    break


        elif event.type == pygame.KEYDOWN and active_index != -1:
            if event.key == pygame.K_BACKSPACE:
                input_texts[active_index] = input_texts[active_index][:-1]
            elif event.unicode.isdigit() and len(input_texts[active_index]) < 2:
                input_texts[active_index] += event.unicode
        try:
            hour = int(input_texts[0])
            ampm = int(input_texts[1])
            day = int(input_texts[2])

            # 🔁 Plug in your model call here
            # prediction = model.fullForwardPass([hour, ampm, day])[0] * 100
            prediction = predict(hour, ampm, day)  # placeholder

            result = f"Predicted Busy: {prediction:.1f}% full"
        except:
            result = "..."

    draw()
    clock.tick(30)
