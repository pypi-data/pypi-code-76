#!/usr/bin/python3
# code is based on https://forum-raspberrypi.de/forum/thread/19020-newtron-radio-aufloesungsunabhaengiges-tron-radio/?postID=395720#post395720
# pylint: disable=no-member,c-extension-no-member
# coding=utf-8
# v3.2 rev.01
from random import randint
import json
from operator import itemgetter
from select import select
from urllib import request, error
import datetime
import sys
import os
import pwd
import re
import shutil
import socket
import subprocess
from mpd import MPDClient, CommandError, ConnectionError
import pygame
import svg

##### Pfade und Environment ################################
# Umgebungsvariablen für den Konsolenmodus

if not os.getenv('SDL_FBDEV'):
    os.environ["SDL_FBDEV"] = "/dev/fb1"
if not os.getenv('SDL_MOUSEDEV'):
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
if not os.getenv('SDL_MOUSEDRV'):
    os.environ["SDL_MOUSEDRV"] = "TSLIB"

if not os.getenv("TSLIB_FBDEVICE"):
    os.environ["TSLIB_FBDEVICE"] = os.getenv('SDL_FBDEV')
if not os.getenv("TSLIB_TSDEVICE"):
    os.environ["TSLIB_TSDEVICE"] = os.getenv('SDL_MOUSEDEV')

# Pfad zur Konfigurationsdatei
HOME = pwd.getpwuid(os.getuid()).pw_dir
CONFIGFILE = os.path.join(HOME, ".newtron-radio.conf")
config = {}

# Pfad zum Programmverzeichnis
SCRIPTPATH = os.path.dirname(__file__)

##### Bildschirm ###########################################
# Bildschirmgrösse (fbcon)
# nur setzen, wenn die Automatik nicht geht!
# WIDTH=320
# HEIGHT=240

# Bildschimgrösse (für X-Display)
SHOWCURSOR = True
config['fullscreen'] = False
# X-Aufloesung, wenn FULLSCREEN = False
X_WIDTH = 320
X_HEIGHT = 240

###### W-LAN Device ########################################
# Welches device soll für die Empfangsstärkenanzeige
# verwendet werden.
WLAN_DEVICE = 'wlan0'

###### Playlistenmanagement ################################
# Vollständiger Pfad zur mpd.conf
MPD_CONFIG = '/etc/mpd.conf'
DEFAULTPLAYLIST = 'Radio BOB!'  # eine Playlist aus dem 'playlist_directory'
SORT_PLAYLISTS = True

# Name der Datei in die die aktuelle Playliste
# gespeichert werden soll (MPC.save())
SAVE_FILENAME = 'saved_playlist'

##### Diverse weitere Konfiguration ########################

# max. Framerate
FPS = 5

# Audioausgabevariablen
# Der hier gesetzte Wert von oldvol wird nur verwendet,
# wenn beim Start die Lautstärkeinfo vom mpd nicht geholt
# werden kann
OLDVOL = 80

# Einstellung fürs Eventhandling
MINUTES = 0

###### Skin Konfiguration ##################################
# Dicts, die die Konfiguration enthalten
skincfg = {}
colors = {}
fontsize = {}
fonts = {}
# Farben für die Datei-/Playlistenanzeigen
colors['pls'] = (0, 224, 224)  # Farbe für Playlisten im music-dir
colors['dir'] = (224, 144, 64)  # Farbe für Verzeichnisse
colors['mp3'] = (0, 224, 0)  # Farbe für Dateien
colors['rad'] = (0, 150, 200)  # Farbe für playlisten im playlists-dir
colors['err'] = (255, 0, 0)  # Farbe für Playlistauswahlfehler
colors['ple'] = (192, 192, 192)  # Farbe für Inhalt der Playliste
###### Touchbutton + Skin Dateien ##########################
MSG_FRAME = "Status"
BTN_LIST = ["Stop", "Pause", "Up", "Mute", "Prev", "Next", "Down", "Next_Page", "Cloud", "Color",
            "Exit", "Quit", "Poweroff", "Reboot", "Refresh", "Play", "Unmute", "Empty", "Plug",
            "Enter", "Updir", "Prev_Page", "Trash", "Save", "Shuffle", "Config", "Plus", "Minus"]
WLAN_LIST = ["wlan000", "wlan025", "wlan050", "wlan075", "wlan100"]
CHK_LIST = ["Checkbox", "Checkbox_Sel", "Checkbox_down", "Checkbox_up"]
SELECTION_FRAME = "Selection"
SELECT_PL = "Playlist_msg"
# Buffer für die Hintergründe der Oberfläche
bg_buf = {}


# -------- Funktions- und Klassendefinitionen --------
def pi_power_off():
    run_command('sudo poweroff', shell=True)


def pi_restart():
    run_command('sudo reboot', shell=True)


def mpd_restart():
    print('restart mpd service')
    subprocess.call("service --user mpd restart", shell=True)


def run_command(cmd, shell):
    print('The executed is {}.'.format(cmd))
    exit(0)
    # subprocess.call(cmd, shell)


def disp_init():  # (halbautomatische) Erkennung des Displays
    disp_found = False
    x_disp = os.getenv('DISPLAY')
    if x_disp:
        print('using X-Display ' + os.getenv('DISPLAY'))
        try:
            os.putenv('SDL_VIDEODRIVER', 'x11')
            pygame.display.init()
            pygame.display.set_caption('NewTRON-Radio v3.x', 'NewTRON-Radio')
            if SHOWCURSOR:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_cursor((8, 8), (4, 4),
                                        (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
            if config['fullscreen']:
                info = pygame.display.Info()
                width = info.current_w
                height = info.current_h
            else:
                width = X_WIDTH
                height = X_HEIGHT
            disp_found = True
        except pygame.error as err:
            print(err)
            print('Problem with X11-Driver!')
            pygame.display.quit()
    elif os.getenv('SDL_VIDEODRIVER'):
        print('using ' + os.getenv('SDL_VIDEODRIVER') + ' from SDL_VIDEODRIVER env var.')
        try:
            pygame.display.init()
            pygame.mouse.set_visible(False)
            disp_found = True
        except pygame.error as err:
            print(err)
            print('Driver ' + os.getenv('SDL_VIDEODRIVER') + ' from SDL_VIDEODRIVER env var failed!')
            print('Is your SDL_VIDEODRIVER entry correct?')
            print('Also check:')
            print('SDL_FBDEV = ' + os.getenv('SDL_FBDEV'))
            print('SDL_MOUSEDEV = ' + os.getenv('SDL_MOUSEDEV'))
            print('SDL_MOUSEDRV = ' + os.getenv('SDL_MOUSEDRV'))
            print('Are theese correct? Set them in Line 26ff.')
            pygame.display.quit()
    else:
        print('trying fbcon')
        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        try:
            pygame.display.init()
            pygame.mouse.set_visible(False)
            print('using ' + pygame.display.get_driver())
            disp_found = True
        except pygame.error as err:
            print(err)
            print('Driver fbcon failed!')
            print('Is libts/libts-bin installed?')
            print('Also check:')
            print('SDL_FBDEV = ' + os.getenv('SDL_FBDEV'))
            print('SDL_MOUSEDEV = ' + os.getenv('SDL_MOUSEDEV'))
            print('SDL_MOUSEDRV = ' + os.getenv('SDL_MOUSEDRV'))
            print('Are theese correct? Set them in Line 26ff.')
            pygame.display.quit()

    if disp_found:
        try:
            width or height  # check if WIDTH or HEIGHT are defined
        except UnboundLocalError:
            width = pygame.display.Info().current_w
            height = pygame.display.Info().current_h
    else:
        raise Exception('No suitable video driver found!')
    return width, height


def reboot():
    LCD.fill(colors['bg'])
    reboot_label = fonts['big'].render("Reboot...", 1, (colors['font']))
    LCD.blit(reboot_label, reboot_label.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    pi_restart();


def poweroff():
    LCD.fill(colors['bg'])
    poweroff_label = fonts['big'].render("Shutdown...", 1, (colors['font']))
    LCD.blit(poweroff_label, poweroff_label.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    pi_power_off()


def waiting(msg_text1='please wait...', msg_text2=None):
    LCD.fill(colors['bg'])
    text_label = fonts['big'].render(msg_text1, 1, (colors['font']))
    if msg_text2 is None:
        LCD.blit(text_label, text_label.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    else:
        LCD.blit(text_label,
                 text_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - text_label.get_height() // 2)))
        text_label = fonts['big'].render(msg_text2, 1, (colors['font']))
        LCD.blit(text_label,
                 text_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + text_label.get_height() // 2)))
    pygame.display.flip()


def draw_text(win, text, font, color, align='topleft', pos=(0, 0)):
    label = font.render(text, 1, color)
    label_pos = label.get_rect()
    if align == 'centerx':
        label_pos.centerx = win.get_rect().centerx
    if align == 'topright':
        label_pos.topright = win.get_rect().topright
    if skincfg['dropshadow']:
        label_shadow = font.render(text, 1, colors['shadow'])
        win.blit(label_shadow, (label_pos[0] + pos[0] + 1, label_pos[1] + pos[1] + 1))
    win.blit(label, (label_pos[0] + pos[0], label_pos[1] + pos[1]))


def mpd_connect(client):
    try:
        client.connect("localhost", "6600")
        print("connected using unix socket...")
    except ConnectionError as err:
        if 'Already connected' in str(err):
            print('trying to reconnect...')
            # Das folgende disconnect() schlägt fehl (broken pipe)
            # obwohl von python_mpd2 'Already connected' gemeldet wurde
            # Aber erst ein auf das disconnect() folgender connect()
            # ist erfolgreich...
            try:
                client.disconnect()
                pygame.time.wait(1500)
                client.connect("/var/run/mpd/socket")
                # mpd_connect(client)
                print("connected using unix socket...")
            except socket.error as err:
                print('Zeile 246:', str(err))
                mpd_connect(client)
    except socket.error as err:
        print('Zeile 249:', str(err))
        # socket.error: [Errno 111] Connection refused
        # socket.error: [Errno 2] No such file or directory
        try:
            # Nötig, um einen 'service mpd restart' zu überstehen
            pygame.time.wait(1500)
            client.connect("localhost", 6600)
            print("connected using localhost:6600")
        except:
            exctype, value = sys.exc_info()[:2]
            print(str(exctype) + ': ' + str(value))
            print("restarting mpd...")
            mpd_restart()
            pygame.time.wait(1500)
            mpd_connect(client)


def getbool(value):
    tval = ['1', 'yes', 'true', 'on']
    fval = ['0', 'no', 'false', 'off']
    if str(value).lower() in tval:
        return True
    if str(value).lower() in fval:
        return False
    raise ValueError('getbool(): wrong value:' + str(value))


def getcolortuple(value):
    rgb = tuple(map(int, value.strip('() ').split(',')))
    if len(rgb) != 3:
        raise ValueError('getcolortuple(): wrong length:' + str(len(rgb)) + ' value:' + str(rgb))
    for item in rgb:
        if not 0 <= item <= 255:
            raise ValueError('getcolortuple(): wrong colorvalue:' + str(item))
    return rgb


def save_config():
    with open(CONFIGFILE, 'w') as cfg:
        cfg.write('owm_key=' + config.setdefault("owm_key", "") + '\n')
        cfg.write('owm_zip=' + config.setdefault("owm_zip", "") + '\n')
        cfg.write('owm_id=' + config.setdefault("owm_id", "") + '\n')
        cfg.write('owm_city=' + config.setdefault("owm_city", "") + '\n')
        cfg.write('owm_coord=' + config.setdefault("owm_coord", "") + '\n')
        cfg.write('skin=' + config.setdefault("skin", "Tron") + '\n')
        cfg.write('screensaver_mode=' + config.setdefault("screensaver_mode", "clock") + '\n')
        cfg.write('screensaver_timer=' + str(config.setdefault("screensaver_timer", 10)) + '\n')
        cfg.write('x_button=' + str(config.setdefault("x_button", True)) + '\n')
        cfg.write('plus_button=' + str(config.setdefault("plus_button", True)) + '\n')
        cfg.write('fullscreen=' + str(config.setdefault("fullscreen", False)) + '\n')


def read_config():
    if os.path.isfile(CONFIGFILE):
        with open(CONFIGFILE) as cfg:
            for line in cfg:
                if len(line.split('=')) > 1:
                    key = line.strip().split('=')[0].lower().rstrip()
                    value = line.strip().split('=')[1].split('#')[0].strip()
                    if value:
                        value = value.strip("\'\"")
                        if key == 'screensaver_mode':
                            config['screensaver_mode'] = value.lower()
                        elif key == 'screensaver_timer':
                            config['screensaver_timer'] = int(value)
                        elif key == 'x_button':
                            config['x_button'] = getbool(value)
                        elif key == 'plus_button':
                            config['plus_button'] = getbool(value)
                        elif key == 'fullscreen':
                            config['fullscreen'] = getbool(value)
                        else:
                            for item in ['skin', 'owm_key', 'owm_zip', 'owm_id', 'owm_city', 'owm_coord']:
                                if key == item:
                                    config[item] = value
    else:
        print('No ConfigFile found, using defaults')
        save_config()


def show_config():
    draw_text(MSG_WIN, 'NewTron-Radio Settings', fonts['std'], colors['status'], align='centerx')
    if config['x_button']:
        CHK_WIN[0].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[0].blit(btn["Checkbox"], (0, 0))
    draw_text(CHK_WIN[0], ' X-Button', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), 0))
    if config['plus_button']:
        CHK_WIN[1].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[1].blit(btn["Checkbox"], (0, 0))
    draw_text(CHK_WIN[1], ' Plus-Button', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), 0))
    if config['fullscreen']:
        CHK_WIN[2].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[2].blit(btn["Checkbox"], (0, 0))
    draw_text(MSG_WIN, ' Fullscreen (Save & Restart required)', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), CHK_WIN[2].get_offset()[1]))
    draw_text(LCD, 'Skin-Name: ' + config['skin'], fonts['std'], colors['font'], align='centerx',
              pos=(0, CHK_WIN[4].get_abs_offset()[1]))
    draw_text(STATUS_WIN, 'Screensaver: ' + config['screensaver_mode'] + \
              ' (' + str(config['screensaver_timer']) + 'min)', fonts['std'],
              colors['status'], align='centerx')


def set_config(idx=None):
    if idx == 0:
        config['x_button'] = config['x_button'] ^ True
    if idx == 1:
        config['plus_button'] = config['plus_button'] ^ True
    if idx in (2, 3):
        config['fullscreen'] = config['fullscreen'] ^ True
    if idx in (4, 5):
        switch_skin()
    if idx == 9:
        ss_mode = ['clock', 'weather', 'black', 'off']
        ss_idx = ss_mode.index(config['screensaver_mode']) + 1
        if ss_idx >= len(ss_mode):
            ss_idx = 0
        config['screensaver_mode'] = (ss_mode[ss_idx])
    return True


def read_skin_config(skin_path: str):
    # Default-Farben
    colors['font'] = (0, 150, 200)
    colors['bg'] = (0, 0, 0)
    colors['weather_bg'] = (0, 0, 48)
    colors['weather_font'] = (0, 150, 200)
    colors['skin'] = (0, 150, 200)
    colors['status'] = (0, 150, 200)
    colors['clock_font'] = (0, 150, 200)
    colors['shadow'] = (32, 32, 32)

    # Default-Fontgrössen, wenn kein Font angegeben wurde
    fontsize['std'] = HEIGHT // 11
    fontsize['big'] = HEIGHT // 8
    fontsize['title'] = HEIGHT // 6
    fontsize['clock'] = HEIGHT // 3

    # Sonstige Skin-Konfiguration
    skincfg['background'] = None
    skincfg['weather_bg'] = None
    skincfg['text_on_top'] = True
    skincfg['dropshadow'] = False

    skin_font = None
    skin_config = os.path.join(skin_path, "skin.cfg")
    if os.path.isfile(skin_config):
        # Setze Default-Fontgrössen, wenn ein Font angegeben wurde
        with open(skin_config) as s_cfg:
            for line in s_cfg:
                if len(line.split('=')) > 1:
                    key = line.strip().split('=')[0].lower().rstrip()
                    value = line.strip().split('=')[1].split('#')[0].strip()
                    if value:
                        if key == 'skin_font':
                            if os.path.isfile(value.strip("\'\"")):
                                skin_font = value.strip("\'\"")
                                fontsize['std'] = HEIGHT // 17
                                fontsize['big'] = HEIGHT // 12
                                fontsize['title'] = HEIGHT // 9
                                fontsize['clock'] = HEIGHT // 3
                        elif key == 'font_color':
                            colors['font'] = getcolortuple(value.upper())
                        elif key == 'background_color':
                            colors['bg'] = getcolortuple(value.upper())
                        elif key == 'weather_background_color':
                            colors['weather_bg'] = getcolortuple(value.upper())
                        elif key == 'weather_font_color':
                            colors['weather_font'] = getcolortuple(value.upper())
                        elif key == 'skin_color':
                            colors['skin'] = getcolortuple(value.upper())
                        elif key == 'status_color':
                            colors['status'] = getcolortuple(value.upper())
                        elif key == 'clock_font_color':
                            colors['clock_font'] = getcolortuple(value.upper())
                        elif key == 'shadow_color':
                            colors['shadow'] = getcolortuple(value.upper())
                        elif key == 'background':
                            if os.path.isfile(os.path.join(skin_path, value.strip("\'\""))):
                                skincfg['background'] = os.path.join(skin_path, value.strip("\'\""))
                        elif key == 'weather_background':
                            if os.path.isfile(os.path.join(skin_path, value.strip("\'\""))):
                                skincfg['weather_bg'] = os.path.join(skin_path, value.strip("\'\""))
                        elif key == 'text_on_top':
                            skincfg['text_on_top'] = getbool(value)
                        elif key == 'dropshadow':
                            skincfg['dropshadow'] = getbool(value)
    else:
        print("No skin.cfg found. trying defaults...")

    # Default Fonts
    fonts['std'] = pygame.font.Font(skin_font, fontsize['std'])
    fonts['big'] = pygame.font.Font(skin_font, fontsize['big'])
    fonts['title'] = pygame.font.Font(skin_font, fontsize['title'])
    fonts['clock'] = pygame.font.Font(skin_font, fontsize['clock'])


class OpenWeatherMap:
    """ Klasse für Openweathermap """

    def __init__(self):
        self.stadt = 'n/a'
        self.temperatur = '-'
        self.luftdruck = '-'
        self.luftfeuchte = '-'
        self.wetterlage = 'na'
        self.heute_min = '-'
        self.heute_max = '-'
        self.morgen_min = '-'
        self.morgen_max = '-'
        self.vorschau = 'na'
        self.owm_key = None
        self.owm_loc = None

    def get_config(self):
        """ hole OpenWeatherMap Ortsdaten und Key """
        # Falls existent, hole die Daten aus dem config-dict
        if 'owm_key' in config:
            self.owm_key = config['owm_key']
        if 'owm_zip' in config:
            self.owm_loc = 'zip=' + config['owm_zip']
        elif 'owm_id' in config:
            self.owm_loc = 'id=' + config['owm_id']
        elif 'owm_city' in config:
            self.owm_loc = 'q=' + config['owm.city']
        elif 'owm_coord' in config:
            self.owm_loc = config['owm_coord']
        # Falls OWM_ Umgebungsvariablen existieren, nehme diese
        if os.getenv('OWM_KEY'):
            self.owm_key = os.getenv('OWM_KEY')
        if os.getenv('OWM_ZIP'):
            self.owm_loc = 'zip=' + os.getenv('OWM_ZIP')
        elif os.getenv('OWM_ID'):
            self.owm_loc = 'id=' + os.getenv('OWM_ID')
        elif os.getenv('OWM_CITY'):
            self.owm_loc = 'q=' + os.getenv('OWM_CITY')
        elif os.getenv('OWM_COORD'):
            self.owm_loc = os.getenv('OWM_COORD')

    def get_data(self):
        """ Hole Wetterdaten """
        if not self.owm_key:
            waiting('Please get an API-Key from', 'openweathermap.org/appid')
            pygame.time.wait(5000)
            pygame.event.get()  # werfe aufgelaufene Events weg
        if not self.owm_loc:
            waiting('Please set a location', 'for openweathermap')
            pygame.time.wait(5000)
            pygame.event.get()  # werfe aufgelaufene Events weg

        openweather_base = 'http://api.openweathermap.org/data/2.5/'
        try:
            weather = request.urlopen(openweather_base + 'weather?' + \
                                      self.owm_loc + '&units=metric&lang=de&mode=json&APPID=' + self.owm_key)
            weather_data = json.loads(weather.read().decode('utf-8'))
            self.stadt = weather_data['name']
            #  -273.15 if units!=metric
            self.temperatur = str(int(round(weather_data['main']['temp'], 0)))
            self.luftdruck = str(int(weather_data['main']['pressure']))
            self.luftfeuchte = str(int(weather_data['main']['humidity']))
            self.wetterlage = weather_data['weather'][0]['icon']
        except (error.URLError, TypeError, UnboundLocalError):
            print(datetime.datetime.now().strftime('%H:%M') + ': No Weather Data.')

        try:  # Älterer owm_key
            pygame.time.wait(150)  # Warte 150ms um HttpError 429 zu vermeiden
            daily = request.urlopen(openweather_base + 'forecast/daily?' + \
                                    self.owm_loc + '&units=metric&lang=de&mode=json&APPID=' + self.owm_key)
            daily_data = json.loads(daily.read().decode('utf-8'))
            self.heute_min = str(round(daily_data['list'][0]['temp']['min'], 1))
            self.heute_max = str(round(daily_data['list'][0]['temp']['max'], 1))
            self.morgen_min = str(round(daily_data['list'][1]['temp']['min'], 1))
            self.morgen_max = str(round(daily_data['list'][1]['temp']['max'], 1))
            self.vorschau = daily_data['list'][1]['weather'][0]['icon']
            print("Alter OWM_KEY")
        except (error.URLError, TypeError, UnboundLocalError):
            try:  # Neuerer owm_key
                pygame.time.wait(150)  # Warte 150ms um HttpError 429 zu vermeiden
                forecast5 = request.urlopen(openweather_base + 'forecast?' +
                                            self.owm_loc + '&units=metric&lang=de&mode=json&APPID=' + self.owm_key)
                forecast5_data = json.loads(forecast5.read().decode('utf-8'))
                # 5-Tagesvorhersage in dreistunden Abschnitten
                # Wir brauchen "nur" den Rest von heute und den ganzen Tag morgen
                # Minimum und maximum self.temperatur werden zwischen 6 und 24Uhr ermittelt.
                # dt_txt -> 2018-12-17 21:00:00
                # dt_txt[11:13] = '21'
                zeit = int(forecast5_data['list'][0]['dt_txt'][11:13])
                for idx in range(8, 0, -1):
                    if 3 * idx + zeit == 24:
                        heute_24uhr = idx
                        heute_start = max((heute_24uhr - 6), 0)
                        break
                t_list = []
                # Vorhandene Temp.-Daten bis Mitternacht
                for idx in range(heute_start, heute_24uhr + 1):
                    t_list.append(forecast5_data['list'][idx]['main']['temp'])
                t_list.append(weather_data['main']['temp'])  # aktuelle Temp. mit einbeziehen
                self.heute_max = str(round(max(t_list), 1))
                self.heute_min = str(round(min(t_list), 1))
                t_list = []
                # Alle Temp.-Daten von morgen ab 6 Uhr
                for idx in range(heute_24uhr + 2, heute_24uhr + 9):
                    t_list.append(forecast5_data['list'][idx]['main']['temp'])
                self.morgen_max = str(round(max(t_list), 1))
                self.morgen_min = str(round(min(t_list), 1))
                # Icon von morgen 12 Uhr
                self.vorschau = forecast5_data['list'][heute_24uhr + 4]['weather'][0]['icon']
            except (error.URLError, TypeError, UnboundLocalError):
                print(datetime.datetime.now().strftime('%H:%M') + ': No Forecast Data.')

    def show(self):
        """ Anzeige des Wetters """
        self.get_data()
        SS_WEATHER_WIN.fill(colors['weather_bg'])
        if bg_buf['weather_bg']:
            SS_WEATHER_WIN.blit(bg_buf['weather_bg'], (0, 0), area=SS_WEATHER_RECT)
        fc_height = fonts['big'].get_height() // 4
        draw_text(LCD, 'Wetter für ' + self.stadt,
                  fonts['big'], colors['weather_font'], align='centerx', pos=(0, fc_height))
        fc_height = fonts['big'].get_height() * 5 // 4
        draw_text(LCD,
                  'Jetzt: ' + self.temperatur + '°C' + ' / ' + \
                  self.luftdruck + 'mb' + ' / ' + self.luftfeuchte + '%rel.',
                  fonts['big'], colors['weather_font'], align='centerx', pos=(0, fc_height))
        fc_height = fc_height + fonts['big'].get_height()
        draw_text(LCD, 'Heute', fonts['std'], colors['weather_font'],
                  align='centerx', pos=(-SS_WEATHER_WIN.get_width() // 4, fc_height))
        draw_text(LCD, 'Morgen', fonts['std'], colors['weather_font'],
                  align='centerx', pos=(SS_WEATHER_WIN.get_width() // 4, fc_height))

        icon = os.path.join(WEATHERPATH, self.wetterlage + '.png')
        if not os.path.exists(icon):
            icon = os.path.join(WEATHERPATH, 'na.png')
        icon2 = os.path.join(WEATHERPATH, self.vorschau + '.png')
        if not os.path.exists(icon2):
            icon2 = os.path.join(WEATHERPATH, 'na.png')
        icon = pygame.image.load(icon).convert_alpha()
        icon2 = pygame.image.load(icon2).convert_alpha()
        icon = pygame.transform.smoothscale(icon, (SS_WEATHER_WIN.get_height() * 8 // 16,
                                                   SS_WEATHER_WIN.get_height() * 8 // 16))
        icon2 = pygame.transform.smoothscale(icon2, (SS_WEATHER_WIN.get_height() * 8 // 16,
                                                     SS_WEATHER_WIN.get_height() * 8 // 16))
        fc_height = fc_height + fonts['std'].get_height()
        LCD.blit(icon, (SS_WEATHER_WIN.get_width() // 4 - icon.get_width() // 2, fc_height))
        LCD.blit(icon2, (SS_WEATHER_WIN.get_width() * 3 // 4 - icon.get_width() // 2, fc_height))

        fc_height = fc_height + icon.get_height()
        heute_text = self.heute_min + '/' + self.heute_max + '°C'
        draw_text(LCD, heute_text, fonts['std'], colors['weather_font'],
                  align='centerx', pos=(-SS_WEATHER_WIN.get_width() // 4, fc_height))
        morgen_text = self.morgen_min + '/' + self.morgen_max + '°C'
        draw_text(LCD, morgen_text, fonts['std'], colors['weather_font'],
                  align='centerx', pos=(SS_WEATHER_WIN.get_width() // 4, fc_height))
        pygame.display.update(SS_WEATHER_RECT)


class Playlists:
    def __init__(self):
        self.lists = []
        self.index = 0
        self.old_index = [0]
        # default playlistdir/musicdir - DO NOT CHANGE!
        self.pl_dir = '/var/lib/mpd/playlists'
        self.pl_src = os.path.join(SCRIPTPATH, 'playlists')
        self.music_dir = '/var/lib/mpd/music'
        self.dir = '/'
        self.in_playlist = True
        self.replace_list = True

    def copy_playlists(self):
        """ Versuche die Beispiel-Radio-Playlisten ins
            mpd Playlisten Verzeichnis zu kopieren """
        print("copying some playlists to " + self.pl_dir)
        try:
            if os.path.isdir(self.pl_dir) and os.path.isdir(self.pl_src):
                for pl_file in os.listdir(self.pl_src):
                    if pl_file.endswith(".m3u"):
                        shutil.copy2(os.path.join(self.pl_src, pl_file), self.pl_dir)
            else:
                print("missing " + self.pl_dir + " or " + self.pl_src)
            if os.path.isdir(self.pl_dir):
                MPC.update(os.path.basename(self.pl_dir))
        except:
            exctype, value = sys.exc_info()[:2]
            print(str(exctype) + ': ' + str(value))
            print("failed to copy playlists!")

    def initialize(self):
        """ Versuche das mpd Playlisten Verzeichnis aus mpd.conf herauszulesen """
        try:
            with open(MPD_CONFIG) as m_cfg:
                for line in m_cfg:
                    if line.strip():
                        if line.strip().split()[0].lower() == 'playlist_directory':
                            self.pl_dir = line.strip().split()[1].strip("\'\"")
                        if line.strip().split()[0].lower() == 'music_directory':
                            self.music_dir = line.strip().split()[1].strip("\'\"")
        except FileNotFoundError:
            print("mpd config file " + MPD_CONFIG + " not found, using default directories")
            print(self.pl_dir + " and " + self.music_dir)

        # scriptuserid = os.getuid()
        # if not scriptuserid: # Script läuft nicht als 'root'
        #     # Scriptuser sollte im Normalfall der User 'pi' sein
        #     scriptuser = pwd.getpwuid(scriptuserid).pw_name
        #     if not scriptuser in grp.getgrnam('audio').gr_mem:
        #         # Der Scriptuser sollte Mitglied der Gruppe 'audio' sein
        #         subprocess.call("sudo usermod -a -G audio " + scriptuser, shell=True)
        #
        # if os.path.isdir(self.pl_dir):
        #     # Mache das mpd Playlisten Verzeichnis für
        #     # die Gruppe 'audio' beschreibbar
        #     if grp.getgrgid(os.stat(self.pl_dir).st_gid).gr_name != 'audio':
        #         subprocess.call("sudo chgrp audio "+self.pl_dir, shell=True)
        #     if os.stat(self.pl_dir).st_mode != 17917: # oktal: 42755 = drwxrwsr-x
        #         subprocess.call("sudo chmod 2755 "+self.pl_dir, shell=True)
        #
        # if os.path.isdir(self.music_dir):
        #     # Mache das mpd music Verzeichnis für
        #     # die Gruppe 'audio' beschreibbar
        #     if grp.getgrgid(os.stat(self.music_dir).st_gid).gr_name != 'audio':
        #         subprocess.call("sudo chgrp audio "+self.music_dir, shell=True)
        #     if os.stat(self.music_dir).st_mode != 17917: # oktal: 42755 = drwxrwsr-x
        #         subprocess.call("sudo chmod 2775 "+self.music_dir, shell=True)

        if MPC.listplaylists() == []:
            self.copy_playlists()

        # Ist vielleicht eine Playlist im mpd 'state'-file
        if int(MPC.status()['playlistlength']) > 0:
            if MPC.status()['state'] != 'play':
                MPC.play()
        else:
            try:
                MPC.load(DEFAULTPLAYLIST)
                MPC.play()
            except CommandError as err:
                if 'No such playlist' in str(err):
                    print("Playlist '" + DEFAULTPLAYLIST + "' not found")
                    print("Starting with empty list.")
                    self.in_playlist = False
        if self.read_pl():
            self.index = int(MPC.currentsong().get('pos', '0'))

    def read_dir(self, mdir='/'):
        self.in_playlist = False
        try:
            files = MPC.lsinfo(mdir)
        except CommandError as err:
            print("Playlists.read_dir()", err)
            mdir = '/'
            files = MPC.lsinfo(mdir)
        self.dir = mdir
        self.lists = self.get(files)
        return True

    def read_pl(self):
        files = MPC.playlistinfo()
        if not files:
            self.lists = [['e', self.dir + '/empty playlist ...', colors['err']]]
            self.old_index = [0]
            self.index = 0
            return False
        self.lists = self.get(files)
        self.in_playlist = True
        return True

    def del_pl_entry(self):
        if self.lists[self.index][0] == "f":
            MPC.delete(self.index)
            MPC.play()
            self.read_pl()
            self.index = int(MPC.currentsong().get('pos', '0'))

    def get(self, filelist):
        self.lists = []
        for m_file in filelist:
            if 'directory' in m_file:
                if m_file['directory'][-4:].lower() != '.zip':  # alles außer .zip-Dateien
                    self.lists.append(['d', m_file['directory'], colors['dir']])
            if 'playlist' in m_file:
                if m_file['playlist'][-4:].lower() == '.m3u':
                    self.lists.append(['p', m_file['playlist'], colors['pls']])
                elif m_file['playlist'][-4:].lower() == '.pls':
                    self.lists.append(['p', m_file['playlist'], colors['pls']])
                else:
                    self.lists.append(['p', m_file['playlist'], colors['rad']])
            if 'file' in m_file:
                if self.in_playlist:
                    try:
                        self.lists.append(['f', m_file['name'], colors['ple']])
                    except KeyError:
                        self.lists.append(['f', m_file['file'], colors['ple']])
                else:
                    self.lists.append(['f', m_file['file'], colors['mp3']])
        if not self.lists:
            self.lists = [['e', self.dir + '/no playlists or files found ...', colors['err']]]
        if SORT_PLAYLISTS:
            if not self.in_playlist:
                self.lists.sort(key=itemgetter(0, 1))  # sort ABCabcÄä
                # sort AÄaäBbCc (locale benötigt):
                # sort AaBbCcÄä (ohne locale):
                # self.lists.sort(key=itemgetter(1))
                # self.lists.sort(key=lambda x: locale.strxfrm(str.lower(x[1])))
                # self.lists.sort(key=itemgetter(0))
        return self.lists

    def clear(self):
        MPC.clear()
        self.in_playlist = False
        self.old_index.append(self.index)
        self.index = 0

    def load_list(self):
        try:
            if self.lists[self.index][0] == 'p':
                self.clear()
                MPC.load(self.lists[self.old_index.pop()][1])
                self.replace_list = True
                MPC.play()
            elif self.lists[self.index][0] == 'f':
                if self.in_playlist:
                    MPC.play(self.index)
                else:
                    if self.replace_list:
                        self.replace_list = False
                        self.clear()
                        MPC.add(self.lists[self.old_index.pop()][1])
                    else:
                        MPC.add(self.lists[self.index][1])
                    MPC.play()
            elif self.lists[self.index][0] == 'd':
                self.read_dir(self.lists[self.index][1])
                return False
            elif self.lists[self.index][0] == 'e':  # Keine Playlisten oder Dateien gefunden
                if not self.in_playlist:
                    return False
        except CommandError as err:
            print("Senderfehler...", err)
        except IndexError as err:
            print('Playlists.load_list() ', err)
            return False
        return True

    def show(self):
        old_len = len(self.lists)
        if self.in_playlist:
            self.read_pl()
        else:
            self.read_dir(self.dir)
        if len(self.lists) != old_len:
            self.index = int(MPC.currentsong().get('pos', '0'))
        if not self.lists:
            draw_text(LIST_WIN[0], 'no playlists found...', fonts['big'], colors['font'])
            return True
        if len(self.lists) > 3:
            draw_text(LIST_WIN[2], self.lists[self.index - 2][1].split('/')[-1],
                      fonts['std'], self.lists[self.index - 2][2])
        if len(self.lists) > 1:
            draw_text(LIST_WIN[1], self.lists[self.index - 1][1].split('/')[-1],
                      fonts['std'], self.lists[self.index - 1][2])
        draw_text(LIST_WIN[0], re.sub(".pls|.m3u", "", self.lists[self.index][1].split('/')[-1]),
                  fonts['big'], self.lists[self.index][2])
        if len(self.lists) > 2:
            draw_text(LIST_WIN[3], self.lists[(self.index + 1) % len(self.lists)][1].split('/')[-1],
                      fonts['std'], self.lists[(self.index + 1) % len(self.lists)][2])
        if len(self.lists) > 4:
            draw_text(LIST_WIN[4], self.lists[(self.index + 2) % len(self.lists)][1].split('/')[-1],
                      fonts['std'], self.lists[(self.index + 2) % len(self.lists)][2])
        return True

    def up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.lists) - 1

    def down(self):
        self.index += 1
        if self.index >= len(self.lists):
            self.index %= len(self.lists)

    def updir(self):
        if self.in_playlist:
            self.in_playlist = False
            self.read_dir(self.dir)
        else:
            up_dir = os.path.dirname(self.dir)
            self.read_dir(up_dir)
        self.index = 0
        if self.old_index:
            self.index = self.old_index.pop()

    def enter(self):
        if self.load_list():
            if not self.in_playlist:
                self.old_index.append(self.index)
                self.index = int(MPC.currentsong()['pos'])
            self.in_playlist = True
            self.read_pl()
        else:
            self.in_playlist = False
            self.read_dir(self.dir)
            self.old_index.append(self.index)
            self.index = 0


def status_update():
    """ Anzeige von Zeit, Tracknr. und Lautstärke (statusbar)"""
    info = MPC.currentsong()
    status = MPC.status()
    try:
        songtime = int(info['time'])
        if songtime == 0:
            raise KeyError
        s_min, s_sec = divmod(songtime, 60)
        s_hour, s_min = divmod(s_min, 60)
        elapsed = int(status['elapsed'].split('.')[0])
        e_min, e_sec = divmod(elapsed, 60)
        e_hour, e_min = divmod(e_min, 60)
        if not s_hour:
            hms_elapsed = "%02d:%02d" % (e_min, e_sec)
            hms_songtime = "%02d:%02d" % (s_min, s_sec)
        else:
            hms_elapsed = "%d:%02d:%02d" % (e_hour, e_min, e_sec)
            hms_songtime = "%d:%02d:%02d" % (s_hour, s_min, s_sec)
        time_text = hms_elapsed + '/' + hms_songtime
    except KeyError:
        time_text = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    draw_text(STATUS_WIN, time_text, fonts['std'], colors['status'], align='centerx')
    # Lautstärkeanzeige
    if 'volume' in status:
        volume = 'Vol.: ' + status['volume'] + '%'
    else:
        volume = 'Vol.: 0'
    draw_text(STATUS_WIN, volume, fonts['std'], colors['status'])
    # Anzeige der Stück-/Stationsnummer
    pln = str(int(info.get('pos', '-1')) + 1) + '/' + status.get('playlistlength', '0')
    draw_text(STATUS_WIN, pln, fonts['std'], colors['status'], align='topright')
    # Anzeige der Bitrate
    bitrate = status.get('bitrate', '0') + 'kbps'
    draw_text(BITRATE_WIN, bitrate, fonts['std'], colors['status'], align='topright')


def get_xfade_state():
    draw_text(MSG_WIN, 'MPD Playback Settings', fonts['std'], colors['status'], align='centerx')
    status = MPC.status()
    if 'xfade' in status:
        xf_state = status['xfade'] + 's'
    else:
        xf_state = 'off'
    draw_text(LCD, 'Crossfade: ' + xf_state, fonts['std'], colors['font'],
              align='centerx', pos=(0, CHK_WIN[0].get_abs_offset()[1]))
    CHK_WIN[0].blit(btn["Checkbox_down"], (0, 0))
    CHK_WIN[1].blit(btn["Checkbox_up"], (CHK_WIN[5].get_width() - btn["Checkbox_up"].get_width(), 0))

    mr_db = 'MixRamp threshold: ' + str(round(float(status['mixrampdb']), 1)) + 'dB'
    draw_text(LCD, mr_db, fonts['std'], colors['font'],
              align='centerx', pos=(0, CHK_WIN[2].get_abs_offset()[1]))
    CHK_WIN[2].blit(btn["Checkbox_down"], (0, 0))
    CHK_WIN[3].blit(btn["Checkbox_up"], (CHK_WIN[3].get_width() - btn["Checkbox_up"].get_width(), 0))
    mr_dl = 'MixRamp delay: off'
    if 'mixrampdelay' in status:
        if round(float(status['mixrampdelay']), 1) != 0.0:
            mr_dl = 'MixRamp delay: ' + str(round(float(status['mixrampdelay']), 1)) + 's'
    draw_text(LCD, mr_dl, fonts['std'], colors['font'],
              align='centerx', pos=(0, CHK_WIN[4].get_abs_offset()[1]))
    CHK_WIN[4].blit(btn["Checkbox_down"], (0, 0))
    CHK_WIN[5].blit(btn["Checkbox_up"], (CHK_WIN[5].get_width() - btn["Checkbox_up"].get_width(), 0))
    draw_text(STATUS_WIN, 'Touch here for Basic Settings',
              fonts['std'], colors['status'], align='centerx')


def set_xfade_state(idx=None):
    # MixRamp benötigt MixRamp-Tags in den mp3-Dateien
    # Fallback ist Crossfade, wenn die Tags nicht vorhanden sind
    status = MPC.status()
    if idx == 0:
        secs = 0
        if 'xfade' in status:
            secs = int(status['xfade']) - 1
            if secs <= 0:
                secs = 0
        MPC.crossfade(secs)
    elif idx == 1:
        if 'xfade' in status:
            secs = int(status['xfade'])
            if secs > 14:
                secs = 14
        else:
            secs = 0
        MPC.crossfade(secs + 1)
    elif idx == 2:
        mr_db = float(status['mixrampdb']) - 0.5
        if mr_db < -30.0:
            mr_db = -30.0
        MPC.mixrampdb(mr_db)
    elif idx == 3:
        mr_db = float(status['mixrampdb']) + 0.5
        if mr_db > 0.0:
            mr_db = 0.0
        MPC.mixrampdb(mr_db)
    elif idx == 4:
        mr_dl = 'nan'
        if 'mixrampdelay' in status:
            mr_dl = float(status['mixrampdelay']) - 0.5
            if mr_dl <= 0.0:
                mr_dl = 'nan'
        MPC.mixrampdelay(mr_dl)
    elif idx == 5:
        mr_dl = 0.5
        if 'mixrampdelay' in status:
            mr_dl = float(status['mixrampdelay']) + 0.5
            if mr_dl > 15.0:
                mr_dl = 15.0
        MPC.mixrampdelay(mr_dl)
    else:
        return False
    return True


def get_playback_state():
    draw_text(MSG_WIN, 'MPD Playback Settings', fonts['std'], colors['status'], align='centerx')
    status = MPC.status()
    if status['repeat'] == '1':
        CHK_WIN[0].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[0].blit(btn["Checkbox"], (0, 0))
    draw_text(CHK_WIN[0], ' Repeat', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), 0))
    if status['random'] == '1':
        CHK_WIN[1].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[1].blit(btn["Checkbox"], (0, 0))
    draw_text(CHK_WIN[1], ' Random', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), 0))
    if status['consume'] == '1':
        CHK_WIN[2].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[2].blit(btn["Checkbox"], (0, 0))
    draw_text(CHK_WIN[2], ' Consume', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), 0))
    if status['single'] == '1':
        CHK_WIN[3].blit(btn["Checkbox_Sel"], (0, 0))
    else:
        CHK_WIN[3].blit(btn["Checkbox"], (0, 0))
    draw_text(CHK_WIN[3], ' Single', fonts['std'], colors['font'],
              pos=(btn["Checkbox"].get_width(), 0))
    draw_text(LCD, 'Replay-Gain:  ' + MPC.replay_gain_status(), fonts['std'], colors['font'],
              align='centerx', pos=(0, CHK_WIN[4].get_abs_offset()[1]))
    draw_text(STATUS_WIN, 'Touch here for X-Fade Settings',
              fonts['std'], colors['status'], align='centerx')


def set_playback_state(idx=None):
    status = MPC.status()
    if idx == 0:
        MPC.repeat(int(status['repeat']) ^ 1)
    elif idx == 1:
        MPC.random(int(status['random']) ^ 1)
    elif idx == 2:
        MPC.consume(int(status['consume']) ^ 1)
    elif idx == 3:
        MPC.single(int(status['single']) ^ 1)
    elif idx in (4, 5):
        rg_mode = ['off', 'track', 'album', 'auto']
        idx = rg_mode.index(MPC.replay_gain_status()) + 1
        if idx >= len(rg_mode):
            idx = 0
        MPC.replay_gain_mode(rg_mode[idx])
    else:
        return False
    return True


def get_outputs():
    try:
        outputs = MPC.outputs()
    except:
        exctype, value = sys.exc_info()[:2]
        print("get_outputs()", str(exctype) + ': ' + str(value))
        mpd_connect(MPC)
        outputs = MPC.outputs()
    n_out = len(outputs)
    if n_out > 6:
        n_out = 6
    for idx in range(n_out):
        if outputs[idx]['outputenabled'] == '1':
            CHK_WIN[idx].blit(btn["Checkbox_Sel"], (0, 0))
        else:
            CHK_WIN[idx].blit(btn["Checkbox"], (0, 0))
        draw_text(CHK_WIN[idx], ' ' + outputs[idx]['outputname'],
                  fonts['std'], colors['font'], pos=(btn["Checkbox"].get_width(), 0))


def set_outputs(idx=None):
    try:
        outputs = MPC.outputs()
    except:
        exctype, value = sys.exc_info()[:2]
        print("set_outputs()", str(exctype) + ': ' + str(value))
        mpd_connect(MPC)
        outputs = MPC.outputs()
    n_out = len(outputs)
    if 0 <= idx < n_out:
        if outputs[idx]['outputenabled'] == '1':
            MPC.disableoutput(idx)
        else:
            MPC.enableoutput(idx)
            MPC.play()
        return True
    return False


def pygame_svg(svg_file, color, size):
    print(svg_file)
    with open(svg_file, "r+") as svgf:
        svgbuf = svgf.read()
    colorstr = '#%02x%02x%02x' % color
    if '#00ffff' in svgbuf:
        svgbuf = svgbuf.replace("#00ffff", colorstr)
    elif '"#0ff"' in svgbuf:
        svgbuf = svgbuf.replace('"#0ff"', '"' + colorstr + '"')

    w_svg, h_svg = size
    # Modifiziere SVG für Skalierung
    if 'viewBox="' in svgbuf:
        if re.search('<svg.((?!>).)*height=', svgbuf, re.MULTILINE | re.DOTALL):
            svgbuf = re.sub(r'width="(\d+)', 'width="' + str(w_svg), svgbuf, 1)
            svgbuf = re.sub(r'height="(\d+)', 'height="' + str(h_svg), svgbuf, 1)
        else:
            svgbuf = re.sub('viewBox="',
                            'width="' + str(w_svg) + '" height="' + str(h_svg) + '" viewBox="', svgbuf, 1)
    else:
        wo_svg = re.search(r'<svg\s+?((?!>).)*width="(\d+)"', svgbuf, re.MULTILINE | re.DOTALL)
        ho_svg = re.search(r'<svg\s+?((?!>).)*height="(\d+)"', svgbuf, re.MULTILINE | re.DOTALL)
        svgbuf = re.sub(r'<svg\s+?',
                        '<svg viewBox="0 0 ' + wo_svg.group(2) + ' ' + ho_svg.group(2) + '" ', svgbuf, 1)
        svgbuf = re.sub(r'width="(\d+)', 'width="' + str(w_svg), svgbuf, 1)
        svgbuf = re.sub(r'height="(\d+)', 'height="' + str(h_svg), svgbuf, 1)

    svgimg = svg.Parser.parse(svgbuf)
    rast = svg.Rasterizer()
    strbuf = rast.rasterize(svgimg, w_svg, h_svg)
    image = pygame.image.frombuffer(strbuf, size, "RGBA")
    return image


def load_skin(skin_name: str):
    skin_path = os.path.join(SKINBASE, skin_name)
    if os.path.isdir(skin_path):
        read_skin_config(skin_path)
        config['skin'] = skin_name
    else:
        print('Could not find Skin "' + skin_name + '".')
        print("exiting...")
        pygame.quit()
        sys.exit()

    # Buttons laden
    btn.update({MSG_FRAME: pygame_svg(os.path.join(skin_path, MSG_FRAME + ".svg"),
                                      colors['skin'], (WIDTH, HEIGHT // 2))})
    for btn_name in BTN_LIST:
        if os.path.isfile(os.path.join(skin_path, btn_name + ".svg")):
            btn.update({btn_name: pygame_svg(os.path.join(skin_path, btn_name + ".svg"),
                                             colors['skin'], (WIDTH // 4, HEIGHT // 4))})
    for chk_name in CHK_LIST:
        if os.path.isfile(os.path.join(skin_path, chk_name + ".svg")):
            btn.update({chk_name: pygame_svg(os.path.join(skin_path, chk_name + ".svg"),
                                             colors['font'], (fonts['std'].get_height(),
                                                              fonts['std'].get_height()))})
    bg_buf['sel'] = pygame_svg(os.path.join(skin_path, SELECTION_FRAME + ".svg"),
                               colors['skin'], (WIDTH, HEIGHT // 2))
    bg_buf['sel_msg'] = pygame_svg(os.path.join(skin_path, SELECT_PL + ".svg"),
                                   colors['skin'], (WIDTH // 2, HEIGHT // 2))
    for wln in WLAN_LIST:
        if os.path.isfile(os.path.join(skin_path, wln + ".svg")):
            btn.update({wln: pygame_svg(os.path.join(skin_path, wln + ".svg"),
                                        colors['status'], (fonts['std'].get_height() * 5 // 4,
                                                           fonts['std'].get_height()))})

    # Hintergrundbilder laden
    if skincfg['background']:
        bg_buf['bg'] = pygame.image.load(skincfg['background']).convert()
        bg_buf['bg'] = pygame.transform.scale(bg_buf['bg'], (WIDTH, HEIGHT))
    else:
        bg_buf['bg'] = None
    if skincfg['weather_bg']:
        bg_buf['weather_bg'] = pygame.image.load(skincfg['weather_bg']).convert()
        bg_buf['weather_bg'] = pygame.transform.scale(bg_buf['weather_bg'], (WIDTH, HEIGHT))
    else:
        bg_buf['weather_bg'] = None

    # Hintergrund für LCD.update(dirty_rects) erzeugen
    LCD.fill(colors['bg'])
    if bg_buf['bg']:
        LCD.blit(bg_buf['bg'], (0, 0))
    if skincfg['text_on_top']:
        BTN_WIN[0].blit(bg_buf['sel'], (0, 0))  # SELECTION_FRAME
    bg_buf['list_bg'] = LIST_WIN[0].copy()
    LCD.fill(colors['bg'])
    if bg_buf['bg']:
        LCD.blit(bg_buf['bg'], (0, 0))
    if skincfg['text_on_top']:
        BTN_WIN[0].blit(btn["Status"], (0, 0))  # skin surface
    bg_buf['station_bg'] = STATION_WIN.copy()
    bg_buf['artist_bg'] = ARTIST_WIN.copy()
    bg_buf['title_bg'] = TITLE_WIN.copy()
    bg_buf['status_bg'] = STATUS_WIN.copy()
    bg_buf['bitrate_bg'] = BITRATE_WIN.copy()
    bg_buf['btn1'] = BTN_WIN[1].copy()
    bg_buf['btn2'] = BTN_WIN[2].copy()
    bg_buf['btn4'] = BTN_WIN[4].copy()

    pygame.event.get()  # werfe aufgelaufene Events weg


def skin1_base():
    # Hintergrund erzeugen
    LCD.fill(colors['bg'])
    if bg_buf['bg']:
        LCD.blit(bg_buf['bg'], (0, 0))
    # Buttons darauflegen
    if "Plus" in btn:
        BTN_WIN[3].blit(btn["Plus"], (0, 0))  # vol_up
    else:
        BTN_WIN[3].blit(btn["Up"], (0, 0))
    BTN_WIN[5].blit(btn["Prev"], (0, 0))  # prev
    BTN_WIN[6].blit(btn["Next"], (0, 0))  # next
    if "Minus" in btn:
        BTN_WIN[7].blit(btn["Minus"], (0, 0))  # vol_down
    else:
        BTN_WIN[7].blit(btn["Down"], (0, 0))
    BTN_WIN[8].blit(btn["Next_Page"], (0, 0))  # next_page


def skin2_base():
    BTN_WIN[3].blit(btn["Up"], (0, 0))  # up
    BTN_WIN[4].blit(btn["Updir"], (0, 0))  # updir
    BTN_WIN[7].blit(btn["Down"], (0, 0))  # down
    BTN_WIN[8].blit(btn["Enter"], (0, 0))  # enter
    LCD.blit(bg_buf['sel_msg'], BTN_RECT[1])  # 'Select Music'-Text
    BTN_WIN[0].blit(bg_buf['sel'], (0, 0))  # SELECTION_FRAME


def skin3_base():
    BTN_WIN[0].blit(btn["Status"], (0, 0))  # msg_frame
    BTN_WIN[1].blit(btn["Refresh"], (0, 0))  # refresh
    BTN_WIN[2].blit(btn["Trash"], (0, 0))  # trash
    BTN_WIN[3].blit(btn["Save"], (0, 0))  # save
    BTN_WIN[4].blit(btn["Shuffle"], (0, 0))  # shuffle
    BTN_WIN[5].blit(btn["Prev_Page"], (0, 0))  # prev_page
    BTN_WIN[8].blit(btn["Next_Page"], (0, 0))  # next_page


def skin4_base():
    BTN_WIN[0].blit(btn["Status"], (0, 0))  # msg_frame
    BTN_WIN[1].blit(btn["Cloud"], (0, 0))  # cloud (WTR.show())
    BTN_WIN[2].blit(btn["Config"], (0, 0))  # config
    BTN_WIN[3].blit(btn["Reboot"], (0, 0))  # reboot
    BTN_WIN[4].blit(btn["Poweroff"], (0, 0))  # poweroff
    BTN_WIN[5].blit(btn["Prev_Page"], (0, 0))  # prev_page
    BTN_WIN[8].blit(btn["Next_Page"], (0, 0))  # next_page


def skin5_base():
    BTN_WIN[0].blit(btn["Status"], (0, 0))  # msg_frame
    BTN_WIN[1].blit(btn["Save"], (0, 0))  # save
    BTN_WIN[2].blit(btn["Color"], (0, 0))  # color (change_skin)
    BTN_WIN[3].blit(btn["Refresh"], (0, 0))  # refresh (restart radio)
    if "Plus" in btn:
        BTN_WIN[4].blit(btn["Plus"], (0, 0))  # vol_up
    else:
        BTN_WIN[4].blit(btn["Up"], (0, 0))  # vol_up
    BTN_WIN[5].blit(btn["Prev_Page"], (0, 0))  # prev_page
    BTN_WIN[6].blit(btn["Exit"], (0, 0))  # exit (quit radio)
    BTN_WIN[7].blit(btn["Quit"], (0, 0))  # quit (quit radio & mpd)
    if "Minus" in btn:
        BTN_WIN[8].blit(btn["Minus"], (0, 0))  # vol_up
    else:
        BTN_WIN[8].blit(btn["Down"], (0, 0))  # vol_up


def switch_skin():
    skins = []
    for dirs in os.walk(SKINBASE):
        if 'skin.cfg' in dirs[2]:
            skins.append(os.path.basename(dirs[0]))
    if "skin_idx" not in switch_skin.__dict__:
        switch_skin.idx = skins.index(config['skin'])
    switch_skin.idx += 1
    if switch_skin.idx >= len(skins):
        switch_skin.idx = 0
    load_skin(skins[switch_skin.idx])


def get_wlan_level(netdev):
    level = 0
    with open('/proc/net/wireless') as procf:
        for line in procf:
            wlan = line.split()
            if wlan[0] == netdev + ':':
                value = float(wlan[3])
                if value < 0:
                    # Näherungsweise Umrechnung von dBm in %
                    # -35dBm -> 100, -95dBm -> 0
                    level = int((value + 95) / 0.6)
                else:
                    level = int(value)
    return level


def get_info():  # Aufbereitung der Song-Daten von mpd
    info = MPC.currentsong()
    # Welcher Sender
    try:
        station = info['album']
    except KeyError:
        station = None
    if not station:
        try:
            station = info['name']
        except KeyError:
            station = "no data"

    # Welcher Titel
    try:
        title = info['title'].strip()
        # mit Spezialbehandlung für diverse Sender,
        # die vor den Songtitel nochmal den Sendernamen klatschen:
        if station.upper().split()[-1][-3:] + ': ' in title.upper():
            match = re.search('(.*): (.*)', title)
            title = match.group(2)
        # Spezialbehandlung für diverse Icecast-Radiostationen
        if 'text=' in title:
            match = re.search('(.*)text="([^"]*)"', title)
            title = match.group(1) + match.group(2)
    except KeyError:
        title = "no data"
    try:
        artist = info['artist'].strip()
        if not artist:
            artist = None
    except KeyError:
        if ' - ' in title:
            match = re.search('(.*?) - (.*)', title)
            artist = match.group(1)
            title = match.group(2)
        else:
            artist = None

    return station, title, artist


def fit_text(text, width, fontobj):
    if fontobj.size(text)[0] > width:
        while fontobj.size(text)[0] > width:
            text = text[:-1]
        text = text[:-3] + '...'
    return text


def show_ss_status(big_clock=False):
    ss_station, ss_title, ss_artist = get_info()
    # Wenn der Titel zu lang ist, kürzen und mit '...' ergänzen
    if ss_artist:
        ss_title = ss_artist + ' - ' + ss_title
    ss_title = fit_text(ss_title, WIDTH, fonts['std'])
    ss_clock = datetime.datetime.now().strftime('%H:%M')
    if big_clock:
        ss_station = fit_text(ss_station, WIDTH, fonts['big'])
        LCD.fill(colors['bg'])
        clock_label = fonts['clock'].render(ss_clock, 1, colors['clock_font'], colors['bg'])
        LCD.blit(clock_label,
                 (randint(0, WIDTH - clock_label.get_width()),
                  randint(0,
                          HEIGHT - SS_TITLE_WIN.get_height() - \
                          SS_CLOCK_WIN.get_height() - clock_label.get_height())))
        draw_text(SS_CLOCK_WIN, ss_station, fonts['big'], colors['status'], align='centerx')
        draw_text(SS_TITLE_WIN, ss_title, fonts['std'], colors['status'], align='centerx')
        pygame.display.flip()
    else:
        SS_TITLE_WIN.fill(colors['weather_bg'])
        if bg_buf['weather_bg']:
            SS_TITLE_WIN.blit(bg_buf['weather_bg'], (0, 0), area=SS_TITLE_RECT)
        SS_CLOCK_WIN.fill(colors['weather_bg'])
        if bg_buf['weather_bg']:
            SS_CLOCK_WIN.blit(bg_buf['weather_bg'], (0, 0), area=SS_CLOCK_RECT)
        draw_text(SS_CLOCK_WIN, ss_clock, fonts['big'], colors['status'], align='centerx')
        draw_text(SS_TITLE_WIN, ss_title, fonts['std'], colors['status'], align='centerx')
        pygame.display.update([SS_TITLE_RECT, SS_CLOCK_RECT])


class ScrollText:
    """
    Einfacher Lauftext
    Modified version of https://github.com/gunny26/pygame/blob/master/ScrollText.py
    """

    def __init__(self, surface, text, font, color, bkg, skin_buf):
        """
        (pygame.Surface) surface - surface to draw on
        (string) text - text to draw
        (int) hpos - horizontal position on y axis
        (pygame.font.Font) - font to use
        (pygame.Color) color - color of font
        (pygame.Surface.copy) bkg - copy of surface background
        """
        self.surface = surface
        self.text = text
        self.font = font
        self.color = color
        self.bkg = bkg.convert()
        self.skin_buf = skin_buf.convert_alpha()
        # initialize
        self.rflag = True
        self.pos = 0
        self.oldpos = -1
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.rect = self.surface.get_rect(topleft=self.surface.get_abs_offset())
        self.surface.set_colorkey((127, 127, 127))
        # self.surface.fill((127, 127, 127))
        if skincfg['dropshadow']:
            self.text_shadow = self.font.render(self.text, True, colors['shadow']).convert_alpha()
        self.text_surface = self.font.render(self.text, True, self.color).convert_alpha()
        self.text_width = self.text_surface.get_width()

    def __str__(self):
        return self.__class__.__name__

    def update(self, redraw=False):
        """update every frame if text width is larger than surface width """
        if redraw:
            self.oldpos = -1
        if self.oldpos != self.pos:
            self.surface.blit(self.bkg, (0, 0))
            if skincfg['dropshadow']:
                self.surface.blit(self.text_shadow,
                                  (1, 1),
                                  (self.pos, 0, self.width, self.height)
                                  )
            self.surface.blit(self.text_surface,
                              (0, 0),
                              (self.pos, 0, self.width, self.height)
                              )
            self.oldpos = self.pos
            if not skincfg['text_on_top']:
                LCD.blit(self.skin_buf, self.rect, area=self.rect)
            pygame.display.update(self.rect)
        if ((self.text_width - self.pos) >= self.width) and self.rflag:
            self.pos += 1
        else:
            self.rflag = False
        if (self.pos > 0) and not self.rflag:
            self.pos -= 1
        else:
            self.rflag = True


class Screen:
    """ Die Benutzeroberfläche... """

    def __init__(self):
        self.station_label = ScrollText(STATION_WIN, "", fonts['std'],
                                        colors['status'], bg_buf['station_bg'], btn["Status"])
        self.title_label = ScrollText(TITLE_WIN, "", fonts['title'],
                                      (colors['font']), bg_buf['title_bg'], btn["Status"])
        self.artist_label = ScrollText(ARTIST_WIN, "", fonts['std'],
                                       (colors['font']), bg_buf['artist_bg'], btn["Status"])
        self.select_label = ScrollText(LIST_WIN[0], "", fonts['big'],
                                       (colors['font']), bg_buf['list_bg'], bg_buf['sel'])
        self.station = ""
        self.title = ""
        self.artist = ""
        self.tick = 0
        self.sec = 0
        self.xf_page = False  # MPD Playback Settings: Crossfade-Page
        self.oldvolume = MPC.status().get('volume', '-1')
        if (self.oldvolume == 0):
            self.muted = True
        else:
            self.muted = False

        self.menu = 1
        if not any(out['outputenabled'] == '1' for out in MPC.outputs()):
            self.menu = 4
        self.screensaver = False
        self.refresh = True  # complete redraw
        self.status_update = True  # for status-bar update
        self.dirty = True  # for ScrollText.update()
        self.dirty_rects = []  # for screen.update()
        self.event = []  # eventlist for MPC.fetch_idle()
        MPC.idle()  # check for MPD-events

    def button(self, number):  # which button (and which menu) was pressed on touch
        """ wo wurde getouched? """
        self.refresh = False

        try:
            status = MPC.status()
        except CommandError as err:
            print("button()", err)
            return

        if self.menu == 1:  # Main Screen
            if number == 0:  # msg_win
                if PLS.read_pl():
                    PLS.index = int(MPC.currentsong().get('pos', '0'))
                self.menu = 2
                self.refresh = True
            elif number == 1:  # stop/play
                if status['state'] == 'stop':
                    MPC.play()
                else:
                    MPC.stop()
            elif number == 2:  # pause/play
                MPC.pause()
            elif number == 3:  # vol up
                vol = int(status['volume'])
                if vol >= 95:
                    MPC.setvol(100)
                else:
                    MPC.setvol((vol + 5))
            elif number == 4:  # mute/unmute
                vol = int(status['volume'])
                if vol != 0:
                    self.oldvolume = vol
                    MPC.setvol(0)
                    self.muted = True
                else:
                    MPC.setvol(self.oldvolume)
                    self.muted = False
            elif number == 5:  # prev
                PLS.up()
                PLS.enter()
            elif number == 6:  # next
                PLS.down()
                PLS.enter()
            elif number == 7:  # vol down
                vol = int(status['volume'])
                if vol <= 5:
                    MPC.setvol(0)
                else:
                    MPC.setvol((vol - 5))
            elif number == 8:  # next page
                # Gehe zum Menu 3
                self.menu = 3
                self.refresh = True
        elif self.menu == 2:  # File Selection Screen
            self.refresh = True
            if number == 0:  # selection_win
                self.menu = 1
                if PLS.in_playlist:
                    if config['x_button'] and PLUS_RECT.collidepoint(POS):
                        PLS.del_pl_entry()
                        self.menu = 2
                elif config['plus_button'] and PLUS_RECT.collidepoint(POS):
                    if PLS.lists[PLS.index][0] == 'd':
                        waiting('adding Directory to Playlist')
                        MPC.add(PLS.lists[PLS.index][1])
                        pygame.time.wait(1500)
                        pygame.event.get()  # werfe aufgelaufene Events weg
                        self.menu = 2
                else:
                    PLS.read_pl()
                SCR.update()
            elif number == 3:  # up
                PLS.up()
            elif number == 4:  # updir
                PLS.updir()
            elif number == 7:  # down
                PLS.down()
            elif number == 8:  # return
                PLS.enter()
            else:
                self.refresh = False
        elif self.menu == 3:  # MPD Playback Settings Screen
            self.refresh = True
            if number == 0:
                chk = None
                for idx, item in enumerate(CHK_RECT):
                    if item.collidepoint(POS):
                        chk = idx
                if chk is not None:  # chk == 0..5
                    if self.xf_page:  # Crossfade Seite
                        set_xfade_state(chk)
                    else:  # Basic Settings Seite
                        set_playback_state(chk)
                    self.refresh = False
                if STATUS_RECT.collidepoint(POS):
                    self.xf_page ^= True  # Seite Umschalten
            elif number == 1:
                waiting('updating mpd-Database...')
                try:
                    MPC.update()
                except CommandError as err:
                    print("button() menu 3-1 ", err)
                pygame.time.wait(2500)
                pygame.event.get()  # werfe aufgelaufene Events weg
            elif number == 2:
                PLS.clear()
                waiting('cleared Playlist!')
                pygame.time.wait(1500)
                pygame.event.get()  # werfe aufgelaufene Events weg
                self.menu = 2
            elif number == 3:
                waiting('saved Playlist as', '\'' + SAVE_FILENAME + '\'')
                try:
                    MPC.rm(SAVE_FILENAME)
                except CommandError as err:
                    print("button() menu 3-3 ", err)
                MPC.save(SAVE_FILENAME)
                pygame.time.wait(1500)
                pygame.event.get()  # werfe aufgelaufene Events weg
            elif number == 4:
                waiting('shuffling Playlist...')
                MPC.shuffle()
                pygame.time.wait(1500)
                pygame.event.get()  # werfe aufgelaufene Events weg
            elif number == 5:
                self.menu = 1
            elif number == 8:
                self.menu = 4
        elif self.menu == 4:  # MPD audio_outputs Screen
            self.refresh = True
            # mpd audio_outputs menu
            if number == 0:
                output = None
                for idx, rect in enumerate(CHK_RECT):
                    if rect.collidepoint(POS):
                        output = idx
                if output is not None:  # output == 0..5
                    set_outputs(output)
                self.refresh = False
            elif number == 1:
                self.menu = 6
            elif number == 2:
                self.menu = 5
            elif number == 3:
                # Neustart
                reboot()
            elif number == 4:
                # Ausschalten
                poweroff()
            elif number == 5:
                self.menu = 3
            elif number == 8:
                # Gehe zum Menu 1
                self.menu = 1
        elif self.menu == 5:  # NewTron-Radio Settings Screen
            self.refresh = True
            if number == 0:
                chk = None
                if STATUS_RECT.collidepoint(POS):
                    chk = 9
                for idx, item in enumerate(CHK_RECT):
                    if item.collidepoint(POS):
                        chk = idx
                if chk is not None:  # chk == 0..5
                    self.refresh = set_config(chk)
            if number == 1:
                waiting('saving configuration...')
                save_config()
                pygame.time.wait(1500)
                pygame.event.get()  # werfe aufgelaufene Events weg
            elif number == 2:
                # switch skin
                switch_skin()
            elif number == 3:
                # Auffrischen
                waiting("refreshing...")
                pygame.time.wait(1500)
                pygame.quit()
                os.execl(sys.argv[0], sys.argv[0])
            elif number == 4:
                config['screensaver_timer'] += 1
                if config['screensaver_timer'] > 120:
                    config['screensaver_timer'] = 120
            elif number == 5:
                self.menu = 4
            elif number == 6:
                # Oberfläche beenden
                pygame.quit()
                sys.exit()
            elif number == 7:
                # Stop Radio und beende Oberfläche
                MPC.stop()
                pygame.quit()
                sys.exit()
            elif number == 8:
                config['screensaver_timer'] -= 1
                if config['screensaver_timer'] <= 0:
                    config['screensaver_timer'] = 1
        elif self.menu == 6:  # Weather Screen
            self.refresh = True
            self.menu = 4
        self.refresh = True

    def update(self):
        """ Darstellung auf dem Touchscreen """
        self.tick += 1
        if self.tick >= FPS:
            self.tick = 0
            self.sec += 1

        if select([MPC], [], [], 0)[0]:
            self.event = MPC.idle()
            print(self.event)
            self.dirty_rects = []
            MPC.idle()

        if not self.screensaver:
            if self.menu == 1:  # Main Screen
                if self.refresh:
                    skin1_base()
                    if skincfg['text_on_top']:
                        BTN_WIN[0].blit(btn["Status"], ((0, 0)))  # msg_frame
                        self.dirty_rects.append(BTN_RECT[0])
                    self.dirty_rects.append(BTN_RECT[3])
                    self.dirty_rects.append(BTN_RECT[5])
                    self.dirty_rects.append(BTN_RECT[6])
                    self.dirty_rects.append(BTN_RECT[7])
                    self.dirty_rects.append(BTN_RECT[8])

                if 'playlist' in self.event or self.refresh:
                    self.station, self.title, self.artist = get_info()
                    self.station_label = ScrollText(STATION_WIN, self.station,
                                                    fonts['std'], colors['status'],
                                                    bg_buf['station_bg'], btn["Status"])
                    self.title_label = ScrollText(TITLE_WIN, self.title,
                                                  fonts['title'], (colors['font']),
                                                  bg_buf['title_bg'], btn["Status"])
                    if not self.artist:
                        self.artist = "Now Playing:"
                    self.artist_label = ScrollText(ARTIST_WIN, self.artist,
                                                   fonts['std'], (colors['font']),
                                                   bg_buf['artist_bg'], btn["Status"])
                    self.dirty = True
                    if not self.refresh:
                        self.event.remove('playlist')

                if 'player' in self.event or self.refresh:
                    status = MPC.status()
                    BTN_WIN[1].blit(bg_buf['btn1'], ((0, 0)))
                    BTN_WIN[2].blit(bg_buf['btn2'], ((0, 0)))
                    if 'state' in status:
                        if status['state'] == 'stop':
                            BTN_WIN[1].blit(btn["Play"], ((0, 0)))  # Empty
                            BTN_WIN[2].blit(btn["Empty"], ((0, 0)))  # Play
                        elif status['state'] == 'pause':
                            BTN_WIN[1].blit(btn["Stop"], ((0, 0)))  # stop
                            BTN_WIN[2].blit(btn["Play"], ((0, 0)))  # play
                        else:
                            BTN_WIN[1].blit(btn["Stop"], ((0, 0)))  # stop
                            BTN_WIN[2].blit(btn["Pause"], ((0, 0)))  # pause
                    self.event += 'mixer'
                    self.dirty_rects.append(BTN_RECT[1])
                    self.dirty_rects.append(BTN_RECT[2])
                    self.dirty_rects.append(BTN_RECT[4])
                    self.status_update = True
                    if not self.refresh:
                        self.event.remove('player')

                if 'mixer' in self.event or self.refresh:
                    BTN_WIN[4].blit(bg_buf['btn4'], ((0, 0)))
                    if self.muted == True:
                        BTN_WIN[4].blit(btn["Unmute"], ((0, 0)))  # unmute
                    else:
                        BTN_WIN[4].blit(btn["Mute"], ((0, 0)))  # mute
                    self.dirty_rects.append(BTN_RECT[4])
                    self.status_update = True
                    if not self.refresh:
                        self.event.remove('mixer')

                if self.refresh:
                    self.refresh = False
                    self.status_update = True
                    if not skincfg['text_on_top']:
                        BTN_WIN[0].blit(btn["Status"], ((0, 0)))  # msg_frame
                        self.dirty_rects.append(BTN_RECT[0])

                if self.sec:
                    self.sec = 0
                    self.status_update = True

                if self.status_update:
                    self.status_update = False
                    STATUS_WIN.blit(bg_buf['status_bg'], (0, 0))
                    BITRATE_WIN.blit(bg_buf['bitrate_bg'], (0, 0))
                    status_update()
                    if not skincfg['text_on_top']:
                        LCD.blit(btn["Status"], STATUS_RECT, area=STATUS_RECT)
                        LCD.blit(btn["Status"], BITRATE_RECT, area=BITRATE_RECT)
                    self.dirty_rects.append(BITRATE_RECT)
                    self.dirty_rects.append(STATUS_RECT)
                    pygame.display.update(self.dirty_rects)
                    self.dirty_rects = []

                self.station_label.update(self.dirty)
                self.title_label.update(self.dirty)
                self.artist_label.update(self.dirty)
                self.dirty = False

            elif self.menu == 2:  # Playlist Selection
                if 'playlist' in self.event or 'update' in self.event or self.refresh:
                    LCD.fill(colors['bg'])
                    if bg_buf['bg']:
                        LCD.blit(bg_buf['bg'], (0, 0))
                    if skincfg['text_on_top']:
                        skin2_base()
                    PLS.show()
                    if config['x_button'] and PLS.in_playlist:
                        pygame.draw.rect(PLUS_WIN, (colors['font']),
                                         PLUS_WIN.get_rect(), PLUS_WIN.get_width() // 7)
                        pygame.draw.line(PLUS_WIN, (colors['font']),
                                         (PLUS_WIN.get_width() // 4, PLUS_WIN.get_height() // 4),
                                         (PLUS_WIN.get_width() * 3 // 4, PLUS_WIN.get_height() * 3 // 4),
                                         PLUS_WIN.get_width() // 8)
                        pygame.draw.line(PLUS_WIN, (colors['font']),
                                         (PLUS_WIN.get_width() // 4, PLUS_WIN.get_height() * 3 // 4),
                                         (PLUS_WIN.get_width() * 3 // 4, PLUS_WIN.get_height() // 4),
                                         PLUS_WIN.get_width() // 8)
                    if config['plus_button']:
                        if PLS.lists[PLS.index][0] == 'd':
                            pygame.draw.rect(PLUS_WIN, (colors['font']),
                                             PLUS_WIN.get_rect(), PLUS_WIN.get_width() // 7)
                            pygame.draw.line(PLUS_WIN, (colors['font']),
                                             (PLUS_WIN.get_width() // 2, PLUS_WIN.get_height() // 4),
                                             (PLUS_WIN.get_width() // 2, PLUS_WIN.get_height() * 3 // 4),
                                             PLUS_WIN.get_width() // 8)
                            pygame.draw.line(PLUS_WIN, (colors['font']),
                                             (PLUS_WIN.get_width() // 4, PLUS_WIN.get_height() // 2),
                                             (PLUS_WIN.get_width() * 3 // 4, PLUS_WIN.get_height() // 2),
                                             PLUS_WIN.get_width() // 8)
                    if not skincfg['text_on_top']:
                        skin2_base()
                    self.select_label = \
                        ScrollText(LIST_WIN[0], re.sub(r"\.pls|\.m3u", "",
                                                       PLS.lists[PLS.index][1].split('/')[-1]),
                                   fonts['big'], PLS.lists[PLS.index][2],
                                   bg_buf['list_bg'], bg_buf['sel'])
                    pygame.display.flip()
                    if self.refresh:
                        self.refresh = False
                    if 'playlist' in self.event:
                        self.event.remove('playlist')
                    if 'update' in self.event:
                        self.event.remove('update')
                self.select_label.update()

            elif self.menu == 3:  # MPD Playback Settings
                if 'options' in self.event or self.refresh:
                    LCD.fill(colors['bg'])
                    if bg_buf['bg']:
                        LCD.blit(bg_buf['bg'], (0, 0))
                    if skincfg['text_on_top']:
                        skin3_base()
                    if self.xf_page:  # Crossfade Seite
                        get_xfade_state()
                    else:  # Basic Settings Seite
                        get_playback_state()
                    if not skincfg['text_on_top']:
                        skin3_base()
                    pygame.display.flip()
                    if self.refresh:
                        self.refresh = False
                    else:
                        self.event.remove('options')

            elif self.menu == 4:  # MPD Audio Outputs
                # Mindestens alle 5 Sekunden Aktualisieren
                if self.sec > 5:
                    self.sec = 0
                    self.refresh = True

                if self.refresh or 'output' in self.event:
                    LCD.fill(colors['bg'])
                    if bg_buf['bg']:
                        LCD.blit(bg_buf['bg'], (0, 0))
                    if skincfg['text_on_top']:
                        skin4_base()
                    draw_text(MSG_WIN, 'MPD Audio Outputs', fonts['std'],
                              colors['status'], align='centerx')
                    get_outputs()
                    current_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
                    draw_text(STATUS_WIN, current_time, fonts['std'], colors['status'])

                    # get and display ip
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.connect(('8.8.8.8', 0))  # dummy IP
                        ip_text = 'IP: ' + sock.getsockname()[0]
                        sock.close()
                    except OSError:
                        # <class 'OSError'>: [Errno 101] Network is unreachable
                        exctype, value = sys.exc_info()[:2]
                        print("Screen.update()", str(exctype) + ': ' + str(value))
                        ip_text = 'IP: No Network!'
                    # Wlan Level
                    wlanlevel = get_wlan_level(WLAN_DEVICE)
                    if wlanlevel >= 80:
                        STATUS_WIN.blit(btn["wlan100"],
                                        (STATUS_WIN.get_width() // 2 - \
                                         btn["wlan100"].get_width() // 2, 0))
                    elif wlanlevel >= 55:
                        STATUS_WIN.blit(btn["wlan075"],
                                        (STATUS_WIN.get_width() // 2 - \
                                         btn["wlan075"].get_width() // 2, 0))
                    elif wlanlevel >= 30:
                        STATUS_WIN.blit(btn["wlan050"],
                                        (STATUS_WIN.get_width() // 2 - \
                                         btn["wlan050"].get_width() // 2, 0))
                    elif wlanlevel >= 5:
                        STATUS_WIN.blit(btn["wlan025"],
                                        (STATUS_WIN.get_width() // 2 - \
                                         btn["wlan025"].get_width() // 2, 0))
                    else:
                        STATUS_WIN.blit(btn["wlan000"],
                                        (STATUS_WIN.get_width() // 2 - \
                                         btn["wlan000"].get_width() // 2, 0))
                    draw_text(STATUS_WIN, ip_text, fonts['std'], colors['status'], align='topright')
                    if not skincfg['text_on_top']:
                        skin4_base()
                    pygame.display.flip()
                    if self.refresh:
                        self.refresh = False
                    else:
                        self.event.remove('output')

            elif self.menu == 5:  # NewTron-Radio Settings
                if self.refresh:
                    self.refresh = False
                    LCD.fill(colors['bg'])
                    if bg_buf['bg']:
                        LCD.blit(bg_buf['bg'], (0, 0))
                    if skincfg['text_on_top']:
                        skin5_base()
                    show_config()
                    if not skincfg['text_on_top']:
                        skin5_base()
                    pygame.display.flip()

            elif self.menu == 6:  # Weather Screen
                if self.sec > 60 or self.refresh:  # Wetter jede Minute abfragen
                    self.sec = 0
                    WTR.show()
                if not self.tick and not self.sec % 5:  # Alle 5 Sekunden aktualisieren
                    self.refresh = True
                if self.refresh or 'playlist' in self.event:
                    show_ss_status()
                    if self.refresh:
                        self.refresh = False
                    else:
                        self.event.remove('playlist')

        else:  # self.screensaver == True:
            if config['screensaver_mode'] == 'weather':
                if self.sec > 600 or self.refresh:  # Wetter alle 10 Minuten abfragen
                    self.sec = 0
                    WTR.show()
                if not self.tick and not self.sec % 5:  # Alle 5 Sekunden aktualisieren
                    self.refresh = True
                if self.refresh or 'playlist' in self.event:
                    show_ss_status()
                    if self.refresh:
                        self.refresh = False
                    else:
                        self.event.remove('playlist')
            elif config['screensaver_mode'] == 'clock':
                if self.sec > 5 or self.refresh:
                    self.sec = 0
                    self.refresh = False
                    show_ss_status(big_clock=True)
            elif config['screensaver_mode'] == 'black':
                if self.sec > 600 or self.refresh:  # Alle 10 Minuten aktualisieren
                    self.sec = 0
                    self.refresh = False
                    LCD.fill(colors['bg'])
                    pygame.display.flip()
            else:
                self.screensaver = False


##### Ende der Funktions- und Klassendefinitionen ##########

def main():
    print("Hello World!")
    global WIDTH, HEIGHT, LCD, MSG_WIN, CHK_WIN, btn, STATUS_WIN, SS_WEATHER_WIN, SS_WEATHER_RECT, WEATHERPATH, MPC,\
        LIST_WIN, BITRATE_WIN, SKINBASE, BTN_WIN, LIST_WIN, STATION_WIN, ARTIST_WIN, TITLE_WIN, BTN_RECT, SS_TITLE_WIN,\
        SS_CLOCK_WIN, SS_TITLE_RECT, SS_CLOCK_RECT, PLS, PLUS_RECT, POS, SCR, CHK_RECT, STATUS_RECT, BITRATE_RECT,\
        PLUS_WIN, WTR, MINUTES
    # Initialisiere das Display und ermittle die Dimensionen
    WIDTH, HEIGHT = disp_init()
    pygame.init()
    pygame.font.init()
    print('Display area size: %d x %d' % (WIDTH, HEIGHT))
    if config['fullscreen']:
        LCD = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA | pygame.FULLSCREEN)
    else:
        LCD = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)

    ##### Festlegung der Zeichenbereiche #######################

    # dazu muss die Auflösung des Displays bekannt sein

    # Abstand des Textes von den Bildschirmrändern
    # relativ zur Basisgrösse des Skins (480x320)
    BORDER_TOP = 10 * HEIGHT // 320
    BORDER_SIDE = 20 * WIDTH // 480
    # Höhe der Fenster zur Textausgabe
    STD_HEIGHT = HEIGHT // 14
    BIG_HEIGHT = HEIGHT // 8

    # rects for Sreensaver and Weather
    SS_TITLE_WIN = LCD.subsurface(
        [0,
         HEIGHT - STD_HEIGHT * 4 // 3,
         WIDTH,
         STD_HEIGHT * 4 // 3])
    SS_TITLE_RECT = SS_TITLE_WIN.get_rect(topleft=SS_TITLE_WIN.get_abs_offset())

    SS_CLOCK_WIN = LCD.subsurface(
        [0,
         SS_TITLE_WIN.get_abs_offset()[1] - BIG_HEIGHT,
         WIDTH,
         BIG_HEIGHT])
    SS_CLOCK_RECT = SS_CLOCK_WIN.get_rect(topleft=SS_CLOCK_WIN.get_abs_offset())

    SS_WEATHER_WIN = LCD.subsurface(
        [0,
         0,
         WIDTH,
         SS_CLOCK_WIN.get_abs_offset()[1]])
    SS_WEATHER_RECT = SS_WEATHER_WIN.get_rect(topleft=SS_WEATHER_WIN.get_offset())

    # Fenster für alles innerhalb des msg_frames
    MSG_WIN = LCD.subsurface(
        [BORDER_SIDE,
         BORDER_TOP,
         WIDTH - 2 * BORDER_SIDE,
         HEIGHT // 2 - 2 * BORDER_TOP])

    # Fenster für den Stationsnamen (left,top,width,height)
    STATION_WIN = MSG_WIN.subsurface(
        [0,
         0,
         MSG_WIN.get_width() * 12 // 16,
         STD_HEIGHT])
    STATION_RECT = STATION_WIN.get_rect(topleft=STATION_WIN.get_abs_offset())

    # Fenster für die Anzeige der Bitrate (left,top,width,height)
    BITRATE_WIN = MSG_WIN.subsurface(
        [MSG_WIN.get_width() * 12 // 16,
         0,
         MSG_WIN.get_width() * 4 // 16,
         STD_HEIGHT])
    BITRATE_RECT = BITRATE_WIN.get_rect(topleft=BITRATE_WIN.get_abs_offset())

    # Fenster in dem der Künstler eingeblendet wird (left,top,width,height)
    ARTIST_WIN = MSG_WIN.subsurface(
        [0,
         MSG_WIN.get_height() // 2 - STD_HEIGHT * 4 // 3,
         MSG_WIN.get_width(),
         STD_HEIGHT])

    # Fenster in dem der Titel eingeblendet wird (left,top,width,height)
    TITLE_WIN = MSG_WIN.subsurface(
        [0,
         MSG_WIN.get_height() // 2,
         MSG_WIN.get_width(),
         MSG_WIN.get_height() // 2 - STD_HEIGHT])

    # Fenster für die Statusinfos (left,top,width,height)
    STATUS_WIN = MSG_WIN.subsurface(
        [0,
         MSG_WIN.get_height() - STD_HEIGHT,
         MSG_WIN.get_width(),
         STD_HEIGHT])
    STATUS_RECT = STATUS_WIN.get_rect(topleft=STATUS_WIN.get_abs_offset())

    PLUS_WIN = MSG_WIN.subsurface(
        [MSG_WIN.get_width() - STD_HEIGHT,
         MSG_WIN.get_height() // 2 - STD_HEIGHT * 2,
         STD_HEIGHT,
         STD_HEIGHT])
    PLUS_RECT = PLUS_WIN.get_rect(topleft=PLUS_WIN.get_abs_offset())

    # Bereiche für die Checkboxen
    CHK_WIN = [MSG_WIN.subsurface(
        [0,
         MSG_WIN.get_height() * 1 // 5 + STD_HEIGHT // 4,
         MSG_WIN.get_width() // 2,
         STD_HEIGHT]),
        MSG_WIN.subsurface(
            [MSG_WIN.get_width() // 2,
             MSG_WIN.get_height() * 1 // 5 + STD_HEIGHT // 4,
             MSG_WIN.get_width() // 2,
             STD_HEIGHT]),
        MSG_WIN.subsurface(
            [0,
             MSG_WIN.get_height() * 2 // 5 + STD_HEIGHT // 4,
             MSG_WIN.get_width() // 2,
             STD_HEIGHT]),
        MSG_WIN.subsurface(
            [MSG_WIN.get_width() // 2,
             MSG_WIN.get_height() * 2 // 5 + STD_HEIGHT // 4,
             MSG_WIN.get_width() // 2,
             STD_HEIGHT]),
        MSG_WIN.subsurface(
            [0,
             MSG_WIN.get_height() * 3 // 5 + STD_HEIGHT // 4,
             MSG_WIN.get_width() // 2,
             STD_HEIGHT]),
        MSG_WIN.subsurface(
            [MSG_WIN.get_width() // 2,
             MSG_WIN.get_height() * 3 // 5 + STD_HEIGHT // 4,
             MSG_WIN.get_width() // 2,
             STD_HEIGHT])]
    CHK_RECT = []
    for checkbox in CHK_WIN:
        CHK_RECT.append(checkbox.get_rect(topleft=checkbox.get_abs_offset()))

    # Fenster für die Playlistenauswahl
    LIST_WIN = [LCD.subsurface(
        [BORDER_SIDE,
         HEIGHT // 4 - BIG_HEIGHT * 2 // 5,
         WIDTH - 2 * BORDER_SIDE,
         BIG_HEIGHT]),
        LCD.subsurface(
            [BORDER_SIDE,
             HEIGHT // 4 - BIG_HEIGHT // 2 - STD_HEIGHT,
             # wg. config['x_button'] und config['plus_button']
             MSG_WIN.get_width() - STD_HEIGHT,
             STD_HEIGHT]),
        LCD.subsurface(
            [BORDER_SIDE,
             HEIGHT // 4 - BIG_HEIGHT // 2 - STD_HEIGHT * 2,
             MSG_WIN.get_width(),
             STD_HEIGHT]),
        LCD.subsurface(
            [BORDER_SIDE,
             HEIGHT // 4 + BIG_HEIGHT // 2 + STD_HEIGHT // 6,
             MSG_WIN.get_width(),
             STD_HEIGHT]),
        LCD.subsurface(
            [BORDER_SIDE,
             HEIGHT // 4 + BIG_HEIGHT // 2 + STD_HEIGHT * 7 // 6,
             MSG_WIN.get_width(),
             STD_HEIGHT])]

    BTN_WIN = [LCD.subsurface([0, 0, WIDTH, HEIGHT // 2]),  # Obere Hälfte des Screens
               LCD.subsurface([0, HEIGHT // 2, WIDTH // 4, HEIGHT // 4]),  # BTN1
               LCD.subsurface([WIDTH // 4, HEIGHT // 2, WIDTH // 4, HEIGHT // 4]),  # BTN2
               LCD.subsurface([WIDTH // 2, HEIGHT // 2, WIDTH // 4, HEIGHT // 4]),  # BTN3
               LCD.subsurface([WIDTH * 3 // 4, HEIGHT // 2, WIDTH // 4, HEIGHT // 4]),  # BTN4
               LCD.subsurface([0, HEIGHT * 3 // 4, WIDTH // 4, HEIGHT // 4]),  # BTN5
               LCD.subsurface([WIDTH // 4, HEIGHT * 3 // 4, WIDTH // 4, HEIGHT // 4]),  # BTN6
               LCD.subsurface([WIDTH // 2, HEIGHT * 3 // 4, WIDTH // 4, HEIGHT // 4]),  # BTN7
               LCD.subsurface([WIDTH * 3 // 4, HEIGHT * 3 // 4, WIDTH // 4, HEIGHT // 4]),  # BTN8
               LCD.subsurface([0, HEIGHT // 2, WIDTH, HEIGHT // 2])]  # Untere Hälfte des Screens

    # Touchbutton Positionen (LCD)
    btn = {}  # Buffer-Dict der Button-Grafiken
    BTN_RECT = []  # Rects der Buttons
    for IDX, ITEM in enumerate(BTN_WIN):
        BTN_RECT.append(ITEM.get_rect(topleft=ITEM.get_abs_offset()))

    ##### MPD Initialisierung ##################################
    # Verbinde mit MPD
    MPC = MPDClient()
    MPC.timeout = 10
    mpd_connect(MPC)
    # Kontrollverbindung für MPD-Events
    try:
        MPC.update()
    except CommandError as err:
        print("Init - MPC.update() ", err)
    if 'volume' in MPC.status():
        if int(MPC.status()['volume']) < 5:
            MPC.setvol(OLDVOL)
    else:
        print("could not set volume - continuing anyway...")

    ##### Skin management ######################################

    # Pfad zu den Button und Imagedateien des Skins
    SKINBASE = os.path.join(SCRIPTPATH, "skins")
    WEATHERPATH = os.path.join(SKINBASE, "weather")

    # Startbildschirm anzeigen
    SPLASHSCREEN = os.path.join(SKINBASE, "Splash.png")
    try:
        SPLASH_BUF = pygame.image.load(SPLASHSCREEN).convert_alpha()
        SPLASH_BUF = pygame.transform.smoothscale(SPLASH_BUF, (WIDTH, HEIGHT))
        LCD.blit(SPLASH_BUF, (0, 0))
        del SPLASH_BUF
    except pygame.error as err:
        print("Show Splash: ", err)
    pygame.display.flip()

    # Lese Konfigurationsdaten
    read_config()
    # Lade den Skin
    load_skin(config['skin'])

    # Hole Playlisten
    PLS = Playlists()
    PLS.initialize()

    # Wetterkonfiguration
    WTR = OpenWeatherMap()
    WTR.get_config()

    ###### Start der Anzeige ###################################

    SCR = Screen()

    # userevent on every minute, used for screensaver
    pygame.time.set_timer(pygame.USEREVENT, 60000)
    # userevent on every 30 seconds, used for MPC.ping()
    pygame.time.set_timer(pygame.USEREVENT + 1, 30000)
    SCLOCK = pygame.time.Clock()

    ##### Start der Eventschleife ##############################

    try:
        RUNNING = True
        while RUNNING:
            SCLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    MINUTES += 1
                if event.type == pygame.USEREVENT + 1:
                    # try to keep connection to mpd alive
                    try:
                        MPC.ping()
                    except ConnectionError:
                        mpd_connect(MPC)
                        MPC.stop()
                        MPC.play()
                        SCR.refresh = True
                    except:
                        EXCTYPE, VALUE = sys.exc_info()[:2]
                        print("Main loop", str(EXCTYPE) + ': ' + str(VALUE))
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                # if screensaver is enabled and the screen was touched,
                # just disable screensaver, reset timer and update screen
                # no button state will be checked
                try:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if SCR.screensaver:
                            SCR.refresh = True
                            MINUTES = 0
                            SCR.screensaver = False
                            # Wetteranzeige über Wolkenbutton wenn Screensaver = Wetter beenden
                            if SCR.menu == 6 and config['screensaver_mode'] == 'weather':
                                SCR.menu = 4
                        else:
                            # if screen was touched and screensaver is
                            # disabled, get position of touched button,
                            # reset timer and call button()
                            POS = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                            MINUTES = 0
                            for tbtn in range(len(BTN_RECT) - 1):
                                if BTN_RECT[tbtn].collidepoint(POS):
                                    SCR.button(tbtn)
                except KeyError:
                    pass
            # enable screensaver on timer overflow
            if MINUTES >= config['screensaver_timer']:
                if config['screensaver_mode'] != 'off':
                    if not SCR.screensaver:
                        SCR.refresh = True
                        SCR.screensaver = True
            try:
                SCR.update()
            except (ConnectionError, socket.error) as err:
                print('Connection Error (update): ' + str(err))
                mpd_connect(MPC)
                # MPC.idle()
                MPC.stop()
                MPC.play()
                SCR.refresh = True
    except KeyboardInterrupt:
        # Clean exit if Ctrl-C was pressed
        print("\nCtrl-C pressed - exiting...")
        pygame.quit()
        sys.exit()
    finally:
        MPC.disconnect()
        print("\nbye...\n")


if __name__ == "__main__":
    main()
