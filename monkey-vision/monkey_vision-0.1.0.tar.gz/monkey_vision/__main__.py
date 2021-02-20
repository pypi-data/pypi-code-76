"""
##################################
###        monkey vision       ###
##################################

Usage:
------
 $ monkey_vision [options] [id] [id ...]

 Help:
 ------
 $ monkey_vision -h
 $ monkey_vision --help


 Get image event point:
 Will return the list of possible interaction coordinates (event points)
 visible in the provided screenshot.
 ------
 $ monkey_vision -r imagePath
 $ monkey_vision --run imagePath


 Percentage compare between two images:
 Will return an array of the percentage comparison of the base image, the first argument, with the rest of the arguments.
 ------
 $ monkey_vision -m imagePath1 imagePath2 ... imagePathN
 $ monkey_vision --match imagePath1 imagePath2 ... imagePathN

Percentage compare between two images focusing on a particular area of the image.
This functionality works similarly to the normal percentage compare.
The first argument of the focused percentage match is the center coordinate of the comparison area.
------
$ monkey_vision -fm "(XX, YY)" imagePath1 imagePath2 ... imagePathN
$ monkey_vision --focusedMatch "(XX, YY)" imagePath1 imagePath2 ... imagePathN

"""

import sys
from monkey_vision.vision import (
    get_event_points,
    percengate_compare,
    focused_percentage_compare,
)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return

    run_monkey_vision = "-r" in opts or "--run" in opts
    run_monkey_compare = "-m" in opts or "--match" in opts
    run_monkey_focused_compare = "-fm" in opts or "--focusedMatch" in opts

    if run_monkey_vision:
        if not args:
            print("Error: An image path is required to analyze event points")
            return
        event_points = get_event_points(args[0])
        print(event_points)
        return event_points

    if run_monkey_focused_compare:
        percentage_match = focused_percentage_compare(args[0], *args[1:])
        print(percentage_match)
        return percentage_match

    if run_monkey_compare:
        if not args or len(args) < 2:
            print("Error: Two image paths are required to run comparison.")
            return
        percentage_match = percengate_compare(*args)
        print(percentage_match)
        return percentage_match

    print(
        "NO operation! Please refer to `monkey_vision --help` for more information."
    )


if __name__ == "__main__":
    main()
