from arcade import color, key
from arcade import *
import random

WIDTH = 800
HEIGHT = 600
TITLE = "Hit The Block"
RECT_WIDTH = 100
RECT_HEIGHT = 10
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 20


# 球拍类
class Rect:
    def __init__(self):
        self.rect_color = color.DARK_BLUE
        self.rect_center_x = WIDTH // 2
        self.rect_center_y = RECT_HEIGHT // 2
        self.rect_move_x = 45

    def drawRect(self):
        draw_rectangle_filled(self.rect_center_x, self.rect_center_y, RECT_WIDTH,
                              RECT_HEIGHT, self.rect_color)

    # 球拍的移动
    def moveRect(self):
        # 球拍的y坐标被固定，只考虑是否和窗体左右边缘碰撞
        if self.rect_center_x <= RECT_WIDTH // 2:
            self.rect_center_x = RECT_WIDTH // 2
        if self.rect_center_x >= WIDTH - RECT_WIDTH // 2:
            self.rect_center_x = WIDTH - RECT_WIDTH // 2


# 小球类
class Ball:
    def __init__(self):
        self.ball_color = color.RED
        self.ball_speed_x = random.choice([-5, -4, -3, 3, 4, 5])
        self.ball_speed_y = random.choice([3, 4, 5])
        self.ball_radius = 10
        self.ball_center_x = WIDTH // 2
        self.ball_center_y = RECT_HEIGHT + self.ball_radius
        self.rect_x = WIDTH // 2
        self.rect_y = RECT_HEIGHT // 2
        self.over = False

    def drawBall(self):
        draw_circle_filled(self.ball_center_x, self.ball_center_y, self.ball_radius,
                           self.ball_color)

    # 小球的移动
    def moveBall(self):
        # 小球出界
        if self.ball_center_y <= 0:
            self.over = True

        # 小球有没有和窗体左右边缘碰撞
        if self.ball_radius <= self.ball_center_y <= HEIGHT - self.ball_radius:
            if self.ball_center_x <= self.ball_radius or \
                    self.ball_center_x >= WIDTH - self.ball_radius:
                self.ball_speed_x = -self.ball_speed_x

        # 小球有没有和球拍边缘和上边缘碰撞
        elif self.ball_radius <= self.ball_center_x <= WIDTH - self.ball_radius:
            if self.ball_center_y >= HEIGHT - self.ball_radius:
                # 上边缘碰撞
                self.ball_speed_y = -self.ball_speed_y
            elif self.ball_center_y <= self.ball_radius + RECT_HEIGHT:
                # 球拍边缘碰撞
                if self.rect_x <= self.ball_center_x <= self.rect_x + RECT_WIDTH:
                    self.ball_speed_y = -self.ball_speed_y
                else:
                    self.over = True

        self.ball_center_x += self.ball_speed_x
        self.ball_center_y += self.ball_speed_y


class Brick:
    def __init__(self, center_x, center_y):
        self.color = (139, 126, 102)
        self.center_x = center_x
        self.center_y = center_y
        self.height = BLOCK_HEIGHT
        self.width = BLOCK_WIDTH

    def drawBrick(self):
        draw_rectangle_filled(self.center_x, self.center_y,
                              self.width, self.height, self.color)


# 游戏窗口类
class Game(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg_color = color.SKY_BLUE
        self.ball = Ball()
        self.rect = Rect()
        self.total_time = 0
        self.last_time = 0
        self.game_over = False
        self.win = False
        self.score = 0
        set_background_color(self.bg_color)
        self.block_list = []
        for y in range(570, 209, -50):
            for x in range(40, 761, 144):
                self.block_list.append(Brick(x, y))

    # 绘制界面
    def on_draw(self):
        start_render()
        draw_text(f"Score: {self.score}", 10, 10, color.ORANGE,
                  font_name=("SimHei", "PingFang"), font_size=20)
        self.ball.drawBall()
        self.rect.drawRect()
        for brick in self.block_list:
            brick.drawBrick()

        if self.game_over:  # 失败
            draw_text('Game Over', WIDTH // 2 - 100, HEIGHT // 2,
                      color.RED, font_name=('SimHei', 'PingFang'), font_size=40)
        if self.win:  # 获胜
            draw_text('You Win', WIDTH // 2 - 50, HEIGHT // 2 - 50,
                      color.RED, font_name=('SimHei', 'PingFang'), font_size=40)

    # 更新界面
    def on_update(self, delta_time):
        if self.ball.over:  # 失败
            self.game_over = True

        if self.game_over or self.win:
            return

        self.total_time += delta_time
        if int(self.total_time) % 500 == 0 and \
                int(self.last_time) != int(self.total_time):
            if self.ball.ball_speed_x >= 0:
                self.ball.ball_speed_x += 2
            else:
                self.ball.ball_speed_x -= 2

            if self.ball.ball_speed_y >= 0:
                self.ball.ball_speed_y += 2
            else:
                self.ball.ball_speed_y -= 2
            self.last_time = self.total_time

        self.ball.rect_x = self.rect.rect_center_x - RECT_WIDTH // 2
        self.ball.rect_y = self.rect.rect_center_y + RECT_HEIGHT // 2
        self.ball.moveBall()

    # 按键触发事件
    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.rect.rect_center_x += self.rect.rect_move_x
            self.rect.moveRect()

        elif symbol == key.LEFT:
            self.rect.rect_center_x -= self.rect.rect_move_x
            self.rect.moveRect()


# 开始游戏
def run_game():
    Game(WIDTH, HEIGHT, TITLE)
    run()


if __name__ == "__main__":
    run_game()
