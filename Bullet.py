import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,position,speed):
        pygame.sprite.Sprite.__init__(self)
        self.rect=self.img.get_rect()
        self.rect.center=position
        self.speed=speed
        self.mask=pygame.mask.from_surface(self.img)
    def move(self):
        self.rect=self.rect.move(self.speed)
    def show(self,screen):
        screen.blit(self.img,self.rect)

class Bullet1(Bullet):
    def __init__(self,position):
        self.img=pygame.image.load("img/bullet1.png").convert_alpha()
        Bullet.__init__(self,position,(0,-12))

class Bullet2(Bullet):
    def __init__(self,position):
        self.img=pygame.image.load("img/bullet2.png").convert_alpha()
        Bullet.__init__(self,position,(0,-12))

class Super_Bullet(Bullet):
    def __init__(self,position,xspeed):
        self.img=pygame.image.load("img/super_bullet.png").convert_alpha()
        Bullet.__init__(self,position,(xspeed,-4))