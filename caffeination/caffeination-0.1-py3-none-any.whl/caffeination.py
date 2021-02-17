import pyautogui
import time
import sys

def print_help():
    print('How to use Caffeination:')
    print('  Run: python3 caffeination.py [seconds]')
    print('\nOptional run command (if you only have python and not python3):')
    print('  Run: python caffeination.py [seconds]')
    print('\n- the seconds parameter is not needed, but you can use it to determine')
    print('  your own time between one and the next key press in the background')
    print('  Default amount of seconds is 30')
    sys.exit()
    
def check_args():
    if len(sys.argv) == 2:
        if 'help' in sys.argv[1] or sys.argv[1] == '-h':
            print_help()
        seconds = sys.argv[1]
    elif len(sys.argv) > 2:
        print_help()
    elif len(sys.argv) == 1:
        seconds = 30
        
    if 'seconds' not in locals():
        seconds = 30

    try:
        seconds = int(seconds)
    except:
        print('You must pass an integer! Try again...')
        print('\nYou can run Caffeination with --help flag to print the manual')
        sys.exit()
    return seconds

def run_caffeination(seconds):
    try:
        print('Caffeination started')
        print(f'A background action to prevent sleep will take place every {seconds} seconds...')
        print('Press CTRL + C to stop caffeination')
        pyautogui.FAILSAFE = False
        while True:
            mouse_x, mouse_y = pyautogui.position()
            pyautogui.moveTo(mouse_x + 1, mouse_y + 1)
            pyautogui.moveTo(mouse_x - 1, mouse_y - 1)
            time.sleep(seconds)
    except KeyboardInterrupt:
        print('\nCaffeination stopped')
        sys.exit()
        
def main():
    seconds = check_args()
    run_caffeination(seconds)

if __name__ == '__main__':
    main()


