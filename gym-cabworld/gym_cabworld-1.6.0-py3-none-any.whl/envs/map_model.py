import csv
import math
import os
import random

import numpy as np
import pygame


class Map:
    def __init__(self, map_file, screen_size, game_mode, data_path):
        """
        Map for the cabworld defined by image
        @param map_file: map to create world
        """
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175, 171, 171, 255)  # define color of street for radar
        self.passengers = []

        if game_mode in [0, 1]:
            map_file = "small_map.dat"
        else:
            map_file = "map.dat"

        map_dat_path = os.path.join(data_path, map_file)
        streets = []
        with open(map_dat_path, "r") as fd:
            reader = csv.reader(fd)
            for row in reader:
                streets.append([int(x) for x in row])

        self.streets = np.array(streets)
        self.grid_size = int(screen_size / len(self.streets))

        self.used_rand_pos = []

    def get_grid_size(self):
        return self.grid_size

    def add_passenger(self, passenger):
        """
        Add passenger to map
        @param passenger: passenger to add on map
        """
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        """
        Remove passenger from map
        @param passenger: passenger to remove from map
        """
        if passenger in self.passengers:
            self.passengers.remove(passenger)

    def calc_distance(self, pos1, pos2):
        """
        Calculate distance between two objects
        @param pos1: position of 1.object
        @param pos2: position of 2.object
        @return distance in pixels
        """
        return round(math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2), 2)

    def get_n_passengers(self, pos, n):
        """
        Get n passenger sorted by spawn time
        @param pos: position of cab
        @return nearest passengers
        """
        tmp_passengers = [p for p in self.passengers if not p.in_cab]
        tmp_passengers.sort()
        passengers = tmp_passengers[: (min(n, len(tmp_passengers)))]
        return passengers

    def draw_passengers(self, screen):
        """
        Draw all the passengers on the map
        @param screen: to print on
        """
        for passenger in self.passengers:
            passenger.draw(screen)

    def all_passengers_reached_dest(self):
        """
        Test if all passengers on the map have reached their destination
        """
        for tmp_passenger in self.passengers:
            if not tmp_passenger.reached_destination:
                return False
        return True

    def get_random_pos_on_map(self):
        """
        Get random position on map (on the street)
        @return pos  in pixels
        """
        x, y = 0, 0
        while self.streets[y][x] != 1 or (x, y) in self.used_rand_pos:
            x = random.randint(0, len(self.streets) - 1)
            y = random.randint(0, len(self.streets) - 1)
        self.used_rand_pos.append((x, y))
        if len(self.used_rand_pos) > 10:
            self.used_rand_pos.pop(0)
        return [
            x * self.grid_size + int(self.grid_size / 2),
            y * self.grid_size + int(self.grid_size / 2),
        ]

    def create_layer(self, pos):
        """
        Create layer for state deck
        @param pos: one-hot
        @return layer
        """
        layer = np.zeros((len(self.streets), len(self.streets)))
        x, y = pos
        x = int((x - (self.grid_size / 2)) / self.grid_size)
        y = int((y - (self.grid_size / 2)) / self.grid_size)
        layer[x][y] = 1
        return layer

    def create_state_deck(self, cab_pos):
        """
        Create state deck
        @param cab_pos: position of cab
        @return layer
        """
        # 1 layer -> map
        street_layer = self.streets
        # 2 layer -> cab
        cab_layer = self.create_layer(cab_pos)
        # 3 layer -> passenger pos
        passenger = self.get_nearest_passenger(cab_pos)
        pass_pos_layer = self.create_layer(passenger.pos)
        # 4 layer -> passenger dest
        pass_dest_layer = self.create_layer(passenger.destination)

        state_deck = np.array(
            [street_layer, cab_layer, pass_pos_layer, pass_dest_layer]
        )
        return state_deck
