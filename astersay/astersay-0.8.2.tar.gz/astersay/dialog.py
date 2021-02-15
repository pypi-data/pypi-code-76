#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
"""
Функционал для обработки моделей диалогов.
"""
import json
import logging
import re
import subprocess
import wave
from collections import OrderedDict
from gettext import gettext as _
from os.path import splitext, basename
from tempfile import NamedTemporaryFile
from time import time, sleep
from threading import Thread

from astersay.exceptions import AgiError, AgiSigpipeError

logger = logging.getLogger(__name__)
log_debug = logger.debug
log_info = logger.info
log_warning = logger.warning
log_error = logger.error


class TextBuffer(list):

    def __init__(self, key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key
        # Список индексов зафиксированных текстов.
        self.fixed = []

    def get_text(self, mode=1):
        """
        Возвращает текст буфера в режимах:
        1 - финальный, 2 - промежуточный, 3 - весь, 4 - весь с разметкой.
        """
        fixed = self.fixed
        if mode == 1:
            L = [x for i, x in enumerate(self) if x and i in fixed]
        elif mode == 2:
            L = [x for i, x in enumerate(self) if x and i not in fixed]
        elif mode == 3:
            L = [x for x in self if x]
        else:
            L = ['%s: %s' % (i + 1, x) for i, x in enumerate(self) if x]
        return '\n'.join(L)


def _make_say_params(saydata, variables):
    """Возвращает готовые аргументы для метода say()."""
    params = {'text': '', 'escape_digits': '', 'voice': ''}

    if 'voice' in saydata:
        params['voice'] = saydata['voice'] % variables
    elif 'file' in saydata:
        params['voice'] = splitext(saydata['file'])[0] % variables
    else:
        params['text'] = saydata['text'] % variables

    if 'escape_digits' in saydata:
        escape_digits = saydata['escape_digits']
        if not isinstance(escape_digits, str):
            escape_digits = ''.join(map(str, escape_digits))
        params['escape_digits'] = escape_digits

    if 'nonblocking' in saydata:
        params['nonblocking'] = bool(saydata['nonblocking'])

    return params


def _make_pause(data, key):
    try:
        pause = float(data.get(key, 0))
    except ValueError:
        pause = 0
    if pause:
        log_debug(_('Основной поток приостановлен. Пауза %s секунд.'), pause)
        sleep(pause)
        log_debug(_('Основной поток продолжен.'))
    return pause


def _prepare_answer(answer, export_name, script, variables, source=None):
    export_name_source = export_name + '_source'
    if source is True:
        variables[export_name_source] = answer
    elif source is not None:
        variables[export_name_source] = source

    booleanize = script.get('booleanize')
    convert = script.get('convert')
    if booleanize:
        if booleanize.get('to_lowercase', True):
            answer = answer.lower()
        answer = bool(answer in booleanize['true_list'])
        text_true = booleanize.get('text_true') or _('Да')
        text_false = booleanize.get('text_false') or _('Нет')
        export_name_text = (
            booleanize.get('export_name_text') or
            export_name + '_text'
        )
        variables[export_name_text] = text_true if answer else text_false
    elif convert:
        variables[export_name + '_convert_from'] = answer
        if convert.get('to_lowercase', True):
            answer = answer.lower()
        default = convert.get('default')
        if default is None:
            default = answer
        answer = convert['values'].get(answer, default)
        labels = convert.get('labels')
        if labels and answer in labels:
            variables[export_name + '_label'] = labels[answer]
        names = convert.get('names')
        if names and answer in names:
            variables[export_name + '_name'] = labels[answer]
        texts = convert.get('texts')
        if texts and answer in texts:
            variables[export_name + '_text'] = labels[answer]
    # Устанавливаем изменённый текст ответа в главную переменную.
    variables[export_name] = answer


class Dialog:
    """Диалог робота с позвонившим на номер абонентом."""
    is_closed = False
    # Значение меняется экземпляром распознавателя в процессе считывания стрима.
    stream_size = 0
    # Значение меняется каждый раз перед вызовом парсеров.
    partials_begin = 0
    # Заполнен в момент воспроизведения голоса.
    _voice = None
    _voice_duration = 0
    _voice_nonblocking = False

    def __init__(self, agi, settings, stream):
        self.agi = agi
        self.settings = settings
        self.stream = stream

        self.synthesizer = settings.get_synthesizer()
        self.recognizer = settings.get_recognizer()
        if hasattr(self.recognizer, 'token_manager'):
            self.recognizer.token_manager.update_token()
        self.morphology_processor = settings.get_morphology_processor()
        self.text_buffers = OrderedDict()
        # Словарь для экспортируемых после завершения в Asterisk переменных.
        self.export = OrderedDict()

    def make_text_buffer(self, key=None):
        if not key:
            key = len(self.text_buffers)
        text_buffer = TextBuffer(key)
        self.text_buffers[text_buffer.key] = text_buffer
        log_debug(_('Новый текстовый буфер: %s'), key)
        return key

    def get_last_text_buffer(self):
        text_buffers = self.text_buffers
        return text_buffers[list(text_buffers.keys())[-1]]

    def text_to_text_buffer(self, text, fixed=False, text_buffer=None):
        if text_buffer is None:
            text_buffer = self.get_last_text_buffer()
        text = text.strip()
        if not text:
            return
        # Первые передварительные результаты не принимаются до заданного
        # ограничения.
        if not fixed:
            recognizer = getattr(self, 'recognizer', None)
            if recognizer and recognizer.partials_counter < self.partials_begin:
                return
        if not text_buffer:
            text_buffer.append(text)
        else:
            text_buffer[-1] = text
        # Для блокировки делаем пустую новую строку, в неё и будет писаться
        # текст в дальнейшем.
        if fixed:
            text_buffer.fixed.append(len(text_buffer) - 1)
            text_buffer.append('')

    def text_from_text_buffer(self, mode=1, text_buffer=None):
        """
        Возвращает текст буфера в режимах:
        1 - финальный, 2 - промежуточный, 3 - весь, 4 - весь с разметкой.
        """
        if text_buffer is None:
            text_buffer = self.get_last_text_buffer()
        return text_buffer.get_text(mode)

    def parse_names(self, mode=1, text_buffer=None):
        """Метод ищет в тексте буфера все имена."""
        # Слова должны быть в оригинальной последовательности.
        text = self.text_from_text_buffer(mode, text_buffer)
        processor = self.morphology_processor
        return processor.parse_names(text), text

    def search_by_buffer(self, regexp, mode=1, text_buffer=None):
        """Метод ищет в тексте буфера по регулярному выражению."""
        text = self.text_from_text_buffer(mode, text_buffer)
        return regexp.search(text), text

    def text_processing(self, name, mode=1, text_buffer=None):
        """
        Метод отправляет текст буфера в подпроцесс обработчика текста и
        возвращает результат его обработки им.
        """
        text = self.text_from_text_buffer(mode, text_buffer)
        if not text:
            return '', text
        text = text.replace('\n', ' ')
        processor = self.settings.get_processor(name)
        procname = basename(processor)
        log_debug('> PROCESSOR %s %r', procname, text)
        res = subprocess.run(
            [processor, text],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # universal_newlines=True,
        )
        if res.returncode:
            result = ''
            log_error(_('Текстовый процессор %r сломан.'), processor)
            log_error('< PROCESSOR %s', res.stderr)
        else:
            result = res.stdout.decode('utf-8').rstrip()
            log_debug('< PROCESSOR %s %r', procname, result)
        return result, text

    def say(self, text: str, voice: str, escape_digits: str, nonblocking=False):
        if not text and not voice:
            log_error(_('Текст и файл голоса отсутствуют.'))
            return

        # Здесь "voice" - это путь к файлу без его расширения.
        if voice:
            log_info(_('Голос робота: %s'), voice)
        else:
            log_info(_('Текст робота: %s'), text)
            try:
                voice = self.synthesizer.make_voice(text)
            except Exception as e:
                log_error(_('Ошибка синтеза речи.'), exc_info=e)
                return

        n = 0
        while self._voice and n < 1000:
            log_warning(_('Другой голос %s ещё не завершён.'), self._voice)
            n += 1
            sleep(0.5)

        if self._voice:
            log_warning(_('Заменяем голос %s на новый.'), self._voice)

        self._voice = voice
        with wave.open(voice + '.wav') as f:
            duration = f.getnframes() / f.getframerate()
            log_debug(_('Продолжительность голоса %s секунд.'), duration)
            self._voice_duration = duration

        if nonblocking:
            log_debug(_('Голос отправляется в неблокирующем режиме.'))
        else:
            log_debug(_('Голос отправляется в блокирующем режиме.'))

        def clear_voice():
            rest = duration
            while rest > 0 and self._voice == voice:
                sleep(0.5)
                rest -= 0.5
            if self._voice == voice:
                self._voice = None
                self._voice_duration = 0
                log_debug(_('Голос %s завершён.'), voice)

        try:
            self.agi.stream_file(voice, escape_digits=escape_digits)
        except AgiSigpipeError:
            self._voice = None
            self._voice_duration = 0
            self.is_closed = True
            log_info(_('Голос не отправлен. Связь разорвана.'))
            return

        thread = Thread(target=clear_voice, daemon=True)
        thread.start()

        self._voice_nonblocking = nonblocking
        if not nonblocking:
            log_debug(_('Останавливаем основной поток на %s секунд.'), duration)
            # Останавливаем основной поток.
            sleep(duration)

    def has_start_recognize(self):
        if self.is_closed:
            return False
        agi = self.agi
        return not agi.is_sighup and not agi.is_hungup

    def start(self):
        if getattr(self, '_recognizer_thread', None):
            raise RuntimeError(_('Другой поток распознавания уже запущен.'))
        if not self.text_buffers:
            raise RuntimeError(_('Начальный текстовый буфер удалён.'))

        def listen():
            # От начала и до конца беседы поток голоса абонента анализируется.
            # Причём, когда объём потока превышает разрешённые 10 мегабайт
            # и парсинг завершается, мы запускаем новый парсинг.
            while self.has_start_recognize():
                log_debug(_('Запуск recognizer.recognize()'))
                self.recognizer.listen(self)
                log_debug(_('Остановка recognizer.recognize()'))
            thread = self._recognizer_thread
            self._recognizer_thread = None
            log_debug(_('Завершён поток распознавания %s.'), thread)

        self.is_closed = False
        log_debug(_('Запуск отдельного потока распознавания.'))
        thread = Thread(target=listen, daemon=True)
        thread.start()
        log_debug(_('Запущен поток распознавания %s.'), thread)
        self._recognizer_thread = thread
        return thread

    def stop(self):
        log_debug(_('Диалог останавливается.'))
        self.is_closed = True
        # Отключаем здесь листенер, чтобы быстрее выйти, а не ждать слова в
        # трубку.
        if hasattr(self.recognizer, 'listener'):
            listener = self.recognizer.listener
            listener.stop()
            log_debug(_('Слушатель выключен.'))
        else:
            log_error(_('Слушатель не был подключен.'))

    def run(self):
        log_info(
            _('Диалог начат: %(agi_callerid)s (%(agi_calleridname)s)'),
            self.agi.params,
        )
        # Делаем самый первый текстовый буфер.
        self.make_text_buffer()
        # Затем запускаем процесс потокового распознавания речи.
        self.start()
        try:
            self.main_script()
        except AgiError as e:
            log_error(_('Ошибка в AGI.'), exc_info=e)
        except Exception as e:
            log_error(_('Ошибка в сценарии диалога.'), exc_info=e)
        self.stop()

        agi = self.agi
        for key, value in self.export.items():
            if key.startswith('_'):
                continue
            value = str(value)
            log_debug(
                _('Экспорт %(key)s=%(value)s'), {'key': key, 'value': value})
            agi.set(key, value)
        filename = self.settings.export_dialog(
            self.agi.params, self.export, self.text_buffers
        )
        if filename:
            log_info(_('Диалог экспортирован в файл %s'), filename)

        for key, text_buffer in self.text_buffers.items():
            for line in text_buffer.get_text(4).split('\n'):
                log_debug(_('Текст буфера %(key)s: %(line)s'),
                          {'key': key, 'line': line})

        log_info(_('Диалог завершён.'))

    def main_script(self):
        started = time()
        scheme = self.settings.dialog_scheme
        constants = scheme.get('constants', {})
        self.export = variables = OrderedDict()
        variables.update(constants)
        # Словарь скриптов.
        scripts = scheme.get('scripts', {})
        # Программа главного скрипта.
        program = OrderedDict([(p['name'], p) for p in scheme['main_script']])
        index = tuple(program.keys())
        process = program[index[0]]
        log_debug(_('Главный скрипт начат.'))
        while process and not self.is_closed:
            name = process['name']
            script = scripts.get(name)
            if not script:
                break
            scrypt_type = script['type']
            # Здесь должна возникать ошибка AttributeError для сломанных схем.
            method = getattr(self, '_script_%s' % scrypt_type)
            log_debug('  SCRIPT %s', name.upper())
            if 'partials_begin' in script:
                try:
                    self.partials_begin = int(script['partials_begin'])
                except ValueError:
                    self.partials_begin = 0
            result, speech = method(script, variables)
            log_debug('  RESULT %r', result)
            log_debug('  SPEECH %r', speech)

            # Запускаем плагин при его наличии.
            plugin_name = process.get('plugin')
            if plugin_name:
                plugin = self.settings.get_plugin(plugin_name)
                log_debug('> PLUGIN %s', plugin)
                plugin_data = {
                    'agi_params': self.agi.params,
                    'work_dir': self.settings.work_dir,
                    'speech': speech,
                    'variables': variables,
                    'text_buffers': self.text_buffers,
                }
                if isinstance(result, (str, list, tuple, int, float)):
                    plugin_data['result'] = result
                else:
                    plugin_data['result'] = str(result)
                tempfile = NamedTemporaryFile(mode='w', suffix='.json')
                tempfile_name = tempfile.name
                json.dump(plugin_data, tempfile)
                tempfile.flush()
                log_debug('JSONFILE %s', tempfile_name)
                res = subprocess.run(
                    [plugin, tempfile_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                )
                if res.returncode:
                    log_error(_('Плагин %r сломан.'), plugin)
                    log_error('< PLUGIN %s', res.stderr)
                else:
                    log_debug('< PLUGIN %s', res.stdout)
                    # Плагин может установить свои переменные в процессе своей
                    # работы.
                    plugin_data = json.load(open(tempfile_name))
                    variables.update(plugin_data['variables'])
                tempfile.close()

            # Устанавливаем следующий процесс.
            success = process.get('success')
            if isinstance(success, dict):
                success = success.get(result)
            # Динамическое определение следующего скрипта может определяться
            # из ранее установленных переменных.
            if success and '%(' in success:
                success %= variables
            fail = process.get('fail')
            log_debug(' SUCCESS %s', success)
            log_debug('    FAIL %s', fail)
            if process.get('finish', False):
                log_debug('  FINISH')
                process = None
            elif result and success in program:
                process = program[success]
            elif not result and fail in program:
                process = program[fail]
            else:
                try:
                    process = program.get(index[index.index(name) + 1])
                except IndexError:
                    process = None
            log_debug('    NEXT %s', process)

            # Восстанавливаем константы. Это проще, чем городить лес кода.
            variables.update(constants)

        finished = time()
        variables['_time_start_'] = started
        variables['_time_finish_'] = finished
        variables['_time_duration_'] = finished - started

        log_debug(_('Главный скрипт завершён.'))

    def _agi_execute(self, commands, key):
        try:
            command = commands.get(key, [])
            assert isinstance(command, list)
        except AssertionError:
            command = []
        if command:
            # Обрабатываем аргументы, преобразовывая шаблонные переменные.
            kw = self.agi.params.copy()
            kw.update(self.export)
            for i, val in enumerate(command):
                # Пропускаем первый аргумент и все не строковые аргументы.
                if i and isinstance(val, str):
                    command[i] = val.format(**kw)
            log_debug(_('Выполняется команда AGI: %s'), command)
            self.agi.execute(*command)
            log_debug(_('Команда выполнена.'))
        return command

    def _agi_stop_playback(self, saydata=None):
        log_debug('_agi_stop_playback')
        if not saydata or not isinstance(saydata, dict):
            log_debug(_('Нечего опрерывать, saydata=%s'), saydata)
            return
        if not saydata.get('nonblocking', False):
            log_debug(_('Нечего прерывать, был задан блокирующий режим.'))
            return

        stop_voice = splitext(self.settings.get_stop_file())[0]
        if not stop_voice:
            log_debug(_('Стоп-голоса для прерывания нет.'))
            return
        if not self._voice:
            log_debug(_('Нечего прерывать, голос уже закончился.'))
            return
        try:
            self.agi.stream_file(stop_voice)
        except AgiSigpipeError:
            self.is_closed = True
            log_info(_('Стоп-голос не отправлен. Связь разорвана.'))
            return
        except Exception as e:
            self.is_closed = True
            raise e
        self._voice = None
        self._voice_duration = 0
        log_debug(_('Прерывание воспроизведения выполнено.'))

    def _script_parse_names(self, script, variables):
        assert script['type'] == 'parse_names'

        assert 'export_name' in script
        export_name = script['export_name']
        assert export_name and isinstance(export_name, str)

        pauses = script.get('pauses', {})
        _make_pause(pauses, 'before')

        commands = script.get('commands', {})
        self._agi_execute(commands, 'before')

        mode = int(script.get('mode_buffer', 1))
        assert mode in (1, 2, 3)
        if script.get('new_buffer', False):
            self.make_text_buffer()

        saydata = script.get('say_start')
        if saydata:
            _make_pause(pauses, 'before_say_start')
            self._agi_execute(commands, 'before_say_start')
            self.say(**_make_say_params(saydata, variables))
            _make_pause(pauses, 'after_say_start')
            self._agi_execute(commands, 'after_say_start')

        attempts = script.get('attempts') or {}
        attempts_count = abs(int(attempts.get('count', 0))) or 1
        attempts_iter_time = float(attempts.get('iter_time', 0))
        attempts_iter_pause = float(attempts.get('iter_pause', 0)) or 1.0

        func = self.parse_names
        names, speech = func(mode=mode)
        if names:
            log_debug(_('Первая попытка успешна. Имена: %s'), names)
        else:
            log_debug(_('Первая попытка провалилась. Имена: %s'), names)
        for attempt in range(attempts_count):
            _iter_time = attempts_iter_time
            if attempt == 0:
                # В блокирующем режиме голоса его длина уже будет сброшена в 0.
                _iter_time += self._voice_duration
            second = 0
            while not names and second < _iter_time:
                log_debug(_('Ответа пока нет, ждём %d-ю секунду.'), second)
                second += attempts_iter_pause
                sleep(attempts_iter_pause)
                names, speech = func(mode=mode)
                if self.is_closed:
                    log_debug(_('Диалог завершился до приёма данных.'))
                    break
            if names:
                length_names = int(script.get('length_names', 2))
                answer = ' '.join(names[:length_names])
                log_debug(_('Ответ: %r'), answer)
                _prepare_answer(
                    answer=answer, source=answer, export_name=export_name,
                    script=script, variables=variables)

                self._agi_stop_playback(script.get('say_start'))

                saydata = script.get('say_success')
                if saydata:
                    _make_pause(pauses, 'before_say_success')
                    self._agi_execute(commands, 'before_say_success')
                    self.say(**_make_say_params(saydata, variables))
                    _make_pause(pauses, 'after_say_success')
                    self._agi_execute(commands, 'after_say_success')
                break
            elif attempt < attempts_count - 1:
                if attempts.get('new_buffer', False):
                    self.make_text_buffer()
                saydata = attempts.get('say')
                if saydata:
                    _make_pause(pauses, 'before_say_attempt')
                    self._agi_execute(commands, 'before_say_attempt')
                    self.say(**_make_say_params(saydata, variables))
                    _make_pause(pauses, 'after_say_attempt')
                    self._agi_execute(commands, 'after_say_attempt')
        if not names:
            log_debug(_('Ответа нет.'))
            saydata = script.get('say_fail')
            if saydata:
                _make_pause(pauses, 'before_say_fail')
                self._agi_execute(commands, 'before_say_fail')
                self.say(**_make_say_params(saydata, variables))
                _make_pause(pauses, 'after_say_fail')
                self._agi_execute(commands, 'after_say_fail')

        _make_pause(pauses, 'after')
        self._agi_execute(commands, 'after')
        return names, speech

    def _script_search_by_buffer(self, script, variables):
        assert script['type'] == 'search_by_buffer'

        assert 'export_name' in script
        export_name = script['export_name']
        assert export_name and isinstance(export_name, str)

        assert 'regexp' in script
        regexp = script['regexp']
        assert regexp and isinstance(regexp, dict)

        assert 'pattern' in regexp
        pattern = regexp['pattern']
        assert pattern and isinstance(pattern, str)

        pauses = script.get('pauses', {})
        _make_pause(pauses, 'before')

        commands = script.get('commands', {})
        self._agi_execute(commands, 'before')

        mode = int(script.get('mode_buffer', 1))
        assert mode in (1, 2, 3)
        if script.get('new_buffer', False):
            self.make_text_buffer()

        saydata = script.get('say_start')
        if saydata:
            _make_pause(pauses, 'before_say_start')
            self._agi_execute(commands, 'before_say_start')
            self.say(**_make_say_params(saydata, variables))
            _make_pause(pauses, 'after_say_start')
            self._agi_execute(commands, 'after_say_start')

        attempts = script.get('attempts') or {}
        attempts_count = abs(int(attempts.get('count', 0))) or 1
        attempts_iter_time = float(attempts.get('iter_time', 0))
        attempts_iter_pause = float(attempts.get('iter_pause', 0)) or 1.0

        func = self.search_by_buffer
        flag = re.UNICODE
        if regexp.get('ignorecase', False):
            flag |= re.IGNORECASE
        pattern = re.compile(pattern, flag)
        match, speech = func(pattern, mode=mode)
        answer = None
        for attempt in range(attempts_count):
            _iter_time = attempts_iter_time
            if attempt == 0:
                # В блокирующем режиме голоса его длина уже будет сброшена в 0.
                _iter_time += self._voice_duration
            second = 0
            while not match and second < _iter_time:
                log_debug(_('Ответа пока нет, ждём %d-ю секунду.'), second)
                second += attempts_iter_pause
                sleep(attempts_iter_pause)
                match, speech = func(pattern, mode=mode)
                if self.is_closed:
                    log_debug(_('Диалог завершился до приёма данных.'))
                    break
            if match:
                answer = match.group()
                log_debug(_('Ответ: %r'), answer)
                _prepare_answer(
                    answer=answer, source=answer, export_name=export_name,
                    script=script, variables=variables)

                self._agi_stop_playback(script.get('say_start'))

                saydata = script.get('say_success')
                if saydata:
                    _make_pause(pauses, 'before_say_success')
                    self._agi_execute(commands, 'before_say_success')
                    self.say(**_make_say_params(saydata, variables))
                    _make_pause(pauses, 'after_say_success')
                    self._agi_execute(commands, 'after_say_success')
                break
            elif attempt < attempts_count - 1:
                if attempts.get('new_buffer', False):
                    self.make_text_buffer()
                saydata = attempts.get('say')
                if saydata:
                    _make_pause(pauses, 'before_say_attempt')
                    self._agi_execute(commands, 'before_say_attempt')
                    self.say(**_make_say_params(saydata, variables))
                    _make_pause(pauses, 'after_say_attempt')
                    self._agi_execute(commands, 'after_say_attempt')
        if not match:
            log_debug(_('Ответа нет.'))
            saydata = script.get('say_fail')
            if saydata:
                _make_pause(pauses, 'before_say_fail')
                self._agi_execute(commands, 'before_say_fail')
                self.say(**_make_say_params(saydata, variables))
                _make_pause(pauses, 'after_say_fail')
                self._agi_execute(commands, 'after_say_fail')

        _make_pause(pauses, 'after')
        self._agi_execute(commands, 'after')
        return answer, speech

    def _script_text_processing(self, script, variables):
        assert script['type'] == 'text_processing'

        assert 'export_name' in script
        export_name = script['export_name']
        assert export_name and isinstance(export_name, str)

        assert 'file' in script
        filename = script['file']
        assert filename and isinstance(filename, str)

        pauses = script.get('pauses', {})
        _make_pause(pauses, 'before')

        commands = script.get('commands', {})
        self._agi_execute(commands, 'before')

        mode = int(script.get('mode_buffer', 1))
        assert mode in (1, 2, 3)
        if script.get('new_buffer', False):
            self.make_text_buffer()

        saydata = script.get('say_start')
        if saydata:
            _make_pause(pauses, 'before_say_start')
            self._agi_execute(commands, 'before_say_start')
            self.say(**_make_say_params(saydata, variables))
            _make_pause(pauses, 'after_say_start')
            self._agi_execute(commands, 'after_say_start')

        attempts = script.get('attempts') or {}
        attempts_count = abs(int(attempts.get('count', 0))) or 1
        attempts_iter_time = float(attempts.get('iter_time', 0))
        attempts_iter_pause = float(attempts.get('iter_pause', 0)) or 1.0

        func = self.text_processing
        response, speech = func(filename, mode=mode)
        if response:
            log_debug(_('Первая попытка успешна. Ответ: %s'), response)
        else:
            log_debug(_('Первая попытка провалилась. Ответа нет.'))
        for attempt in range(attempts_count):
            _iter_time = attempts_iter_time
            if attempt == 0:
                # В блокирующем режиме голоса его длина уже будет сброшена в 0.
                _iter_time += self._voice_duration
            second = 0
            while not response and second < _iter_time:
                log_debug(_('Ответа пока нет, ждём %d-ю секунду.'), second)
                second += attempts_iter_pause
                sleep(attempts_iter_pause)
                response, speech = func(filename, mode=mode)
                if self.is_closed:
                    log_debug(_('Диалог завершился до приёма данных.'))
                    break
            if response:
                answer = response
                log_debug(_('Ответ: %r'), answer)
                _prepare_answer(
                    answer=answer, source=speech, export_name=export_name,
                    script=script, variables=variables)

                self._agi_stop_playback(script.get('say_start'))

                saydata = script.get('say_success')
                if saydata:
                    _make_pause(pauses, 'before_say_success')
                    self._agi_execute(commands, 'before_say_success')
                    self.say(**_make_say_params(saydata, variables))
                    _make_pause(pauses, 'after_say_success')
                    self._agi_execute(commands, 'after_say_success')
                break
            elif attempt < attempts_count - 1:
                if attempts.get('new_buffer', False):
                    self.make_text_buffer()
                saydata = attempts.get('say')
                if saydata:
                    _make_pause(pauses, 'before_say_attempt')
                    self._agi_execute(commands, 'before_say_attempt')
                    self.say(**_make_say_params(saydata, variables))
                    _make_pause(pauses, 'after_say_attempt')
                    self._agi_execute(commands, 'after_say_attempt')
        if not response:
            log_debug(_('Ответа нет.'))
            saydata = script.get('say_fail')
            if saydata:
                _make_pause(pauses, 'before_say_fail')
                self._agi_execute(commands, 'before_say_fail')
                self.say(**_make_say_params(saydata, variables))
                _make_pause(pauses, 'after_say_fail')
                self._agi_execute(commands, 'after_say_fail')

        _make_pause(pauses, 'after')
        self._agi_execute(commands, 'after')
        return response, speech

    def _script_simple_say(self, script, variables):
        assert script['type'] == 'simple_say'

        if 'export_name' in script and 'export_value' in script:
            variables[script['export_name']] = str(script['export_value'])

        pauses = script.get('pauses', {})
        _make_pause(pauses, 'before')

        commands = script.get('commands', {})
        self._agi_execute(commands, 'before')

        mode = int(script.get('mode_buffer', 1))
        assert mode in (1, 2)
        if script.get('new_buffer', False):
            self.make_text_buffer()

        saydata = script.get('say_start')
        if saydata:
            _make_pause(pauses, 'before_say_start')
            self._agi_execute(commands, 'before_say_start')
            self.say(**_make_say_params(saydata, variables))
            _make_pause(pauses, 'after_say_start')
            self._agi_execute(commands, 'after_say_start')

        _make_pause(pauses, 'after')
        self._agi_execute(commands, 'after')

        speech = self.text_from_text_buffer()
        return True, speech
