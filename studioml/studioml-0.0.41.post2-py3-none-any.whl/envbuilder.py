import venv
from subprocess import Popen, PIPE

def main():
    myBuilder = venv.EnvBuilder(symlinks=True, with_pip=True)

    myBuilder.create("./xyz")

    #pip_installer = Popen(["./xyz/bin/pip", "install", "-r", "./myreqs.txt", "--disable-pip-version-check"])
    #pip_installer = Popen(["pip", "install", "-r", "./myreqs.txt", "--disable-pip-version-check"])
    #pip_installer.wait()


if __name__ == "__main__":
    main()






