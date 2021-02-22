from datetime import datetime, timedelta
import json
import logging

import requests

def pypi_stats(package_name):
    url = f'https://pypistats.org/api/packages/{package_name}/overall'
    r = requests.get(url)
    res = r.json()
    downloads = [
        (d['date'], d['downloads']) for d in res['data']
        if d['category'] == 'without_mirrors']
    tot_downloads = sum(int(download_n) for _date, download_n in downloads)
    return ("SuperHELP - Total PyPI downloads (non-mirrored): "
        f"{tot_downloads:,}")

def github_stats():
    """
    Better to look at Insights>traffic (available to me given I have upload
    permissions). But only 14 days. And what python-trending cares about is
    stars - that's it!
    """
    url = 'https://api.github.com/repos/grantps/superhelp/releases'
    #url = 'https://api.github.com/repos/psf/requests/releases'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Unable to get data from GitHub :-(")
        return
    data = r.json()
    tot_downloads = 0
    for release in data:
        for asset in release.get('assets', []):
            tot_downloads += int(asset['download_count'])
    return f"SuperHELP - Total GitHub Asset Downloads: {tot_downloads:,}"

def binderhub_stats():
    yesterday = datetime.today().date() - timedelta(days=1)
    yesterday_str = yesterday.isoformat()
    url = f"https://archive.analytics.mybinder.org/events-{yesterday_str}.jsonl"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Unable to read data - HTTP status code {r.status_code}")
    raw_jsonl = r.text
    lines = [line for line in raw_jsonl.split('\n') if line]
    records = []
    for n, line in enumerate(lines, 1):
        try:
            line_data = json.loads(line)
            spec = line_data['spec'].split('/')[0]
            if 'superhelp' not in spec.lower():
                continue
            records.append(line_data)
        except json.JSONDecodeError as e:
            logging.debug(f"Failed on line {n:,} out of {len(lines)} total lines "
                f"with {e} - original line '{line}'")
    for record in records:
        print(record)
    return f"{len(records):,} total records on '{yesterday_str}'"


print(pypi_stats(package_name='superhelp'))
# print(binderhub_stats())
#print(github_stats())

