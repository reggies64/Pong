import pygame
import math
import random

pygame.init()

#  Window Parameters:
Win_x = 1600
Win_y = 900

pygame.display.set_caption("Pong.exe")
game_window = pygame.display.set_mode((Win_x, Win_y))


def draw_game_board(p1, p2, ball):
    # Draw game board:
    game_window.fill((0, 0, 0))
    outer_border = [(10, 10), (10, Win_y-10), (Win_x-10, Win_y-10), (Win_x-10, 10)]
    pygame.draw.lines(game_window, (255, 255, 255), True, outer_border, 1)
    pygame.draw.line(game_window, (255, 255, 255), (Win_x/2, 10), (Win_x/2, Win_y-10), 1)

    # Draw Score
    scorefont = pygame.font.SysFont("8-Bit Madness", 72)
    p1scoresurf, p1scorerect = text_objects(str(p1.Score), scorefont)
    p2scoresurf, p2scorerect = text_objects(str(p2.Score), scorefont)
    p1scorerect.center = (Win_x/2 + 100, Win_y/9)
    p2scorerect.center = (Win_x / 2 - 100, Win_y / 9)
    game_window.blit(p1scoresurf, p1scorerect)
    game_window.blit(p2scoresurf, p2scorerect)


    # Draw players and ball:
    pygame.draw.rect(game_window, (255, 255, 255), (p1.x, p1.y, p1.width, p1.height))
    pygame.draw.rect(game_window, (255, 255, 255), (p2.x, p2.y, p2.width, p2.height))
    pygame.draw.circle(game_window, (255, 255, 255), (int(ball.ball_x), int(ball.ball_y)), 10, 10)

    # Update Display:
    pygame.display.update()


def text_objects(text, font):
    textsurface = font.render(text, True, (255, 255, 255))
    return textsurface, textsurface.get_rect()


class Player:

    y = Win_y/2
    width = 10
    height = 100
    Score = 0
    vel = 10

    def __init__(self, x):
        self.x = x


class Ball:
    ball_x = Win_x/2
    ball_y = Win_y/2
    ball_vel = 6
    ball_dir = random.randrange(0, 360, 1)

    def update(self, p1, p2):
        self.check_bounce(p1, p2)
        self.check_score(p1, p2)
        self.ball_x += self.ball_vel * math.cos(math.radians(self.ball_dir))
        self.ball_y += self.ball_vel * math.sin(math.radians(self.ball_dir))

    def check_bounce(self, p1, p2):
        if self.ball_y <= 20:
            self.ball_dir = -self.ball_dir
        if self.ball_y >= 870:
            self.ball_dir = -self.ball_dir
        if (self.ball_x >= p1.x - 10) and (self.ball_y - p1.y <= 100) and (self.ball_y - p1.y > 0):
            self.ball_dir = 180 - self.ball_dir - p1.dir*p1.vel*3
            self.ball_vel *= 1.05
        if (self.ball_x <= p2.x + 20) and (self.ball_y - p2.y <= 100) and (self.ball_y - p2.y > 0):
            self.ball_dir = 180 - self.ball_dir + p2.dir*p2.vel*3
            self.ball_vel *= 1.05

    def check_score(self, p1, p2):
        if self.ball_x > Win_x + 20:
            p2.Score += 1
            self.reset()
        elif self.ball_x < -20:
            p1.Score += 1
            self.reset()

    def reset(self):
        self.ball_x = Win_x / 2
        self.ball_y = random.randrange(100, Win_y-100, 1)
        self.ball_vel = 6
        a = random.randrange(-45, 45, 1)
        b = random.randrange(0, 2, 1)
        self.ball_dir = a + 180*b


def start_menu():
    start_menu = True
    while start_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu = False
                pygame.quit
                quit()

        game_window.fill((0, 0, 0))
        outer_border = [(10, 10), (10, 890), (1590, 890), (1590, 10)]
        pygame.draw.lines(game_window, (255, 255, 255), True, outer_border, 1)
        game_title = pygame.font.Font('8-Bit Madness.ttf', 115)
        title_surf, title_rect = text_objects("Pong", game_title)
        title_rect.center = ((Win_x / 2), (Win_y / 3))
        game_window.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        # print(mouse_pos)

        if (Win_x/2 + 100 > mouse_pos[0] > Win_x/2 - 100) and (Win_y/2 + 20 > mouse_pos[1] > Win_y/2 - 20):
            # pygame.draw.rect(game_window, (0, 0, 0), (Win_x/2, Win_y/2, 100, 50))
            game_start = pygame.font.Font('8-Bit Madness.ttf', 60)
            start_surf, start_rect = text_objects("Start", game_start)
            start_rect.center = ((Win_x / 2), (Win_y / 2))
            game_window.blit(start_surf, start_rect)
            if mouse_click[0] == 1:
                start_menu = False
        else:
            # pygame.draw.rect(game_window, (0, 0, 0), (Win_x/2, Win_y/2, 100, 50))
            game_start = pygame.font.Font('8-Bit Madness.ttf', 40)
            start_surf, start_rect = text_objects("Start", game_start)
            start_rect.center = ((Win_x / 2), (Win_y / 2))
            game_window.blit(start_surf, start_rect)
        # Add more if/elif statements for more buttons

        pygame.display.update()


def game_loop():
    p1 = Player(Win_x-40)
    p2 = Player(30)
    ball = Ball()
    run = True
    global pause
    while run:
        pygame.time.delay(10)
        draw_game_board(p1, p2, ball)
        ball.update(p1, p2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        p1.dir = 0
        p2.dir = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if p1.y <= 10:
                p1.y = 10   # p1.dir = 1
            else:
                p1.dir = -1
                p1.y = p1.y + p1.dir * p1.vel
        if keys[pygame.K_DOWN]:
            if p1.y >= 780:
                p1.y = 780
            else:
                p1.dir = 1
                p1.y = p1.y + p1.dir * p1.vel
        if keys[pygame.K_w]:
            if p2.y <= 10:
                p2.y = 10
            else:
                p2.dir = -1
                p2.y = p2.y + p2.dir * p2.vel
        if keys[pygame.K_s]:
            if p2.y >= 780:
                p2.y = 780
            else:
                p2.dir = 1
                p2.y = p2.y + p2.dir * p2.vel
        if keys[pygame.K_SPACE]:
            pause = True
            paused(p1, p2, ball)
        if keys[pygame.K_r]:
            pygame.time.delay(10)
            ball.reset()
        if keys[pygame.K_ESCAPE]:
            break


def unpause():
    global pause
    pause = False


def paused(p1, p2, ball):
    global pause

    draw_game_board(p1, p2, ball)
    pygame.draw.rect(game_window, (0, 0, 0), (Win_x/2, Win_y/3-65, 100, 130))
    pause_text = pygame.font.SysFont("8-Bit Madness.ttf", 115)
    pause_surf, pause_rect = text_objects("Paused", pause_text)
    pause_rect.center = ((Win_x/2), (Win_y/3))
    game_window.blit(pause_surf, pause_rect)

    while pause:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if (Win_x/2 + 100 > mouse_pos[0] > Win_x/2 - 100) and (Win_y/2 + 25 > mouse_pos[1] > Win_y/2 - 25):
            pygame.draw.rect(game_window, (0, 0, 0), (Win_x/2 - 100, Win_y/2 - 25, 200, 50))
            cont = pygame.font.Font('8-Bit Madness.ttf', 60)
            cont_surf, cont_rect = text_objects("Continue?", cont)
            cont_rect.center = ((Win_x / 2), (Win_y / 2))
            game_window.blit(cont_surf, cont_rect)
            if mouse_click[0] == 1:
                unpause()
        else:
            pygame.draw.rect(game_window, (0, 0, 0), (Win_x/2 - 150, Win_y/2 - 25, 300, 50))
            cont = pygame.font.Font('8-Bit Madness.ttf', 40)
            cont_surf, cont_rect = text_objects("Continue?", cont)
            cont_rect.center = ((Win_x / 2), (Win_y / 2))
            game_window.blit(cont_surf, cont_rect)

        pygame.display.update()

start_menu()
game_loop()
pygame.quit
quit()