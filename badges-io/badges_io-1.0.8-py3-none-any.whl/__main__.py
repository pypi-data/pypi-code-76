import argparse
import sys
import re

import badges_io.slug as slug
from badges_io.badges import upload, get_color


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", help="Where to post badge data", default='https://badges.vidstige.se')
    parser.add_argument("--user", help="User part of slug. Defaults to autodetect")
    parser.add_argument("--repo", help="Repo part of slug. Defaults to autodetect")
    parser.add_argument("--min", help="Max value for auto-computed color", type=int, default=0)
    parser.add_argument("--max", help="Max value for auto-computed color", type=int, default=100)
    parser.add_argument("--value", help="Value to compute color from", type=int, default=None)
    parser.add_argument('subject', help="Subject, e.g. 'coverage'")
    parser.add_argument('status', help="Subject, e.g. '97%'")
    parser.add_argument('color', help="Color, e.g. 'green' or a hex string", nargs='?')
    args = parser.parse_args()

    auto_user, auto_repo = slug.autodetect() if not args.user or not args.repo else (None, None)
    user, repo = args.user or auto_user, args.repo or auto_repo
    if user and repo:
        color = args.color
        if color is None:
            value = args.value
            if value is None:
                match = re.search(r'[\d\.]+', args.status)
                if match:
                    value = float(match.group())
            if value is None:
                print('No color nor value specified', file=sys.stderr)
            color = get_color(args.min, args.max, value)

        svg = upload(
            args.url, user, repo,
            args.subject, args.status, color)
        print(svg)
    else:
        print("Could not auto detect slug and --user and --repo not given", file=sys.stderr)
        return -1

    return 0


if __name__ == "__main__":
    sys.exit(main())
