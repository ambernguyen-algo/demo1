#import libraries
from pygame import *
from random import randint

#create window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"

#upload background image
background = transform.scale(image.load(img_back), (win_width,win_height))

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#bullet sound
fire_sound = mixer.Sound('fire.ogg')

#parent class GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 
        
#main Player class
class Player(GameSprite):
    #method for controlling the player with keyboard arrows
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed 
            
    #bullet method
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 15, -20)
        bullets.add(bullet)
        
bullets = sprite.Group()

#Class enemy
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        
        global lost
        
        #disappears if it reaches the edge of the screen
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#bullet sprite class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #disappears if it reaches the edge of the screen
        if self.rect.y < 0:
            self.kill()
    
#create objects
player = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#create a group of enemy sprites
enemies = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    enemies.add(monster)
    
#set up fonts
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

font2 = font.Font(None, 30)

score = 0 #ships hit
lost = 0 #ships missed
goal = 5 #how many ships need to be hit to win
max_lost = 2 #lost if this many missed

#Main game loop
finish = False #not finish
run = True 

while run: #while True: 
    #press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        #press on the spacebar event - the sprite fires
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
                
    #sprite actions, checking rules of game, re-drawing
    if not finish:
        #refresh background
        window.blit(background, (0,0))
        
        #writing text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        #sprite movements
        player.update()
        enemies.update()
        bullets.update()
        
        #update new location
        player.reset()
        enemies.draw(window)
        bullets.draw(window)
        
        #collision check
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) #1 object enemy
            enemies.add(monster) #add 5 enemies to group enemies
            
        #collides between player and enemies, possible loss
        if sprite.spritecollide(player, enemies, False) or lost >= max_lost:
            finish = True #lost
            window.blit(lose, (200, 200))
        
        #check win condition
        if score >= goal:
            finish = True #win
            window.blit(win, (200, 200))
            
        display.update()
        
    #the loop runs every 0.05 seconds
    time.delay(70)    
        
        
        
        