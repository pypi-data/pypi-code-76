import os
import random
from random import randint

import pygame

from gym_cabworld.envs.cab_model import Cab
from gym_cabworld.envs.game import Game
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000
number_cabs = 2

number_passengers = 1  # initial
max_number_passengers = 1
min_number_passengers = 0
respawn_rate = 50  # steps


class MultiAgentGame(Game):
    def __init__(self, game_mode):
        """
        Multi agent world
        """
        pygame.init()
        pygame.display.set_caption("Cabworld-v" + str(game_mode))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.game_mode = game_mode
        self.number_cabs = number_cabs

        dirname = os.path.dirname(__file__)
        self.img_path = os.path.join(dirname, "..", "images")
        data_path = os.path.join(dirname, "..", "data")

        assert game_mode in [1, 3]

        if game_mode == 1:
            img = "small_map_gen.png"
        elif game_mode == 3:
            img = "map_gen.png"

        self.map = Map(
            os.path.join(self.img_path, img), screen_width, game_mode, data_path
        )
        self.grid_size = self.map.get_grid_size()

        self.passenger_id = 0
        for _ in range(number_passengers):
            self.add_passenger()

        self.cabs = []
        for _ in range(number_cabs):
            random_pos = self.map.get_random_pos_on_map()
            cab = Cab(
                os.path.join(self.img_path, "cab.png"),
                self.map,
                random_pos,
                self.grid_size,
            )
            self.cabs.append(cab)

        self.game_speed = 60
        self.mode = 0
        self.steps = 0

    def action(self, actions):
        """ "
        Execute action on cab
        @param actions: action to perform
        """
        assert len(actions) == len(self.cabs)

        # prevent deadlock if mult cabs want top pick-up same passenger
        if actions.count(4) > 1:
            pick_ups_possible = [cab.check_pick_up_possible() for cab in self.cabs]
            idx = [
                i
                for i in range(len(actions))
                if (actions[i] == 4 and pick_ups_possible[i])
            ]
            if len(idx) > 1:
                rand_idx = random.sample(idx, 1)[0]
                actions[rand_idx] = 6

        for cab, action in zip(self.cabs, actions):
            cab.rewards = 0
            if action == 0:
                cab.move_up()
            if action == 1:
                cab.move_right()
            elif action == 2:
                cab.move_down()
            elif action == 3:
                cab.move_left()
            elif action == 4:
                cab.pick_up_passenger()
            elif action == 5:
                cab.drop_off_passenger()
            elif action == 6:
                cab.do_nothing()

            cab.update()
            self.steps += 1

        if (
            len(self.map.passengers) < max_number_passengers
            and self.steps % respawn_rate == 0
        ) or len(self.map.passengers) < min_number_passengers:
            self.add_passenger()

    def evaluate(self):
        """ "
        Evaluate rewards
        @return reward
        """
        return [cab.rewards for cab in self.cabs]

    def is_done(self):
        """ "
        Check if all passengers have reached their destination
        @return bool
        """
        # return self.map.all_passengers_reached_dest()
        return False

    def observe(self):
        """ "
        Observe environment
        @return state of environment
        """
        observations = []
        for cab in self.cabs:
            # Possible actions
            r1, r2, r3, r4 = cab.radars
            passng = 1 if cab.passenger else -1
            pos_x, pos_y = cab.pos
            state = [r1, r2, r3, r4, passng, pos_x, pos_y]

            if cab.passenger:
                # add destination of passenger in the correct position
                dest_x, dest_y = cab.passenger.destination
                passenger_arr_pos = cab.next_passengers.index(cab.passenger)
                for _ in range(passenger_arr_pos):
                    state.append(-1)
                    state.append(-1)
                state.append(dest_x)
                state.append(dest_y)
            else:
                # add positions of passengers
                for passenger in cab.next_passengers:
                    pass_x, pass_y = passenger.pos
                    state.append(pass_x)
                    state.append(pass_y)

            observations.append(self.normalise(state))
        return observations

    def view(self):
        """ "
        Render environment using Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mode += 1
                    self.mode = self.mode % 3

        self.screen.blit(self.map.map_img, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        for cab in self.cabs:
            cab.check_radar()
            cab.draw(self.screen)

        self.map.draw_passengers(self.screen)
        pygame.display.flip()
        self.clock.tick(self.game_speed)
