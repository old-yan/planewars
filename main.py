import traceback
import MyPlane
import Enemy
import Supply
import random
import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(20)

#主屏幕、背景
size=[width,height]=[480,700]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("飞机大战".center(110))
bg_img=pygame.image.load("img/background.png").convert_alpha()

#暂停、继续按钮图标
pause_img=pygame.image.load("img/pause.png").convert_alpha()
pause_pressed_img=pygame.image.load("img/pause_pressed.png").convert_alpha()
resume_img=pygame.image.load("img/resume.png").convert_alpha()
resume_pressed_img=pygame.image.load("img/resume_pressed.png").convert_alpha()
pause_rect=pause_img.get_rect()
pause_rect.right=width-10
pause_rect.top=5
pause_bg=bg_img.subsurface(pause_rect)

#音乐、音效
pygame.mixer.music.load("sound/bg_music.ogg")
pygame.mixer.music.set_volume(0.1)
button_sound=pygame.mixer.Sound("sound/button.wav")
button_sound.set_volume(0.2)
supply_sound=pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
upgrade_sound=pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)

def main():
    #播放背景音乐
    pygame.mixer.music.play(-1)

    #我的飞机，设定生命
    myplane=MyPlane.MyPlane(size)
    myplane.life=3

    #敌机
    enemies=pygame.sprite.Group()
    enemies1=pygame.sprite.Group()
    enemies2=pygame.sprite.Group()
    enemies3=pygame.sprite.Group()
    def add_enemy1(n):
        for i in range(n):
            e=Enemy.Enemy1(size)
            enemies.add(e)
            enemies1.add(e)
    def add_enemy2(n):
        for i in range(n):
            e=Enemy.Enemy2(size)
            enemies.add(e)
            enemies2.add(e)
    def add_enemy3(n):
        for i in range(n):
            e=Enemy.Enemy3(size)
            enemies.add(e)
            enemies3.add(e)
    def speedup(group,increment):
        for each in group:
            each.speed+=increment
    add_enemy1(15)
    add_enemy2(4)
    add_enemy3(2)

    #补给定时，设置定时事件
    supplies=[Supply.Bullet_Supply(size),Supply.Bomb_Supply(size),Supply.Super_Supply(size)]
    for each in supplies:
        each.active=0
    SUPPLY_COME=pygame.USEREVENT
    supply_time=300
    supply_n=supply_time
    pygame.time.set_timer(SUPPLY_COME,100)
    BULLET2_RESET=pygame.USEREVENT+1
    BULLET3_RESET=pygame.USEREVENT+2

    #分数
    score=0
    score_font=pygame.font.Font("font/xiaozhuan.ttf",36)

    #设置难度级别
    level=1
    level_font=pygame.font.Font("font/xiaozhuan.ttf",36)
    level_dict=["简单","普通","困难","王者","地狱"]

    def levelup():
        nonlocal level
        if level==1:
            if score>5000:
                level=2
                upgrade_sound.play()
                add_enemy1(3)
                add_enemy2(2)
                add_enemy3(1)
                speedup(enemies1,1)
        elif level==2:
            if score>30000:
                level=3
                upgrade_sound.play()
                add_enemy1(5)
                add_enemy2(3)
                add_enemy3(2)
                speedup(enemies1,1)
                speedup(enemies2,1)
        elif level==3:
            if score>100000:
                level=4
                upgrade_sound.play()
                add_enemy1(5)
                add_enemy2(3)
                add_enemy3(2)
                speedup(enemies1,1)
                speedup(enemies2,1)
        elif level==4:
            if score>300000:
                level=5
                upgrade_sound.play()
                add_enemy1(5)
                add_enemy2(3)
                add_enemy3(2)
                speedup(enemies,1)
    running=1
    paused=0
    usebomb=0
    ending=0
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=0
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    myplane.up+=1
                elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    myplane.down+=1
                elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    myplane.left+=1
                elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    myplane.right+=1
                elif event.key==pygame.K_SPACE:
                    if not paused:
                        usebomb=1
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_UP or event.key==pygame.K_w:
                    myplane.up-=1
                elif event.key==pygame.K_DOWN or event.key==pygame.K_s:
                    myplane.down-=1
                elif event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    myplane.left-=1
                elif event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    myplane.right-=1
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if pause_rect.collidepoint(event.pos):
                        if paused and resume_img.get_at((event.pos[0]-pause_rect.left,event.pos[1]-pause_rect.top))[3]:
                            paused=0
                            button_sound.play()
                            pygame.time.set_timer(SUPPLY_COME,100)
                            if myplane.bullet_type==2:
                                pygame.time.set_timer(BULLET2_RESET,100)
                            if myplane.bullet_type==3:
                                pygame.time.set_timer(BULLET3_RESET,100)
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
                        elif not paused and pause_img.get_at((event.pos[0]-pause_rect.left,event.pos[1]-pause_rect.top))[3]:
                            paused=1
                            usebomb=0
                            button_sound.play()
                            pygame.time.set_timer(SUPPLY_COME,0)
                            if myplane.bullet_type==2:
                                pygame.time.set_timer(BULLET2_RESET,0)
                            if myplane.bullet_type==3:
                                pygame.time.set_timer(BULLET3_RESET,0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
            elif event.type==SUPPLY_COME:
                supply_n-=1
                if not supply_n:
                    supply_n=supply_time
                    supply_sound.play()
                    rand=random.randint(0,9)
                    if rand<5:
                        supplies[0].reset()
                    elif rand<9:
                        supplies[1].reset()
                    else:
                        supplies[2].reset()
            elif event.type==BULLET2_RESET or event.type==BULLET3_RESET:
                myplane.bullet_check()
        if running:
            if paused:
                screen.blit(pause_bg,pause_rect)
                pos=pygame.mouse.get_pos()
                if pause_rect.collidepoint(pos) and resume_img.get_at((pos[0]-pause_rect.left,pos[1]-pause_rect.top))[3]:
                    screen.blit(resume_pressed_img,pause_rect)
                else:
                    screen.blit(resume_img,pause_rect)
            else:
                screen.blit(bg_img,(0,0))
                #敌机行动
                for each in enemies:
                    each.move()
                #炸弹行动
                if usebomb:
                    usebomb=0
                    score+=myplane.usebomb(enemies)
                #子弹行动
                myplane.bullet_make()
                myplane.bullet_move()
                score+=myplane.bullet_collide(enemies)
                #飞机行动
                myplane.move()
                score+=myplane.collide(enemies)
                #补给行动
                for each in supplies:
                    each.move()
                myplane.getsupply(supplies)
                #敌机画出
                for each in enemies3:
                    each.show(screen)
                for each in enemies2:
                    each.show(screen)
                for each in enemies1:
                    each.show(screen)
                #子弹画出
                myplane.bullet_show(screen)
                #补给画出
                for each in supplies:
                    each.show(screen)
                #飞机画出（包括炸弹、生命）
                myplane.show(screen)
                #分数画出
                screen.blit(score_font.render("Score: %09d"%score,1,(0,0,0)),(10,5))
                #等级画出
                levelup()
                screen.blit(level_font.render("Level: %s"%level_dict[level-1],1,(0,0,0)),(10,5+score_font.get_linesize()))
                #按钮画出
                pos=pygame.mouse.get_pos()
                if pause_rect.collidepoint(pos) and pause_img.get_at((pos[0]-pause_rect.left,pos[1]-pause_rect.top))[3]:
                    screen.blit(pause_pressed_img,pause_rect)
                else:
                    screen.blit(pause_img,pause_rect)
                if myplane.life<0:
                    running=0
                    ending=1
            pygame.display.flip()
            pygame.time.delay(20)
    if ending:
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        pygame.time.set_timer(SUPPLY_COME,0)
        pygame.time.set_timer(BULLET2_RESET,0)
        pygame.time.set_timer(BULLET3_RESET,0)
        with open("record.txt",'r') as file:
            try:
                best_score=int(file.read())
            except:
                best_score=0
        if best_score<score:
            best_score=score
            with open("record.txt",'w') as file:
                file.write(str(score))
        end_font=pygame.font.Font("font/xiaozhuan.ttf",50)
        font1=score_font.render("Best Score:%d"% best_score,1,(0,0,0))
        font1_rect=font1.get_rect()
        font1_rect.left,font1_rect.top=50,50
        font2=end_font.render("Your Score:",1,(0,0,0))
        font2_rect=font2.get_rect()
        font2_rect.centerx=width//2
        font2_rect.top=230
        font3=end_font.render("%d"%score,1,(0,0,0))
        font3_rect=font3.get_rect()
        font3_rect.centerx=width//2
        font3_rect.top=300
        gameover_img=pygame.image.load("img/gameover.png").convert_alpha()
        gameover_rect=gameover_img.get_rect()
        gameover_rect.centerx=width//2
        gameover_rect.top=420
        gameover_pressed_img=pygame.image.load("img/gameover_pressed.png").convert_alpha()
        gameover_pressed_rect=gameover_pressed_img.get_rect()
        gameover_pressed_rect.center=gameover_rect.center
        restart_img=pygame.image.load("img/restart.png").convert_alpha()
        restart_rect=gameover_img.get_rect()
        restart_rect.centerx=width//2
        restart_rect.top=480
        restart_pressed_img=pygame.image.load("img/restart_pressed.png").convert_alpha()
        restart_pressed_rect=restart_pressed_img.get_rect()
        restart_pressed_rect.center=restart_rect.center
    while ending:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                ending=0
                break
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if restart_rect.collidepoint(event.pos) and restart_img.get_at((event.pos[0]-restart_rect.left,event.pos[1]-restart_rect.top))[3]:
                        Enemy.enemy3_flying_playlist.clear()
                        return 1
                    elif gameover_rect.collidepoint(event.pos) and gameover_img.get_at((event.pos[0]-gameover_rect.left,event.pos[1]-gameover_rect.top))[3]:
                        return 0
        if ending:
            screen.blit(bg_img,(0,0))
            screen.blit(font1,font1_rect)
            screen.blit(font2,font2_rect)
            screen.blit(font3,font3_rect)
            pos=pygame.mouse.get_pos()
            if gameover_rect.collidepoint(pos) and gameover_img.get_at((pos[0]-gameover_rect.left,pos[1]-gameover_rect.top))[3]:
                screen.blit(gameover_pressed_img,gameover_pressed_rect)
            else:
                screen.blit(gameover_img,gameover_rect)
            if restart_rect.collidepoint(pos) and restart_img.get_at((pos[0]-restart_rect.left,pos[1]-restart_rect.top))[3]:
                screen.blit(restart_pressed_img,restart_pressed_rect)
            else:
                screen.blit(restart_img,restart_rect)
            pygame.display.flip()
            pygame.time.delay(20)
    return 0

if __name__=="__main__":
    restart=1
    while restart:
        try:
            restart=main()
        except:
            restart=0
            traceback.print_exc()
            a=input()
    pygame.quit()