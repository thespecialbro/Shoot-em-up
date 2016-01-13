#! python

'''
Shoot-'em-up
version 1.6.3
'''

# ----- IMPORTS ----- #
import time

try:
    import pygame
except Exception:
    print('This game requires Pygame to work!')
    time.sleep(5)
    raise SystemExit

try:
    import pgu
    from pgu.gui.const import *
except ImportError:
    print('This game requires PGU to work!')
#    time.sleep(5)
#    raise SystemExit

import random
import os
import sys

try:
    import config
except ImportError:
    print('Did you remember to NOT delete the config.py file?')
    time.sleep(5)
    raise SystemExit


# ----- TEST THINGS ----- #
print('Testing Python version...')
if sys.version_info[0] >= 3:
    if sys.version_info[1] >= 5:
        print('Python version is verified to be 3.5 or higher\n')
    elif sys.version_info[1] < 5:
        print('Python version is verified to be 3.x or higher\n')
else:
    print('Python version is out of date!\nYou must use Python version 3 or higher!')
    time.sleep(5)
    raise SystemExit

print('Testing Pygame version...')
if pygame.version.ver != "1.9.2a0":
    print('''WARNING:
This version of pygame is not the version it was written in!
Some features may not work the same!
''')
else:
    print('Pygame version is verified to be {}\n'.format(pygame.version.ver))

if config.difficulty < 0.5:
    config.difficulty = 0.5
if config.difficulty > 2.0:
    config.difficulty = 2.0
if config.music_volume > 1.0:
    config.music_volume = 1.0


# ----- CONSTANTS ----- #
WIDTH  = 450
HEIGHT = 650
FPS    = 60

# COLORS
WHITE     = (255, 255, 255)
LIGHTGRAY = (150, 150, 150)
GRAY      = (100, 100, 100)
DARKGRAY  = ( 50,  50,  50)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
CYAN      = (  0, 255, 255)
YELLOW    = (255, 255,   0)


# ----- Setup ----- #
# Set up game folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'textures')
snd_folder = os.path.join(game_folder, 'sound')

# Initialize pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()

# Create window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (config.wind_pos_x, config.wind_pos_y)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
icon = pygame.image.load(os.path.join(img_folder, 'icon.png'))
pygame.display.set_icon(icon)
pygame.display.set_caption('Shoot-\'em-up!')
clock = pygame.time.Clock()


# ----- Functions ----- #
font_name = pygame.font.match_font('arial')
def drawText(surf=screen, text='Foo', size=18, x=100, y=100, color=(255,255,255), antialias=True):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, antialias, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newMob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def startGame():
    # Spawn initial sprites
    global all_sprites, mobs, player, bullets, lasers
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        newMob()

def menu():   # Broken right now. Investigating solutions
    global all_sprites
    app = pgu.gui.App()
    start_button = pgu.gui.Button('START')
    start_button.connect(CLICK, startGame)
    start_button.resize(width = 100, height = 50)

    #quit_button = pgu.gui.Button('QUIT')
    #quit_button.connect(CLICK, pygame.QUIT
    #quit_button.resize(width = 100, height = 50)

    app.run(start_button)#, quit_button)

def drawShieldBar(surf, x, y, pct, color, outline=True):
    # Check if shield percentage is below zero: set it to zero
    if pct < 0:
        pct = 0

    # CONSTANTS
    BAR_LENGTH = 100
    BAR_HEIGHT = 10

    # Create rectangles
    fill = (pct / player.max_shield) * BAR_LENGTH
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    # Draw rectangles
    pygame.draw.rect(surf, color, fill_rect)
    if outline:
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

def drawLaserCharge(surf, x, y, pct, color, outline=True):
    # Check if laser is below zero: set it to zero
    if pct < 0:
        pct = 0

    # CONSTANTS
    BAR_LENGTH = 100
    BAR_HEIGHT = 10

    # Create rectangles
    fill = (pct / player.max_laser) * BAR_LENGTH
    fill_rect = pygame.Rect(x+1, y, fill, BAR_HEIGHT)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    # Draw rectangles
    pygame.draw.rect(surf, color, fill_rect)
    if outline:
        pygame.draw.rect(surf, BLUE, outline_rect, 2)

def debugInfo():
    drawText(text='player speed: {}'.format(str(player.speedx)), size=11, x=350, y=0, color=YELLOW)
    drawText(text='player pos: {}'.format(str(player.rect.x)), size=11, x=350, y=12, color=YELLOW)
    number = 24
    for bullet in bullets:
        drawText(text='bullet ({},{})'.format(str(bullet.rect.x),str(bullet.rect.y)), size=11, x=350, y=number, color=YELLOW)
        number += 12
    for mob in mobs:
        pygame.draw.circle(screen, RED, (mob.rect.centerx, mob.rect.centery), mob.radius, 2)
    pygame.draw.circle(screen, GREEN, (player.rect.centerx, player.rect.centery), player.radius, 2)
    for sprite in all_sprites:
        pygame.draw.rect(screen, YELLOW, sprite.rect, 1)
    for bullet in bullets:
        pygame.draw.rect(screen, CYAN, bullet.rect, 1)


# ----- Classes ----- #
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize sprite with player_img and radius
        pygame.sprite.Sprite.__init__(self)
        self.image = player_images[0]
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

        # Shield
        self.shield = 100
        self.max_shield = 100
        self.rchg_delay = 1000
        self.last_rchg = pygame.time.get_ticks()
        self.allow_shield_rchg = True

        # Auto-fire
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        # Laser
        self.laser_pwr = 0
        self.max_laser = 10
        self.last_laser = pygame.time.get_ticks()
        self.lrchg_delay = 1000
        self.last_lrchg = pygame.time.get_ticks()
        self.allow_laser_rchg = True

    def update(self):
        # Movement, controlled by keyboard
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        # Make sure player doesn't go off screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # Shield
        if config.shield_recharge:
            now = pygame.time.get_ticks()
            if self.shield > self.max_shield:
                self.shield = self.max_shield
                self.allow_shield_rchg = False
            elif self.shield < self.max_shield:
                self.allow_shield_rchg = True
            if now - self.last_rchg > self.rchg_delay and self.allow_shield_rchg:
                self.last_rchg = now
                self.shield += 1

        # Shooting
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_c]:
            self.laser()

        now = pygame.time.get_ticks()
        if self.laser_pwr >= self.max_laser:
            self.shield = self.max_shield
            self.allow_laser_rchg = False
        elif self.laser_pwr < self.max_laser:
            self.allow_laser_rchg = True
        if score > 0: # if score > 24999:
            if now - self.last_lrchg > self.lrchg_delay and self.allow_laser_rchg:
                self.last_lrchg = now
                self.laser_pwr += 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            laser_sound.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def laser(self):
        now = pygame.time.get_ticks()
        if self.laser_pwr > 0 and now - self.last_laser > 90: # >= self.max_laser:
            laser_sound.play()
            laser = Laser(self.rect.centerx, self.rect.top)
            all_sprites.add(laser)
            lasers.add(laser)
            self.laser_pwr -= 1 # = 0
            self.last_laser = now

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize sprite with choice from meteor_images and radius based on size
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * .85 / 2) + (self.rect.height * .85 / 2) / 2)

        # Spawn sprite at random location above the screen and give random movement values
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8) * config.difficulty
        self.speedx = random.randrange(-3, 3) * config.difficulty

        # Animation setup
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        # Animation
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # Do animation
        self.rotate()

        # Move
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # If it is off-screen, move to random location above screen with random movement values
        if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Initialize sprite with bullet_img
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)

        # Sprite spawns just above player_img
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        # Set movement, based on self.speedy
        self.rect.y += self.speedy

        # Destroy if sprite moves off screen
        if self.rect.bottom < 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4, HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.life = 1000
        self.lived = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lived > self.life:
            self.lived = now
            self.kill()

class Hat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = hat_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.speedx = 0

        # Spawn sprite right above player
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        # Movement, controlled by keyboard
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx

        # Make sure hat doesn't leave player
        if self.rect.right > WIDTH - 17:
            self.rect.right = WIDTH - 17
        if self.rect.left < 17:
            self.rect.left = 17

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        # Animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # If animation frame is the last frame: destroy sprite
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            # Otherwise: continue animation
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Powerup(pygame.sprite.Sprite):
    # Initialize Sprite
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speedx = 5
        self.rect.y = y
        self.rect.x = -60

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()


# Load all game graphics in order
background = pygame.image.load(os.path.join(img_folder, 'starfield.png')).convert()
background_rect = background.get_rect()

background_boss = pygame.image.load(os.path.join(img_folder, 'starfield_boss.png')).convert()
background_boss_rect = background.get_rect()

# Player images
player_images = []
for i in range(4):
    player_images.append(pygame.image.load(os.path.join(img_folder, 'player{}.png'.format(i))).convert())
    player_images[i].set_colorkey(WHITE)

hat_img  = pygame.image.load(os.path.join(img_folder, 'hat.png')).convert()
hat_img1 = pygame.image.load(os.path.join(img_folder, 'hat1.png')).convert()

bullet_img = pygame.image.load(os.path.join(img_folder, 'bullet.png')).convert()

meteor_images = []
meteor_list = ['enemy.png', 'enemy1.png', 'enemy2.png', 'enemy3.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(4):
    filename = 'explode{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(WHITE)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (40, 40))
    explosion_anim['sm'].append(img_sm)
    img_plr = pygame.transform.scale(img, (200, 200))
    explosion_anim['player'].append(img_plr)


# Load all sounds
laser_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'laser.wav'))
laser_sound.set_volume(config.sound_volume * 0.6)

expl_sounds = []
for snd in ['explode.wav', 'explode1.wav', 'explode2.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, snd)))

# Music (doesn't work when made into an executable :/)
pygame.mixer.music.load(os.path.join(snd_folder, 'melodything.ogg'))
pygame.mixer.music.set_volume(config.music_volume)
pygame.mixer.music.play(loops=-1)

#menu() # Doesn't work as of now
startGame()

# Variables
score = 0
lives = 3
shield_color = RED
upgrade = True
upgrade1 = True
upgrade2 = True
upgrade3 = True


# -------------------- Game loop --------------------- #
running = True
while running:
    # Keep loop running at correct speed
    clock.tick(FPS)


    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False

        # Keystate object to sheck for keyboard events
        keystate = pygame.key.get_pressed()

        # Check for escape key: close game
        if keystate[pygame.K_ESCAPE]:
            running = False

        # Check for F1 key: print README.txt to console
        if keystate[pygame.K_F1]:
            with open(os.path.join(game_folder, 'README.txt')) as file:
                data = file.read()
                print(data)

        # Debug screen activation
        if keystate[pygame.K_F3]:
            if config.debug == False:
                config.debug = True
            else:
                config.debug = False

        # Soopwr seekrt things
        if keystate[pygame.K_y]:
            score += 1000


    # Update
    all_sprites.update()

    # Shield upgrades
    if score > 1000 and upgrade:
        upgrade = False
        player.image = player_images[1]
        player.max_shield = 200
        player.shield = 200
        shield_color = GREEN
    if score > 5000 and upgrade1:
        upgrade1 = False
        player.image = player_images[2]
        player.max_shield = 300
        player.shield = 300
        shield_color = CYAN
    if score > 10000 and upgrade2:
        upgrade2 = False
        player.image = player_images[3]
        player.max_shield = 500
        player.shield = 500
        shield_color = YELLOW
    if score > 50000 and upgrade3:
        upgrade3 = False
        player.max_shield = 1000
        player.shield = 1000
        shield_color = WHITE
    if config.hat:
        hat = Hat(player.rect.centerx, player.rect.top)
        all_sprites.add(hat)
        if score > 1000:
            hat.image = hat_img1

    # Check for collisions (bullet / mob)
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += int((50 - hit.radius) / config.difficulty)
        expl_snd = random.choice(expl_sounds)
        expl_snd.set_volume(config.sound_volume * 1.4)
        expl_snd.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newMob()
    # Check for collisions (lasers / mob)
    hits = pygame.sprite.groupcollide(mobs, lasers, True, False)
    for hit in hits:
        score += int((100 - hit.radius) / config.difficulty)
        expl_snd = random.choice(expl_sounds)
        expl_snd.set_volume(config.sound_volume * 1.4)
        expl_snd.play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newMob()
    # Check for collisions (mob / player)
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        newMob()
        expl_snd = random.choice(expl_sounds)
        expl_snd.set_volume(config.sound_volume)
        expl_snd.play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player.shield = 0
            running = False


    # Render / draw
    # Background
    screen.fill(BLACK)
    if score > 10000:
        screen.blit(background_boss, background_boss_rect)
    else:
        screen.blit(background, background_rect)

    # Sprites
    all_sprites.draw(screen)

    # Score
    drawText(screen, str(score), 18, WIDTH / 2, 10, WHITE)

    # Shield
    drawText(screen, str(player.shield) + '/' + str(player.max_shield), 14, 130, 2, CYAN)
    drawShieldBar(screen, 5, 5, player.shield, shield_color)

    drawLaserCharge(screen, 5, 16, player.laser_pwr, RED)

    # Debug info
    if config.debug == True:
        debugInfo()

    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()

print('Your score: ' + str(score))
