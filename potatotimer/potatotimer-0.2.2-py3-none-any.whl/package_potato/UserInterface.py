import time
from datetime import timedelta


class UserInterface:
    def __init__(self, config, engine, screen):
        self._config = config
        self._engine = engine
        self._screen = screen

    def start(self):
        """Start user interface"""
        self._screen.start()
        self.manage_windows()
        try:
            self.main_loop()
        finally:
            self._screen.stop()

    def main_loop(self):
        """User interface main loop
        # 
        # Handles keystrokes, updates UI and runs timer engine
        """
        while True:
            c = self._screen.get_char("statusline")
            if c == ord('q'):
                break
            elif c == ord('s'):
                if self._engine.running:
                    self._engine.stop_timer()
                else:
                    self._engine.start_timer()
            elif c == ord('n'):
                self._engine.next_timer()
                self._engine.reset_timer()
            elif c == ord('r'):
                self._engine.reset_timer()
            elif c == ord('h'):
                self.show_help()

            if self._screen.is_resized:
                self.manage_windows()
                self._screen.ack_resize()

            self._engine.update()
            self.handle_alarm()
            self.update_statusline()
            self.update_sidebar()
            self.update_content()
            time.sleep(0.2)

    def update_statusline(self):
        """Update statusline window"""
        if not self._screen.test_existence("statusline"):
            return

        self._screen.erase_window("statusline")
        max_y, max_x = self._screen.get_max_yx("statusline")
        if self._engine.running:
            color = self.get_color_id(self._engine.timer_name)
            status = f'[ Running: {self._engine.timer_name} ]'
        else:
            color = 0
            status = "[ Stopped ]"

        self._screen.set_background("statusline", " ", color)
        self._screen.add_centered_str("statusline", 0, status)

        if max_y >= 1:
            time_left = self._engine.timer_duration - self._engine.time_elapsed
            percent = time_left / self._engine.timer_duration
            self._screen.draw_progress_bar(
                "statusline", 1, 1, max_x-2, percent)

        self._screen.refresh_window("statusline")

    def update_content(self):
        """Update content window"""
        if not self._screen.test_existence("content"):
            return

        max_y, max_x = self._screen.get_max_yx("content")
        elapsed_delta = timedelta(seconds=round(self._engine.time_elapsed))
        duration_delta = timedelta(seconds=self._engine.timer_duration)
        total_delta = timedelta(seconds=round(self._engine.total_time_elapsed))
        working_delta = timedelta(seconds=round(
            self._engine.total_time_working))
        short_delta = timedelta(seconds=round(
            self._engine.total_time_s_breaks))
        long_delta = timedelta(seconds=round(self._engine.total_time_l_breaks))
        others_delta = timedelta(seconds=round(self._engine.total_time_others))

        self._screen.clear_line("content", 1)
        self._screen.add_str(
            "content",
            1, 
            2, 
            f'{str(elapsed_delta)}/{str(duration_delta)} in {self._engine.timer_name}'
        )

        self._screen.add_str("content", 4, 16, f'{self._engine.work_count}')
        self._screen.add_str("content", 4, 20, f'{working_delta}')
        self._screen.add_str("content", 5, 16, f'{self._engine.short_count}')
        self._screen.add_str("content", 5, 20, f'{short_delta}')
        self._screen.add_str("content", 6, 16, f'{self._engine.long_count}')
        self._screen.add_str("content", 6, 20, f'{long_delta}')
        self._screen.add_str("content", 7, 16, f'{self._engine.others_count}')
        self._screen.add_str("content", 7, 20, f'{others_delta}')
        self._screen.add_str("content", 8, 20, f'{str(total_delta)}')

        if self._engine.started_at is not None:
            start_time = time.strftime("%H:%M:%S", self._engine.started_at)
            self._screen.add_str("content", 10, 25, f'{start_time}')

        if max_x > 12:
            self._screen.add_str("content", 0, max_x-12,
                                 f' {time.strftime("%H:%M:%S")} ')
        else:
            self._screen.add_str(
                "content", 0, 0, f'{time.strftime("%H:%M:%S")}')

        self._screen.refresh_window("content")

    def prepopulate_content(self):
        """Prepopulate content window with static content"""
        if not self._screen.test_existence("content"):
            return

        self._screen.erase_window("content")
        max_y, max_x = self._screen.get_max_yx("content")

        self._screen.add_str("content", 3, 2, 'Completed:')
        self._screen.add_str("content", 4, 2, 'Work stints:')
        self._screen.add_str("content", 5, 2, 'Short breaks:')
        self._screen.add_str("content", 6, 2, 'Long breaks:')
        self._screen.add_str("content", 7, 2, 'Other timers:')
        self._screen.add_str("content", 8, 2, 'Total time spent:')
        self._screen.add_str("content", 10, 2, f'First timer started at')
        self._screen.add_str("content", max_y-2, 2,
                             f"Loaded: {self._config.selected_config}")
        self._screen.add_str("content", max_y-1, 2,
                             "(s)tart/(s)top, (h)elp, (q)uit")

        self._screen.refresh_window("content")

    def update_sidebar(self):
        """Update sidebar window"""
        if not self._screen.test_existence("sidebar"):
            return

        for idx, timer in enumerate(self._config.timers):
            if idx == self._engine.current_timer_id:
                self._screen.add_str("sidebar", idx+4, 2, '>')
            else:
                self._screen.add_str("sidebar", idx+4, 2, ' ')

        self._screen.refresh_window("sidebar")

    def prepopulate_sidebar(self):
        """Prepopulate sidebar window with static content"""
        if not self._screen.test_existence("sidebar"):
            return

        self._screen.erase_window("sidebar")

        self._screen.add_str("sidebar", 1, 2, "Current timers")
        self._screen.add_str("sidebar", 2, 2, "Type (time):")
        self._screen.add_hline("sidebar", 3, "-")

        for idx, timer in enumerate(self._config.timers):
            color = self.get_color_id(timer["type"])
            duration = timedelta(minutes=timer["duration"])

            self._screen.add_str(
                "sidebar",
                idx+4,
                4,
                f'{timer["type"]} ({duration})',
                self._screen.color_pair(color)
            )

        self._screen.refresh_window("sidebar")

    def manage_windows(self):
        """Create, remove and resize windows"""
        lines, cols = self._screen.screen_size()
        content_width = cols

        if cols >= 50:
            content_width = round(cols * 0.6)
            sidebar_width = cols - content_width
            self._screen.resize_or_create_window(
                "sidebar", lines, sidebar_width, 0, content_width)
            self._screen.move_window("sidebar", 0, content_width)
        else:
            self._screen.remove_window("sidebar")

        if lines >= 6:
            self._screen.resize_or_create_window(
                "content", lines-3, content_width, 3, 0)
            self._screen.resize_or_create_window(
                "statusline", 3, content_width, 0, 0)
        else:
            self._screen.remove_window("content")
            self._screen.resize_or_create_window(
                "statusline", 1, content_width, 0, 0)

        self._screen.set_nodelays()
        self.prepopulate_sidebar()
        self.prepopulate_content()

    def get_color_id(self, type):
        """Get the id number of color for timer type"""
        if type == "work":
            return 2
        elif type == "short break":
            return 3
        elif type == "long break":
            return 4
        else:
            return 5

    def handle_alarm(self):
        """Handle timer alarms"""
        if self._engine.alarm_triggered:
            self._screen.alarm()
            self._engine.ack_alarm()

    def show_help(self):
        """Show help inside content window"""
        self._screen.erase_window("content")
        self._screen.add_str("content", 1, 2, "Potato Timer Help")
        self._screen.add_str("content", 3, 2, "s: Start and stop timers")
        self._screen.add_str("content", 4, 2, "n: Next timer (starts from 0)")
        self._screen.add_str("content", 5, 2, "r: Reset current timer")
        self._screen.add_str("content", 6, 2, "h: Show/hide help")
        self._screen.add_str("content", 7, 2, "q: Quit")

        self._screen.add_str(
            "content", 9, 2, "For more help please consult README.md at")
        self._screen.add_str(
            "content", 10, 2, "github.com/mtijas/potato-timer")
        self._screen.add_str("content", 12, 2, "(c) Markus Ijäs")

        self._screen.refresh_window("content")

        while True:
            c = self._screen.get_char("content")
            if c == ord('h'):
                break
            time.sleep(0.5)
        self._screen.erase_window("content")
        self.prepopulate_content()
