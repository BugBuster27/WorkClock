import time
import pygame
import sys
import math
import re
import random

pygame.init()
window_size = (200, 200)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Clock")
font = pygame.font.Font(None, 24)
show_menu = False
input_active = False
input_text_var = ""
error_text_var = ""
clock_color = (255, 255, 255)
old_mouse_x = 0
old_mouse_y = 0

img_icon = pygame.image.load("./icon.png")
pygame.display.set_icon(img_icon)

target_time = "18:10:00"

running = True
clock = pygame.time.Clock()

def draw_hand(color, angle, length):
    angle_rad = math.radians(angle)
    x = window_size[0] // 2 + length * math.cos(angle_rad)
    y = window_size[1] // 2 + 15 + length * math.sin(angle_rad)
    pygame.draw.line(screen, color, (window_size[0] // 2, window_size[1] // 2 + 15), (x, y), 2)

def is_valid_time_format(input_string):
    time_pattern = r'^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'
    
    if re.match(time_pattern, input_string):
        return True
    else:
        return False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    input_text_var = input_text_var[:-1]
                else:
                    input_text_var += event.unicode
    
    screen.fill((255, 255, 255))
    current_time = time.localtime()
    seconds, minutes, hours = current_time.tm_sec, current_time.tm_min, current_time.tm_hour % 12

    if show_menu == False:
        
        # Clock face
        pygame.draw.circle(screen, clock_color, (window_size[0] // 2, window_size[1] // 2 + 15), (window_size[1] // 2) - 20, 0)
        
        # Clock outline
        pygame.draw.circle(screen, (0, 0, 0), (window_size[0] // 2, window_size[1] // 2 + 15), (window_size[1] // 2) - 20, 1)

        # Clock hands
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
        
        # area
        # left, top, width, height
        # 115, 10, 75, 18
        
        if 115 < pygame.mouse.get_pos()[0] < 190:
            if 10 < pygame.mouse.get_pos()[1] < 28:
                if pygame.mouse.get_pressed()[0] == True:
                    show_menu = True
                    input_text_var = target_time
        
        
        circle_center = (window_size[0] // 2, window_size[1] // 2 + 15)
        circle_radius = (window_size[1] // 2) - 20
        distance_to_center = math.sqrt((pygame.mouse.get_pos()[0] - circle_center[0]) ** 2 + (pygame.mouse.get_pos()[1] - circle_center[1]) ** 2)
        if distance_to_center < circle_radius and pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos()[0] != old_mouse_x or pygame.mouse.get_pos()[1] != old_mouse_y:
                clock_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                old_mouse_x = pygame.mouse.get_pos()[0]
                old_mouse_y = pygame.mouse.get_pos()[1]
        else:
            clock_color = (255, 255, 255)
        
        
        # Clock centre dot
        pygame.draw.circle(screen, (0, 0, 0), (window_size[0] // 2, window_size[1] // 2 + 15), 2)
    
    if show_menu == True:
        
        # Close button
        pygame.draw.rect(screen, (0, 0, 0), (130, 180, 70, 20))
        
        # Close text
        close_text = font.render("Close", True, (255, 0, 255))
        close_text_rect = close_text.get_rect(center=(165, 190))
        screen.blit(close_text, close_text_rect)
        
        if 130 < pygame.mouse.get_pos()[0] < 200:
            if 180 < pygame.mouse.get_pos()[1] < 200:
                if pygame.mouse.get_pressed()[0] == True:
                    show_menu = False
                    error_text_var = ""
        
        # Input box
        pygame.draw.rect(screen, (0, 0, 0), (48, 78, 104, 24))
        
        if input_active == False:
            pygame.draw.rect(screen, (170, 170, 170), (50, 80, 100, 20))
        elif input_active == True:
            pygame.draw.rect(screen, (240, 240, 240), (50, 80, 100, 20))
        
        if pygame.mouse.get_pressed()[0] == True:
            if 50 < pygame.mouse.get_pos()[0] < 150:
                if 80 < pygame.mouse.get_pos()[1] < 100:
                    input_active = True
                else:
                    input_active = False
            else:
                input_active = False
        
        # Input text
        input_text = font.render(input_text_var, True, (255, 0, 255))
        input_text_rect = input_text.get_rect(center=(100, 90))
        screen.blit(input_text, input_text_rect)
        
        # Submit button
        pygame.draw.rect(screen, (0, 0, 0), (75, 120, 50, 20))
        
        # Submit text
        submit_text = font.render("Save", True, (255, 0, 255))
        submit_text_rect = submit_text.get_rect(center=(100, 130))
        screen.blit(submit_text, submit_text_rect)
        
        if 75 < pygame.mouse.get_pos()[0] < 125:
            if 120 < pygame.mouse.get_pos()[1] < 140:
                if pygame.mouse.get_pressed()[0] == True:
                    if input_text_var != "":
                        if is_valid_time_format(input_text_var) == True:
                            target_time = input_text_var
                            error_text_var = "Submitted"
                        else:
                            error_text_var = "Enter a valid time"
                    else:
                        error_text_var = "Can't be blank"

        
        # Error message
        error_text = font.render(error_text_var, True, (255, 0, 255))
        error_text_rect = error_text.get_rect(center=(100, 40))
        screen.blit(error_text, error_text_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
