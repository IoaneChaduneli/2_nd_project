import pygame
from utils import load_sprites, loaded_sprites_1, get_random_position, print_text
from models import SpaceShip, Asteroid, Button

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.transform.scale(load_sprites('space', False),(800, 600))
        self.cloack = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.button = Button(350,450,100,50,'Start game', self.font, (0,0,255))
        self.bullets = []
        self.spaceship = SpaceShip((400,300), self.bullets.append)
        self.asteroids = []

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))
        self.message =""


    def reset_game(self):
        self.bullets = []
        self.spaceship = SpaceShip((400,300), self.bullets.append)
        self.asteroids = []
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))
        self.message =""

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Space Rocks')

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

            elif self.button.handle_event(event):
                        self.reset_game()
           
        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_d]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_s]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    self.button.draw(self.screen)
                    break
                    
                

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"
        
    def _draw(self):
        self.screen.blit(self.background,(0,0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        self.button.draw(self.screen)
        
        # self.asteroid.draw(self.screen)
        pygame.display.flip()
        self.cloack.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

        

