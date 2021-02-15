# -*- coding: utf-8 -*-
import os, sys, zipfile, platform
from . import __path__


def get_env_python(env_dir:str = None):
    env_dir = os.path.join(os.getcwd(), "env") if env_dir == None else env_dir
    if platform.system() == "Windows":
        return '"' + os.path.join(env_dir, "Scripts", "python") + '"'
    elif platform.system() == "Darwin":
        return os.path.join(env_dir, "bin", "python").replace(" ", "\\ ")
    else:
        return os.path.join(env_dir, "bin", "python")

def main():
    """Console script for pyvuejs_cli."""
    args = sys.argv[1:]
    if len(args) == 0 or "help" in args[0].lower():
        print("""
Available arguments
- help
- init [project_name(default = "./")]
- serve
""")
        sys.exit()

    kwargs = dict(enumerate(args))
    job = kwargs.pop(0, "serve")

    if job == "init":
        may_project_root = os.getcwd()
        may_project_name = kwargs.pop(1, "./")

        if may_project_name in ("./", ".\\", "."):
            project_root = os.path.dirname(may_project_root)
            project_name = os.path.basename(may_project_root)
        else:
            project_root = may_project_root
            project_name = may_project_name

        template_zip = zipfile.ZipFile(os.path.join(__path__[0], "template.zip"), "r")
        template_zip.extractall(os.path.join(project_root, project_name))

        env_dir = os.path.join(project_root, project_name, "env")
        if not os.path.exists(env_dir):
            os.system(f"{sys.executable} -m pip install virtualenv")
            os.system(f"{sys.executable} -m virtualenv {env_dir}")
            os.system(f"{get_env_python(env_dir)} -m pip install pip pylint --upgrade")
            os.system(f"{get_env_python(env_dir)} -m pip install pyvuejs")
    elif job == "serve":
        may_project_files = os.listdir(os.getcwd())
        if not all(proj_file in may_project_files for proj_file in ("public", "src", "App.vue", "main.py")):
            print("Current directory seems not pyvuejs project")
            sys.exit()

        os.system(f"{get_env_python()} ./main.py")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
