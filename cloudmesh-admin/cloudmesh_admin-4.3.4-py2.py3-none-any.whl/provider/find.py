import os
from pydoc import locate


def find():
    _paths = []

    def find_name(names,
                  template="cloudmesh.compute.{name}",
                  kind=None,
                  on_error="not loaded"):
        _paths = []
        for _name in names:

            _active = False
            try:
                _class = template.format(name=_name)
                _p = locate(_class)
                _where = _p.__file__
                _path = os.path.dirname(_where)
                _active = True
                _provider = locate(f"{_class}.Provider.Provider")
            except Exception as e:
                _path = on_error.format(name=_name)
                _provider = None
            _paths.append({
                "class": _class,
                "path": _path,
                "name": _name,
                "active": _active,
                "service": kind,
                "provider": _provider
            })
        return _paths

    # cloud_dir = os.path.dirname(locate("cloudmesh.compute").__file__)

    #
    # compute
    #
    candidates_compute_name = ["docker",
                               "libcloud",
                               "virtualbox",
                               "vm"]

    candidates_name_compute = ["openstack",
                               "azure",
                               "google",
                               "aws"
                               "multipass"]

    _paths = find_name(candidates_compute_name,
                       template="cloudmesh.compute.{name}",
                       kind="compute",
                       on_error="load with pip install cloudmesh-cloud") + \
             find_name(candidates_name_compute,
                       template="cloudmesh.{name}.compute",
                       kind="compute",
                       on_error="load with pip install cloudmesh-{name}")

    #
    # storage
    #
    candidates_storage_name = [
        "awss3",
        "azureblob",
        "box",
        "gdrive",
        "local",
        "parallelawss3",
        "parallelgdrive",
        "parallelazureblob"]

    candidates_name_storage = [
        "google",
        "oracle"]

    _paths += find_name(candidates_storage_name,
                        template="cloudmesh.storage.provider.{name}",
                        kind="storage",
                        on_error="load with pip install cloudmesh-storage") + \
              find_name(candidates_name_storage,
                        template="cloudmesh.{name}.storage",
                        kind="storage",
                        on_error="load with pip install cloudmesh-{name}")

    candidates_volume = [
        "aws",
        "azure"
        "google",
        "multipass",
        "opensatck",
        "oracle"]

    _paths += find_name(candidates_volume,
                        template="cloudmesh.volume.provider.{name}",
                        kind="volume",
                        on_error="load with pip install cloudmesh-volume")
    return _paths
