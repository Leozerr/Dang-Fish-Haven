# import pygame
import pygame
import numpy as np
from FishData import FishData
from PondData import PondData
import threading
import sys
from Client import Client
from queue import Queue

# sys.path.append('../src')
from Payload import Payload


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, pic_path):
        super().__init__()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Fish(pygame.sprite.Sprite):
    #swimRight = [pygame.image.load('images/R1E.png'),pygame.image.load('images/R2E.png'),pygame.image.load('images/R3E.png'),pygame.image.load('images/R4E.png'),pygame.image.load('images/R5E.png'),pygame.image.load('images/R6E.png'),pygame.image.load('images/R7E.png'),pygame.image.load('images/R11E.png')]#,pygame.image.load('images/R8E.png'),pygame.image.load('images/R9E.png'),pygame.image.load('images/R10E.png'),pygame.image.load('images/R11E.png')]
    #swimLeft = [pygame.image.load('images/L1E.png'),pygame.image.load('images/L2E.png'),pygame.image.load('images/L3E.png'),pygame.image.load('images/L4E.png'),pygame.image.load('images/L5E.png'),pygame.image.load('images/L6E.png'),pygame.image.load('images/L7E.png'),pygame.image.load('images/L11E.png')]#,pygame.image.load('images/L8E.png'),pygame.image.load('images/L9E.png'),pygame.image.load('images/L10E.png'),pygame.image.load('images/L11E.png')]
    swimRight = [pygame.image.load('images/swimRight/R1.png'),pygame.image.load('images/swimRight/R2.png'),pygame.image.load('images/swimRight/R3.png'),pygame.image.load('images/swimRight/R4.png'),pygame.image.load('images/swimRight/R5.png'),pygame.image.load('images/swimRight/R6.png'),pygame.image.load('images/swimRight/R7.png'),pygame.image.load('images/swimRight/R8.png')]
    swimLeft = [pygame.image.load('images/swimLeft/L1.png'),pygame.image.load('images/swimLeft/L2.png'),pygame.image.load('images/swimLeft/L3.png'),pygame.image.load('images/swimLeft/L4.png'),pygame.image.load('images/swimLeft/L5.png'),pygame.image.load('images/swimLeft/L6.png'),pygame.image.load('images/swimLeft/L7.png'),pygame.image.load('images/swimLeft/L8.png')]

    def __init__(self, pos_x, pos_y, width, height, end, fishData):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.end = end
        self.path = [0, 955] #distance of fish
        self.swimCount = 0
        self.vel = 3
        self.life = 0
        self.fishData = fishData
        #print(FishData().id + "\n" + FishData().state + "\n")
        
    
    def draw(self, screen):
        self.move()
        if self.swimCount + 1 >= 22:
            self.swimCount = 0

        if self.vel > 0:
            screen.blit(self.swimRight[self.swimCount //3], (self.x, self.y))
            self.swimCount += 1
        else:
            screen.blit(self.swimLeft[self.swimCount //3], (self.x, self.y))
            self.swimCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.swimCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.swimCount = 0
        #print("x:" + str(self.x))

    # def CountLifetime(self):
    #     while(1):
    #        self.fishData.lifetime -= 10
    #        if self.fishData.lifetime == 0:
    #            self.fishData.status("dead")
    #        print(self.fishData.lifetime)
      
        
# initialize game engine
class main() :
    pygame.init()

    window_width=999
    window_height=674

    #animation_increment=10
    clock_tick_rate=20
    sys.setrecursionlimit(1500)

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

    #test
    f1 = FishData("Dang","123456")
    f2 = FishData("Dang","123456")
    p = PondData("Dang")
    p.addFish(f1)
    p.addFish(f2)
    c = Client(p)
    msg_handler = threading.Thread(target=c.get_msg)   
    msg_handler.start() 
    send_handler = threading.Thread(target=c.send_pond)
    send_handler.start()
    c.migrate_fish(f1,"sick salmon")
    c.migrate_fish(f2,"sick salmon")    

    # Fishes
    listFish = []
    
    for s in range(5):
        f = FishData('dang','123456')
        fish = Fish(np.random.randint(0, 955), np.random.randint(0, 400), 64, 64, 450, f)
        listFish.append(fish)
        c.pond.addFish(f)
        
       
            
           
    
    while(dead==False):

        if(len(c.pond.fishes) > len(listFish)):
            fish_diff = len(c.pond.fishes)-(len(listFish))
            new_list = c.pond.fishes[len(listFish):len(c.pond.fishes)]
            for fish in new_list:
                if(fish.genesis == "peem"):
                    sfish = Fish(np.random.randint(0, 955), np.random.randint(0, 400), 64, 64, 450, fish)
                elif(fish.genesis == "sick-salmon"):
                    sfish = Fish(np.random.randint(0, 955), np.random.randint(0, 400), 64, 64, 450, fish)
                else:
                    sfish = Fish(np.random.randint(0, 955), np.random.randint(0, 400), 64, 64, 450, fish)
                listFish.append(sfish)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = True

        screen.blit(background_image, [0, 0])

        for fishess in listFish:
            fishess.life += 1
            if fishess.life < fishess.fishData.lifetime*10:
                fishess.draw(screen)
            else:
                fishess.fishData.status == "dead"
                
        for x in listFish:
            if x.fishData.status == "dead":
                c.pond.removeFish(x.fishData)
                listFish.remove(x)

            

        
        #fish.CountLifetime()
        crosshair_group.draw(screen)
        crosshair_group.update()

        pygame.display.flip()
        clock.tick(clock_tick_rate)
        