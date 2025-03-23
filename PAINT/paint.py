import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
COLORS = [
    (255, 0, 0),  #RED
    (0, 255, 0),  #GREEN
    (0, 0, 255),  #BLUE
    (255, 255, 0),  #YELLOW
    (0, 255, 255),  #TURQUOISE
    (255, 0, 255),  #PURPLE
    (255, 255, 255),  #WHITE (ERASER)
    (0, 0, 0)  #BLACK
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")
surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill((255, 255, 255))

current_color = COLORS[0]
drawing = False
last_pos = None
tool = 'line'
brush_size = 5

def draw_interface():
    pygame.draw.rect(screen, (150, 150, 150), (0, 0, WIDTH, 60))

    for i, color in enumerate(COLORS):
        pygame.draw.circle(screen, color, (30 + i * 40, 30), 15)

    pygame.draw.circle(screen, current_color, (WIDTH - 30, 30), 15)

    pygame.draw.rect(screen, (200, 200, 200), (10, 70, 50, 30))
    pygame.draw.rect(screen, (200, 200, 200), (70, 70, 50, 30))
    pygame.draw.rect(screen, (200, 200, 200), (130, 70, 50, 30))

    pygame.draw.rect(screen, (200, 200, 200), (190, 70, 30, 30))
    pygame.draw.rect(screen, (200, 200, 200), (230, 70, 30, 30))

    font = pygame.font.Font(None, 24)
    size_text = font.render(str(brush_size), True, (0, 0, 0))
    screen.blit(size_text, (270, 80))

    font = pygame.font.Font(None, 36)
    line_text = font.render("line", True, (0,0,0))
    square_text = font.render("sqr", True, (0,0,0))
    circle_text = font.render("circ", True, (0, 0, 0))
    plus_text = font.render("+", True, (0, 0, 0))
    minus_text = font.render("-", True, (0, 0, 0))
    screen.blit(line_text, (13, 73))
    screen.blit(square_text, (75, 73))
    screen.blit(circle_text, (135, 73))
    screen.blit(plus_text, (195, 73))
    screen.blit(minus_text, (238, 75))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, color in enumerate(COLORS):
                if ((pos[0] - (30 + i * 40)) ** 2 + (pos[1] - 30) ** 2) ** 0.5 < 15: #if in circle
                    current_color = color
                    if color == (255, 255, 255):
                        tool = 'eraser'
                    else:
                        tool = 'line' if tool == 'eraser' else tool
                    break

            if 10 <= pos[0] <= 60 and 70 <= pos[1] <= 100:
                tool = 'line'
            elif 70 <= pos[0] <= 120 and 70 <= pos[1] <= 100:
                tool = 'square'
            elif 130 <= pos[0] <= 180 and 70 <= pos[1] <= 100:
                tool = 'circle'
            elif 190 <= pos[0] <= 220 and 70 <= pos[1] <= 100:
                brush_size = min(20, brush_size + 1)
            elif 230 <= pos[0] <= 260 and 70 <= pos[1] <= 100:
                brush_size = max(1, brush_size - 1)

            if pos[1] > 110:
                drawing = True
                last_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool in ['square', 'circle']:
                current_pos = pygame.mouse.get_pos()
                if tool == 'square':
                    pygame.draw.rect(surface, current_color,
                                     (min(last_pos[0], current_pos[0]),
                                      min(last_pos[1], current_pos[1]),
                                      abs(current_pos[0] - last_pos[0]),
                                      abs(current_pos[1] - last_pos[1])), brush_size)
                elif tool == 'circle':
                    radius = int(((current_pos[0] - last_pos[0]) ** 2 +
                                  (current_pos[1] - last_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(surface, current_color, last_pos, radius, brush_size)
            drawing = False

        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = pygame.mouse.get_pos()
            if tool in ['line', 'eraser']:
                pygame.draw.line(surface, current_color, last_pos, current_pos,
                                 brush_size * 2 if tool == 'eraser' else brush_size)
                last_pos = current_pos

    screen.blit(surface, (0, 0))
    draw_interface()

    if drawing and tool in ['square', 'circle']:
        current_pos = pygame.mouse.get_pos()
        temp_surface = surface.copy()
        if tool == 'square':
            pygame.draw.rect(temp_surface, current_color,
                             (min(last_pos[0], current_pos[0]),
                              min(last_pos[1], current_pos[1]),
                              abs(current_pos[0] - last_pos[0]),
                              abs(current_pos[1] - last_pos[1])), brush_size)
        elif tool == 'circle':
            radius = int(((current_pos[0] - last_pos[0]) ** 2 +
                          (current_pos[1] - last_pos[1]) ** 2) ** 0.5)
            pygame.draw.circle(temp_surface, current_color, last_pos, radius, brush_size)
        screen.blit(temp_surface, (0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()