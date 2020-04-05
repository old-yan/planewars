import pygame
import random

pygame.mixer.init()
enemy1_down_sound=pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound=pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound=pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound=pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.2)
enemy3_flying_playlist=set()

black=(0,0,0)
green=(0,255,0)
red=(255,0,0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,size,speed,score,blood,h,imgs,destroy_imgs,down_sound):
        pygame.sprite.Sprite.__init__(self)
        self.imgs=imgs
        self.img_n=0
        self.destroy_imgs=destroy_imgs
        self.down_sound=down_sound
        self.destroy_n=-1
        self.rect=self.imgs[0].get_rect()
        self.width,self.height=size
        self.speed=speed
        self.mask=pygame.mask.from_surface(self.imgs[0])
        self.score=score
        self.fullblood=blood
        self.init_height=h
        self.reset()
        self.rect=self.rect.move((0,-self.height//2))
    def reset(self):
        self.rect.left=random.randint(0,self.width-self.rect.width)
        self.rect.bottom=random.randint(-self.init_height*self.height,0)
        self.destroy_n=-1
        self.blood=self.fullblood
    def move(self):
        if self.destroy_n<3*len(self.destroy_imgs) and self.rect.top<self.height:
            if hasattr(self,"flying_sound") and self.rect.bottom>=-50 and self not in self.flying_playlist:
                if not len(self.flying_playlist):
                    enemy3_flying_sound.play(-1)
                enemy3_flying_playlist.add(self)
            self.rect.top+=self.speed
        else:
            if hasattr(self,"flying_sound"):
                self.flying_playlist.remove(self)
                if not len(self.flying_playlist):
                    self.flying_sound.stop()
            self.reset()
        if 0<=self.destroy_n<3*len(self.destroy_imgs):
            self.destroy_n+=1
    def attacked(self):
        self.destroy_n=-2
        self.blood-=1
        if not self.blood:
            self.destroy()
    def destroy(self):
        self.destroy_n=0
        self.down_sound.play()
    def img(self):
        if self.destroy_n<0:
            if self.destroy_n==-2:
                self.destroy_n=-1
                return self.hit_img
            else:
                self.img_n=(self.img_n+1)%10
                return self.imgs[self.img_n//5-1]
        else:
            return self.destroy_imgs[self.destroy_n//3]
    def show(self,screen):
        if self.destroy_n<0 or self.destroy_n%3==1:
            screen.blit(self.img(),self.rect)
            if self.fullblood>1:
                pygame.draw.line(screen,black,(self.rect.left,self.rect.top-5),(self.rect.right,self.rect.top-5),2)
                if self.blood<=self.fullblood/4:
                    pygame.draw.line(screen,red,(self.rect.left,self.rect.top-5),((self.rect.left*(self.fullblood-self.blood)+self.rect.right*self.blood)//self.fullblood,self.rect.top-5),2)
                else:
                    pygame.draw.line(screen,green,(self.rect.left,self.rect.top-5),((self.rect.left*(self.fullblood-self.blood)+self.rect.right*self.blood)//self.fullblood,self.rect.top-5),2)

class Enemy1(Enemy):
    def __init__(self,size):
        Enemy.__init__(self,size,2,1000,1,5,[pygame.image.load("img/enemy1.png").convert_alpha()],[pygame.image.load("img/enemy1_down1.png").convert_alpha(),pygame.image.load("img/enemy1_down2.png").convert_alpha(),pygame.image.load("img/enemy1_down3.png").convert_alpha(),pygame.image.load("img/enemy1_down4.png").convert_alpha()],enemy1_down_sound)

class Enemy2(Enemy):
    def __init__(self,size):
        self.hit_img=pygame.image.load("img/enemy2_hit.png").convert_alpha()
        Enemy.__init__(self,size,1,6000,8,10,[pygame.image.load("img/enemy2.png").convert_alpha()],[pygame.image.load("img/enemy2_down1.png").convert_alpha(),pygame.image.load("img/enemy2_down2.png").convert_alpha(),pygame.image.load("img/enemy2_down3.png").convert_alpha(),pygame.image.load("img/enemy2_down4.png").convert_alpha()],enemy2_down_sound)

class Enemy3(Enemy):
    def __init__(self,size):
        self.hit_img=pygame.image.load("img/enemy3_hit.png").convert_alpha()
        self.flying_sound=enemy3_flying_sound
        self.flying_playlist=enemy3_flying_playlist
        Enemy.__init__(self,size,1,10000,20,15,[pygame.image.load("img/enemy3_1.png").convert_alpha(),pygame.image.load("img/enemy3_2.png").convert_alpha()],[pygame.image.load("img/enemy3_down1.png").convert_alpha(),pygame.image.load("img/enemy3_down2.png").convert_alpha(),pygame.image.load("img/enemy3_down3.png").convert_alpha(),pygame.image.load("img/enemy3_down4.png").convert_alpha(),pygame.image.load("img/enemy3_down5.png").convert_alpha(),pygame.image.load("img/enemy3_down6.png").convert_alpha()],enemy3_down_sound)