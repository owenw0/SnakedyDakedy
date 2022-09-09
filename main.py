import sys, os, pygame, random
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

clock = pygame.time.Clock()
fps = 60
total_rows = 17
rows_playable = 15
cell_size = 40
highscore = 0
res = width, width = ((cell_size * total_rows), (cell_size * total_rows))
WINDOW = pygame.display.set_mode(res, HWSURFACE | DOUBLEBUF)

# sprites
SNAKE = pygame.image.load(os.path.join("assets", "snake.png")).convert_alpha()
SNAKE_HEAD = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "snake-head.png")), (cell_size, cell_size)
).convert_alpha()
SNAKE_BODY = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "snake-body.png")), (cell_size, cell_size)
).convert_alpha()
SNAKE_TAIL = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "snake-tail.png")), (cell_size, cell_size)
).convert_alpha()
SNAKE_TURN = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "snake-turn.png")), (cell_size, cell_size)
).convert_alpha()
FRUIT = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "fruit.png")), (cell_size, cell_size)
).convert_alpha()
TROPHY = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "TROPHY.png")), (cell_size, cell_size)
).convert_alpha()
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "bg.png")), res
).convert_alpha()


class Snake:
    def __init__(self):
        self.rotation = 0
        self.snake = [Vector2(5, 8), Vector2(4, 8), Vector2(3, 8)]
        self.move_dir = (1, 0)
        self.last_move = pygame.K_RIGHT
        self.pos = []
        self.score = 0

    def move(self, key):
        if key == pygame.K_RIGHT and self.last_move != pygame.K_LEFT:
            self.last_move = key
            self.move_dir = Vector2(1, 0)
            self.rotation = 0
        if key == pygame.K_LEFT and self.last_move != pygame.K_RIGHT:
            self.last_move = key
            self.move_dir = Vector2(-1, 0)
            self.rotation = 180
        if key == pygame.K_UP and self.last_move != pygame.K_DOWN:
            self.last_move = key
            self.move_dir = Vector2(0, -1)
            self.rotation = 90
        if key == pygame.K_DOWN and self.last_move != pygame.K_UP:
            self.last_move = key
            self.move_dir = Vector2(0, 1)
            self.rotation = -90

        snake_copy = self.snake[:-1]
        snake_copy.insert(0, snake_copy[0] + self.move_dir)
        self.snake = snake_copy[:]

    def update_snake(self):
        for i, block in enumerate(self.snake):
            if i == 0:
                WINDOW.blit(
                    pygame.transform.rotate(SNAKE_HEAD, self.rotation),
                    (self.snake[0].x * cell_size, self.snake[0].y * cell_size),
                )
            elif i == len(self.snake) - 1:
                WINDOW.blit(
                    pygame.transform.rotate(SNAKE_TAIL, self.rotation),
                    (self.snake[-1].x * cell_size, self.snake[-1].y * cell_size),
                )
            else:
                WINDOW.blit(
                    pygame.transform.rotate(SNAKE_BODY, self.rotation),
                    (block.x * cell_size, block.y * cell_size),
                )

    def generate_pos(self):
        row = random.randint(1, rows_playable - 1)
        col = random.randint(1, rows_playable - 1)
        # check if fruit is inside snake
        invalid_pos = False
        for block in self.snake:
            if block.x == row and block.y == col:
                invalid_pos = True
                break

        if not invalid_pos:
            self.pos = [row, col]
            return True

    def update_fruit(self):
        WINDOW.blit(FRUIT, (self.pos[0] * cell_size, self.pos[1] * cell_size))

    def check_consume(self):
        global highscore
        if self.snake[0].x == self.pos[0] and self.snake[0].y == self.pos[1]:
            self.score += 1
            if self.score > highscore:
                highscore = self.score
            return True

    def check_collision(self):
        # check wall collision
        if (
            self.snake[0].x < 1
            or self.snake[0].x > rows_playable
            or self.snake[0].y < 1
            or self.snake[0].y > rows_playable
        ):
            return True

        # check self collision
        for block in self.snake[1:]:
            if block == self.snake[0]:
                return True

        return False

        
    def game_over(self):
        menu = True
        while menu:
            WINDOW.blit(BG, (0, 0))

            fruit = pygame.transform.scale2x(FRUIT)
            fruit_rect = fruit.get_rect()
            fruit_rect.center = (width/3, width/2)
            WINDOW.blit(fruit, fruit_rect)

            score = pygame.font.SysFont("monospace", 40).render(f"{self.score}", True, (255, 255, 255))
            score_rect = score.get_rect()
            score_rect.topleft = (width/3 + 10, width/2)
            WINDOW.blit(score, score_rect)

            trophy = pygame.transform.scale2x(TROPHY)
            trophy_rect = trophy.get_rect()
            trophy_rect.center = (width * 0.66, width/2)
            WINDOW.blit(trophy, trophy_rect)


            highscore_txt = pygame.font.SysFont("monospace", 40).render(f"{highscore}", True, (255, 255, 255))
            highscore_rect = highscore_txt.get_rect()
            highscore_rect.topleft = (width * 0.66 + 10, width/2)
            WINDOW.blit(highscore_txt, highscore_rect)

            sub = pygame.font.SysFont("monospace", 25).render("Press SPACE to return to main menu", True, (255, 255, 255))
            sub_rect = sub.get_rect()
            sub_rect.center = (width/2, width * 0.65)
            WINDOW.blit(sub, sub_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu = False

            pygame.display.flip()
            clock.tick(fps)


def main_menu():
    menu = True
    while menu:
        WINDOW.blit(BG, (0, 0))
        snake_rect = pygame.transform.scale2x(SNAKE).get_rect()
        snake_rect.center = (width/2, width/4)
        WINDOW.blit(pygame.transform.scale2x(SNAKE), snake_rect)
        
        title = pygame.font.SysFont("monospace", 70).render("SnakedyDakedy", True, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.center = (width/2, width/2)
        WINDOW.blit(title, title_rect)

        sub = pygame.font.SysFont("monospace", 25).render("Press SPACE to start", True, (255, 255, 255))
        sub_rect = sub.get_rect()
        sub_rect.center = (width/2, width * 0.65)
        WINDOW.blit(sub, sub_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False

        pygame.display.flip()
        clock.tick(fps)


def main():
    run = True

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    font = pygame.font.SysFont("monospace", 20)

    while run:
        snake = Snake()
        key = pygame.K_RIGHT

        while not snake.generate_pos():
            snake.generate_pos()

        main_menu()
        while not snake.check_collision():
            clock.tick(fps)
            WINDOW.blit(BG, (0, 0))
            # display score
            WINDOW.blit(FRUIT, (0, 0))
            WINDOW.blit(
                font.render(f"{snake.score}", True, (255, 255, 255)),
                (FRUIT.get_width(), 10),
            )
            WINDOW.blit(TROPHY, (FRUIT.get_width() + 20, 0))
            WINDOW.blit(
                font.render(f"{highscore}", True, (255, 255, 255)),
                (FRUIT.get_width() + TROPHY.get_width() + 20, 10),
            )
            snake.update_snake()
            snake.update_fruit()

            # check if fruit consumed
            if snake.check_consume():
                # increase snake length by 1 block
                snake.snake.insert(
                    len(snake.snake) - 1,
                    Vector2(snake.snake[-1].x, snake.snake[-1].y),
                )
                snake.snake[-1] += snake.move_dir
                while not snake.generate_pos():
                    snake.generate_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = event.key
                if event.type == SCREEN_UPDATE:
                    snake.move(key)

            pygame.display.flip()
        
        snake.game_over()

if __name__ == "__main__":
    main()
