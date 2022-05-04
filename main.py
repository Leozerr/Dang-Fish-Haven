# import pygame
import pygame

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, pic_path):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Fish(pygame.sprite.Sprite):
    def __init__(self, pic_path, pos_x, pos_y):
        super().__init__()
        self.image
# initialize game engine
class main() :
    pygame.init()

    window_width=999
    window_height=674

    animation_increment=10
    clock_tick_rate=20

    # Open a window
    size = (window_width, window_height)
    screen = pygame.display.set_mode(size)

    # Set title to the window
    pygame.display.set_caption("Dang Pond")

    dead=False

    clock = pygame.time.Clock()
    background_image = pygame.image.load('images/bg.jpg').convert()
    pygame.mouse.set_visible(False)

    # Crosshair
    crosshair = Crosshair('images/crosshair.png')
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)

    while(dead==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = True

        screen.blit(background_image, [0, 0])
        crosshair_group.draw(screen)
        crosshair_group.update()

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        