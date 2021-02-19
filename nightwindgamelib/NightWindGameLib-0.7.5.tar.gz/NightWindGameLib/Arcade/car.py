from arcade import color, key
from arcade import*
import json
import random


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "冒险小车"


class Road(Sprite):
    def __init__(self, image):
        super().__init__(image)
        # 车道
        self.center_x = SCREEN_WIDTH//2
        self.center_y = SCREEN_HEIGHT//2
        self.change_y = -9

    def update(self):
        super().update()
        if self.center_y <= SCREEN_HEIGHT // 2 - SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT


class SmallCar(Sprite):
    def __init__(self, image):
        super().__init__(image)
        # 小车
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 100

    def update(self):
        super().update()


class Cart(Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.center_y = random.randint(SCREEN_HEIGHT,
                                       SCREEN_HEIGHT + SCREEN_HEIGHT // 2)
        self.change_y = -2


class GameOver(Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2


class StatusBar:
    def __init__(self):
        self.distance = 0
        self.hp = 2
        with open("images_car/score.json", "r") as self.f:
            self.data = json.load(self.f)
            self.top_score = self.data["score"]

    def draw_top_score(self):
        pos_x = SCREEN_WIDTH - 100
        pos_y = SCREEN_HEIGHT - 20
        draw_text(f"Record:{self.top_score}", pos_x, pos_y, color.BLUE,
                  font_name=("SimHei", "PingFang"))

    def draw_bar(self):
        draw_rectangle_filled(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15, SCREEN_WIDTH, 30, color.WHITE
        )
    
    def draw_distance(self):
        pos_x = 10
        pos_y = SCREEN_HEIGHT - 20
        draw_text(f"Distance:{self.distance}", pos_x, pos_y, color.BLUE,
                  font_name=("SimHei", "PingFang"))
    
    def draw_hp(self):
        pos_x = SCREEN_WIDTH // 2 - 50
        pos_y = SCREEN_HEIGHT - 20
        draw_text(f"Heal:", pos_x, pos_y, color.BLUE,
                  font_name=("SimHei", "PingFang"))
        hearts = SpriteList()
        for i in range(self.hp):
            heart = Sprite("images_car/heal.png")
            heart.center_x = pos_x + 50 + heart.width*i
            heart.center_y = pos_y + 5
            hearts.append(heart)
        hearts.draw()
            

class MyCar(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.setup()

    def setup(self):
        self.road1 = Road("images_car/road.png")
        self.road2 = Road("images_car/road.png")
        self.road2.center_y = SCREEN_HEIGHT // 2 + SCREEN_HEIGHT
        self.small_car_list = [f"images_car/small_car{str(i)}" for i in range(1, 5)]
        self.small_car = SmallCar(f"{random.choice(self.small_car_list)}.png")
        self.carts = SpriteList()
        self.create_carts()
        self.total_time = 0
        self.last_time = 0
        self.status_bar = StatusBar()
        self.game_status = True
        self.gameover = GameOver("images_car/game_over.png")

    def on_draw(self):
        start_render()
        self.road1.draw()
        self.road2.draw()
        self.small_car.draw()
        for cart in self.carts:
            cart.draw()
        self.status_bar.draw_bar()
        self.status_bar.draw_distance()
        self.status_bar.draw_hp()
        if not self.game_status:
            self.gameover.draw()
        self.status_bar.draw_top_score()

    def on_update(self, delta_time: float):
        if self.game_status:
            self.small_car.update()
            self.road1.update()
            self.road2.update()
            for cart in self.carts:
                cart.update()
                if cart.top < 0:
                    cart.kill()
            self.total_time += delta_time
            if int(self.last_time) != int(self.total_time) and \
                    int(self.total_time) % 6 == 0:
                self.create_carts()
                self.last_time = self.total_time
            self.status_bar.distance = int(self.total_time)
            hit_list = check_for_collision_with_list(self.small_car, self.carts)
            if hit_list:
                for hit in hit_list:
                    hit.kill()
                    self.status_bar.hp -= 1
            self.judge_game_status()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == key.LEFT and self.small_car.center_x >= SCREEN_WIDTH //2:
            self.small_car.center_x -= 200
        elif symbol == key.RIGHT and self.small_car.center_x <= SCREEN_WIDTH //2:
            self.small_car.center_x += 200

    def create_carts(self):
        cart_list = ["images_car/big_car1.png",
                     "images_car/big_car2.png",
                     "images_car/big_car3.png"]
        num = 2
        x = random.sample([SCREEN_WIDTH // 2 - 200,
                           SCREEN_WIDTH // 2,
                           SCREEN_WIDTH // 2 + 200], 2)
        for i in range(num):
            cart = Cart(random.choice(cart_list))
            cart.center_x = x[i]
            self.carts.append(cart)

    def judge_game_status(self):
        if self.status_bar.hp <= 0:
            self.game_status = False
            if self.status_bar.distance > self.status_bar.top_score:
                self.status_bar.data["score"] = self.status_bar.distance
                with open("images_car/score.json", "w") as f:
                    json.dump(self.status_bar.data, f)


def run_game():
    MyCar(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    run()


if __name__ == "__main__":
    run_game()
