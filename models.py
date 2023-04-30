import pygame

from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import loaded_sprites_1, wrap_position, get_random_velocity, load_sound

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius  

   
        

UP = Vector2(0,-1)

class SpaceShip(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound('Laser')
        self.direction = Vector2(UP)
        super().__init__(position, pygame.transform.scale(loaded_sprites_1('spaceship_3'), (50,50)), Vector2(0))

    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_w]:
            self.velocity += self.direction * self.ACCELERATION
        elif is_key_pressed[pygame.K_s]:
            self.velocity -= self.direction * self.ACCELERATION


    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Asteroid(GameObject):
    def __init__(self, position,create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.explosion_sound = load_sound('asteroid')
        self.destruction_sound = load_sound('destruction_sound')
        self.size = size

        size_to_scale = {
            3:1,
            2:0.5,
            1:0.25
        }
        scale = size_to_scale[size]
        sprite = rotozoom(pygame.transform.scale(loaded_sprites_1('asteroid_3'), (100,100)), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1,3))
    
    def split(self):
        if self.size > 1:
            self.explosion_sound.play()
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)
                self.destruction_sound.play()


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, pygame.transform.scale(loaded_sprites_1('bullets'), (30,30)), velocity)

    def move(self, surface):
        self.position += self.velocity

class Button(pygame.Rect):
    def __init__(self, x, y, width, height, text, font, color):
        super().__init__(x, y, width, height)

        self.text = text
        self.font = font
        self.color = color

    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)
        text_surface = self.font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center = self.center)
        surface.blit(text_surface, text_rect)

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(event.pos):
            return True
        return False