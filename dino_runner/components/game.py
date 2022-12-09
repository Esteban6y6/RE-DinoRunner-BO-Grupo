import pygame
from dino_runner.components.obstacles.obstacle_manager import ObstacleManage
from dino_runner.components.player_heart.player_heart_manager import PlayerHeartManager
from dino_runner.components.power_ups.power_up_manage import PowerUpManager


from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, WHITE_COLOR
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components import text_utils

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        pygame.mixer.music.load('dino_runner/assets/chill.mp3')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dino = Dinosaur()
        self.obstacle_manager = ObstacleManage()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.max_score = 0
        self.death_count = 0
        self.running = True

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
        

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager = ObstacleManage()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager.reset_power_ups(self.points)
        pygame.mixer.music.play(-1) #mixer para reproducir musica
        self.playing = True
        self.game_speed = 20
        self.points = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        input_user = pygame.key.get_pressed()
        self.dino.update(input_user)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.dino)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.clock.tick(FPS)
        if self.points <= 1000:
            self.screen.fill((255, 255, 255))
        else:
            self.screen.fill((50, 50, 50))
        self.score()
        self.draw_power_up_time()
        self.draw_background()
        self.dino.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
 
        pygame.display.update()
        pygame.display.flip()

    def draw_power_up_time(self):
        if self.dino.has_power_up:
            time_to_show = round((self.dino.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                font = pygame.font.Font(FONT_STYLE, 22)
                text = font.render(f"{self.dino.type.capitalize()} enabled for {time_to_show} seconds.", True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (550, 50)
                self.screen.blit(text, text_rect)
            else:
                self.has_power_up = False
                self.dino.type = DEFAULT_TYPE

    def show_menu(self):
        self.running = True
        self.screen.fill(WHITE_COLOR)
        self.print_menu_elements()
        
        pygame.display.update()

        self.handle_key_events_on_menu()
    

    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text, text_rect =text_utils.get_centered_message('press any key to start')
            self.screen.blit(text, text_rect)
        elif self.death_count > 0:
            text, text_rect = text_utils.get_centered_message('press any key to restart')
            score, score_rect = text_utils.get_centered_message('Your score is ' + str(self.points), heigth=half_screen_height + 50)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count), heigth=half_screen_height + 100)
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(death, death_rect)
        
        pygame.display.update()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.run()

    def score(self):
        self.points += 1

        if self.points % 100 == 0:
            self.game_speed +=1
        if self.max_score < self.points:
            self.max_score = self.points

        (text, text_rect) = text_utils.get_score_element(self.points)
        self.screen.blit(text, text_rect)
        (text, text_rect) = text_utils.get_max_score_elements(self.max_score)
        
        self.dino.check_visibility(self.screen)
        
        self.screen.blit(text, text_rect)

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_power_up_active(self):
        if self.dino.has_power_up:
            time_to_show = round((self.dino.power_up_time_up - pygame.time.get_ticks())/1000)
            if time_to_show >=0:
                font = pygame.font.Font(FONT_STYLE, 30)
                powerup_text = font.render(f"Time left: {time_to_show} ", True, (0,0,0) )
                self.screen.blit(powerup_text, (1,1))
                pygame.display.update()
            else:
                self.dino.has_power_up = False
                self.dino.type = DEFAULT_TYPE
