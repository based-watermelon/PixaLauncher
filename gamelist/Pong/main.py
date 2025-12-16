import pygame
import random
import math

pygame.init()
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("hit.wav")
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Pong")
FPS = 60

# Neon colors
BLACK = (0, 0, 10)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 100)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE=(188,19,254)
WHITE = (255, 255, 255)

# Gameplay
PADDLE_W, PADDLE_H = 20, 120
PADDLE_SPEED = 7
BALL_SIZE = 18
BALL_SPEED = 6
MAX_SCORE = 5
# consolas
FONT_BIG = pygame.font.SysFont("retro arcade font", 70)
FONT_MED = pygame.font.SysFont("retro arcade font", 40)
FONT_SMALL = pygame.font.SysFont("retro arcade font", 25)

# Game mode
game_mode = None  # "solo" or "two"

# defining particles
particles = []
ball_trail = []
score_pop = 0


def spawn_particles(x, y, color):
    for _ in range(4):
        particles.append([
            [x, y],
            [random.uniform(-1, 1), random.uniform(-1, 1)],
            random.randint(3, 6),
            color
        ])


def update_particles():
    for p in particles[:]:
        p[0][0] += p[1][0]
        p[0][1] += p[1][1]
        p[2] -= 0.2
        if p[2] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(WIN, p[3],
                               (int(p[0][0]), int(p[0][1])),
                               int(p[2]))


#screen shake
shake_offset = [0, 0]
shake_time = 0


def trigger_shake():
    global shake_time
    shake_time = 10


def apply_shake():
    global shake_time, shake_offset
    if shake_time > 0:
        shake_offset = [random.randint(-5, 5), random.randint(-5, 5)]
        shake_time -= 1
    else:
        shake_offset = [0, 0]


# adding glow effect surface using SRCALPHA
def glow(surface, color, x, y, size):
    glow_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*color, 40),
                       (size * 2, size * 2),
                       size * 2)
    surface.blit(glow_surf, (x - size * 2, y - size * 2))


#center line
def draw_center_line():
    for y in range(0, HEIGHT, 40):
        rect = pygame.Rect(WIDTH // 2 - 5, y, 10, 30)
        pygame.draw.rect(WIN, NEON_BLUE, rect, border_radius=10)
        # glow(WIN, NEON_BLUE, WIDTH // 2, y + 15, 20)


# main game logic
#reset ball randomly
def reset_ball():
    angle = random.uniform(-0.4, 0.4)
    direction = random.choice([-1, 1])
    return (WIDTH // 2,
            HEIGHT // 2,
            math.cos(angle) * BALL_SPEED * direction,
            math.sin(angle) * BALL_SPEED)


def game_loop(mode):
    global particles, ball_trail, score_pop
    particles = []
    ball_trail = []
    score_pop = 0

    left_score = right_score = 0
    left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
    right_paddle = pygame.Rect(WIDTH - 70, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)

    bx, by, bvelx, bvely = reset_ball()
    ball = pygame.Rect(bx, by, BALL_SIZE, BALL_SIZE)
    paused = False

    clock = pygame.time.Clock()
    run = True

    while run:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        if paused:
            draw_pause()
            continue

        keys = pygame.key.get_pressed()

        # key binding paddles 
        if mode == "solo":
            if keys[pygame.K_UP] and left_paddle.top > 0:
                left_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and left_paddle.bottom < HEIGHT:
                left_paddle.y += PADDLE_SPEED
            ai_move(right_paddle, ball)
        else:
            if keys[pygame.K_w] and left_paddle.top > 0:
                left_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                left_paddle.y += PADDLE_SPEED
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += PADDLE_SPEED

        # -ball movement
        bx += bvelx
        by += bvely
        ball.center = (int(bx), int(by))

        spawn_particles(ball.centerx, ball.centery, NEON_YELLOW)

        # adding a trail effect to ball
        ball_trail.append((ball.centerx, ball.centery))
        if len(ball_trail) > 15:
            ball_trail.pop(0)

        # defining collisions
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            bvely *= -1

        if ball.colliderect(left_paddle):
            bvelx = abs(bvelx)
            hit_sound.play()
            score_pop = 12
            trigger_shake()

        if ball.colliderect(right_paddle):
            bvelx = -abs(bvelx)
            hit_sound.play()
            score_pop = 12
            trigger_shake()

        # updating scores based on ball position
        if ball.left < 0:
            right_score += 1
            score_pop = 15
            trigger_shake()
            bx, by, bvelx, bvely = reset_ball()

        if ball.right > WIDTH:
            left_score += 1
            score_pop = 15
            trigger_shake()
            bx, by, bvelx, bvely = reset_ball()

        apply_shake()

        # --- Drawing ---
        WIN.fill(BLACK)
        WIN.blit(WIN, shake_offset)

        draw_center_line()

        # Ball glow layers
        glow(WIN, NEON_YELLOW, ball.centerx, ball.centery, 50)
        glow(WIN, NEON_YELLOW, ball.centerx, ball.centery, 25)

        # Draw ball trail
        for i, pos in enumerate(ball_trail):
            alpha = int(200 * (i / len(ball_trail)))
            trail = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(trail, (255, 255, 0, alpha), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
            WIN.blit(trail, (pos[0] - BALL_SIZE // 2, pos[1] - BALL_SIZE // 2))

        # Paddle glows
        glow(WIN, NEON_BLUE, left_paddle.centerx, left_paddle.centery, 40)
        glow(WIN, NEON_PINK, right_paddle.centerx, right_paddle.centery, 40)

        pygame.draw.rect(WIN, NEON_BLUE, left_paddle, border_radius=10)
        pygame.draw.rect(WIN, NEON_PINK, right_paddle, border_radius=10)

        pygame.draw.ellipse(WIN, NEON_YELLOW, ball)

        update_particles()

        # Score pop effect
        font_size = 40 + score_pop
        if score_pop > 0:
            score_pop -= 1
        score_text = pygame.font.SysFont("retro arcade font", font_size).render(f"{left_score}    {right_score}", True, NEON_BLUE)
        WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        pygame.display.update()

        # Win condition
        if left_score >= MAX_SCORE or right_score >= MAX_SCORE:
            if mode == "solo":
                winner = "YOU WIN" if left_score > right_score else "COMPUTER WINS"
            else:
                winner = " PLAYER 1 " if left_score > right_score else " PLAYER 2 "
            return winner


# -------- AI --------
def ai_move(right_paddle, ball):
    if random.random() < 0.5:
        if ball.centery < right_paddle.centery:
            right_paddle.y -= PADDLE_SPEED
        else:
            right_paddle.y += PADDLE_SPEED
    else:
        right_paddle.y += random.choice([-PADDLE_SPEED, PADDLE_SPEED])
    right_paddle.y = max(0, min(HEIGHT - PADDLE_H, right_paddle.y))


# -------- MENUS --------
def draw_mode_selection():
    while True:
        WIN.fill((5, 5, 20))

        for i in range(5):
            glow(WIN, NEON_PINK, WIDTH // 2, HEIGHT // 2 - 200, 100 + i * 40)
            glow(WIN, NEON_BLUE, WIDTH // 2, HEIGHT // 2 + 100, 80 + i * 35)

        title = FONT_BIG.render("NEON PONG", True, NEON_YELLOW)
        solo_text = FONT_MED.render("1. Solo vs Computer", True, NEON_BLUE)
        two_text = FONT_MED.render("2. Two Players", True, NEON_PINK)

        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 200))
        WIN.blit(solo_text, (WIDTH // 2 - solo_text.get_width() // 2, HEIGHT // 2 - 20))
        WIN.blit(two_text, (WIDTH // 2 - two_text.get_width() // 2, HEIGHT // 2 + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "solo"
                if event.key == pygame.K_2:
                    return "two"

        pygame.display.update()


def draw_pause():
    pause_text = FONT_MED.render("PAUSED — PRESS P", True, WHITE)
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()


def draw_game_over(winner):
    while True:
        WIN.fill(BLACK)

        glow(WIN, NEON_PURPLE, WIDTH // 2, HEIGHT // 2, 100)
        glow(WIN, NEON_PURPLE, WIDTH // 2, HEIGHT // 2, 50)

        text = FONT_MED.render(f"{winner} WINS!", True, NEON_YELLOW)
        press = FONT_SMALL.render("PRESS SPACE TO RETURN TO MENU", True, WHITE)

        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
        WIN.blit(press, (WIDTH // 2 - press.get_width() // 2, HEIGHT // 2 + 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "menu"

        pygame.display.update()


def main():
    while True:
        choice = draw_mode_selection()
        if choice == "quit":
            break

        result = game_loop(choice)
        if result == "quit":
            break

        again = draw_game_over(result)
        if again == "quit":
            break

    pygame.quit()


main()
