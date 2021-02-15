"""
This file defines the class definition of a Karel world.

The sub header comment defines important notes about the Karel
world file format.

General Notes About World Construction
- Streets run EAST-WEST (rows)
- Avenues run NORTH-SOUTH (columns)

World File Constraints:
- World file should specify one component per line in the format
  KEYWORD: PARAMETERS
- Any lines with no colon delimiter will be ignored
- The accepted KEYWORD, PARAMETER combinations are as follows:
    - Dimension: (num_avenues, num_streets)
    - Wall: (avenue, street); direction
    - Beeper: (avenue, street) count
    - Karel: (avenue, street); direction
    - Color: (avenue, street); color
    - Speed: delay
    - BeeperBag: num_beepers
- Multiple parameter values for the same keyword should be separated by a semicolon
- All numerical values (except delay) must be expressed as ints. The exception
  to this is that the number of beepers can also be INFINITY
- Any specified color values must be valid TKinter color strings, and are limited
  to the set of colors
- Direction is case-insensitive and can be one of the following values:
    - East
    - West
    - North
    - South

Original Author: Nicholas Bowman
Credits: Kylie Jue, Tyler Yep
License: MIT
Version: 1.0.0
Email: nbowman@stanford.edu
Date of Creation: 10/1/2019
Last Modified: 3/31/2020
"""
import collections
import copy
import os
import re
import sys

from .karel_definitions import COLOR_MAP, INFINITY, Direction, Wall

INIT_SPEED = 50
VALID_WORLD_KEYWORDS = [
    "dimension",
    "wall",
    "beeper",
    "karel",
    "speed",
    "beeperbag",
    "color",
]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"
DEFAULT_WORLD_FILE = "default_world.w"


class KarelWorld:
    def __init__(self, world_file):
        """
        Karel World constructor
        Parameters:
            world_file: filename containing the initial state of Karel's world
        """
        self.world_name = world_file
        self.world_file = self.process_world(world_file)

        # Map of beeper locations to the count of beepers at that location
        self.beepers = collections.defaultdict(int)

        # Map of corner colors, defaults to None
        self.corner_colors = collections.defaultdict(lambda: "")

        # Set of Wall objects placed in the world
        self.walls = set()

        # Dimensions of the world
        self.num_streets = 1
        self.num_avenues = 1

        # Initial Karel state saved to enable world reset
        self.karel_starting_location = (1, 1)
        self.karel_starting_direction = Direction.EAST
        self.karel_starting_beeper_count = 0

        # Initial speed slider setting
        self.init_speed = INIT_SPEED

        # If a world file has been specified, load world details from the file
        if self.world_file:
            self.load_from_file()

        # Save initial beeper state to enable world reset
        self.init_beepers = copy.deepcopy(self.beepers)

    def __eq__(self, other):
        return (
            self.beepers == other.beepers
            and self.walls == other.walls
            and self.num_streets == other.num_streets
            and self.num_avenues == other.num_avenues
            and self.corner_colors == other.corner_colors
        )

    @staticmethod
    def process_world(world_file):
        """
        If no world_file is provided, use default world.
        Find world file that matches program name in the current worlds/ directory.
        If not found, search the provided default worlds directory.
        """
        default_worlds_path = os.path.join(os.path.dirname(__file__), "worlds")
        if not world_file:
            default_world = os.path.join(default_worlds_path, DEFAULT_WORLD_FILE)
            if os.path.isfile(default_world):
                print("Using default world...")
                return open(default_world)
            raise FileNotFoundError(
                f"Default world cannot be found in: {default_worlds_path}\n"
                "Please raise an issue on the stanfordkarel GitHub."
            )

        if os.path.isfile(world_file):
            return open(world_file)

        for worlds_path in ("worlds", default_worlds_path):
            if os.path.isdir(worlds_path):
                full_world_path = os.path.join(worlds_path, world_file + ".w")
                if os.path.isfile(full_world_path):
                    return open(full_world_path)

        if not os.path.isdir("worlds"):
            print("Could not find worlds/ folder in current directory.\n")

        sys.tracebacklimit = 0
        available_worlds = "\n".join(
            [
                f"  {os.path.splitext(world)[0]}"
                for world in sorted(os.listdir(default_worlds_path))
            ]
        )
        raise FileNotFoundError(
            "The specified file was not one of the provided worlds.\n"
            "Please store custom worlds in a folder named worlds/, "
            f"or use a world listed below:\n{available_worlds}"
            "\nPass the default world as a parameter in run_karel_program().\n"
            "    e.g. run_karel_program('checkerboard_karel')"
        )

    @staticmethod
    def get_alt_wall(wall):
        if wall.direction == Direction.NORTH:
            return Wall(wall.avenue, wall.street + 1, Direction.SOUTH)
        if wall.direction == Direction.SOUTH:
            return Wall(wall.avenue, wall.street - 1, Direction.NORTH)
        if wall.direction == Direction.EAST:
            return Wall(wall.avenue + 1, wall.street, Direction.WEST)
        if wall.direction == Direction.WEST:
            return Wall(wall.avenue - 1, wall.street, Direction.EAST)
        raise ValueError

    @staticmethod
    def parse_parameters(keyword, param_str):
        params = {}
        for param in param_str.split(PARAM_DELIM):
            param = param.strip()

            # check to see if parameter encodes a location
            coordinate = re.match(r"\((\d+),\s*(\d+)\)", param)
            if coordinate:
                # avenue, street
                params["location"] = int(coordinate.group(1)), int(coordinate.group(2))
                continue

            # check to see if the parameter is a direction value
            if param in (d.value for d in Direction):
                params["direction"] = Direction(param)

            # check to see if parameter encodes a numerical value or color string
            elif keyword == "color":
                if param.title() not in COLOR_MAP:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                    )
                params["color"] = param.title()

            # handle the edge case where Karel has infinite beepers
            elif param in ("infinity", "infinite") and keyword == "beeperbag":
                params["val"] = INFINITY

            # float values are only valid for the speed parameter.
            elif keyword == "speed":
                try:
                    params["val"] = int(100 * float(param))
                except ValueError as e:
                    raise ValueError(
                        f"Error: {param} is an invalid parameter for {keyword}."
                    ) from e

            # must be a digit then
            elif param.isdigit():
                params["val"] = int(param)

            else:
                raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")
        return params

    def load_from_file(self):
        for i, line in enumerate(self.world_file):
            # Ignore blank lines and lines with no comma delineator
            line = line.strip()
            if not line:
                continue

            if KEYWORD_DELIM not in line:
                print(f"Incorrectly formatted line. Ignoring line {i} of file: {line}")
                continue

            keyword, param_str = line.lower().split(KEYWORD_DELIM)

            # only accept valid keywords as defined in world file spec
            # TODO: add error detection for keywords with insufficient parameters
            params = self.parse_parameters(keyword, param_str)

            # handle all different possible keyword cases
            if keyword == "dimension":
                # set world dimensions based on location values
                self.num_avenues, self.num_streets = params["location"]

            elif keyword == "wall":
                # build a wall at the specified location
                (avenue, street), direction = params["location"], params["direction"]
                self.walls.add(Wall(avenue, street, direction))

            elif keyword == "beeper":
                # add the specified number of beepers to the world
                self.beepers[params["location"]] += params["val"]

            elif keyword == "karel":
                # Give Karel initial state values
                self.karel_starting_location = params["location"]
                self.karel_starting_direction = params["direction"]

            elif keyword == "beeperbag":
                # Set Karel's initial beeper bag count
                self.karel_starting_beeper_count = params["val"]

            elif keyword == "speed":
                # Set delay speed of program execution
                self.init_speed = params["val"]

            elif keyword == "color":
                # Set corner color to be specified color
                self.corner_colors[params["location"]] = params["color"]

            else:
                print(f"Invalid keyword - ignoring line {i} of world file: {line}")

    def add_beeper(self, avenue, street):
        self.beepers[(avenue, street)] += 1

    def remove_beeper(self, avenue, street):
        if self.beepers[(avenue, street)] == 0:
            return
        self.beepers[(avenue, street)] -= 1

    def add_wall(self, wall):
        alt_wall = self.get_alt_wall(wall)
        if wall not in self.walls and alt_wall not in self.walls:
            self.walls.add(wall)

    def remove_wall(self, wall):
        alt_wall = self.get_alt_wall(wall)
        if wall in self.walls:
            self.walls.remove(wall)
        if alt_wall in self.walls:
            self.walls.remove(alt_wall)

    def paint_corner(self, avenue, street, color):
        self.corner_colors[(avenue, street)] = color

    def corner_color(self, avenue, street):
        return self.corner_colors[(avenue, street)]

    def reset_corner(self, avenue, street):
        self.beepers[(avenue, street)] = 0
        self.corner_colors[(avenue, street)] = ""

    def wall_exists(self, avenue, street, direction):
        wall = Wall(avenue, street, direction)
        return wall in self.walls

    def in_bounds(self, avenue, street):
        return 0 < avenue <= self.num_avenues and 0 < street <= self.num_streets

    def reset_world(self):
        """ Reset initial state of beepers in the world """
        self.beepers = copy.deepcopy(self.init_beepers)
        self.corner_colors = collections.defaultdict(lambda: "")

    def reload_world(self, filename=None):
        """ Reloads world using constructor. """
        self.__init__(filename)

    def save_to_file(self, filename, karel):
        with open(filename, "w") as f:
            # First, output dimensions of world
            f.write(f"Dimension: ({self.num_avenues}, {self.num_streets})\n")

            # Next, output all walls
            for wall in self.walls:
                f.write(
                    f"Wall: ({wall.avenue}, {wall.street}); {wall.direction.value}\n"
                )

            # Next, output all beepers
            for loc, count in self.beepers.items():
                f.write(f"Beeper: ({loc[0]}, {loc[1]}); {count}\n")

            # Next, output all color information
            for loc, color in self.corner_colors.items():
                if color:
                    f.write(f"Color: ({loc[0]}, {loc[1]}); {color}\n")

            # Next, output Karel information
            f.write(
                f"Karel: ({karel.avenue}, {karel.street}); {karel.direction.value}\n"
            )

            # Finally, output beeperbag info
            beeper_output = karel.num_beepers if karel.num_beepers >= 0 else "INFINITY"
            f.write(f"BeeperBag: {beeper_output}\n")
