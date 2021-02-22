import datetime
import math
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

RE = 6371.00877  # 지구 반경(km)
GRID = 5.0  # 격자 간격(km)
SLAT1 = 30.0  # 투영 위도1(degree)
SLAT2 = 60.0  # 투영 위도2(degree)
OLON = 126.0  # 기준점 경도(degree)
OLAT = 38.0  # 기준점 위도(degree)
XO = 43  # 기준점 X좌표(GRID)
YO = 136  # 기1준점 Y좌표(GRID)


def radians(x):
    return x / 180.0 * math.pi


def degrees(x):
    return x * 180.0 / math.pi


def xy2lonlat(v1, v2, reverse=False):
    return lonlat2xy(v1, v2, not reverse)


def lonlat2xy(v1, v2, reverse=False):
    re = RE / GRID
    s_lat1 = radians(SLAT1)
    s_lat2 = radians(SLAT2)
    o_lon = radians(OLON)
    o_lat = radians(OLAT)

    sn = math.tan(math.pi * 0.25 + s_lat2 * 0.5) / math.tan(math.pi * 0.25 + s_lat1 * 0.5)
    sn = math.log(math.cos(s_lat1) / math.cos(s_lat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + s_lat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(s_lat1) / sn
    ro = math.tan(math.pi * 0.25 + o_lat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    if (reverse):
        x = v1
        y = v2

        xn = x - XO
        yn = ro - y + YO
        ra = math.sqrt(xn * xn + yn * yn)
        if sn < 0.0:
            ra = -ra
        a_lat = math.pow((re * sf / ra), (1.0 / sn))
        a_lat = 2.0 * math.atan(a_lat) - math.pi * 0.5

        theta = 0.0
        if abs(xn) > 0.0:
            if abs(yn) <= 0.0:
                theta = math.pi * 0.5
                if xn < 0.0:
                    theta = -theta
            else:
                theta = math.atan2(xn, yn)
        a_lon = theta / sn + o_lon

        lon = degrees(a_lon)
        lat = degrees(a_lat)

        return [lon, lat]
    else:
        lon = radians(v1)
        lat = radians(v2)

        ra = math.tan(math.pi * 0.25 + lat * 0.5)
        ra = re * sf / math.pow(ra, sn)
        theta = lon - o_lon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        if theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= sn

        x = math.floor(ra * math.sin(theta) + XO + 0.5)
        y = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

        return [x, y]


def lazy_float(x):
    try:
        return float(x)
    except:
        pass
    return x


def latest_dwf(lon, lat):
    x, y = lonlat2xy(lon, lat)
    url = f'https://www.kma.go.kr/wid/queryDFS.jsp?gridx={x}&gridy={y}'
    url = urllib.request.Request(url)

    resp = urllib.request.urlopen(url)
    resp = resp.read()
    resp = resp.decode('utf-8')

    root = ET.fromstring(resp)

    tm = None
    ts = None
    items = []
    for child1 in root:
        if child1.tag == 'header':
            for child2 in child1:
                if child2.tag == 'tm':
                    tm = datetime.datetime.strptime(child2.text, '%Y%m%d%H%M')
                if child2.tag == 'ts':
                    ts = int(child2.text)
        elif child1.tag == 'body':
            for child2 in child1:
                item = {
                    x.tag: lazy_float(x.text)
                    for x in child2
                }
                items.append(item)
    return dict(
        tm=tm,
        ts=ts,
        items=items,
    )


if __name__ == '__main__':
    import sys

    lon = float(sys.argv[1])
    lat = float(sys.argv[1])
    print(lon, lat)
    v = latest_dwf(lon, lat)
    print(v)
