import sys
import argparse
import os
from PyQt5 import QtWidgets, QtCore
from fileplayer import main_window
from fileplayer import globa

"""
cmd_arg_file_path_str = ""
print(f"{__file__=}")
print(f"{os.getcwd()=}")
print(f"{sys.path[0]=}")
print(f"{sys.argv=}")
if sys.argv and len(sys.argv) > 1:
    cmd_arg_str = sys.argv[1]
    print(f"{cmd_arg_str=}")
    if os.path.isabs(cmd_arg_str):
        cmd_arg_file_path_str = cmd_arg_str
    else:
        cmd_arg_file_path_str = os.path.join(os.getcwd(), cmd_arg_str)
    if not os.path.isfile(cmd_arg_file_path_str):
        cmd_arg_file_path_str = ""
else:
    print("No arguments provided")

"""


def main():
    temp_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.TempLocation)[0]
    path_to_lock_file: str = os.path.join(temp_dir, "file-player.lock")

    short_descr_str = globa.SHORT_DESCRIPTION_STR
    argument_parser = argparse.ArgumentParser(description=short_descr_str)
    argument_parser.add_argument("--version", "-v", help="Show application version", action="store_true")
    argument_parser.add_argument("file", nargs="?")
    args_namespace = argument_parser.parse_args()
    if args_namespace.version:
        print(f"{globa.APPLICATION_NAME_STR} version: {globa.VERSION_STR}")
        sys.exit()

    app = QtWidgets.QApplication(sys.argv)
    main_win = main_window.MainWindow(args_namespace.file)

    lock_file = QtCore.QLockFile(path_to_lock_file)
    lock_result: bool = lock_file.tryLock(100)
    if not lock_result:
        # main_win = main_window.MainWindow()
        # main_win.showNormal()
        # main_win.raise_()
        QtWidgets.QMessageBox.warning(main_win, "instance already running", "____ instance already running")
        sys.exit(1)

    app.setQuitOnLastWindowClosed(False)
    app.aboutToQuit.connect(main_win.on_about_to_quit)  # -not working, unknown why
    main_win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
