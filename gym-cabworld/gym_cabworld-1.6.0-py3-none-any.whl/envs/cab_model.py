import math

import pygame


class Cab:
    def __init__(self, cab_file, map, pos, grid_size):
        """
        Cab moving on map trying to pickup passengers
        @param cab_file: icon for cab
        @param map: to put the cab on
        @param pos: position of the passenger
        """
        self.map = map
        self.img_size = grid_size
        self.pos = pos
        self.angle = 0
        self.speed = 0
        self.radars = [0, 0, 0, 0]

        self.pick_up_possible = -1
        self.drop_off_possible = -1
        self.pick_up_index = 0

        self.is_alive = True
        self.distance = 0
        self.time_spent = 0
        self.passenger = None
        self.next_passengers = self.map.get_n_passengers(self.pos, 1)
        self.debug = False
        self.grid_size = grid_size

        self.cab_img = pygame.image.load(cab_file)
        self.cab_img = pygame.transform.scale(
            self.cab_img, (self.img_size, self.img_size)
        )
        self.rotate_cab_img = self.cab_img
        self.img_pos = [
            int(self.pos[0] - (self.img_size / 2)),
            int(self.pos[1] - (self.img_size / 2)),
        ]

        # rewards
        self.pick_up_reward = 100
        self.drop_off_reward = 100

        # motivate cab to drive the shortest path
        self.path_penalty = -1
        self.step_penalty = -1
        self.wrong_pick_up_penalty = -10
        self.wrong_drop_off_penalty = -10
        self.illegal_move_penalty = -5
        self.do_nothing_penalty = -5
        self.rewards = 0
        self.check_radar()

    def check_radar(self):
        """
        Check if there is a street up, right, down, left
        Uses compares color values
        """
        self.radars = [-1, -1, -1, -1]
        sensor_field = self.grid_size

        # up
        if self.check_if_street(self.pos[0], self.pos[1] - sensor_field):
            self.radars[0] = 1
        # right
        if self.check_if_street(self.pos[0] + sensor_field, self.pos[1]):
            self.radars[1] = 1
        # down
        if self.check_if_street(self.pos[0], self.pos[1] + sensor_field):
            self.radars[2] = 1
        # left
        if self.check_if_street(self.pos[0] - sensor_field, self.pos[1]):
            self.radars[3] = 1

    def check_for_passengers(self):
        """
        Check if a passenger can be picked up or dropped off
        """
        self.drop_off_possible = -1
        self.pick_up_possible = -1
        if self.passenger is None:
            # Empty cab -> check if pick-up is possible
            self.next_passengers = self.map.get_n_passengers(self.pos, 1)
            for i, passenger in enumerate(self.next_passengers):
                distance = self.map.calc_distance(self.pos, passenger.pos)
                if distance == 0:
                    self.pick_up_possible = 1
                    self.pick_up_index = i
                    break
        if self.passenger:
            # Occupied cab -> check if drop-off possible
            distance = self.map.calc_distance(self.pos, self.passenger.destination)
            if distance == 0:
                self.drop_off_possible = 1

    def calc_rewards(self):
        """
        Calculate current rewards
        """
        self.rewards += self.step_penalty

    def update(self):
        """
        Update the values of the cab after movement
        """
        # rotate image
        self.rotate_cab_img = self.rot_center(self.cab_img, self.angle)
        # move cab
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed

        # keep track of distance and time
        self.distance += self.speed
        self.time_spent += 1
        self.img_pos = [
            int(self.pos[0]) - (self.img_size / 2),
            int(self.pos[1]) - (self.img_size / 2),
        ]
        self.speed = 0
        self.check_radar()
        if not self.passenger:
            self.next_passengers = self.map.get_n_passengers(self.pos, 1)

        self.calc_rewards()
        # self.check_for_passengers()

    def move_up(self):
        if self.radars[0] == 1:
            self.speed = self.grid_size
            self.angle = 90
        else:
            self.rewards += self.illegal_move_penalty + 1

    def move_right(self):
        if self.radars[1] == 1:
            self.speed = self.grid_size
            self.angle = 0
        else:
            self.rewards += self.illegal_move_penalty + 1

    def move_down(self):
        if self.radars[2] == 1:
            self.speed = self.grid_size
            self.angle = -90
        else:
            self.rewards += self.illegal_move_penalty + 1

    def move_left(self):
        if self.radars[3] == 1:
            self.speed = self.grid_size
            self.angle = 180
        else:
            self.rewards += self.illegal_move_penalty + 1

    def check_pick_up_possible(self):
        if self.passenger is None:
            for passenger in self.next_passengers:
                if self.map.calc_distance(self.pos, passenger.pos) == 0:
                    return True
        return False

    def pick_up_passenger(self):
        """
        Picks up a the nearest passenger if available
        """
        self.speed = 0
        if self.passenger is None:
            for passenger in self.next_passengers:
                if self.map.calc_distance(self.pos, passenger.pos) == 0:
                    self.passenger = passenger
                    self.passenger.get_in_cab()
                    self.rewards += self.pick_up_reward + 1
                    next_passengers = self.map.get_n_passengers(self.pos, 1)
                    return
        self.rewards += self.wrong_pick_up_penalty + 1

    def drop_off_passenger(self):
        """
        Drops off a passenger
        """
        self.speed = 0
        if self.passenger:
            distance_pos_destination = self.map.calc_distance(
                self.pos, self.passenger.destination
            )
            if distance_pos_destination == 0:
                self.passenger.pos[0], self.passenger.pos[1] = self.pos[0], self.pos[1]
                self.passenger.reached_destination = True
                self.passenger.get_out_of_cab()
                self.map.remove_passenger(self.passenger)
                self.passenger = None
                self.rewards += self.drop_off_reward + 1
                self.next_passengers = self.map.get_n_passengers(self.pos, 1)
                return
        self.rewards += self.wrong_drop_off_penalty + 1

    def do_nothing(self):
        # Remove step penalty
        if self.passenger:
            self.rewards += self.do_nothing_penalty
        self.rewards += 1

    def draw(self, screen):
        """
        Draw to cab on the map
        @param screen: to draw on
        """
        screen.blit(self.rotate_cab_img, self.img_pos)
        if self.passenger:
            light_size = int(self.grid_size / 10)
            pygame.draw.circle(
                screen, self.passenger.color, self.pos, light_size, light_size
            )

    def rot_center(self, image, angle):
        """
        Rotate image around center
        @param image: image to rotate
        @param angle: angle to rotate the image
        """
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def check_if_street(self, x, y):
        """
        Check if there is street at a given position
        @param x: x-Postion to check
        @param y: y-Postion to check
        """
        delta = 10
        try:
            color = self.map.map_img.get_at((int(x), int(y)))
            street_color = self.map.street_color
            red_similar = (
                (street_color[0] - delta) < color[0] < (street_color[0] + delta)
            )
            green_similar = (
                (street_color[1] - delta) < color[1] < (street_color[1] + delta)
            )
            blue_similar = (
                (street_color[2] - delta) < color[2] < (street_color[2] + delta)
            )
            return red_similar and green_similar and blue_similar
        except IndexError:
            return False
