from arcade import color, key
from arcade import *
import random

# 大鱼吃小鱼游戏
WIDTH = 1200
HEIGHT = 800
TITLE = '大鱼吃小鱼'
SPEED = 5
LEFT = 0
RIGHT = 1


class Player(Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.append_texture(load_texture('images_fish/player.png', mirrored=True))
        self.size = 2
        self.level = 0
        self.upgrade = [10, 40, 130]

    def update(self):
        super().update()
        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH:
            self.right = WIDTH

        if self.top > HEIGHT:
            self.top = HEIGHT
        elif self.bottom < 0:
            self.bottom = 0

    def evolution(self, score):
        if score >= self.upgrade[2]:
            self.size = 8
            self.scale = 1.5
        elif score >= self.upgrade[1]:
            self.size = 6
            self.scale = 1.3
            self.level = self.upgrade[2]
        elif score >= self.upgrade[0]:
            self.size = 4
            self.scale = 1.175
            self.level = self.upgrade[1]
        else:
            self.level = self.upgrade[0]


class Enemy(Sprite):
    def __init__(self, image):
        super().__init__(image)
        face = random.choice(['left', 'right'])
        speed = random.choice([1, 2, 3, 4, 5])
        if face == 'left':
            self.center_x = WIDTH + 60
            self.change_x = -speed
        elif face == 'right':
            self.center_x = -60
            self.append_texture(load_texture(image, mirrored=True))
            self.set_texture(RIGHT)
            self.change_x = speed
        self.center_y = random.randint(0, HEIGHT)


class Status(Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2


class Game(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.setup()

    def setup(self):
        self.bg = Sprite('images_fish/newsea.png')
        self.bg.center_x = WIDTH // 2
        self.color = ["yellow", "green", "red", "purple", "blue"]
        self.bg.center_y = HEIGHT // 2
        self.fishes = [
            'images_fish/{}_fish.png'.format(self.color[i]) for i in range(5)]
        self.sizes = [1, 3, 5, 7, 9]
        self.enemy_list = SpriteList()
        self.player = Player("images_fish/player.png")
        self.total_time = 0
        self.last_time = 0
        self.create_num = 1
        self.player_list = SpriteList()
        self.player_list.append(self.player)
        self.score = 0
        self.game_over_status = False
        self.game_over = Status('images_fish/game_over.png')
        self.game_pause_status = False
        self.game_pause = Status('images_fish/game_pause.png')
        self.achievement = 300
        self.achieve_goal = False
        self.eat_sound = load_sound('images_fish/eat_sound.wav')
        self.game_over_sound = load_sound('images_fish/game_over_sound.wav')

    def on_draw(self):
        start_render()
        self.bg.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        draw_text(f'Score : {self.score}', 0, HEIGHT - 25, color.WHITE,
                  font_name=('SimHei', 'PingFang'), font_size=20)
        draw_text(f'Goal : Reach {self.achievement} scores', 110,
                  HEIGHT - 25, color.WHITE,
                  font_name=('SimHei', 'PingFang'), font_size=20)
        self.upgrade_till_next_level()
        if self.game_over_status:
            self.game_over.draw()
            if int(self.total_time) % 2 == 0:
                draw_text('Press Tab to restart',
                          WIDTH // 2 - 120, HEIGHT // 2 - 180, color.WHITE,
                          font_name=('SimHei', 'PingFang'), font_size=20)

        if self.game_pause_status:
            self.game_pause.draw()

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.game_over_status or self.game_pause_status or self.achieve_goal:
            return

        if int(self.total_time) != int(self.last_time) and \
                int(self.total_time) % 300 == 0:
            self.create_num += 1

        if int(self.total_time) != int(self.last_time) and \
                int(self.total_time) % 1 == 0:
            self.create_enemy()
            self.last_time = self.total_time

        self.player_list.update()
        self.enemy_list.update()
        for enemy in self.enemy_list:
            if enemy.center_x < -60 or enemy.center_x > WIDTH + 60:
                enemy.kill()

        hit_list = check_for_collision_with_list(self.player, self.enemy_list)
        if hit_list:
            for hit in hit_list:
                if self.player.size > hit.size:
                    play_sound(self.eat_sound)
                    hit.kill()
                    self.score += (hit.size + 1) // 2
                else:
                    self.player.kill()
                    play_sound(self.game_over_sound)
                    self.game_over_status = True

        self.player.evolution(self.score)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.player.change_y = SPEED

        elif symbol == key.DOWN:
            self.player.change_y = -SPEED

        elif symbol == key.LEFT:
            self.player.change_x = -SPEED
            self.player.set_texture(LEFT)

        elif symbol == key.RIGHT:
            self.player.change_x = SPEED
            self.player.set_texture(RIGHT)

        elif symbol == key.RETURN:
            image = get_image(0, 0, WIDTH, HEIGHT)
            image.save('images_fish/screenshot.png')

        elif symbol == key.ESCAPE:
            self.game_pause_status = not self.game_pause_status

        elif symbol == key.TAB:
            if self.game_over_status:
                self.setup()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP or symbol == key.DOWN:
            self.player.change_y = 0
        elif symbol == key.LEFT or symbol == key.RIGHT:
            self.player.change_x = 0

    def upgrade_till_next_level(self):
        if self.player.level >= self.score:
            draw_text(f'{self.player.level - self.score} more scores to next level',
                      400, HEIGHT - 25, color.WHITE,
                      font_name=('SimHei', 'PingFang'), font_size=20)

        elif self.player.upgrade[2] < self.score < self.achievement:
            draw_text(f'{self.achievement - self.score} more scores to reach the goal',
                      400, HEIGHT - 25, color.WHITE,
                      font_name=('SimHei', 'PingFang'), font_size=20)

        elif self.score >= self.achievement:
            draw_text('You win!', WIDTH // 2, HEIGHT // 2 - 75, color.RED,
                      font_name=('SimHei', 'PingFang'), font_size=80)
            self.achieve_goal = True

    def create_enemy(self):
        for i in range(self.create_num):
            fish = random.choices(self.fishes, [0.3, 0.15, 0.125, 0.125, 0.3])[0]
            size = self.sizes[self.fishes.index(fish)]
            enemy = Enemy(fish)
            enemy.size = size
            self.enemy_list.append(enemy)


def run_game():
    Game(WIDTH, HEIGHT, TITLE)
    run()


if __name__ == "__main__":
    run_game()
