from typing import Any
import pygame
from pygame.sprite import Group
#ill be honest i had a little bit of help from chat GPT cut i can asure you I am able to understand the code
pygame.init()
scx = 1000
scy = 600
speed = [1,1]
dis = pygame.display.set_mode((scx,scy))
run = True
class settings:
    def __init__(self,score,highscore,rounds,lives):
        self.score = score
        self.highscore = highscore
        self.rounds = rounds 
        self.lives = lives
        self.last = 0
    def update(self,g1,g2,pl):
        col = pygame.sprite.groupcollide(g1,g2,True,True)
        if self.score > self.highscore:
            self.highscore = self.score
        if col:
            self.score += 1
            print(self.highscore)
        now = pygame.time.get_ticks()
        if pygame.sprite.spritecollideany(pl,g2) and now - self.last >= 2000:
            self.lives -= 1
            self.last = pygame.time.get_ticks()
        

class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,xp,yp,accelerate):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x,y))
        self.rect = self.image.get_rect(center = (xp,yp))
        self.speedd = accelerate
        self.image.fill('Red')
    def update(self):
        self.rect.y -= self.speedd


def reset(s,group):
    s = 0
    group.empty()
    createfleet(20,group)
    return s
    

def createfleet(fl,grop):
        ee11 = enemies(40,40,fl,scy//2 -230,1)
        ee111 = enemies(40,40,fl+100,scy//2 -230,1)
        ee211 = enemies(40,40,fl+250,scy//2 -230,1)
        ee311 = enemies(40,40,fl+400,scy//2 -230,1)
        
        ee22 = enemies(40,40,fl,scy//2 -130,1)
        ee122 = enemies(40,40,fl+100,scy//2 -130,1)
        ee222 = enemies(40,40,fl+250,scy//2 -130,1)
        ee322 = enemies(40,40,fl+400,scy//2 -130,1)

        ee33 = enemies(40,40,fl,scy//2 -30,1)
        ee133 = enemies(40,40,fl+100,scy//2 -30,1)
        ee233 = enemies(40,40,fl+250,scy//2 -30,1)
        ee333 = enemies(40,40,fl+400,scy//2 -30,1)

        grop.add(ee11,ee111,ee211,ee311,ee22,ee122,ee222,ee322,ee33,ee133,ee233,ee333)




class ship(pygame.sprite.Sprite):
    def __init__(self,x,y,xpo,ypo,speed_lis,bullet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x,y))
        self.rect = self.image.get_rect(center = (xpo,ypo))
        self.image.fill('Black')
        self.bullet = bullet
        self.speed_lis = speed_lis
        self.last = pygame.time.get_ticks()

    def move(self,side,bg):
        motion  = 0
        cooldown = 400
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.right <= side: 
            motion = self.speed_lis[0] 
        if keys[pygame.K_a] and self.rect.left >= 0: 
            motion = -self.speed_lis[1]
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last >= cooldown:
                newbull = self.bullet(10,15,self.rect.centerx,self.rect.top,10)
                bg.add(newbull)
                self.last = pygame.time.get_ticks()
        self.rect.x += motion

def check(g1):
    drop = False
    for g in g1.sprites():
        if g.rect.left <= -10 or g.rect.right >= 1000:
            drop = True
            break
        
    if drop:
        for i in g1:
            i.rect.y += 15
            i.spe *= -1
            
                


            
class enemies(pygame.sprite.Sprite):
    def __init__(self,x,y,xpo,ypo,spe):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x,y))
        self.rect = self.image.get_rect(center = (xpo,ypo))
        self.spe = spe
    def update(self):
        self.rect.x += self.spe
        if self.rect.bottom >= 600:
            print('lose')
        






settin = settings(0,0,0,3)
player = ship(20,20,scx//2,scy//2+260,speed,bullet)
bullets = Group()
players = Group(player)
emies = Group()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
lass = pygame.time.get_ticks()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            exit()
    dis.fill('White')
    highscored = my_font.render("highscore: "+str(settin.highscore),False,(0,0,0))
    dis.blit(highscored, (scx//2,0))
    scored = my_font.render("current score: "+str(settin.score),False,(0,0,0))
    dis.blit(scored, (0,0))
    rounds = my_font.render(str(settin.rounds),False,(0,0,0))
    dis.blit(rounds, (0,30))
    lives = my_font.render(str(settin.lives),False,(0,0,0))
    dis.blit(lives, (30,30))
    now = pygame.time.get_ticks()
    if pygame.sprite.spritecollideany(player,emies)and settin.lives <= 0 :
        settin.score = reset(settin.score,emies)
        settin.rounds = 0
    elif pygame.sprite.spritecollideany(player,emies)and settin.lives > 0 and now - lass >= 2000:
        emies.empty()
        createfleet(10,emies)
        lass = pygame.time.get_ticks()
        settin.lives = 3
    
    players.draw(dis)
    player.move(scx,bullets)
    emies.update()
    check(emies)
    emies.draw(dis)
    
    if not emies.sprites():
        createfleet(10,emies)
        settin.rounds += 1

    bullets.update()
    bullets.draw(dis)
    settin.update(bullets,emies,player)
    pygame.display.update()