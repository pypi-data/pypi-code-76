from sys import argv
import pip
import venv
import os

if argv[1] == "new":
    if argv[2] == "project":
        venv.create(argv[3])
        open(argv[3] + "/main.py","x")
        os.environ["PYMLKIT_PROJ"] = argv[3]
        if argv[3] == "geo":
            pip.main(["install","-t","./" + argv[3] + "/Lib/site-packages","matplotlib","numpy","scipy","scikit-learn","seaborn","geopandas"])
        elif argv[3] == "nerual":
            pip.main(["install","-t","./" + argv[3] + "/Lib/site-packages","tensorflow","keras"])
        elif argv[3] == "bigquery":
            pip.main(["install","-t","./" + argv[3] + "/Lib/site-packages","numpy","pandas","matplotlib","bigquery"])
        elif argv[3] == "basic":
            pip.main(["install","-t","./" + argv[3] + "/Lib/site-packages","scikit-learn","numpy","pandas","xgboost","seaborn","matplotlib"])
elif argv[1] == "install":
    pip.main(["install","-t","./" + os.environ["PYMLKIT_PROJ"],argv[2]])
