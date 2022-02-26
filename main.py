import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space PvP!')

WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (181, 23, 158)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_FIRE_SOUND_BLUE = pygame.mixer.Sound(os.path.join('assets', 'laser1.wav'))
BULLET_FIRE_SOUND_GREEN = pygame.mixer.Sound(os.path.join('assets', 'laser2.wav'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('assets', 'win-sound1.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40, True)
WINNER_FONT = pygame.font.SysFont('comicsans', 100, True)

FPS = 120
VEL = 4
BULLET_VEL = 11
MAX_BULLETS = 3

BLUE_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

BLUE_SPACESHIP = pygame.image.load(os.path.join('assets', 'blue-spaceship.PNG'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP, (120, 90)), -90)

GREEN_SPACESHIP = pygame.image.load(os.path.join('assets', 'green-spaceship.PNG'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP, (120, 90)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space-background.png')), (WIDTH, HEIGHT))

def blue_handle_movment(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0: #Left
        blue.x -= VEL
    elif keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x: #Rigth
        blue.x += VEL
    elif keys_pressed[pygame.K_w] and blue.y - VEL > 0: #Up
        blue.y -= VEL
    elif keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT: #Down
        blue.y += VEL

def green_handle_movment(keys_pressed, green):
    if keys_pressed[pygame.K_LEFT] and green.x - VEL > BORDER.x + BORDER.width: #Left
        green.x -= VEL
    elif keys_pressed[pygame.K_RIGHT] and green.x + VEL + green.width < WIDTH: #Rigth
        green.x += VEL
    elif keys_pressed[pygame.K_UP] and green.y + VEL > 0: #Up
        green.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT: #Down
        green.y += VEL

def handle_bullets(blue_bullets, green_bullets, blue, green):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)
    
    for bullet in green_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)

def draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))
    
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    
    
    for bullet in green_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in blue_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PINK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(100, 300, 100, 100)
    green = pygame.Rect(700, 300, 100, 100)
    
    blue_bullets = []
    green_bullets = []
    
    blue_health = 10
    green_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND_BLUE.play()
                    
                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND_GREEN.play()
                    
            if event.type == BLUE_HIT:
                blue_health -= 1
                
            if event.type == GREEN_HIT:
                green_health -= 1
                
        winner_text = ""
        if blue_health <= 0:
            winner_text = "Green Wins!"
            
        if green_health <= 0:
            winner_text = "Blue Wins!"
            
        if winner_text != "":
            WIN_SOUND.play()
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movment(keys_pressed, blue)
        green_handle_movment(keys_pressed, green)
        
        handle_bullets(blue_bullets, green_bullets, blue, green)
        
        draw_window(green, blue, green_bullets, blue_bullets, green_health, blue_health)
                
    main()
                
if __name__ == "__main__":
    main()