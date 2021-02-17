import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtMultimedia
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence, QColor
from PyQt5.QtPrintSupport import QPrintDialog
import wikipedia
from CHP import run, prettify, String
import json

Name = 'CHP Editor PyQt5'
INPUT = None
RESULTS = []
COMMAND = None

def load(prop = None):
    with open('settings.json') as f:
        data = json.load(f)
    if prop:
        return data[prop]
    else:
        return data

def write(prop, value):
    data = load()
    with open('settings.json', 'w') as f:
        data[prop] = value
        json.dump(data, f, indent = 4, sort_keys = True)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        wikipedia.set_lang('es')
        self.find_info = False
        self.isPlaying = False
        self.music_path = load('music_path')
        self.setWindowTitle(Name)
        self.width, self.height = 600, 600
        self.resize(self.width, self.height)
        self.setWindowIcon(QIcon('./icons/notepad.ico'))

        self.setStyleSheet(
            '''
            background-color: #262626;
            color: white;
            font-size: 14px;
            font-weight: 2px;
            selection-background-color: #01559a;
            '''
        )

        self.filterTypes = 'All Files (*.*);; Text Files (*.txt);; CHP File;; Python File (*.py)'
        self.path = None
        self.update_title()
        mainLayout = QVBoxLayout()

        #editor
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet(
            '''
            background-color: #323232;
            selection-background-color: #01559a;
            selection-color: #ffffff;
            color: #ffffff;
            font-size: 16
            '''
        )
        mainLayout.addWidget(self.editor)

        #status bar
        self.statusBar = self.statusBar()

        #app container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)
        self.layoutDirection()  

        # finder
        toolsLayout = QHBoxLayout()
        self.finder = QLineEdit()
        self.finder.setPlaceholderText('Find...')
        self.site = QComboBox()
        sites = [
            ('Wikipedia', 33),
            ('Google', 0),
            ('Open Browser', 0)
        ]
        self.site.setMinimumWidth(300)
        for index, s in enumerate(sites):
            site, condition = s
            self.site.addItem(site)
            self.site.setItemData(index, condition, Qt.UserRole - 1)
        self.finder_button = QPushButton('Search', self)
        self.finder_button.clicked.connect(self.search)
        self.finder_button.setMinimumWidth(100)
        self.results = QComboBox()
        self.results.setDisabled(True)
        self.results.setMinimumWidth(300)
        toolsLayout.addWidget(self.site)
        toolsLayout.addWidget(self.results)
        toolsLayout.addWidget(self.finder_button)
        toolsLayout.addWidget(self.finder)
        mainLayout.addLayout(toolsLayout)

        calcLayout = QHBoxLayout()
        self.calc_input = QLineEdit()
        self.calc_input.setPlaceholderText('Calculate...')
        self.calc_button = QPushButton('Enter', self)
        self.calc_button.clicked.connect(self.calculate)
        self.calc_button.setMinimumWidth(100)
        calcLayout.addWidget(self.calc_button)
        calcLayout.addWidget(self.calc_input)
        mainLayout.addLayout(calcLayout)

        #player
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setPlaylist(self.playlist)

        playLayout = QVBoxLayout()
        volumeLayout = QHBoxLayout()
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.valueChanged.connect(self.volume)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setPageStep(1)
        self.volume_label = QLabel()
        self.volume_label.setText(str(self.volume_slider.value()))
        self.volume_label.setMinimumWidth(50)
        self.volume_slider.setValue(50)
        volumeLayout.addWidget(self.volume_label)
        volumeLayout.addWidget(self.volume_slider)
        playLayout.addLayout(volumeLayout)
        plaButtonsLayer = QHBoxLayout()
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon('./icons/play.ico'))
        self.play_button.clicked.connect(lambda: self.play('play'))
        self.play_button.setStyleSheet( '''background-color: #8f8f8f''')
        self.play_button.setMinimumWidth(100)
        self.next_button = QPushButton()
        self.next_button.setIcon(QIcon('./icons/next.ico'))
        self.next_button.clicked.connect(lambda: self.play('next'))
        self.next_button.setStyleSheet( '''background-color: #8f8f8f''')
        self.next_button.setMinimumWidth(100)
        self.prev_button = QPushButton()
        self.prev_button.setIcon(QIcon('./icons/prev.ico'))
        self.prev_button.clicked.connect(lambda: self.play('prev'))
        self.prev_button.setStyleSheet( '''background-color: #8f8f8f''')
        self.prev_button.setMinimumWidth(100)
        plaButtonsLayer.addWidget(self.prev_button)
        plaButtonsLayer.addWidget(self.play_button)
        plaButtonsLayer.addWidget(self.next_button)
        # self.set_playlist()
        playLayout.addLayout(plaButtonsLayer)
        mainLayout.addLayout(playLayout)
        self.layouts = [
            toolsLayout,
            calcLayout,
            playLayout
        ]
        self.hide_all_layouts()

        #file menu
        file_menu = self.menuBar().addMenu('&File')
        file_toolbar = QToolBar('File')
        file_toolbar.setMovable(0)
        file_toolbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.LeftToolBarArea, file_toolbar)
        new_file = self.create_action(self, (file_menu, file_toolbar), './icons/new.ico', 'New File...', 'New File', self.new_file, QKeySequence.New)
        open_file = self.create_action(self, (file_menu, file_toolbar), './icons/open.ico', 'Open File...', 'Open File', self.file_open, QKeySequence.Open)
        file_menu.addSeparator()
        save_file = self.create_action(self, (file_menu, file_toolbar), './icons/save.ico', 'Save File...', 'Save File', self.save_file, QKeySequence.Save)
        saveas_file = self.create_action(self, (file_menu, file_toolbar), './icons/saveas.ico', 'Save File As...', 'Save File As', self.saveas_file, QKeySequence('Ctrl+Shift+S'))
        file_menu.addSeparator()
        print_file = self.create_action(self, (file_menu, file_toolbar), './icons/print.ico', 'Print File...', 'Print File', self.print_file, QKeySequence.Print)
        file_menu.addSeparator()
        exit_button = self.create_action(self, (file_menu, file_toolbar), './icons/exit.ico', 'Exit...', 'Exit', self.close, QKeySequence('Ctrl+Shift+Esc'))

        #edit menu
        edit_menu = self.menuBar().addMenu('&Edit')
        undo = self.create_action(self, (edit_menu, file_toolbar), './icons/undo.ico', 'Undo...', 'Undo', self.editor.undo, QKeySequence.Undo)
        redo = self.create_action(self, (edit_menu, file_toolbar), './icons/redo.ico', 'Redo...', 'Redo', self.editor.redo, QKeySequence.Redo)
        selectAll = self.create_action(self, (edit_menu, file_toolbar), './icons/select.ico', 'Select All...', 'Select All', self.editor.redo, QKeySequence.SelectAll)
        edit_menu.addSeparator()
        cut = self.create_action(self, (edit_menu, file_toolbar), './icons/cut.ico', 'Cut...', 'Cut', self.editor.cut, QKeySequence.Cut)
        copy = self.create_action(self, (edit_menu, file_toolbar), './icons/copy.ico', 'Copy...', 'Copy', self.editor.copy, QKeySequence.Copy)
        paste = self.create_action(self, (edit_menu, file_toolbar), './icons/paste.ico', 'Paste...', 'Paste', self.editor.paste, QKeySequence.Paste)
        edit_menu.addSeparator()
        clear = self.create_action(self, (edit_menu, file_toolbar), './icons/clear.ico', 'Clear...', 'Clear', self.editor.clear, QKeySequence.Close)
        wrap = self.create_action(self, (edit_menu, file_toolbar), './icons/wrap.ico', 'Wrap...', 'Wrap', self.wrap_text)

        #tools menu
        tools_menu = self.menuBar().addMenu('&Tools')
        search = self.create_action(self, (tools_menu, ), './icons/search.ico', 'Search...', 'Search', lambda: self.rise(toolsLayout))
        calculator = self.create_action(self, (tools_menu, ), './icons/calculator.ico', 'Calculator...', 'Calculator', lambda: self.rise(calcLayout))
        player = self.create_action(self, (tools_menu, ), './icons/player.ico', 'Play Music...', 'Calculator', lambda: self.rise(playLayout))
        hideAll = self.create_action(self, (tools_menu, ), './icons/hide.ico', 'Hide...', 'Hide', self.hide_all_layouts)

        #settings menu
        settings_menu = self.menuBar().addMenu('&Settings')
        music_path = self.create_action(self, (settings_menu, ), './icons/music.ico', 'Change Music Path...', 'Change Music Path', lambda: self.change_path('music_path'))
        # music_path = self.create_action(self, (settings_menu, ), './icons/music.ico', 'Change Music Path...', 'Change Music Path', lambda: self.change_path(self.music_path))

    def change_path(self, prop = None):
        new_dir = QFileDialog.getExistingDirectory(
            self,
            "Open a folder"
        )
        path = new_dir + '/'
        if prop:
            write(prop, path)
        return path

    def volume(self):
        self.player.setVolume(self.volume_slider.value())
        self.volume_label.setText(str(self.volume_slider.value()))

    def set_playlist(self, path):
        if not path:
            path = self.change_path('music_path')
        files = os.listdir(path)
        for f in files:
            self.playlist.addMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(path + f)))

    def play(self, command):
        self.set_playlist(self.music_path)
        if command == 'play':
            if self.isPlaying:
                self.player.pause()
                self.play_button.setIcon(QIcon('./icons/play.ico'))
            else:
                self.player.play()
                self.play_button.setIcon(QIcon('./icons/pause.ico'))
            self.isPlaying = not self.isPlaying
        elif command == 'next':
            self.playlist.next()
            self.player.play()
        elif command == 'prev':
            self.playlist.previous()
            self.player.play()

    def assign(self, command, results):
        result = ''
        while command != '':
            if command[:7] == 'INPUT()':
                command = command[7:]
                result += results.pop(0)
            else:
                result += command[0]
                command = command[1:]
        return result

    def run(self, oper):
        value, error = run('CHP', oper, console = False)
        if value:
            elements = [str(element) for element in value.elements]
            result = ','.join(elements)
            if error: print(error)
            else: self.calc_input.insert(result)
        else: self.calc_input.insert('Invalid')

    def calculate(self): 
        global INPUT
        global RESULTS
        global COMMAND
        inputs = 0
        oper = self.calc_input.text()
        self.calc_input.clear()
        if INPUT:
            self.calc_input.insert('>>')
            oper = oper.replace('>>', '')
            RESULTS += [f'"{oper}"']
            INPUT -= 1
            if INPUT == 0:
                if RESULTS:
                    command = self.assign(COMMAND, RESULTS)
                    RESULTS = []
                    self.run(command)
                    return 0
        else:
            inputs = oper.count('INPUT()')
            if inputs:
                self.calc_input.insert('>>')
                INPUT = inputs
                COMMAND = oper
            else:
                self.run(oper)

    def hide_all_layouts(self):
        for lay in self.layouts:
            self.hide_layout(lay)

    def hide_layout(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            try:
                widget = item.widget()
                widget.hide()
            except:
                self.hide_layout(item)
    
    def show_layout(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            try:
                widget = item.widget()
                widget.show()
            except:
                self.show_layout(item)

    def rise(self, layout):
        for lay in self.layouts:
            self.hide_layout(lay)
        if layout: self.show_layout(layout)

    def search(self):
        site = self.site.currentText()
        if site == 'Wikipedia': 
            search = self.finder.text()
            if not search and not self.find_info: return 0
            self.finder.clear()
            if not self.find_info:
                # print(search)
                self.results.clear()
                results = wikipedia.search(search)
                self.results.setDisabled(False)
                self.results.addItems(results)
                self.find_info = True
            else:
                self.wikipedia()
                self.find_info = False
                self.results.clear()
        else:
            self.finder.clear()
            self.finder.insert('Browser Not Available')

    def wikipedia(self):
        wikipedia.set_lang("es")
        text = wikipedia.page(self.results.currentText())
        title = text.title
        content = text.content
        url = text.url
        text = f'{title}\n {url} \n {content} '
        # text = url
        if text:
            self.editor.appendPlainText(text)
            self.finder.clear()

    def wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def new_file(self): 
        self.path = None
        self.editor.clear()
        self.update_title()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent = self, 
            caption = 'Open File',
            directory = '',
            filter = self.filterTypes
        )
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def save_file(self):
        text = self.editor.toPlainText()
        if self.path:
            try:
                with open(self.path, 'w') as f:
                    f.write(text)
            except Exception as e:
                self.dialog_message(str(e))
        else:
            self.saveas_file()

    def saveas_file(self):
        path, _ = QFileDialog.getSaveFileName(
            parent = self, 
            caption = 'Open File',
            directory = '',
            filter = self.filterTypes
        )
        text = self.editor.toPlainText()
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(text)
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()

    def print_file(self):
        printDialog = QPrintDialog()
        if printDialog.exec_():
            self.editor.print_(printDialog.printer())

    def create_action(self, parent, menus, icon, name, status, trigger, shortcut = None):
        action = QAction(QIcon(icon), name, parent)
        action.setStatusTip(status)
        action.triggered.connect(trigger)
        if shortcut:
            action.setShortcut(shortcut)
        for menu in menus:
            menu.addAction(action)
        return action

    def update_title(self):
        self.setWindowTitle('{} {}'.format(os.path.basename(self.path) if self.path else 'Untitled', Name))

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

app = QApplication(sys.argv)
notepad = App()
notepad.show()
sys.exit(app.exec_())