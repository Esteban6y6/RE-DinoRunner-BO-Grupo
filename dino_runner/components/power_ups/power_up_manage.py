from secrets import choice
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
import random
import pygame

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.points = 0
        self.when_appears = 0


    def update(self, points, game_speed, player):
        self.generate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if (player.dino_rect.colliderect(power_up.rect)):
                power_up.start_time = pygame.time.get_ticks()
                player.shield = True
                player.type = power_up.type
                power_up.start_time = pygame.time.get_ticks()
                time_random = random.randrange(5, 8)
                player.shield_time_up = power_up.start_time + (time_random * 1000)

                self.power_ups.remove(power_up)    
            
    
    def generate_power_ups(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            choice = random.randint(0, 1)
            if choice == 0:
                self.power_ups.append(Shield())
            else:
                self.power_ups.append(Hammer())
                    
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self, points):
        self.power_ups = []
        self.points = points
        self.when_appears = random.randint(200, 300) + self.points


