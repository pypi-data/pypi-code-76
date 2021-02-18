from ..g2p.generator import PyniniDictionaryGenerator as Generator, G2P_DISABLED

from PyQt5 import QtGui, QtCore, QtWidgets, QtMultimedia

import pyqtgraph as pg

import librosa
import numpy as np


class DetailedMessageBox(QtWidgets.QMessageBox):  # pragma: no cover
    # Adapted from http://stackoverflow.com/questions/2655354/how-to-allow-resizing-of-qmessagebox-in-pyqt4
    def __init__(self, *args, **kwargs):
        super(DetailedMessageBox, self).__init__(*args, **kwargs)
        self.setWindowTitle('Error encountered')
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.setStandardButtons(QtWidgets.QMessageBox.Close)
        self.setText("Something went wrong!")
        self.setInformativeText("Please copy the text below and send to Michael.")

        self.setMinimumWidth(200)

    def resizeEvent(self, event):
        result = super(DetailedMessageBox, self).resizeEvent(event)
        details_box = self.findChild(QtWidgets.QTextEdit)
        if details_box is not None:
            details_box.setFixedHeight(details_box.sizeHint().height())
        return result


class MediaPlayer(QtMultimedia.QMediaPlayer):  # pragma: no cover
    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.max_time = None
        self.min_time = None
        self.sr = None
        self.setNotifyInterval(1)
        self.positionChanged.connect(self.checkStop)

    def setMaxTime(self, max_time):
        self.max_time = max_time * self.sr

    def setMinTime(self, min_time):
        self.min_time = min_time * self.sr

    def setSr(self, sr):
        self.sr = sr

    def checkStop(self, position):
        if self.state() == QtMultimedia.QMediaPlayer.PlayingState:
            if self.min_time is not None:
                if position < self.min_time:
                    self.setPosition(self.min_time)
            if self.max_time is not None:
                if position > self.max_time:
                    self.stop()


class UtteranceListWidget(QtWidgets.QWidget):  # pragma: no cover
    utteranceChanged = QtCore.pyqtSignal(object)
    utteranceMerged = QtCore.pyqtSignal()
    saveFile = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super(UtteranceListWidget, self).__init__(parent=parent)
        self.setMaximumWidth(500)
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setColumnCount(4)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_widget.setHorizontalHeaderLabels(['Utterance', 'Speaker', 'File', 'OOV found'])
        self.table_widget.setSortingEnabled(True)
        self.table_widget.currentItemChanged.connect(self.update_utterance)
        self.table_widget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton('Save current file')
        self.saveButton.clicked.connect(self.save_file)
        button_layout.addWidget(self.saveButton)
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.corpus = None
        self.dictionary = None
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table_widget.setFocusPolicy(QtCore.Qt.NoFocus)

    def save_file(self):
        current_utt = self.get_current_selection()[0]
        if self.corpus.segments:
            current_file = self.corpus.segments[current_utt].split()[0]
        else:
            current_file = current_utt
        self.saveFile.emit(current_file)

    def update_utterance(self, cell):
        utterance = self.table_widget.item(cell.row(), 0).text()
        self.utteranceChanged.emit(utterance)

    def get_current_selection(self):
        utts = []
        for i in self.table_widget.selectedItems():
            if i.column() == 0:
                utts.append(i.text())
        return utts

    def merge_utterances(self):
        utts = {}
        rows = []
        for i in self.table_widget.selectedItems():
            if i.column() == 0:
                utts[i.row()] = i.text()
            else:
                rows.append(i.row())
        row = None
        for r in sorted(rows):
            if row is not None:
                if r - row != 1:
                    return
            row = r
        min_begin = 1000000000
        max_end = 0
        text = ''
        speaker = None
        text_file = None
        for r, old_utt in sorted(utts.items(), key=lambda x: x[0]):
            if old_utt in self.corpus.segments:
                seg = self.corpus.segments[old_utt]
                if speaker is None:
                    speaker = self.corpus.utt_speak_mapping[old_utt]
                    text_file = self.corpus.utt_text_file_mapping[old_utt]
                filename, beg, end = seg.split(' ')
                if 'channel' in filename:
                    actual_filename, channel_suffix = filename.split('_')
                    channel_suffix = '_' + channel_suffix
                else:
                    channel_suffix = ''
                    actual_filename = filename
                beg = round(float(beg), 4)
                end = round(float(end), 4)
                if beg < min_begin:
                    min_begin = beg
                if end > max_end:
                    max_end = end
                utt_text = self.corpus.text_mapping[old_utt]
                text += utt_text + ' '
            else:
                return
        text = text[:-1]
        new_utt = '{}_{}_{}_{}'.format(speaker, actual_filename, min_begin, max_end).replace('.', '_')
        new_utt += channel_suffix
        new_seg = '{} {} {}'.format(filename, min_begin, max_end)
        self.corpus.segments[new_utt] = new_seg
        self.corpus.utt_speak_mapping[new_utt] = speaker
        self.corpus.utt_text_file_mapping[new_utt] = text_file
        self.corpus.text_mapping[new_utt] = text
        for r, old_utt in sorted(utts.items(), key=lambda x: x[0]):
            del self.corpus.segments[old_utt]
            del self.corpus.utt_speak_mapping[old_utt]
            del self.corpus.utt_text_file_mapping[old_utt]
            del self.corpus.text_mapping[old_utt]
        self.refresh_list()
        self.utteranceMerged.emit()
        self.select_utterance(new_utt)

    def select_utterance(self, utt):
        cur = self.get_current_selection()
        self.table_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        if utt is None:
            self.table_widget.clearSelection()
        else:
            for r in range(self.table_widget.rowCount()):
                if self.table_widget.item(r, 0).text() == utt:
                    self.table_widget.selectRow(r)
                    break
        self.table_widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def refresh_corpus(self, utt=None):
        self.refresh_list()
        self.table_widget.clearSelection()
        self.select_utterance(utt)

    def update_corpus(self, corpus):
        self.corpus = corpus
        self.refresh_list()

    def update_dictionary(self, dictionary):
        self.dictionary = dictionary
        self.refresh_list()

    def refresh_list(self):
        self.table_widget.setRowCount(len(self.corpus.text_mapping))
        if self.corpus is not None:
            for i, (u, t) in enumerate(sorted(self.corpus.text_mapping.items(),
                                              key=lambda x: [float(x) if j > 0 else x for j, x in
                                                             enumerate(self.corpus.segments[x[0]].split())])):
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(u))
                self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.corpus.utt_speak_mapping[u]))
                self.table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.corpus.utt_file_mapping[u]))
                oov_found = False
                if self.dictionary is not None:
                    words = t.split(' ')
                    for w in words:
                        if not self.dictionary.check_word(w):
                            oov_found = True
                if oov_found:
                    t = QtWidgets.QTableWidgetItem('yes')
                    t.setBackground(QtCore.Qt.red)
                else:
                    t = QtWidgets.QTableWidgetItem('no')
                    t.setBackground(QtCore.Qt.green)
                self.table_widget.setItem(i, 3, t)


class TranscriptionWidget(QtWidgets.QTextEdit):  # pragma: no cover
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            event.ignore()
            return
        super(TranscriptionWidget, self).keyPressEvent(event)


class UtteranceDetailWidget(QtWidgets.QWidget):  # pragma: no cover
    lookUpWord = QtCore.pyqtSignal(object)
    createWord = QtCore.pyqtSignal(object)
    saveUtterance = QtCore.pyqtSignal(object, object)
    selectUtterance = QtCore.pyqtSignal(object)
    mergeSelected = QtCore.pyqtSignal()
    refreshCorpus = QtCore.pyqtSignal(object)
    updateSpeaker = QtCore.pyqtSignal(object, object)

    def __init__(self, parent):
        super(UtteranceDetailWidget, self).__init__(parent=parent)
        self.corpus = None
        self.dictionary = None
        self.utterance = None
        self.audio = None
        self.sr = None
        self.current_time = 0
        self.min_time = 0
        self.max_time = None
        self.m_audioOutput = MediaPlayer()
        #self.m_audioOutput.error.connect(self.showError)
        self.m_audioOutput.positionChanged.connect(self.notified)
        self.m_audioOutput.stateChanged.connect(self.handleAudioState)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ax = pg.PlotWidget()
        self.ax.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line = pg.InfiniteLine(
            pos=-20,
            pen=pg.mkPen('r', width=3),
            movable=False  # We have our own code to handle dragless moving.
        )
        self.ax.getPlotItem().hideAxis('left')
        self.ax.getPlotItem().setMouseEnabled(False, False)
        self.ax.addItem(self.line)
        self.ax.getPlotItem().setMenuEnabled(False)
        self.ax.scene().sigMouseClicked.connect(self.update_current_time)
        layout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QVBoxLayout()
        self.play_button = QtWidgets.QPushButton('Play')
        self.play_button.clicked.connect(self.play_audio)
        self.speaker_dropdown = QtWidgets.QComboBox()
        self.speaker_dropdown.currentIndexChanged.connect(self.update_speaker)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.speaker_dropdown)
        self.text_widget = TranscriptionWidget()
        self.text_widget.setMaximumHeight(300)
        self.text_widget.textChanged.connect(self.update_utterance_text)
        self.text_widget.setFontPointSize(20)
        self.text_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.text_widget.customContextMenuRequested.connect(self.generate_context_menu)
        text_layout = QtWidgets.QHBoxLayout()
        text_layout.addWidget(self.text_widget)
        text_layout.addLayout(button_layout)
        layout.addWidget(self.ax)
        layout.addLayout(text_layout)
        self.setLayout(layout)
        self.wav_path = None
        self.wave_data = None
        self.long_file = None
        self.sr = 1000
        self.file_utts = []

    def update_speaker(self):
        self.updateSpeaker.emit(self.utterance, self.speaker_dropdown.currentText())

    def update_utterance_text(self):
        new_text = self.text_widget.toPlainText().strip().lower()
        self.corpus.text_mapping[self.utterance] = new_text

    def update_plot_scale(self):
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())

    def refresh_speaker_dropdown(self):
        self.speaker_dropdown.clear()
        speakers = sorted(self.corpus.speak_utt_mapping.keys())
        print(speakers)
        for s in self.corpus.speak_utt_mapping.keys():
            if not s:
                continue
            self.speaker_dropdown.addItem(s)

    def update_corpus(self, corpus):
        self.corpus = corpus
        self.refresh_speaker_dropdown()
        if self.utterance:
            self.reset_text()

    def update_dictionary(self, dictionary):
        self.dictionary = dictionary

    def generate_context_menu(self, location):

        menu = self.text_widget.createStandardContextMenu()
        cursor = self.text_widget.cursorForPosition(location)
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        word = cursor.selectedText()
        # add extra items to the menu
        lookUpAction = QtWidgets.QAction("Look up '{}' in dictionary".format(word), self)
        createAction = QtWidgets.QAction("Add pronunciation for '{}'".format(word), self)
        lookUpAction.triggered.connect(lambda : self.lookUpWord.emit(word))
        createAction.triggered.connect(lambda : self.createWord.emit(word))
        menu.addAction(lookUpAction)
        menu.addAction(createAction)
        # show the menu
        menu.exec_(self.text_widget.mapToGlobal(location))

    def update_current_time(self, ev):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        point = self.ax.getPlotItem().vb.mapSceneToView(ev.scenePos())
        x = point.x()
        if modifiers == QtCore.Qt.ControlModifier:
            time = x / self.sr
            utt = None
            for u in self.file_utts:
                if u['end'] < time:
                    continue
                if u['begin'] > time:
                    break
                utt = u
            if utt is not None:
                self.selectUtterance.emit(utt['utt'])
        self.current_time = x / self.sr
        if self.current_time < self.min_time:
            self.current_time = self.min_time
            x = self.current_time * self.sr
        if self.current_time > self.max_time:
            self.current_time = self.max_time
            x = self.current_time * self.sr

        self.line.setPos(x)
        self.m_audioOutput.setMinTime(self.current_time)
        self.m_audioOutput.setPosition(self.m_audioOutput.min_time)

    def refresh_utterances(self):
        self.file_utts =[]
        for u, s in self.corpus.segments.items():
            _, b, e = s.split(' ')
            b = float(b)
            e = float(e)

            self.file_utts.append({'utt': u, 'begin': b, 'end': e, 'text': self.corpus.text_mapping[u]})
        self.file_utts.sort(key=lambda x: x['begin'])
        self.min_time = None
        self.max_time = None

    def update_utterance(self, utterance):
        if utterance is None:
            return
        self.utterance = utterance
        self.reset_text()
        if self.utterance in self.corpus.segments:
            segment = self.corpus.segments[self.utterance]
            file_name, begin, end = segment.split(' ')
            begin = float(begin)
            end = float(end)
            if self.max_time is not None and self.min_time is not None:
                if self.min_time + 1 <= end <= self.max_time - 1:
                    return
                if self.min_time + 1 <= begin <= self.max_time - 1:
                    return
            if self.wav_path != self.corpus.utt_wav_mapping[file_name]:
                self.file_utts =[]
                for u, s in self.corpus.segments.items():
                    _, b, e = s.split(' ')
                    b = float(b)
                    e = float(e)

                    self.file_utts.append({'utt': u, 'begin': b, 'end': e, 'text': self.corpus.text_mapping[u],
                                           'speaker': self.corpus.utt_speak_mapping[u]})
                self.file_utts.sort(key=lambda x: x['begin'])
            self.wav_path = self.corpus.utt_wav_mapping[file_name]
            self.long_file = True
        else:
            self.wav_path = self.corpus.utt_wav_mapping[self.utterance]
            self.long_file = False
            begin = 0
            end = 0
        begin -= 1
        end += 1

        self.update_plot(begin, end)
        p = QtCore.QUrl.fromLocalFile(self.wav_path)
        self.m_audioOutput.setMedia(QtMultimedia.QMediaContent(p))

    def update_plot(self, begin, end):
        print('UPDATING PLOT')
        if end <= 0:
            end = self.max_time
        if begin < 0:
            begin = 0
        print(begin, end)
        if self.long_file:
            duration = end - begin
            self.wave_data, self.sr = librosa.load(self.wav_path, offset=begin, duration=duration, sr=self.sr)
            y = self.wave_data
        elif self.wave_data is None:
            self.wave_data, self.sr = librosa.load(self.wav_path, sr=self.sr)
        begin_samp = int(begin * self.sr)
        end_samp = int(end * self.sr)
        if not self.long_file:
            y = self.wave_data[begin_samp:end_samp]
            x = np.arange(start=begin_samp, stop=end_samp)
        else:
            x = np.arange(start=begin_samp, stop=begin_samp+y.shape[0])
        self.min_time = begin
        self.max_time = end
        self.ax.getPlotItem().clear()
        self.ax.plot(x, y, pen=pg.mkPen('w', width=3))
        self.updatePlayTime(self.min_time)
        self.ax.addItem(self.line)
        for u in self.file_utts:
            if u['end'] < self.min_time:
                continue
            if u['begin'] > self.max_time:
                break
            b_s = u['begin'] * self.sr
            e_s = u['end'] * self.sr
            mid_b = self.min_time
            mid_e = self.max_time
            from functools import partial
            if u['begin'] > self.min_time:
                u['begin_line'] = pg.InfiniteLine(
                        pos=b_s,
                        pen=pg.mkPen('g', width=3),
                        movable=True  # We have our own code to handle dragless moving.
                    )
                func = partial(self.update_utt_times, u, begin=True)
                u['begin_line'].sigPositionChangeFinished.connect(func)
                self.ax.addItem(u['begin_line'])
                mid_b = u['begin']
            if u['end'] < self.max_time:
                u['end_line'] = pg.InfiniteLine(
                        pos=e_s,
                        pen=pg.mkPen('y', width=3),
                        movable=True  # We have our own code to handle dragless moving.
                    )
                func = partial(self.update_utt_times, u, begin=False)
                u['end_line'].sigPositionChangeFinished.connect(func)
                self.ax.addItem(u['end_line'])
                mid_e = u['end']
            mid_point = (mid_e - mid_b) # * self.sr
            mid_point *= 0.5
            mid_point += mid_b
            mid_point *= self.sr
            t = pg.TextItem(u['utt'], anchor=(0.5, 0.5))
            min_point = y.min()
            t.setPos(mid_point, min_point)
            self.ax.addItem(t)
        self.ax.setXRange(begin_samp, end_samp)
        self.ax.setYRange(y.min(), y.max())
        self.ax.getPlotItem().getAxis('bottom').setScale(1/self.sr)
        self.m_audioOutput.setSr(self.sr)
        self.m_audioOutput.setMinTime(self.min_time)
        self.m_audioOutput.setMaxTime(self.max_time)
        self.updatePlayTime(begin)

    def update_utt_times(self, utt, x, begin=False):
        new_time = round(x.pos()[0] /self.sr, 4)
        if begin:
            line = utt['begin_line']
            utt['begin'] = new_time
        else:
            line = utt['end_line']
            utt['end'] = new_time
        line.setPos(int(new_time * self.sr))
        old_utt = utt['utt']
        speaker = self.corpus.utt_speak_mapping[old_utt]
        text_file = self.corpus.utt_text_file_mapping[old_utt]
        text = self.corpus.text_mapping[old_utt]
        if old_utt in self.corpus.segments:
            seg = self.corpus.segments[old_utt]
            filename, old_beg, old_end = seg.split(' ')
            if 'channel' in filename:
                actual_filename, channel_suffix = filename.split('_')
                channel_suffix = '_' + channel_suffix
            else:
                channel_suffix = ''
                actual_filename = filename
            new_utt = '{}_{}_{}_{}'.format(speaker, actual_filename, utt['begin'], utt['end']).replace('.', '_')
            new_utt += channel_suffix
            new_seg = '{} {} {}'.format(filename, utt['begin'], utt['end'])
            utt['utt'] = new_utt
            del self.corpus.segments[old_utt]
            self.corpus.segments[new_utt] = new_seg

        del self.corpus.utt_speak_mapping[old_utt]
        self.corpus.utt_speak_mapping[new_utt] = speaker

        del self.corpus.utt_text_file_mapping[old_utt]
        self.corpus.utt_text_file_mapping[new_utt] = text_file

        del self.corpus.text_mapping[old_utt]
        self.corpus.text_mapping[new_utt] = text
        self.update_plot(self.min_time, self.max_time)
        self.refreshCorpus.emit(new_utt)

    def reset_text(self):
        if self.utterance not in self.corpus.text_mapping:
            self.utterance = None
            self.audio = None
            self.sr = None
            self.text_widget.setText('')
            return
        text = self.corpus.text_mapping[self.utterance]
        words = text.split(' ')
        mod_words = []
        if self.dictionary is not None:
            for i, w in enumerate(words):
                if i != len(words) - 1:
                    space = ' '
                else:
                    space = ''
                if not self.dictionary.check_word(w):
                    w = '<span style=\" font-size: 20pt; font-weight:600; color:#ff0000;\" >{}{}</span>'.format(w, space)
                else:
                    w = '<span style=\" font-size: 20pt\" >{}{}</span>'.format(w, space)
                mod_words.append(w)

        else:
            mod_words = words
        self.text_widget.setText(''.join(mod_words))
        self.speaker_dropdown.setCurrentText(self.corpus.utt_speak_mapping[self.utterance])

    def showError(self, e):
        reply = DetailedMessageBox()
        reply.setDetailedText(str(e))
        ret = reply.exec_()

    def play_audio(self):
        if self.m_audioOutput.state() == QtMultimedia.QMediaPlayer.StoppedState or \
                self.m_audioOutput.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.m_audioOutput.play()
        elif self.m_audioOutput.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.m_audioOutput.pause()
        elif self.m_audioOutput.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.m_audioOutput.play()

    def keyPressEvent(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.min_time is None:
            return
        shift = round((self.max_time - self.min_time) * 0.25, 3)
        cur_duration = self.max_time - self.min_time
        if event.key() == QtCore.Qt.Key_Space:
            if self.utterance is None:
                return
            self.play_audio()
        elif event.key() == QtCore.Qt.Key_M and modifiers == QtCore.Qt.ControlModifier:
            self.mergeSelected.emit()
        elif event.key() == QtCore.Qt.Key_O and modifiers == QtCore.Qt.ControlModifier:
            if cur_duration + 2 * shift > 40:
                shift = (40 - cur_duration) / 2
            self.min_time -= shift
            self.max_time += shift
            self.update_plot(self.min_time, self.max_time)
        elif event.key() == QtCore.Qt.Key_I and modifiers == QtCore.Qt.ControlModifier:
            if cur_duration - 2 * shift < 1:
                shift = (cur_duration - 1) / 2
            self.min_time += shift
            self.max_time -= shift
            self.update_plot(self.min_time, self.max_time)
        elif event.key() == QtCore.Qt.Key_Left:
            if self.min_time < shift:
                shift = self.min_time
            self.min_time -= shift
            if self.min_time < 0:
                self.min_time = 0
            self.max_time -= shift
            self.update_plot(self.min_time, self.max_time)
        elif event.key() == QtCore.Qt.Key_Right:
            self.min_time += shift
            self.max_time += shift
            self.update_plot(self.min_time, self.max_time)


    def updatePlayTime(self, time):
        if not time:
            return
        if self.max_time and time > self.max_time:
            return
        if self.sr:
            pos = int(time * self.sr)
            self.line.setPos(pos)

    def notified(self, position):
        time = position / self.sr
        self.updatePlayTime(time)

    def handleAudioState(self, state):
        if state == QtMultimedia.QMediaPlayer.StoppedState:
            min_time = self.min_time
            self.m_audioOutput.setPosition(0)
            self.updatePlayTime(min_time)


class InformationWidget(QtWidgets.QWidget):  # pragma: no cover
    resetDictionary = QtCore.pyqtSignal()
    saveDictionary = QtCore.pyqtSignal(object)
    newSpeaker = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(InformationWidget, self).__init__(parent=parent)
        self.setMaximumWidth(500)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dictionary = None
        self.corpus = None

        self.tabs = QtWidgets.QTabWidget()

        layout = QtWidgets.QVBoxLayout()
        dict_layout = QtWidgets.QVBoxLayout()
        self.dictionary_widget = QtWidgets.QTableWidget()
        self.dictionary_widget.verticalHeader().setVisible(False)
        self.dictionary_widget.setColumnCount(2)
        self.dictionary_widget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.dictionary_widget.setHorizontalHeaderLabels(['Word', 'Pronunciation'])
        dict_layout.addWidget(self.dictionary_widget)

        button_layout = QtWidgets.QHBoxLayout()
        self.reset_button = QtWidgets.QPushButton('Reset dictionary')
        self.save_button = QtWidgets.QPushButton('Save dictionary')

        self.reset_button.clicked.connect(self.resetDictionary.emit)
        self.save_button.clicked.connect(self.create_dictionary_for_save)

        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)

        dict_layout.addLayout(button_layout)

        dict_widget = QtWidgets.QWidget()
        dict_widget.setLayout(dict_layout)

        speaker_layout = QtWidgets.QVBoxLayout()
        self.speaker_widget = QtWidgets.QTableWidget()
        self.speaker_widget.verticalHeader().setVisible(False)
        self.speaker_widget.setColumnCount(2)
        self.speaker_widget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.speaker_widget.setHorizontalHeaderLabels(['Speaker', 'Utterances'])
        speaker_layout.addWidget(self.speaker_widget)

        add_layout = QtWidgets.QHBoxLayout()
        self.speaker_edit = QtWidgets.QLineEdit()
        self.save_speaker_button = QtWidgets.QPushButton('Add speaker')

        self.save_speaker_button.clicked.connect(self.save_speaker)

        add_layout.addWidget(self.speaker_edit)
        add_layout.addWidget(self.save_speaker_button)

        speaker_layout.addLayout(add_layout)

        speak_widget = QtWidgets.QWidget()
        speak_widget.setLayout(speaker_layout)

        self.tabs.addTab(dict_widget, 'Dictionary')
        self.tabs.addTab(speak_widget, 'Speakers')
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def save_speaker(self):
        new_speaker = self.speaker_edit.text()
        if new_speaker in self.corpus.speak_utt_mapping:
            return
        if not new_speaker:
            return
        self.corpus.speak_utt_mapping[new_speaker] = []
        self.refresh_speakers()
        self.newSpeaker.emit()

    def refresh_speakers(self):
        if self.corpus is None:
            return
        speakers = sorted(self.corpus.speak_utt_mapping.keys())
        print(speakers)
        self.speaker_widget.setRowCount(len(speakers))

        for i, s in enumerate(speakers):
            self.speaker_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(s))
            self.speaker_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(len(self.corpus.speak_utt_mapping[s]))))

    def update_corpus(self, corpus):
        self.corpus = corpus
        print('LOADED', corpus)
        self.refresh_speakers()

    def update_dictionary(self, dictionary):
        self.dictionary = dictionary
        self.dictionary_widget.setRowCount(len(self.dictionary))
        cur_index = 0
        for word, prons in sorted(self.dictionary.words.items()):
            for p in prons:
                pronunciation = ' '.join(p['pronunciation'])
                self.dictionary_widget.setItem(cur_index, 0, QtWidgets.QTableWidgetItem(word))
                self.dictionary_widget.setItem(cur_index, 1, QtWidgets.QTableWidgetItem(pronunciation))
                cur_index += 1

    def update_g2p(self, g2p_model):
        self.g2p_model = g2p_model

    def create_dictionary_for_save(self):
        from collections import defaultdict
        words = defaultdict(list)
        phones = set()
        for i in range(self.dictionary_widget.rowCount()):
            word = self.dictionary_widget.item(i, 0).text()
            pronunciation = self.dictionary_widget.item(i, 1).text()
            pronunciation = tuple(pronunciation.split(' '))
            phones.update(pronunciation)
            words[word].append((pronunciation, None))
        new_phones = phones - self.dictionary.phones
        if new_phones:
            print("ERROR can't save because of new phones: {}".format(new_phones))
            return
        self.saveDictionary.emit(words)

    def create_pronunciation(self, word):
        if self.dictionary is None:
            return
        if not word:
            return
        pronunciation = None
        if self.g2p_model is not None and not G2P_DISABLED:
            gen = Generator(self.g2p_model, [word])
            results = gen.generate()
            pronunciation = results[word]
            self.dictionary.words[word].append((tuple(pronunciation.split(' ')), 1))
        for i in range(self.dictionary_widget.rowCount()):
            row_text = self.dictionary_widget.item(i, 0).text()
            if not row_text:
                continue
            if row_text < word:
                continue
            self.dictionary_widget.insertRow(i)
            self.dictionary_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(word))
            if pronunciation is not None:
                self.dictionary_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(pronunciation))
            self.dictionary_widget.scrollToItem(self.dictionary_widget.item(i, 0))
            self.dictionary_widget.selectRow(i)
            break

    def look_up_word(self, word):
        if self.dictionary is None:
            return
        if not word:
            return
        for i in range(self.dictionary_widget.rowCount()):
            if self.dictionary_widget.item(i, 0).text() == word:
                self.dictionary_widget.scrollToItem(self.dictionary_widget.item(i, 0))
                self.dictionary_widget.selectRow(i)
                break
