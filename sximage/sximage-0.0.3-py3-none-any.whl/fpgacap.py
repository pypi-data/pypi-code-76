import os
import sys
import time
import argparse

from .sximage import open_fpga, close_fpga, call_fpga

def fpgacap():
    parser = argparse.ArgumentParser(prog='fpgacap', description='SxImage FPGA CLI')
    parser.add_argument('-d','--decimal', action='store_true', help='decimal display')
    parser.add_argument('-u','--unsigned', action='store_true', help='unsigned display')
    parser.add_argument('-r','--rgb', action='store_true', help='rgb image')
    parser.add_argument('-g','--gray', action='store_true', help='grayscale image')
    parser.add_argument('-w','--width', type=int, default=None)
    parser.add_argument('-l','--loop', action='store_true')
    parser.add_argument('-o','--out', default=None)
    parser.add_argument('--interval', type=int, default=200)
    parser.add_argument('port')
    args = parser.parse_args()

    if args.rgb or args.gray:
        import cv2
        import numpy as np

    if args.rgb or args.gray:
        if not args.width:
            print('The width option must be present with --rgb or --gray')
            sys.exit(1)
    elif args.loop:
        if not args.width:
            print('The width option must be present with --loop')
            sys.exit(1)

    frameno = 0
    if args.loop and args.out:
        while frameno < 9999:
            name = "%s-%04d.tiff" % (args.out, frameno)
            if not os.path.exists(name):
                break
            frameno += 1
        if frameno >= 10000:
            print('Exceeded maximum frame series')
            sys.exit(1)
        if frameno > 0:
            print('Resuming capture series at '+name)

    def calc_size():
        if args.rgb:
            return (args.width, args.width * 3)
        elif args.gray:
            return (args.width, args.width)
        return (args.width, 1)

    def toint(b):
        if b > 127:
            return int(b) - 256
        return int(b)

    def emit(buf):
        if args.decimal:
            print('\t'.join(['%d' % toint(x) for x in buf]))
        elif args.unsigned:
            print('\t'.join(['%d' % x for x in buf]))
        else:
            print(buf.hex())

    def write_img(img):
        global frameno
        if args.loop:
            name = "%s-%04d.tiff" % (args.out, frameno)
            cv2.imwrite(name, img)
            frameno += 1
        else:
            cv2.imwrite(args.out, img)

    def show_rgb(ba, width, height):
        img = np.fromstring(ba, dtype=np.uint8).reshape(height, width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('capture', img)
        if args.out:
            write_img(img)

    def show_gray(ba, width, height):
        img = np.fromstring(ba, dtype=np.uint8).reshape(height, width)
        cv2.imshow('capture', img)
        if args.out:
            write_img(img)

    if args.loop:
        secs = args.interval / 1000.0
        (n, sz) = calc_size()
        open_fpga(args.port)
        while True:
            data = call_fpga(sz, n)
            if len(data) == (n * sz):
                if args.rgb:
                    show_rgb(data, args.width, args.width)
                    cv2.waitKey(args.interval)
                elif args.gray:
                    show_gray(data, args.width, args.width)
                    cv2.waitKey(0)
                else:
                    emit(data)
                    time.sleep(secs)
            else:
                print('Read timeout');
                time.sleep(secs)
    elif args.width:
        (n, sz) = calc_size()
        open_fpga(args.port)
        data = call_fpga(sz, n)
        if len(data) == (n * sz):
            if args.rgb:
                show_rgb(data, args.width, args.width)
                cv2.waitKey(0)
            elif args.gray:
                show_gray(data, args.width, args.width)
                cv2.waitKey(0)
            else:
                emit(data)
        else:
            print('Read timeout');
    else:
        ser = open_fpga(args.port)
        ser.write(b' ')
        while True:
            x = ser.read()
            if len(x):
                emit(x)
            else:
                break

    close_fpga()

if __name__ == '__main__':
    fpgacap()
