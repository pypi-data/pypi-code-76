import curses
import time


class Screen:
    def __init__(self, config):
        self._config = config
        self._windows = {}  # Store windows as a dictionary for easy usage
        self._is_resized = False
        self._use_colors = False

    def start(self):
        """Initialize curses with defaults"""
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.try_colors()
        self.stdscr.keypad(True)
        curses.setsyx(-1, -1)

    def stop(self):
        """Revert terminal to original state"""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def try_colors(self):
        """Try to use colors"""
        if curses.has_colors and self._config.use_colors:
            self._use_colors = True
            curses.start_color()
            self._init_colors()

    """Window-specific functions"""

    def resize_or_create_window(self, win, height, width, start_y, start_x):
        """Resize window
        #
        # Creates a new window if window does not already exist
        """
        if self.test_existence(win):
            self._windows[win].resize(height, width)
        else:
            self._windows[win] = curses.newwin(height, width, start_y, start_x)

    def remove_window(self, win):
        """Remove window"""
        if self.test_existence(win):
            del self._windows[win]

    def move_window(self, win, y, x):
        """Move window"""
        self._windows[win].mvwin(y, x)

    def set_background(self, win, chr, color):
        """Set window background"""
        if self._use_colors:
            self._windows[win].bkgd(chr, curses.color_pair(color))

    def get_char(self, win):
        """Get character from specified curses window"""
        c = self._windows[win].getch()
        self.update_status(c)
        return c

    def erase_window(self, win):
        """Clear window and redraw border"""
        if self.test_existence(win):
            self._windows[win].erase()
            y, x = self._windows[win].getmaxyx()
            if y >= 3 and x >= 3:  # borders only for big enough window
                self._windows[win].border()

    def refresh_window(self, win):
        """Refresh selected window"""
        self._windows[win].refresh()

    def set_nodelays(self):
        """Set nodelay attributes to True for all windows"""
        for window in self._windows.values():
            window.nodelay(True)

    def test_existence(self, win):
        """Test for window existence"""
        return win in self._windows

    def get_max_yx(self, win):
        """Get max y and x"""
        return self._windows[win].getmaxyx()

    @property
    def is_resized(self):
        """Getter for is_resized flag"""
        return self._is_resized

    def ack_resize(self):
        """Acknowledge is_resized flag (situation handled)"""
        self._is_resized = False

    """Text management functions"""

    def add_str(self, win, y, x, message, color=None):
        """Add string to screen"""
        max_y, max_x = self._windows[win].getmaxyx()
        max_len = max_x-x-1  # accommodate borders + padding
        if y < max_y and x < max_x and max_len > 0:
            if color is not None and self._use_colors:
                self._windows[win].addnstr(y, x, message, max_len, color)
            else:
                self._windows[win].addnstr(y, x, message, max_len)

    def add_centered_str(self, win, y, message, color=None):
        """Add centered string to screen"""
        x = self.calc_start_x(win, message)
        self.add_str(win, y, x, message, color)

    def add_hline(self, win, y, chr):
        """Add horizontal line"""
        max_y, max_x = self._windows[win].getmaxyx()
        max_len = max_x-4  # accommodate borders + padding
        if y < max_y:
            self._windows[win].hline(y, 2, chr, max_len)

    def calc_start_x(self, win, text):
        """Calculate starting point for horizontally centered text"""
        y, x = self._windows[win].getmaxyx()
        pos = x // 2 - len(text) // 2
        if pos >= 0:
            return pos
        return 0

    def draw_progress_bar(self, win, y, x, total_len, percent, color=None):
        """Draw horizontal bar"""
        needed_chars = round(total_len * percent)
        if needed_chars > total_len:
            needed_chars = total_len
        elif needed_chars < 0:
            needed_chars = 0

        bar = ""
        for i in range(0, needed_chars):
            bar += "#"

        self.add_str(win, y, x, bar, color)

    def clear_line(self, win, y):
        """Clear a line while retaining borders and padding"""
        self.add_hline(win, y, " ")

    """Helpers"""

    def update_status(self, c):
        """Update screen status"""
        if c == curses.KEY_RESIZE:
            self._is_resized = True

    def screen_size(self):
        """Get screen size"""
        curses.update_lines_cols()
        return curses.LINES, curses.COLS

    def color_pair(self, i):
        """Returns curses color pair
        # 
        # Returns NoneType if colors are not in use
        """
        if self._use_colors:
            return curses.color_pair(i)
        else:
            return None

    def alarm(self):
        """Sound the actual alarm"""
        for i in range(self._config.alarm_repeat):
            if self._config.alarm_type == "beep":
                curses.beep()
            elif self._config.alarm_type == "flash":
                curses.flash()
            time.sleep(0.5)

    def _init_colors(self):
        """Initialize colors"""
        curses.use_default_colors()

        if curses.can_change_color() and not self._config.prefer_terminal_colors:
            curses.init_color(curses.COLOR_RED, 1000, 300, 300)
            curses.init_color(curses.COLOR_GREEN, 500, 1000, 300)
            curses.init_color(curses.COLOR_BLUE, 300, 700, 1000)
            curses.init_color(curses.COLOR_YELLOW, 1000, 750, 0)

        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
