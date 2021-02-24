#!/usr/bin/python
from .extractors._rules import allDirectRules, directRules
from .extractors import Base
from . import __version__
from urllib.parse import urlparse
from shutil import get_terminal_size
from pkg_resources import parse_version
from .thirdparty.exrex import getone as regex_to_string, generate as generate_strings
import os
import glob
import importlib
import logging
import PyInquirer
import sys
import argparse
import re
import json
import colorama
colorama.init()


basedir = os.path.join(os.path.dirname(__file__), "extractors")
for file in glob.glob(f"{basedir}/*.py"):
    filename = os.path.basename(file)
    if not filename.startswith("__"):
        importlib.import_module(f"lk21.extractors.{filename[:-3]}")

logging.basicConfig(format=f"\x1b[K%(message)s", level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


def parse_range(raw):
    assert re.match(r"[\s\d:]+", raw), f"invalid syntax: {raw!r}"
    if "," in raw:
        for rg in re.split(r"\s*,\s*", raw):
            if ":" not in rg:
                yield rg
            else:
                assert len(re.findall(r":", raw)
                           ) <= 1, f"invalid syntax: {raw!r}"
                yield from parse_range(rg)
    else:
        spl = re.split(r"\s*:\s*", raw)
        if not spl[0]:
            spl[0] = "1"

        start, end = map(lambda x: int(x) if x else None, spl)
        if end:
            assert start < end, "angka pertama tidak boleh lebih dari angka kedua"
            yield from range(start, end + 1)
        else:
            while True:
                yield start
                start += 1


def title(text, rtn=False):
    r = f" [\x1b[92m{text}\x1b[0m]"
    if rtn:
        return r
    logging.info(r)


def _check_version():
    try:
        base = Base()
        raw = base.session.get("https://pypi.org/project/lk21", timeout=2)
        soup = base.soup(raw)

        if (name := soup.find(class_="package-header__name")):
            version = name.text.split()[-1]
            fmt = "{{0:0<{}}}".format(max(len(version), len(__version__)))
            if parse_version(fmt.format(__version__)) < parse_version(fmt.format(version)):
                return (
                    "\x1b[93m"
                    f"WARNING: Anda menggunakan lk21 versi {__version__}, sedangkan versi {version} telah tersedia.\n"
                    "Anda harus mempertimbangkan untuk mengupgrade melalui perintah 'python -m pip install --upgrade lk21'."
                    "\x1b[0m")
    except Exception:
        return


def recursive_choice(extractor, result):
    prevresult = None
    index = 0
    last = False
    while True:
        keys = [
            f"{key} (direct)" if isinstance(
                value, str) and allDirectRules.search(value) else key
            for key, value in result.items() if value
        ]
        if prevresult and index > 0:
            keys.extend([PyInquirer.Separator(), "00. Kembali"])
        key = extractor.choice(keys)

        if key == "00. Kembali":
            last = False
            result = prevresult
            index -= 1
        else:
            prevresult = result
            result = result[key]
            index += 1
            if last:
                break
        if not all(isinstance(v, dict) for v in result.values()):
            last = True
    if result.startswith("re:"):
        id = extractor.getPath(result.removeprefix("re:"))
        logging.info(f"Mengekstrak link unduhan: {id}")
        result = extractor.extract(id)
        result = recursive_choice(extractor, result)
    return result


def main():
    global extractor

    extractors = {
        obj.__name__: obj for obj in Base.__subclasses__() if obj
    }
    _version_msg = _check_version()

    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=get_terminal_size().lines),
        epilog=_version_msg)
    parser.add_argument("query", metavar="query",
                        nargs="*", help="kueri, judul, kata kunci")
    parser.add_argument("-v", "--version", action="store_true", help="show version and exit")
    parser.add_argument("-d", "--debug", action="store_true",
                        help=argparse.SUPPRESS)
    parser.add_argument("-p", metavar="page", dest="page",
                        help=("halaman situs, contoh penggunaan:\n"
                              "  - 1,2,3\n"
                              "  - 1:2, 2:8\n"
                              "  - 1,2,3:8\n"
                              "  - default halaman pertama\n"
                              "    dan seterusnya"), type=str, default="1:")
    parser.add_argument("-i", "--information", dest="info",
                        action="store_true", help="cetak informasi dari item yang dipilih")
    parser.add_argument("-c", "--command", metavar="cmd",
                        help=("jalankan 'perintah' dengan argument berupa\n"
                              "url yang dipilih.\n\n"
                              "contoh: axel2 {}"))

    valid_e_rules = re.compile(
        r"\[\^.+?\][+*]")
    valid_allDirectRules = valid_e_rules.sub("[A-Za-z0-9-.]{5,7}", allDirectRules.pattern)
    parser.add_argument("-e", "--extract-direct", metavar="url",
                        help=("bypass situs download\n\n"
                              f"contoh url: {regex_to_string(valid_allDirectRules, 3)!r}\n"
                              ))

    parser.add_argument("--list-direct-rules", action="store_true",
                        help="cetak semua daftar situs download yang dapat\ndi-bypass")

    extractor_group = parser.add_argument_group("Daftar Extractor",
                                                description=(
                                                    f"pilih salah satu dari ke-{len(extractors)} situs berikut:"
                                                ))
    extractor = extractor_group.add_mutually_exclusive_group()
    for egn, kls in extractors.items():
        if hasattr(kls, "host"):
            pa = urlparse(kls.host)
            for index in range(1, len(egn)):
                try:
                    arg = [f"-{egn[:index]}"]
                    if arg[0] != f"-{egn}":
                        arg.append(f"--{egn}")
                    extractor.add_argument(*arg, action="store_true",
                                           help=f"site: {pa.scheme}://{pa.netloc} [{kls.tag}]")
                    break
                except argparse.ArgumentError:
                    continue
    args = parser.parse_args()

    if args.version:
        sys.exit(__version__)

    _direct = extractors.pop("_direct")(logging)

    if args.list_direct_rules:
        add_color = lambda x: x.replace(r"[id]", "\x1b[32m[id]\x1b[0m")
        for name, (rule, _) in directRules.items():
            if _ is not None:
                valid_url = re.sub(r"\[\^.+?\][+*]|\\[a-zA-Z][+*]", "\[id\]", rule.pattern)
                logging.info(title(name, rtn=True))
                for s in generate_strings(valid_url):
                    logging.info(f"  - {add_color(s)}")
        sys.exit(0)
    elif args.extract_direct:
        logging.info(
            "\n" + _direct.extract_direct_url(args.extract_direct) + "\n")
        sys.exit(0)

    if not args.query or (args.command and "{}" not in args.command):
        parser.print_help()
        sys.exit(0)

    extractor = extractors["layarkaca21"]
    for egn, kls in extractors.items():
        if args.__dict__[egn]:
            extractor = kls
            break

    extractor = extractor(logging, args)
    if not extractor.tag and not args.debug:
        sys.exit(f"Module {extractor.__module__} belum bisa digunakan")
    query = " ".join(args.query)

    id = False
    nextPage = True
    Range = parse_range(args.page)
    netloc = urlparse(extractor.host).netloc
    try:
        page = Range.__next__()
        cache = {page: list(extractor.search(query, page=page))}
        while not id:
            print(
                f"Mencari {query!r} -> {netloc} halaman {page}")
            logging.info(
                f"Total item terkumpul: {sum(len(v) for v in cache.values())} item dari total {len(cache)} halaman")
            if not cache[page]:
                sys.exit("Tidak ditemukan")

            if len(cache[page]) == 1:
                response = f"1. " + cache[page][0]["title"]
            else:
                response = extractor.choice([
                    i['title'] for i in cache[page]] + [
                    PyInquirer.Separator(), "00. Kembali", "01. Lanjut", "02. Keluar"], reset_counter=False)
            pgs = list(cache.keys())
            index = pgs.index(page)
            if response.endswith("Keluar"):
                break
            elif response.endswith("Kembali"):
                if extractor.counter > -1:
                    extractor.counter -= len(cache[page])
                print("\x1b[3A\x1b[K", end="")
                if index > 0 and len(pgs) > 1:
                    page = pgs[index - 1]
                    extractor.counter -= len(cache[page])
            elif response.endswith("Lanjut") and nextPage is True:
                if index >= len(pgs) - 1:
                    try:
                        ppage = Range.__next__()
                        if len(res := list(extractor.search(query, page=page))) > 0:
                            page = ppage
                            cache[page] = res
                        else:
                            extractor.counter -= len(cache[page])
                    except StopIteration:
                        nextPage = False
                else:
                    page = pgs[index + 1]
                if nextPage:
                    print("\x1b[3A\x1b[K", end="")
            else:
                for r in cache[page]:
                    if r.get("title") == re.sub(r"^\d+\. ", "", response):
                        extractor.info(
                            f"\n [\x1b[92m{r.pop('title')}\x1b[0m]")
                        for k, v in r.items():
                            extractor.info(
                                f"   {k}: {', '.join(filter(lambda x: x, v)) if isinstance(v, list) else v}")
                        extractor.info("")

                        id = r["id"]
                        break
        if id:
            logging.info(f"Mengekstrak link unduhan: {id}")

            result = extractor.extract(id)
            dlurl = recursive_choice(extractor, result)
            url = _direct.extract_direct_url(dlurl)

            if args.command:
                os.system(args.command.format(url))
            else:
                logging.info("")
                title("Url Dipilih")
                logging.info(f"\n{url}\n")

    except Exception as e:
        logging.info(f"{e}")
        if args.debug:
            raise

    if _version_msg:
        logging.warning(_version_msg)
