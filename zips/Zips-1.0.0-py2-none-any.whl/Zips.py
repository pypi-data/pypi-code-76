import os, argparse, re

formats = [".tar.gz", ".tar", ".zip", ".gz", ".bz2", ".xz"]
nfolder = ["bz2", "xz", "gz"]
def fileformat(filename):
    for f in formats:
        if re.findall(r"%s" % f, filename):
            return f.replace(".", "")
    return False

def argv():
    parse = argparse.ArgumentParser(
        prog="Zip/Unzip",
        description="Compress / Extract six kinds of compression software formats easily.",
        epilog="Contact author: ala98412@gmail.com"
    )
    group = parse.add_mutually_exclusive_group()
    group.add_argument("-zip", choices=["targz", "tar", "gz", "zip", "bz2", "xz"], help="Zip file or directory")
    group.add_argument("-uzip", action='store_true')
    parse.add_argument("file")

    args = parse.parse_args()

    if not args.zip and not args.uzip:
        print("[ERROR] -zip or -uzip must be required !")
        os._exit(-1)

    if args.zip:
        fmt = args.zip
        uz = "zip"
    else:
        fmt = fileformat(args.file)
        uz = "uzip"
        if fmt == False:
            print("[ERROR] Not a zip file or a format not currently supported.")
            os._exit(-1)
    return args.file, fmt, uz

def ziporuzip(filename, fmt, uz):
    if os.path.exists(filename):
        name_ext = os.path.basename(filename)
        name = os.path.splitext(name_ext)[0]
        if os.path.isdir(filename) and fmt in nfolder:
            print("[Error] %s connot compress a directory." % fmt)
            os._exit(-1)

    else:
        print("[ERROR] %s not exists" % filename)
        os._exit(-1)

    if fmt == "targz":
        if uz == "zip":
            os.system("tar zcvf %s.tar.gz %s" % (name, filename))
            print("=> %s.tar.gz" % name)
        else:
            os.system("tar zxvf %s" % filename)
    elif fmt == "tar":
        if uz == "zip":
            os.system("tar cvf %s.tar %s" % (name, filename))
            print("=> %s.tar" % name)
        else:
            os.system("tar xvf %s" % filename)
    elif fmt == "gz":
        if uz == "zip":
            os.system("gzip %s" % filename)
            print("=> %s.gz" % name_ext)
        else:
            os.system("gunzip %s" % filename)
            print("=> %s" % name)
    elif fmt == "bz2":
        if uz == "zip":
            os.system("bzip2 -z %s" % filename)
            print("=> %s.bz2" % name_ext)
        else:
            os.system("bzip2 -d %s" % filename)
            print("=> %s" % name)
    elif fmt == "xz":
        if uz == "zip":
            os.system("xz -z %s" % filename)
            print("=> %s.xz" % name_ext)
        else:
            os.system("xz -d %s" % filename)
            print("=> %s" % name)
    elif fmt == "zip":
        if uz == "zip":
            os.system("zip -r %s.zip %s" % (name, filename))
            print("=> %s.zip" % name)
        else:
            os.system("unzip %s" % filename)
    else:
        print("[Error] How do you made it !?")


if __name__ == "__main__":
    filename, fmt, uz = argv()
    ziporuzip(filename, fmt, uz)
    print("===== Done =====")
