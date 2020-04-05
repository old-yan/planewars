import pygame
import random

pygame.mixer.init()
get_bomb_sound=pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound=pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
get_super_sound=pygame.mixer.Sound("sound/get_super.wav")
get_super_sound.set_volume(0.2)


class Supply(pygame.sprite.Sprite):
    def __init__(self,size):
        pygame.sprite.Sprite.__init__(self)
        self.rect=self.img.get_rect()
        self.width,self.height=size
        self.reset()
        self.speed=5
        self.mask=pygame.mask.from_surface(self.img)
    def reset(self):
        self.rect.left=random.randint(0,self.width-self.rect.width)
        self.rect.top=-100
        self.active=1
    def move(self):
        if self.active:
            self.rect.top+=self.speed
            if self.rect.top>=self.height:
                self.active=0
    def show(self,screen):
        if self.active:
            screen.blit(self.img,self.rect)

class Bullet_Supply(Supply):
    def __init__(self,size):
        self.img=pygame.image.load("img/bullet_supply.png").convert_alpha()
        Supply.__init__(self,size)
    def event(self,plane):
        get_bullet_sound.play()
        plane.bullet_type=2
        plane.bullet2_time=180
        pygame.time.set_timer(pygame.USEREVENT+1,100)

class Bomb_Supply(Supply):
    def __init__(self,size):
        self.img=pygame.image.load("img/bomb_supply.png").convert_alpha()
        Supply.__init__(self,size)
    def event(self,plane):
        get_bomb_sound.play()
        if plane.bomb_num<3:
            plane.bomb_num+=1

class Super_Supply(Supply):
    def __init__(self,size):
        self.img=pygame.image.load("img/super_supply.png").convert_alpha()
        Supply.__init__(self,size)
    def event(self,plane):
        get_super_sound.play()
        plane.bullet_type=3
        plane.bullet3_time=100
        pygame.time.set_timer(pygame.USEREVENT+2,100)