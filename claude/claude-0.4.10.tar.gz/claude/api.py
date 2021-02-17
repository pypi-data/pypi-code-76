import asyncio
import json
import logging
import re
import subprocess
from datetime import date, timedelta
from functools import wraps
from io import StringIO
import pychromecast


from aiohttp import ClientSession, web, BasicAuth
from lxml import etree

from .controller_base import ControllerBase
from .controller_cache import ControllerCache
from .tools import parse_temp, tree_search
from .transmission import Transmission, TransmissionError

logger = logging.getLogger(__name__)

ping_pattern = re.compile(r'64 bytes from ([0-9\.]{7,15}): icmp_.eq=([0-9]{1,2}) ttl=([0-9]{1,4}) time=([0-9\.]{1,7}) ms')

parser = etree.HTMLParser()

def route(path, method = 'GET'):
    def decor(func):
        func._route_data = (path, method)
        return func
    return decor

class CalledProcessorError(Exception):

    def __init__(self, code, stdout, stderr):
        self.code = code
        self.stdout = stdout
        self.stderr = stderr
        super().__init__("CalledProcessorError code %s" % code)

async def check_output(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout = asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise CalledProcessorError(proc.returncode, stdout, stderr)
    return stdout


async def get_json(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(content_type = None)

async def get_xml(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            return etree.parse(StringIO(text), parser)

cache = ControllerCache()

class Api(ControllerBase):

    def __init__(self, app: web.Application):
        for name in dir(self):
            func = getattr(self, name)
            if not hasattr(func, '_route_data'):
                continue
            (path, method) = func._route_data

            app.router.add_route(method, '/api' + path, func)

    @route('/server-status', 'POST')
    async def server_status(self, request: web.Request):

        config = await request.json()

        ip = config['ip']
        status_server_port = config['statusServerPort']

        cnt = 4

        logger.debug("Pinging %s ...", ip)
        try:
            ping_raw = await check_output('ping %s -c %d -i 0.2' % (ip, cnt))
        except CalledProcessorError as e:
            logger.debug("Ping failed %s", e)
            return web.json_response({"ping": None})

        time_sum = 0
        for match in re.finditer(ping_pattern, ping_raw.decode()):
            time_sum += float(match.group(4))

        try:
            server_details = await get_json('http://%s:%s/' % (ip, status_server_port))
        except Exception as e:
            logger.info("Cannot reach %s:%s because %s", ip, status_server_port, e)
            server_details = {}

        return web.json_response({
            'ping': round(time_sum / cnt, 1),
            **server_details,
        })

    @route('/idokep/current/{city}')
    @cache.cached_json_controller(timedelta(minutes = 10))
    async def idokep_current(self, request: web.Request):

        city = request.match_info.get('city')

        base_url = 'https://www.idokep.hu'

        logger.debug("Fetch data from %s", base_url)

        tree = await get_xml('%s/idojaras/%s' % (base_url, city))

        current_container = tree_search('.current-weather-lockup', tree)

        res = {
            'img': base_url + tree_search('.current-weather-icon > img', current_container).attrib['src'],
            'value': parse_temp(tree_search('.current-temperature', current_container).text),
        }

        return res

    @route('/idokep/days/{city}')
    @cache.cached_json_controller(timedelta(hours = 3))
    async def idokep_days(self, request):

        base_url = 'https://www.idokep.hu'

        logger.debug("Fetch data from %s", base_url)
        tree = await get_xml('%s/elorejelzes/%s' % (base_url, request.match_info.get('city')))

        day_columns = tree_search('.dailyForecastCol', tree, False)

        res = []

        col_date = None

        for day_column in day_columns:
            day_cell = tree_search('.dfColHeader .dfDayNum', day_column)
            if day_cell is None:
                continue

            precipitation_val = 0
            precipitation_prob = 0

            day = int(day_cell.text)

            if col_date is None:
                col_date = date.today()
                while col_date.day != day:
                    col_date = col_date + timedelta(days = 1)

            icons_tree = tree_search('.dfIconAlert', day_column)
            # if icons_tree is not None:
            #     prec_val_text = tree_search('.buborek-lent .buborek-sor .buborek-text .csapadek-text', icons_tree).text
            #     prec_prob_text = tree_search('.buborek-lent .buborek-sor .buborek-text .valoszinuseg', icons_tree).text
            #     precipitation_matches = re.search(r'Kb\. ([\d]{1,}) mm', prec_val_text)
            #     precipitation_val = precipitation_matches.group(1) if precipitation_matches else 0
            #     precipitation_prob = re.search(r'.+ ([\d]{1,})%', prec_prob_text).group(1)

            day_data = {
                # 'img': base_url + tree_search('.icon > svg > image', day_column).attrib['xlink:href'],
                'img': base_url + tree_search('.forecast-icon', day_column).attrib['src'],
                'day': day,
                'date': str(col_date),
                'max': int(tree_search('.max a', day_column).text.strip()),
                'min': int(tree_search('.min a', day_column).text.strip()),
                'precipitation': {
                    'value': int(precipitation_val),
                    'probability': int(precipitation_prob),
                },
            }
            res.append(day_data)

            col_date = col_date + timedelta(days = 1)

        return res

    @route('/idokep/hours/{city}')
    @cache.cached_json_controller(timedelta(minutes = 30))
    async def idokep_hours(self, request):

        base_url = 'https://www.idokep.hu'

        logger.debug("Fetch data from %s", base_url)
        tree = await get_xml('%s/elorejelzes/%s' % (base_url, request.match_info.get('city')))

        hour_columns = tree_search('.hourly-forecast-card', tree, False)

        res = []

        for hour_column in hour_columns:
            hour_cell = tree_search('.hourly-forecast-hour', hour_column)
            if hour_cell is None:
                continue

            # prec_val_tree = tree_search('.csapadek-text', day_column)
            # prec_prob_tree = tree_search('.valoszinuseg', day_column)
            precipitation_val = 0
            precipitation_prob = 0

            # if prec_val_tree is not None:
            #     precipitation_val = float(re.search(r'Kb\. ([\.\d]{1,}) .m', prec_val_tree.text).group(1))
            #
            # if prec_prob_tree is not None:
            #     precipitation_prob = float(re.search(r'.+ ([\.\d]{1,})%', prec_prob_tree.text).group(1))

            # wind_element = tree_search('.hourly-wind .wind', hour_column)

            hour_data = {
                'hour': int(hour_cell.text.split(":")[0]),
                'img': base_url + tree_search('.forecast-icon', hour_column).attrib['src'],
                'temp': int(tree_search('.temperature-circled', hour_column).text),
                'precipitation': {
                    'value': precipitation_val,
                    'probability': precipitation_prob,
                },
                'wind': {
                    'img': "",
                    'angle': 0,
                },
                # 'wind': {
                #     'img': base_url + wind_element.attrib['src'],
                #     'angle': int(re.search(r'rotate\(([\d]{1,3})deg\)', wind_element.attrib['style']).group(1)),
                # },
            }

            res.append(hour_data)

        print(res)

        return res

    @route('/chromeasts')
    @cache.cached_json_controller(timedelta(minutes = 5))
    async def chromecast_list(self, request):
        chromecasts = pychromecast.get_chromecasts()

        return [cc.device.friendly_name for cc in chromecasts]

    @route('/transmission', 'POST')
    async def transmission(self, request):

        config = await request.json()

        client = Transmission(config['url'], config.get('username'), config.get('password'))

        try:
            return web.json_response({
                'data': {
                    'session-stats': await client.session_stats(),
                    'torrents': await client.torrent_list(),
                },
                'status': 'success'
            })
        except TransmissionError as e:
            return web.json_response({
                'data': str(e),
                'status': 'error'
            })
