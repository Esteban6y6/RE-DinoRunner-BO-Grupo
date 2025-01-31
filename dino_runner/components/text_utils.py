import pygame

from dino_runner.utils.constants import (FONT_STYLE, BLACK_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT)



def get_score_element(points):
    font = pygame.font.Font(FONT_STYLE, 20)

    text = font.render('Points ' + str(points), True, BLACK_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (1000, 50)
    return text, text_rect

def get_max_score_elements(max_score):
    font = pygame.font.Font(FONT_STYLE, 20)

    text = font.render('Max Point ' + str(max_score), True, BLACK_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (800, 50)
    return text, text_rect

def get_centered_message(message, width=SCREEN_WIDTH // 2, heigth=SCREEN_HEIGHT //2):
    font = pygame.font.Font(FONT_STYLE, 30)

    text = font.render(message, True, BLACK_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (width, heigth)
    return text, text_rect