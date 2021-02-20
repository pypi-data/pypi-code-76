import random
from random import randint

import pygame


class Passenger:
    def __init__(self, passenger_file, map, pos, angle, destination, grid_size, id):
        """
        Passenger who is waiting to be picked up by a cab
        @param passenger_file: icon for passenger
        @param map: to put the passenger on
        @param pos: position of the passenger
        @param angle: of the passenger
        @param destination: of the passenger
        """
        self.id = id
        self.pos = pos
        self.angle = angle
        self.map = map
        self.destination = destination
        self.reached_destination = False
        self.time_waiting = 0
        self.in_cab = False
        self.img_size = int(grid_size / 2)
        self.passenger_img = pygame.image.load(passenger_file)
        self.passenger_img = pygame.transform.scale(
            self.passenger_img, (self.img_size, self.img_size)
        )
        self.passenger_img_rot = self.rot_center(self.passenger_img, self.angle)
        self.img_pos = [
            (self.pos[0] - (self.img_size / 2)),
            (self.pos[1] - (self.img_size / 2)),
        ]
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255), 128)

    def __lt__(self, other):
        return self.id < other.id

    def draw(self, screen):
        """
        Draw the passenger with icon on map
        @param screen: to print on
        """
        if not self.in_cab and not self.reached_destination:
            pygame.draw.circle(
                screen, self.color, self.pos, self.img_size, int(self.img_size / 8)
            )
            screen.blit(self.passenger_img, self.img_pos)

        if not self.reached_destination:
            pygame.draw.circle(
                screen,
                self.color,
                self.destination,
                self.img_size,
                int(self.img_size / 8),
            )

    def get_in_cab(self):
        """
        Passenger get into cab
        """
        self.in_cab = True

    def get_out_of_cab(self):
        """
        Passenger get off cab
        """
        self.in_cab = False

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

    def reached_destination(self):
        """
        Check if the passenger has reached its destination
        @return
        """
        delta = 20  # define how close the taxi has to be to the destination of the passenger
        x_reached = (self.pos[0] - delta) < self.destination[0] < (self.pos[0] + delta)
        y_reached = (self.pos[1] - delta) < self.destination[1] < (self.pos[1] + delta)
        return x_reached and y_reached
