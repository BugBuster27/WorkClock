import time
import pygame
import sys
import math

pygame.init()
window_size = (200, 200)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Clock")

target_time = "17:30:00"

running = True
clock = pygame.time.Clock()

def draw_hand(color, angle, length):
    angle_rad = math.radians(angle)
    x = window_size[0] // 2 + length * math.cos(angle_rad)
    y = window_size[1] // 2 + 15 + length * math.sin(angle_rad)
    pygame.draw.line(screen, color, (window_size[0] // 2, window_size[1] // 2 + 15), (x, y), 2)

font = pygame.font.Font(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    current_time = time.localtime()
    seconds, minutes, hours = current_time.tm_sec, current_time.tm_min, current_time.tm_hour % 12

    pygame.draw.circle(screen, (0, 0, 0), (window_size[0] // 2, window_size[1] // 2 + 15), (window_size[1] // 2) - 20, 1)
    pygame.draw.circle(screen, (0, 0, 0), (window_size[0] // 2, window_size[1] // 2 + 15), 2)

    draw_hand((255, 0, 0), (seconds - 15) * 6, window_size[1] // 2 - 30)
    draw_hand((0, 255, 0), (minutes - 15) * 6, window_size[1] // 2 - 40)
    draw_hand((0, 0, 255), (hours - 3) * 30, window_size[1] // 2 - 60)

    digital_time = time.strftime("%H:%M:%S")
    text = font.render(digital_time, True, (255, 0, 0))
    text_rect = text.get_rect(center=((window_size[0] // 2) - 50, 20))
    screen.blit(text, text_rect)

    target_hours, target_minutes, target_seconds = map(int, target_time.split(":"))

    remaining_hours = target_hours - current_time.tm_hour
    remaining_minutes = target_minutes - current_time.tm_min
    remaining_seconds = target_seconds - current_time.tm_sec

    if remaining_seconds < 0:
        remaining_minutes -= 1
        remaining_seconds += 60
    if remaining_minutes < 0:
        remaining_hours -= 1
        remaining_minutes += 60
    if remaining_hours < 0:
        remaining_hours += 24

    time_difference = f"{remaining_hours:02}:{remaining_minutes:02}:{remaining_seconds:02}"
    
    text = font.render(time_difference, True, (255, 0, 0))
    text_rect = text.get_rect(center=((window_size[0] // 2) + 50, 20))
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
