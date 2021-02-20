import os
from random import randint
import random

import pygame

from gym_cabworld.envs.cab_model import Cab
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000

number_passengers = 1  # initial
max_number_passengers = 1
min_number_passengers = 0
respawn_rate = 100  # steps


class Game:
    def __init__(self, game_mode):
        """
        Create Pygame with map, cab, passenger
        """
        pygame.init()
        pygame.display.set_caption("Cabworld-v" + str(game_mode))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.time.get_ticks()

        dirname = os.path.dirname(__file__)
        self.img_path = os.path.join(dirname, "..", "images")
        data_path = os.path.join(dirname, "..", "data")
        self.game_mode = game_mode

        assert game_mode in [0, 2]

        if game_mode == 0:
            img = "small_map_gen.png"
        else:
            img = "map_gen.png"

        self.map = Map(
            os.path.join(self.img_path, img), screen_width, game_mode, data_path
        )
        self.grid_size = self.map.get_grid_size()

        self.passenger_id = 0
        for _ in range(number_passengers):
            self.add_passenger()

        cab_pos = self.map.get_random_pos_on_map()
        self.cab = Cab(
            os.path.join(self.img_path, "cab.png"), self.map, cab_pos, self.grid_size
        )

        self.game_speed = int(self.grid_size * 1.5)
        self.mode = 0
        self.steps = 0

    def add_passenger(self):
        """ "
        Add passenger with random position and destination on map
        """
        random_pos = self.map.get_random_pos_on_map()
        random_dest = self.map.get_random_pos_on_map()
        img = "person_" + str(randint(1, 3)) + ".png"
        passenger = Passenger(
            os.path.join(self.img_path, img),
            self.map,
            random_pos,
            0,
            random_dest,
            self.grid_size,
            self.passenger_id,
        )
        self.map.add_passenger(passenger)
        self.passenger_id += 1

    def action(self, action):
        """ "
        Execute action on cab
        @param action: action to perform
        """
        # reset rewards
        self.cab.rewards = 0

        if action == 0:
            self.cab.move_up()
        elif action == 1:
            self.cab.move_right()
        elif action == 2:
            self.cab.move_down()
        elif action == 3:
            self.cab.move_left()
        elif action == 4:
            self.cab.pick_up_passenger()
        elif action == 5:
            self.cab.drop_off_passenger()
        elif action == 6:
            self.cab.do_nothing()

        self.steps += 1
        # repawn new passengers
        if (
            len(self.map.passengers) < max_number_passengers
            and self.steps % respawn_rate == 0
        ) or len(self.map.passengers) < min_number_passengers:
            self.add_passenger()

        self.cab.update()

    def evaluate(self):
        """ "
        Evaluate rewards
        @return reward
        """
        return self.cab.rewards

    def is_done(self):
        """ "
        Check if all passengers have reached their destination
        @return bool
        """
        # return self.map.all_passengers_reached_dest()
        return False

    def normalise(self, state):
        """ "
        Normalise state
        @param state
        @return normalised state
        """
        features = list(state)[:5]
        for i in range(5, len(state)):
            if state[i] == -1:
                features.append(-1)
            else:
                features.append(
                    abs(
                        round(
                            (state[i] - (1.5 * self.grid_size))
                            / (screen_width - (3 * self.grid_size)),
                            3,
                        )
                    )
                )
        # fill up the state if not enough passengers
        for _ in range(len(state), 9):
            features.append(-1)
        return tuple(features)

    def observe(self):
        """ "
        Observe environment
        @return state of environment
        """
        # Possible actions
        r1, r2, r3, r4 = self.cab.radars
        passng = 1 if self.cab.passenger else -1
        pos_x, pos_y = self.cab.pos
        state = [r1, r2, r3, r4, passng, pos_x, pos_y]

        if self.cab.passenger:
            # add destination of passenger in the correct position
            dest_x, dest_y = self.cab.passenger.destination
            passenger_arr_pos = self.cab.next_passengers.index(self.cab.passenger)
            # passenger_arr_pos = 0
            for _ in range(passenger_arr_pos):
                state.append(-1)
                state.append(-1)

            state.append(dest_x)
            state.append(dest_y)
        else:
            # add positions of passengers
            for passenger in self.cab.next_passengers:
                pass_x, pass_y = passenger.pos
                state.append(pass_x)
                state.append(pass_y)

        return self.normalise(state)

    def view(self):
        """
        Render environment using Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.blit(self.map.map_img, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        self.cab.check_radar()
        self.cab.draw(self.screen)
        self.map.draw_passengers(self.screen)

        pygame.display.flip()
        self.clock.tick(self.game_speed)
