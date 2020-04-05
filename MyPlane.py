import pygame
import Bullet

pygame.mixer.init()
me_down_sound=pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
bomb_sound=pygame.mixer.Sound("sound/bomb.wav")
bomb_sound.set_volume(0.2)
bullet_sound=pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)

class MyPlane(pygame.sprite.Sprite):
    def __init__(self,size):
        pygame.sprite.Sprite.__init__(self)
        self.imgs=[pygame.image.load("img/me1.png").convert_alpha(),pygame.image.load("img/me2.png").convert_alpha()]
        self.img_n=0
        self.destroy_imgs=[pygame.image.load("img/me_destroy1.png").convert_alpha(),pygame.image.load("img/me_destroy2.png").convert_alpha(),pygame.image.load("img/me_destroy3.png").convert_alpha(),pygame.image.load("img/me_destroy4.png").convert_alpha()]
        self.rect=self.imgs[0].get_rect()
        self.width,self.height=size
        self.speed=10
        self.up=self.down=self.left=self.right=0
        self.mask=pygame.mask.from_surface(self.imgs[0])
        self.bullets=[]
        self.bullet_n=0
        self.bomb_img=pygame.image.load("img/bomb.png").convert_alpha()
        self.life_img=pygame.image.load("img/life.png").convert_alpha()
        self.reset()
    def reset(self):
        self.rect.centerx=self.width//2
        self.rect.bottom=self.height-60
        self.destroy_n=-1
        self.bomb_num=3
        self.bullet_type=1
        self.bullet_interval=10
        self.invincible=160
        pygame.time.set_timer(pygame.USEREVENT+1,0)
    def move_up(self):
        self.rect.top-=self.speed
        if self.rect.top<0:
            self.rect.top=0
    def move_down(self):
        self.rect.bottom+=self.speed
        if self.rect.bottom>self.height-60:
            self.rect.bottom=self.height-60
    def move_left(self):
        self.rect.left-=self.speed
        if self.rect.left<0:
            self.rect.left=0
    def move_right(self):
        self.rect.right+=self.speed
        if self.rect.right>self.width:
            self.rect.right=self.width
    def move(self):
        if self.destroy_n<0:
            if self.up:
                self.move_up()
            if self.down:
                self.move_down()
            if self.left:
                self.move_left()
            if self.right:
                self.move_right()
        elif self.destroy_n==12:
            self.life-=1
            if self.life>=0:
                self.reset()
        else:
            self.destroy_n+=1
    def destroy(self):
        self.destroy_n=0
        me_down_sound.play()
    def img(self):
        if self.destroy_n<0:
            self.img_n=(self.img_n+1)%10
            return self.imgs[self.img_n//5]
        else:
            return self.destroy_imgs[self.destroy_n//3]
    def show(self,screen):
        if self.destroy_n<0 or self.destroy_n%3==1:
            if self.invincible%16<12:
                screen.blit(self.img(),self.rect)
        for i in range(self.bomb_num):
            screen.blit(self.bomb_img,(10+i*self.bomb_img.get_width(),self.height-5-self.bomb_img.get_height()))
        for i in range(self.life):
            screen.blit(self.life_img,(self.width-10-self.life_img.get_width()*(i+1),self.height-5-self.life_img.get_height()))
    def collide(self,enemies):
        score=0
        if self.destroy_n<0:
            if self.invincible:
                self.invincible-=1
            else:
                for each in enemies:
                    if each.destroy_n<0 and pygame.sprite.collide_mask(self,each):
                        each.destroy()
                        score+=each.score
                if score:
                    self.destroy()
        return score
    def bullet(self):
        if self.destroy_n<0:
            if self.bullet_type==1:
                self.bullets.append(Bullet.Bullet1(self.rect.midtop))
            elif self.bullet_type==2:
                self.bullets.append(Bullet.Bullet2((self.rect.centerx-33,self.rect.centery)))
                self.bullets.append(Bullet.Bullet2((self.rect.centerx+33,self.rect.centery)))
            else:
                self.bullets.append(Bullet.Super_Bullet(self.rect.midtop,0))
                self.bullets.append(Bullet.Super_Bullet((self.rect.centerx-17,self.rect.centery),-1))
                self.bullets.append(Bullet.Super_Bullet((self.rect.centerx+17,self.rect.centery),1))
                self.bullets.append(Bullet.Super_Bullet((self.rect.centerx-33,self.rect.centery),-2))
                self.bullets.append(Bullet.Super_Bullet((self.rect.centerx+33,self.rect.centery),2))
            bullet_sound.play()
    def bullet_make(self):
        self.bullet_n=(self.bullet_n+1)%self.bullet_interval
        if not self.bullet_n:
            self.bullet()
    def bullet_move(self):
        for each in self.bullets:
            each.move()
            if each.rect.bottom<=0:
                self.bullets.remove(each)
    def bullet_collide(self,enemies):
        score=0
        for each in self.bullets:
            for enemy in enemies:
                if enemy.destroy_n<0 and pygame.sprite.collide_mask(each,enemy):
                    enemy.attacked()
                    if not enemy.destroy_n:
                        score+=enemy.score
                    self.bullets.remove(each)
                    break
        if score:
            self.bullet()
        return score
    def bullet_show(self,screen):
        for each in self.bullets:
            each.show(screen)
    def usebomb(self,enemies):
        score=0
        if self.destroy_n<0 and self.bomb_num:
            bomb_sound.play()
            self.bomb_num-=1
            for each in enemies:
                if each.rect.bottom>0 and each.destroy_n<0:
                    each.destroy()
                    score+=each.score
        return score
    def getsupply(self,supplies):
        if self.destroy_n<0:
            for each in supplies:
                if each.active and pygame.sprite.collide_mask(self,each):
                    each.active=0
                    each.event(self)
                    break
    def bullet_check(self):
        if self.bullet_type==2:
            self.bullet2_time-=1
            if not self.bullet2_time:
                self.bullet_type=1
                pygame.time.set_timer(pygame.USEREVENT+1,0)
        elif self.bullet_type==3:
            self.bullet3_time-=1
            if not self.bullet3_time:
                self.bullet_type=1
                pygame.time.set_timer(pygame.USEREVENT+2,0)