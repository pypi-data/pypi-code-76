"""main entry for ckgen command-line interface"""


def main():
    from ckgen import CESMKGen
    ret, _ = CESMKGen().run_command()
    return ret


if __name__ == "__main__":
    main()
