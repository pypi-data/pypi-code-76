from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_text_box import UITextBox
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame_gui.windows import UIColourPickerDialog
from pygame_gui import UIManager
from pygame import init, display, Rect, Surface, quit
from pygame.display import update
from pygame.mouse import set_visible
from pygame.time import Clock
from pygame.event import get
from random import randint
class Cat(UIWindow):
    def __init__(self, pos, manager, clear, parse, name):
        super().__init__(Rect(pos, (400, 300)), manager, name, resizable = True)
        self.textbox = UITextBox("", relative_rect = Rect(0, 0, 368, 200), manager = manager, container = self, anchors = {"left": "left", "right": "right", "top": "top", "bottom": "bottom"})
        self.input = UITextEntryLine(relative_rect = Rect(0, -35, 368, 30), manager = manager, container = self, anchors = {"left": "left", "right": "right", "top": "bottom", "bottom": "bottom"})
        self.text = ''
        self.manager = manager
        self.input.focus()
        self.clear = clear
        self.parse = parse
    def process_event(self, event):
        super().process_event(event)
        if event.type == 769 and event.key == 13:
            self.text += self.input.get_text() + "<br>"
            self.input.kill()
            self.textbox.kill()
            self.textbox = UITextBox(self.parse(self.text), relative_rect = Rect(0, 0, 368, 200), manager = self.manager, container = self, anchors = {"left": "left", "right": "right", "top": "top", "bottom": "bottom"})
            self.input = UITextEntryLine(relative_rect = Rect(0, -35, 368, 30), manager = self.manager, container = self, anchors = {"left": "left", "right": "right", "top": "bottom", "bottom": "bottom"})
            self.input.focus()
    def kill(self):
        super().kill()
        self.clear.cats.remove(self)
class Exit(UIButton):
    def __init__(self, pos, manager): super().__init__(Rect(pos, (150, 30)), "exit", manager)
    def process_event(self, event):
        super().process_event(event)
        if event.type == 32774 and event.user_type == 'ui_button_pressed' and self.pressed: exit(quit())
class Clear(UIButton):
    def __init__(self, pos, manager, cats = None):
        super().__init__(Rect(pos, (150, 30)), "clear", manager)
        self.cats = [] if cats is None else cats
        self.manager = manager
    def process_event(self, event):
        super().process_event(event)
        if event.type == 32774 and event.user_type == 'ui_button_pressed' and self.pressed:
            for cat in self.cats:
                cat.textbox.kill()
                cat.textbox = UITextBox("", relative_rect = Rect(0, 0, 368, 200), manager = self.manager, container = cat, anchors = {"left": "left", "right": "right", "top": "top", "bottom": "bottom"})
    def kill_all(self):
        for cat in self.cats: cat.kill()
class Spawn(UIButton):
    def __init__(self, pos, manager, clear, dims, parse, name):
        super().__init__(Rect(pos, (150, 30)), "spawn", manager)
        self.dims = dims
        self.clear = clear
        self.manager = manager
        self.parse = parse
        self.name = name
    def process_event(self, event):
        super().process_event(event)
        if event.type == 32774 and event.user_type == 'ui_button_pressed' and self.pressed: self.clear.cats.append(Cat((randint(0, self.dims[0] - 385 ), randint(0, self.dims[1] - 300)), self.manager, self.clear, self.parse, self.name))
class Killer(UIButton):
    def __init__(self, pos, manager, clear):
        super().__init__(Rect(pos, (150, 30)), "kill", manager)
        self.clear = clear
    def process_event(self, event):
        super().process_event(event)
        if event.type == 32774 and event.user_type == 'ui_button_pressed' and self.pressed: self.clear.kill_all()
class Paint(UIButton):
    paint = None
    def __init__(self, pos, manager):
        super().__init__(Rect(pos, (150, 30)), "paint", manager)
        self.manager = manager
    def process_event(self, event):
        super().process_event(event)
        if event.type == 32774 and event.user_type == 'ui_button_pressed' and self.pressed and (self.paint is None): self.paint = UIColourPickerDialog(Rect((100, 100, 600, 400)), self.manager, window_title = "Set Background Color")
        if event.type == 32774 and (event.user_type == 17 or (event.user_type == 'ui_button_pressed' and self.paint is not None and event.ui_element in [self.paint.cancel_button, self.paint.close_window_button])): self.paint = None
class Main:
    def __init__(self, parse, name = ""):
        init()
        display.init()
        self.DIMS = (display.Info().current_w, display.Info().current_h)
        self.BG = Surface(self.DIMS)
        self.SCREEN = display.set_mode(self.DIMS, -2147483648)
        self.MANAGER = UIManager(self.DIMS)
        set_visible(True)
        update()
        Exit((0, 0), self.MANAGER)
        clear = Clear((0, 30), self.MANAGER)
        Spawn((0, 60), self.MANAGER, clear, self.DIMS, parse, name)
        Killer((0, 90), self.MANAGER, clear)
        Paint((0, 120), self.MANAGER)
        self.clock = Clock()
        while True: self.process_events()
    def process_events(self):
        for event in get():
            if event.type == 32774 and event.user_type == 17: self.BG.fill(event.colour[:-1])
            self.MANAGER.process_events(event)
        self.MANAGER.update(self.clock.tick(60) / 1000)
        self.SCREEN.blit(self.BG, (0, 0))
        self.MANAGER.draw_ui(self.SCREEN)
        update()
