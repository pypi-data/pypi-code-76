import os
import subprocess

import numpy
import rasterio


def v2f(x, nodata):
    try:
        x = float(x)
        if (nodata is not None) and numpy.isclose(x, nodata):
            x = None
    except:
        x = None
    return x


def locationinfo(raster_path, points, loc='-wgs84'):
    num_of_points = len(points)
    if not os.path.exists(raster_path):
        raise FileExistsError(raster_path)
    if not isinstance(points, str):
        points = '\n'.join([f'{s[0]} {s[1]}' for s in points])

    nodata = rasterio.open(raster_path).nodata

    cmd = [
        'gdallocationinfo',
        raster_path,
        '-valonly',
        loc
    ]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    result, err = p.communicate(input=points.encode('utf-8'))
    result = result.decode()
    result = result.split('\n')
    result = result[:-1]
    result = [v2f(x, nodata) for x in result]
    assert len(result) == num_of_points
    return result
