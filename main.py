import sys, os, pygame, random
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

total_rows = 17
rows_playable = 15
cell_size = 40
res = width, width = ((cell_size * total_rows), (cell_size * total_rows))
WINDOW = pygame.display.set_mode(res, HWSURFACE | DOUBLEBUF)

# sprites
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
        elif key == pygame.K_LEFT and self.last_move != pygame.K_RIGHT:
            self.last_move = key
            self.move_dir = Vector2(-1, 0)
            self.rotation = 180
        elif key == pygame.K_UP and self.last_move != pygame.K_DOWN:
            self.last_move = key
            self.move_dir = Vector2(0, -1)
            self.rotation = 90
        elif key == pygame.K_DOWN and self.last_move != pygame.K_UP:
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
        if self.snake[0].x == self.pos[0] and self.snake[0].y == self.pos[1]:
            self.score += 1
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


def main_menu():
    return True


def game_over():
    return False


def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60

    snake = Snake()
    key = pygame.K_RIGHT

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    while not snake.generate_pos():
        snake.generate_pos()

    while run:
        if main_menu():
            while not snake.check_collision():
                clock.tick(fps)
                WINDOW.blit(BG, (0, 0))
                # display score
                WINDOW.blit(
                    pygame.font.SysFont("monospace", 20).render(
                        f"Score: {snake.score}", True, (0, 0, 0)
                    ),
                    (8, 8),
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

            if game_over():
                run = False


if __name__ == "__main__":
    main()
