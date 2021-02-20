#!/usr/bin python

import argparse
import base64
import logging

logging.basicConfig(level=logging.NOTSET,
                    format="%(asctime)s: [%(levelname)s]: %(message)s")

ALLOWED_FILE_FORMAT = ('jpg', 'png', 'jpeg', 'JPG', 'JPEG', 'TIF')


def main():
    parser = argparse.ArgumentParser(
        description='Convert Image into base64 format, supported format is jpg and png.')

    parser.add_argument(
        "-i", "--img", help="Input image or image path to convert into base64")

    args = parser.parse_args()
    if args.img:
        filename = str(args.img).split(".")
        try:
            logging.info("Received file format ['{}']".format(filename[1]))
            if filename[1] not in ALLOWED_FILE_FORMAT:
                logging.error("Bad extention!")
                exit(0)
        except IndexError:
            logging.error("Wrong input!")
            exit(0)
        try:
            with open(args.img, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                logging.info("Image encoding done")
            output_txt_name = filename[0] + "{}".format(".txt")
            output_file = open(output_txt_name, "wb")
            output_file.write(encoded_string)
            logging.info("Output file saved as '{}'".format(
                output_txt_name) + " in same directory")
        except FileNotFoundError:
            logging.error("File not found!")
            exit(0)
