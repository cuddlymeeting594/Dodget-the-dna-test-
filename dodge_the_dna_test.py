import pygame
import random as r
pygame.init()

WIDTH = 1250
HEIGHT = 750

clock = pygame.time.Clock()

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Dodge the DNA test!')

#assets
camp = pygame.transform.scale(pygame.image.load('assets/camp.png'), (WIDTH,HEIGHT))
pavros = pygame.transform.scale(pygame.image.load('assets/pavros_normal.png'), (200,200))
dna_test = pygame.transform.scale_by(pygame.image.load('assets/dnatest.png'), 0.23)
testresult = pygame.image.load('assets/results.png')
wash = pygame.transform.scale_by(pygame.image.load('assets/soap.png',), 0.3)
pygame.display.set_icon(pavros)
music = pygame.mixer.music.load('assets/backgroundmusic.mp3')
pygame.mixer.music.play(-1)

# pavros details
x = 100
y = 500
pavros_vel = 12

class Projectile():
    def __init__(self, x,y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def movement(self):
        if self.x > - dna_test.get_width() :
            self.x -= self.vel
        else:
            self.x = WIDTH
            self.y = r.randint(1,HEIGHT - dna_test.get_height())
        
dna = Projectile(WIDTH,r.randint(1,HEIGHT - dna_test.get_height()),18)
soap = Projectile(r.randint(1,WIDTH - wash.get_width()),- wash.get_height(), 5)

lost = False
def draw(win):
    if not lost:
        #hitbox = (x,y+23,200,177)
        #dnabox = (dna.x + 35,dna.y + 37, dna_test.get_width() - 67,dna_test.get_height() - 71)
        #soapbox = (soap.x + 18, soap.y + 35, wash.get_width() - 33,wash.get_height()- 69)
        win.blit(camp,(0,0))
        #pygame.draw.rect(win, (255,0,0), hitbox, 2)
        #pygame.draw.rect(win, (0,0,0), dnabox, 2)
        #pygame.draw.rect(win, (0,0,255),soapbox, 2)
        font2 = pygame.font.SysFont('comicsans', 40)
        score_board = font2.render(f'Score: {int(score)}',1, (0,0,0))
        win.blit(score_board, (score_board.get_width() - 50, 50))
        win.blit(dna_test, (dna.x,dna.y))
        win.blit(wash, (soap.x,soap.y))
        win.blit(pavros, (x,y))
        pygame.display.update()
    elif lost== True:
        font = pygame.font.SysFont("comicsans", 60)
        font2 = pygame.font.SysFont('comicsans', 40)
        lose_text = font.render('You lost :(',1, (255,255,255))
        quit_text = font2.render('Press Q to quit', 1 , (255,255,255))
        retry_text = font2.render('Press R to retry',1,(255,255,255))
        score_board = font2.render(f'Final score: {int(score)}' , 1 ,(255,255,255))
        win.fill((0,0,0))
        win.blit(testresult, (WIDTH/2 - testresult.get_width()/2,HEIGHT/2 - testresult.get_height()/2 + 50))
        win.blit(quit_text, (80,200))
        win.blit(retry_text,(75,400))
        win.blit(lose_text, (480,30))
        win.blit(score_board, (875,200))

        pygame.display.update()


run = True
score = 0
score_increment = 0.3
while run:
    clock.tick(80)
    score += score_increment
    if lost == True:
        score_increment = 0
    else:
        score_increment = 0.3

    hitbox = (x,y+23,200,177)
    dnabox = (dna.x + 35,dna.y + 37, dna_test.get_width() - 67,dna_test.get_height() - 71)
    soapbox = (soap.x + 18, soap.y + 35, wash.get_width() - 33,wash.get_height()- 69)
    key = pygame.key.get_pressed()
    
    if hitbox[1] < dnabox[1] + dnabox[3] and hitbox[1] + hitbox[3] > dnabox[1]:
       if hitbox[0] + hitbox[2] > dnabox[0] and hitbox[0] < dnabox[0] + dnabox[2]:
            lost = True

    if hitbox[1] < soapbox[1] + soapbox[3] and hitbox[1] + hitbox[3] > soapbox[1]:
        if hitbox[0] + hitbox[2] > soapbox[0] and hitbox[0] < soapbox[0] + soapbox[2]:
            if pavros_vel > 6:
                soap.y = - wash.get_height()
                soap.x = r.randint(1, WIDTH - wash.get_width())
                pavros_vel -= 1
            
    if soap.y < HEIGHT and pavros_vel > 6:
        soap.y += soap.vel
    else:
        soap.y = - wash.get_height()
        soap.x = r.randint(1, WIDTH - wash.get_width())
    
    dna.movement()

    if not lost:
        if key[pygame.K_a] and x > pavros_vel:
            x -= pavros_vel
        if key[pygame.K_d] and x < WIDTH - pavros_vel - pavros.get_width():
            x += pavros_vel
        if key[pygame.K_w] and y > -20:
            y -= pavros_vel
        if key[pygame.K_s] and y < HEIGHT - pavros.get_height() - pavros_vel :
            y += pavros_vel
    
    close = False
    if key[pygame.K_q] and lost==True:
        close = True
    if key[pygame.K_r] and lost == True:
        lost = False
        dna.movement()
        x = 100
        y = 500
        pavros_vel = 12
        score = 0
        
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT or close==True:
            run = False
            break

    draw(win)


pygame.quit()
