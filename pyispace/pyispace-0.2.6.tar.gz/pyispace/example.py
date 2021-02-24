import json
from pathlib import Path


opts = {
    "perf": {"MaxPerf": False, "AbsPerf": True, "epsilon": 0.69},
    "general": {"betaThreshold": 0.55},
    "parallel": {"flag": False, "ncores": 2},
    "auto": {"preproc": True, "featsel": False},
    "bound": {"flag": True},
    "norm": {"flag": True},
    "corr": {"flag": True, "threshold": 10},
    "clust": {"flag": True, "KDEFAULT": 10, "SILTHRESHOLD": 0.9, "NTREES": 50, "MaxIter": 1000, "Replicates": 100},
    "pilot": {"analytic": False, "ntries": 5},
    "cloister": {"pval": 0.05, "cthres": 0.7},
    "pythia": {"cvfolds": 5, "ispolykrnl": True, "useweights": False, "uselibsvm": False},
    "trace": {"usesim": False, "PI": 0.55},
    "selvars": {"smallscaleflag": False, "smallscale": 0.5, "fileidxflag": False, "fileidx": "", "densityflag": False,
                "mindistance": 0.1},
    "outputs": {"csv": True, "web": False, "png": False}
}


def save_opts(path):
    path = Path(path)
    if path.is_dir():
        opts_path = path / 'options.json'
        with open(opts_path, 'w') as f:
            json.dump(opts, f)
    else:
        raise NotADirectoryError(f"Invalid directory '{str(path)}'.")
