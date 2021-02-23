import argparse
import os
import sys


parser = argparse.ArgumentParser(
    description="CLI for interacting with the Arc Web Framework")


parser.add_argument(
    "Data",
    metavar="data",
    type=str,
    help="test"
)

args = parser.parse_args()

path = args.Data

print("Repeated" + data)
