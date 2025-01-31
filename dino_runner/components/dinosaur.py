import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, DEFAULT_TYPE, DUCKING, JUMPING, SHIELD_TYPE, DUCKING_SHIELD, RUNNING_SHIELD, JUMPING_SHIELD, HAMMER_TYPE, DUCKING_HAMMER, RUNNING_HAMMER, JUMPING_HAMMER


class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 320
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}

        self.image = self.run_img[DEFAULT_TYPE][0]
        self.type = DEFAULT_TYPE
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.steps = 0 
        self.running = True
        self.ducking = False
        self.jumping = False
        self.jump_vel = self.JUMP_VEL

        self.has_lives = True

        self.setup_state_booleans()
    

    def setup_state_booleans(self):
        self.has_power_up = False
        self.shield = False
        self.hammer = False
        self.show_text = False
        self.shield_time_up = 0
        self.hammer_time_up = 0

    def update(self, input_user):
        if self.running:
            self.run()

        if self.ducking:
            self.duck()    
        
        if self.jumping:
            self.jump()
        
        if input_user[pygame.K_DOWN] and not self.jumping:
            self.ducking = True
            self.jumping = False
            self.running = False 
        elif input_user[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.ducking = False
            self.running = False  
        elif not self.jumping:
            self.running = True
            self.jumping = False
            self.ducking = False

        if self.steps >= 10:
            self.steps = 0 

    def run(self):
        self.image = self.run_img[self.type][self.steps // 5] 
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.steps += 1
    
    def duck(self):
        self.image = self.duck_img[self.type][self.steps // 5] 
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS + 30
        self.steps += 1

    def jump(self):
        self.image = self.jump_img[self.type]
        self.image = JUMPING
        if self.jumping:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.jumping = False
            self.jump_vel = self.JUMP_VEL
     

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))    
    
    def check_visibility(self, screen):
        if self.shield:
            time_to_show = round( (self.shield_time_up - pygame.time.get_ticks()) / 1000,2)
            if (time_to_show >= 0):
                found = pygame.font.Font('freesansbold.ttf', 18)
                text = found.render(f'shield enable for {time_to_show}', True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (500, 40)
                screen.blit(text, textRect)
            else:
                self.shield = False
                self.update_to_default(SHIELD_TYPE)

    def update_to_default(self, curren_type):
        if self.type == curren_type:
            self.type = DEFAULT_TYPE