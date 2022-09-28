import math

import pygame

import time

clock = pygame.time.Clock()

pygame.init()
window = pygame.display.set_mode( (500, 500))
pygame.display.set_caption("Projectile Game")

#Represents a projectile ball
class projectile(object):
    def __init__(self, vel_x, vel_y):
        self.x = 35
        self.y = 395
        self.radius = 10
        self.color = (247, 112, 79)
        self.vel_x = vel_x
        self.vel_y = vel_y

    #Moves the projectile based on the set velocities
    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        #Accounts for gravity
        self.vel_y += 1

    #Draws projectile on window
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

#Represents the controls to change the power of the launcher
class power_control(object):
    def __init__(self):
        self.power = 50

    #Increases the power of the launcher (max of 100)
    def increase(self):
        if self.power < 100:
            self.power += 1

    #Decreases the power of the launcher (min of 1)
    def decrease(self):
        if self.power > 1:
            self.power -= 1

    #Draws the power control bar and its labels
    def draw(self, win):

        font1 = pygame.font.SysFont('comicsans', 15)
        text = font1.render('Power: ', 1, (0, 0, 0))
        window.blit(text, (45, 60))
        text = font1.render(str(self.power), 1, (0, 0, 0))
        window.blit(text, (45, 10))
        text = font1.render('0', 1, (0, 0, 0))
        window.blit(text, (5, 60))
        text = font1.render('100', 1, (0, 0, 0))
        window.blit(text, (105, 60))
        pygame.draw.rect(win, (255, 0, 255), (10, 30, self.power, 10))

#Represents the controls to change the angle of the launcher
class angle_control(object):
    def __init__(self):
        self.angle = 45

    #Increases the angle of the launcher (max of 90 degrees)
    def increase(self):
        if self.angle < 90:
            self.angle += 1

    #Decreases the angle of the launcher (min of 0 degrees)
    def decrease(self):
        if self.angle > 0:
            self.angle -= 1

    #Draws the angle control bar and its labels
    #Also draws a line representing the direction the projectile will be launched
    def draw(self, win):
        font1 = pygame.font.SysFont('comicsans', 15)
        text = font1.render('Angle: ', 1, (0, 0, 0))
        window.blit(text, (45, 140))
        text = font1.render(str(self.angle), 1, (0, 0, 0))
        window.blit(text, (45, 90))
        text = font1.render('0', 1, (0, 0, 0))
        window.blit(text, (5, 140))
        text = font1.render('90', 1, (0, 0, 0))
        window.blit(text, (105, 140))
        pygame.draw.rect(win, (255, 0, 255), (10, 120, self.angle, 10))
        radians = self.angle * math.pi / 180
        x = 50 * math.cos(radians) + 35
        y = 50 * math.sin((2 * math.pi) - radians) + 395
        pygame.draw.line(win, (0, 0, 0), (35, 395), (x, y), 1)

#Represents the target the projectile will try to hit
class target(object):
    def __init__(self):
        self.x = 250
        self.y = 300
        self.width = 10
        self.color = (125, 125, 125)
        self.vel_x = 3
        self.vel_y = 0
        self.hitbox = (self.x, self.y, self.x + self.width, self.y + self.width)

    #Moves the target in a horizontal fashion
    def move(self):
        if self.x > 480 or self.x < 100:
            self.vel_x *= -1
        if self.y > 480 or self.y < 100:
            self.vel_y *= -1
        self.x += self.vel_x
        self.y += self.vel_y
        self.hitbox = (self.x, self.y, self.x + self.width, self.y + self.width)

    #Draws the target
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

rock = projectile(3, -5)
pc = power_control()
ac = angle_control()
tar = target()

score = 0

#Draws all the objects for the game
def redrawGameWindow():

    pygame.draw.rect(window, (255, 255, 255), (0, 0, 500, 500))
    pygame.draw.rect(window, (0, 185, 255), (0, 0, 500, 420))
    pygame.draw.rect(window, (75, 139, 59), (0, 420, 500, 80))
    pygame.draw.rect(window, (175, 175, 175), (20, 410, 15, 15))
    rock.draw(window)
    pc.draw(window)
    ac.draw(window)
    tar.draw(window)
    font1 = pygame.font.SysFont('comicsans', 15)
    score_text = font1.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(score_text, (400, 20))
    power_keys_text = font1.render('UP and DOWN Arrow Keys', 1, (0, 0, 0))
    window.blit(power_keys_text, (155, 30))
    angle_keys_text = font1.render('LEFT and RIGHT Arrow Keys', 1, (0, 0, 0))
    window.blit(angle_keys_text, (155, 115))
    pygame.display.update()


run = True
isThrown = False
while run:

    redrawGameWindow()

    #Moves Target
    tar.move()

    keys = pygame.key.get_pressed()

    #Readies the projectile for launch if it has not already been launched
    if not(isThrown) and keys[pygame.K_SPACE]:
        isThrown = True
        velocity_x = pc.power * 0.5 * math.cos( ac.angle * math.pi / 180 )
        velocity_y = pc.power * 0.5 * math.sin( ac.angle * math.pi / 180 ) * -1
        rock = projectile(velocity_x, velocity_y)

    #Launches the projectile
    if isThrown:
        rock.move()

    #Checks if any point on the circumference of the projectile has collided with the hitbox of the target
    for i in range(0, 359):
        radians = i * math.pi / 180
        edge_x = rock.radius * math.cos(radians) + rock.x
        edge_y = rock.radius * math.sin(radians) + rock.y
        if edge_x > tar.hitbox[0] and edge_x < tar.hitbox[2] and edge_y > tar.hitbox[1] and edge_y < tar.hitbox[3]:
            score += 1
            isThrown = False
            rock.x = 35
            rock.y = 395

    #Resets the projectile back to its original position if it misses the target
    if rock.y >= 480:
        isThrown = False
        rock.x = 35
        rock.y = 395

    #Increases the angle
    if keys[pygame.K_LEFT]:
        ac.increase()

    #Decreases the angle
    if keys[pygame.K_RIGHT]:
        ac.decrease()

    #Increases the power
    if keys[pygame.K_UP]:
        pc.increase()

    #Decreases the power
    if keys[pygame.K_DOWN]:
        pc.decrease()

    clock.tick(27)

    #Quits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


time.sleep(10)
