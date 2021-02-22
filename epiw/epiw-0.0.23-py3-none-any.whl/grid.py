import os
import shutil
import subprocess
import tempfile
import urllib.request

import rasterio
from dateutil.parser import parse as parse_date
from dateutil.rrule import DAILY, HOURLY, rrule

from epiw import read_as_gpd

_cell_size = 10000
_left, _bottom, _right, _top = 746100, 1458570, 1387980, 2068800


def grid(
        src_path,
        dst_path,
        field,
        query=None, left=_left, bottom=_bottom, right=_right, top=_top, cell_size=_cell_size,
        crs='EPSG:5179',
        algorithm='invdistnn:radius=999999999,max_points=3'
):
    tmp_path = f'{dst_path}.tmp'

    minx = left
    miny = bottom
    maxx = right
    maxy = top

    sizex = int((maxx - minx) / cell_size + 0.5)
    sizey = int((maxy - miny) / cell_size + 0.5)

    maxx = minx + sizex * cell_size
    miny = maxy - sizey * cell_size

    cmd = [
        'gdal_grid',
        '-q',
        '-of', 'GTiff',
        '-ot', 'float32',
        '-co', 'compress=deflate',
        '-co', 'tiled=yes',
        '-zfield', field,
        '-a_srs', crs,
        '-txe', str(minx), str(maxx),
        '-tye', str(maxy), str(miny),
        '-where', f'{field} is not null',
        '-outsize', str(sizex), str(sizey),
        '-a', algorithm,
        src_path,
        tmp_path
    ]

    if query:
        cmd.append('-query')
        cmd.append(query)

    print(' '.join(cmd))

    env = os.environ
    proc = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = proc.communicate()
    if out:
        try:
            out = out.decode('utf-8')
        except:
            pass

        try:
            err = err.decode('utf-8')
        except:
            pass

        raise Exception(f'Failed to run gdal_grid!\nproc.returncode:{proc.returncode}\nerr:{err}\nout:{out}')
    shutil.move(tmp_path, dst_path)


def prepare_elev_collection(cell_size, ignore_original_dem=False, ignore_warped_dem=False):
    temp_dir = tempfile.gettempdir()
    temp_dir = f'{temp_dir}/epiw/'
    os.makedirs(temp_dir, exist_ok=True)

    original_dem_file_path = f'{temp_dir}/dem.tiff'
    warped_dem_file_path = f'{temp_dir}/dem.{cell_size}m.tiff'

    if not os.path.exists(original_dem_file_path) or ignore_original_dem:
        temp_path = f'{original_dem_file_path}.tmp'
        urllib.request.urlretrieve(
            'https://aggregate.epinet.kr/data/static/2020/dem/dem.tiff',
            temp_path
        )
        os.rename(temp_path, original_dem_file_path)

    if not os.path.exists(warped_dem_file_path) or ignore_original_dem or ignore_warped_dem:
        temp_path = f'{warped_dem_file_path}.tmp'
        os.system(
            f'gdalwarp '
            f'-overwrite '
            f'-of GTiff '
            f'-ot float32 '
            f'-co compress=deflate -co tiled=yes '
            f'-r bilinear '
            f'-tr {cell_size} {cell_size} '
            f'{original_dem_file_path} '
            f'{temp_path}'
        )
        os.rename(temp_path, warped_dem_file_path)

    return warped_dem_file_path


def create_grid(
        category,
        interval,
        field,
        begin,
        output_dir,
        until=None,
        query=None,
        left=_left,
        bottom=_bottom,
        right=_right,
        top=_top,
        cell_size=_cell_size,
        crs='EPSG:5179',
        algorithm='invdistnn:radius=999999999,max_points=3',
        elev_correction=None,
        ignore_original_dem_cache=False,
        ignore_warped_dem_cache=False,
):
    begin = isinstance(begin, str) and parse_date(begin)
    until = isinstance(until, str) and parse_date(until) or begin

    itv = {
        'hourly': HOURLY,
        'daily': DAILY,
    }[interval]
    dates = rrule(itv, begin, until=until)

    output_format = {
        'hourly': f'{output_dir}/%Y/%m/%d/{field}.%Y%m%dT%H%M%S.tiff',
        'daily': f'{output_dir}/%Y/%m/%d/{field}.%Y%m%d.tiff'
    }[interval]

    wapred_dem_path = prepare_elev_collection(cell_size, ignore_original_dem_cache, ignore_warped_dem_cache)

    created_files = []

    for date in dates:
        output_path = date.strftime(output_format)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            vect_file_path = f'{output_path}.json'
            data = read_as_gpd(category, interval, date, fields=[field])
            if data.empty:
                print(f'# Warning: retrieved data is null {category}/{interval}/{date}/{field}')
                continue
            data['value'] = data[field]
            if elev_correction:
                data['value'] -= elev_correction(data['elev'])
            data = data.set_crs(4326).to_crs(5179)
            data.drop(['tm'], axis=1).to_file(vect_file_path, driver='GeoJSON')

            tmp_path = f'{output_path}.tmp'
            grid(
                vect_file_path,
                tmp_path,
                'value',
                query=query,
                left=left,
                bottom=bottom,
                right=right,
                top=top,
                cell_size=cell_size,
                crs=crs,
                algorithm=algorithm,
            )

            if elev_correction:
                r1 = rasterio.open(wapred_dem_path)
                d1 = r1.read(1)

                r2 = rasterio.open(tmp_path)
                d2 = r2.read(1)

                d2 += elev_correction(d1)

                r3 = rasterio.open(tmp_path, 'w', **r1.profile)
                r3.write(d2, 1)
                r3.close()

            os.rename(tmp_path, output_path)

            created_files.append(output_path)

    return created_files
