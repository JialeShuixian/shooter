
from pygame import* #open pygame library
from random import randint#random

class GameSprite(sprite.Sprite): #class GameSprite ke thua Sprite co san trong pygame
    def __init__(self, player_image, player_x, player_y, play_speed):#nhan vat, toa do x, y, speed
        super().__init__()#chinh
        self.image = transform.scale(image.load(player_image), (60, 60))#tao hinh anh nhan vat, kick co
        self.speed = play_speed
        self.rect = self.image.get_rect() #luu toa do vao bien rect
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))#ve nhan vat len man hinh

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x <= win_width - 80:
            self.rect.x += self.speed
        
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
 
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    
    def fire(self):
        #create a bullet and 
        bullet = Bullet("shoot.png", self.rect.centerx, self.rect.top, 20)
        #add it in bullet group
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > win_height:
            self.rect.y = 100
            self.rect.x = randint(100, 790)
            miss += 1 #global variable

class Bullet(GameSprite): #inheritance gamesprite
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill() #delete sprite in pygame

win_width = 1000
win_height = 700

#Background
window = display.set_mode((win_width, win_height))#dat kick co
display.set_caption("Shooter")#ten game
backgroundd = transform.scale(image.load("galaxy.png"), (win_width, win_height))#set background
 #cung thu muc
#Player
player = Player("player.png", 5, win_height - 80, 30)#tao nhan vat, x, y, toc do

#Bullet
bullets = sprite.Group()

#Eneny
enemies = sprite.Group()
for ene in range(15): #create 15 enemies
    enemy = Enemy("monsters.png", randint(100, 800), randint(10, 100), randint(1, 3))
    enemies.add(enemy)#add enemy to group


#Score
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(float(0.1)) #set volume

fire = mixer.Sound("fire.ogg")

score = 0

font.init()
font = font.Font("Roboto-Bold.ttf", 50) #Tao phong chu, kieu chu, kick co chu
again = font.render("You lose! \n Press SPACE to try AGAIN", True, (232, 89, 12)) #dung bien font de dat ra dong chu
win = font.render("You win!", True, (0, 0, 0)) #dung bien font de dat ra dong chu

#
# enemy = Enemy("monsters.png", randint(10, 800), 0, 1)
# enemies.add(enemy)
# enemy1 = Enemy("monsters.png", randint(10, 790), 0, 1)

#Run game
run = True #programming running?
finish = False #losing the game
#start = False  #starting the game
score = 0
score_txt = font.render(f"Score: {score}", True, (255, 255, 255))
#score_txt = font.render("Score: " + str(score), True, (0, 0, 0))

miss = 0
miss_txt = font.render(f"Missed: {miss}", True, (255, 255, 255))
rect = Rect(200,200,650,50)
while run:
    
    #event handling
    for e in event.get():
        if e.type == QUIT:
            run = False
        #shooting
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if not finish:
                    player.fire()
                    fire.play()

                else:
                    finish = False

        if e.type == MOUSEBUTTONDOWN:
            player.fire()

        #die == True
    if not finish:

        window.blit(backgroundd, (0,0)) #set background

        #draw.rect(window, (255, 255, 255), rect)

        player.draw()
        player.update()

        enemies.draw(window)
        enemies.update()


        score_txt = font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_txt, (10, 20))

        miss_txt = font.render(f"Missed: {miss}", True, (255, 255, 255))
        window.blit(miss_txt, (10, 60))

        
        # enemy.draw()
        # enemy.update()
        # enemy1.draw()
        # enemy1.update()

        bullets.draw(window)
        bullets.update()
        #window.blit(score_txt)
        

        
        collides = sprite.groupcollide(bullets, enemies, True, True) #1 bullet chet va ememy cung chet
        for c in collides:
            #create an enemy
            enemy = Enemy("monsters.png", randint(10, 800), randint(-5, 0), randint(1, 3))

            #add enemy to group
            enemies.add(enemy)
            
            #increase score
            score += 100

            
#                   LOSE
        if sprite.spritecollide(player, enemies, True):
            #run = False
            #run = True
            #window.blit(backgroundd, (0, 0))
            draw.rect(window, (0, 0, 0), rect)
            window.blit(again, (200, 200))


            

        #window.blit(score_txt)
            finish = True

#                   WIN                
        if (score >= 10000):
            draw.rect(window, (0, 0, 0), rect)
            window.blit(win, (200, 200))
            score = 0
            finish = True
#



        display.update()