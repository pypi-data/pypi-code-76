#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Bamboo - 20201109Mon


import os
import sys
import time
import re
from pathlib import Path
import requests
import argparse
import autosub


SUPPORTED_VIDEO = ['.mp4', '.MP4', '.MOV', '.mov']


def is_video(file):
    sfx = file.suffix
    if sfx in SUPPORTED_VIDEO:
        return True


def is_srt(file):
    sfx = file.suffix
    if sfx in ['.srt']:
        return True


def check_path(path):
    return True if Path(path).exists() else False


def ensure_folder(path):
    if not path.is_dir():
        path = path.parent
    if not path.exists():
        path.mkdir(parents=False)


def get_srts(path):
    path = Path(path)
    videos = [_ for _ in path.rglob('*') if is_video(_)]
    for video in videos:
        autosub.generate_subtitles(video)


def youdao_trans(text, t_type='AUTO'):
    text = text.replace(' ', '%20')
    url = 'http://fanyi.youdao.com/translate?&doctype=json&type=' + t_type + '&i=' + text
    # header = {}
    out = requests.get(url)
    out_json = out.json()
    out_tgt = out_json['translateResult'][0][0]['tgt']
    return out_tgt


def trans_srt(path):
    path = Path(path)
    srts = [_ for _ in path.rglob('*.srt')]
    print('{} srts will be trans'.format(len(srts)))
    for srt in srts:
        srttxt = srt.read_text()
        pattern = r'(\d+)\s*\n(\d+:\d+:\d+,\d+\s?-->\s?\d+:\d+:\d+,\d+)\s*\n(.+)\n\n'
        sentences = re.findall(pattern, srttxt)
        sentences_cn = []
        for sentence in sentences:
            txt = sentence[-1]
            cntxt = youdao_trans(txt)
            sentencestr = '\n'.join(sentence)
            new_sentence = '{}\n{}'.format(sentencestr, cntxt)
            sentences_cn.append(new_sentence)
        trans_sentence = '\n\n'.join(sentences_cn)
        srt.write_text(trans_sentence)


def combine_video(path, quality, rest):
    cmd = 'ffmpeg -i "{vf}" -strict -2 ' \
        '-vf subtitles="{sf}":force_style="Fontsize=20\,FontName=Heiti SC" ' \
        '-qscale:v {q} -threads 2 "{of}"'
    path = Path(path)
    srts = [_ for _ in path.rglob('*.srt')]
    for srt in srts:
        try:
            video = [_ for _ in path.rglob('*') if is_video(_) and _.stem == srt.stem][0]
        except IndexError:
            print('{} not corresponding video'.format(srt.stem))
            raise
        output = srt.parent / 'output_{}'.format(srt.parent.parts[-1]) / \
                '{}.output.mp4'.format(srt.stem)
        ensure_folder(output)
        os.system(cmd.format(vf=video, sf=srt, of=output, q=int(quality)))
        if len(srts) > 1:
            time.sleep(int(rest))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dictate', nargs=1,
                        help='dictate video files and generate srt files')
    parser.add_argument('-t', '--translate', nargs=1,
                        help='translate dictated srt files')
    parser.add_argument('-c', '--combine', nargs=1,
                        help='combine video-srt pairs to new subtitled-video')
    parser.add_argument('-q', '--quality', default=0,
                        help='ffmpeg combine quality setting, default=0')
    parser.add_argument('-r', '--rest', default=20,
                        help='rest time for computer in seconds')
    args = parser.parse_args()
    if args.dictate:
        get_srts(args.dictate[0])
    if args.translate:
        trans_srt(args.translate[0])
    if args.combine:
        combine_video(args.combine[0], args.quality, args.rest)


if __name__ == '__main__':
    sys.exit(main())

