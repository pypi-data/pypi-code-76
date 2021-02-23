#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import List
from loguru import logger
import pathlib
import shutil
import re

from pinecone.utils import hubify
from pinecone.functions.model import HubFunction
from pinecone.functions.model.preprocessor import Preprocessor
from pinecone.functions.model.preprocessor.hub import HubPreprocessor
from pinecone.functions.model.postprocessor import Postprocessor, QueryResult
from pinecone.functions.model.postprocessor.hub import HubPostprocessor

from .constants import Config
from .api_hub import HubAPI
from .api_action import ActionAPI

__all__ = [
    "get_login_cmd",
    "list_repositories",
    "create_repository",
    "delete_repository",
    "list_repository_tags",
    "as_user_image",
    "as_repo_image",
    "ImageBuilder",
    "ImageServer",
    "preprocessor",
    "postprocessor",
    "HubFunction",
    "QueryResult",
]

# Image name consists of repository and tag. Repository and tag can only contain alphanumeric letter, period, dash, or underscore.
IMAGE_REGEX = re.compile("^([a-zA-Z0-9]|[-.]|[_.])+:([a-zA-Z0-9]|[-.]|[_.])+$")


def preprocessor(cls):
    """Decorator for wrapping a class as a Preprocessor.

    .. note::
        By default preprocessors are limited to 4GB of memory.
        If your application needs to use more memory,
        please reach out support@pinecone.io.

    Usage:

    .. code-block:: python

        from pinecone.hub import preprocessor


        @preprocessor
        class MyPreprocessor:
            def transform(self, vectors: np.ndarray) -> np.ndarray:
                return vectors

    """

    @hubify
    class PreprocessorWrapper(Preprocessor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Overrides the transform function.
            self.transform = cls().transform

    return PreprocessorWrapper


def postprocessor(cls):
    """Decorator for wrapping a class as a Postporcessor.

    .. note::
        By default postprocessors are limited to 4GB of memory.
        If your application needs to use more memory,
        please reach out support@pinecone.io.

    Usage:

    .. code-block:: python

        from pinecone.hub improt postprocessor


        @postprocessor
        class MyPostprocessor:
            def transform(self, queries: np.ndarray, matches: Iterable[QueryResult]) -> Iterable[QueryResult]:
                return results

    """

    @hubify
    class PostprocessorWrapper(Postprocessor):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Overrides the transform function.
            self.transform = cls().transform

    return PostprocessorWrapper


def _get_hub_api():
    return HubAPI(host=Config.HUB_HOST, api_key=Config.API_KEY)


def _get_action_api():
    return ActionAPI(host=Config.CONTROLLER_HOST, api_key=Config.API_KEY)


def get_login_cmd() -> str:
    """Returns CLI command for logging into Pinecone hub."""
    api = _get_hub_api()
    return "docker login -u {username} -p {password} {server}".format(**api.get_login())


def list_repositories():
    """Shows all repositories."""
    api = _get_hub_api()
    return api.list_repositories()


def create_repository(name):
    """Creates or unarchives a repository."""
    api = _get_hub_api()
    return api.create_repository(name)


def delete_repository(name):
    """Archives a repository."""
    api = _get_hub_api()
    return api.delete_repository(name)


def list_repository_tags(name):
    """Lists tags of a repository."""
    api = _get_hub_api()
    return api.list_repository_tags(name)


def as_user_image(image):
    """Returns the image name prepended with the user name."""
    user_api = _get_action_api()
    username = user_api.whoami().username
    return "{username}/{image}".format(**locals())


def as_repo_image(image):
    """Returns the complete repository image URI."""
    registry = Config.HUB_REGISTRY.split("https://")[-1].split("https://")[-1]
    user_image = as_user_image(image)
    return "{registry}/{user_image}".format(**locals())


class ImageBuilder:
    """A helper class for building Pinecone Hub models."""

    def __init__(
        self,
        image: str,
        build_path: pathlib.Path,
        model_path: pathlib.Path,
        pip: List[str] = None,
        data_paths: List[pathlib.Path] = None,
    ):
        """
        :param image: name of the docker image in the form :code:`REPOSITORY:TAG`
        :param build_path: path to which artifacts will be saved for building the docker image.
        :param model_path: path to the main model file. The model file is where Pinecone loads the inference APIs.
        :param data_paths: paths to ancillary data, such as serialized Tensorflow models.
            These files will be copied to the docker build path.
        :param pip: additional Python packages to be installed.
            In the base docker image, only *numpy* is preloaded. It is recommended that you use exact versions.
        """
        self._raise_if_invalid_image_name(image)
        self.image = image
        self.build_path = pathlib.Path(build_path)
        self.model_path = pathlib.Path(model_path)
        self.data_paths = [pathlib.Path(pp) for pp in (data_paths or [])]
        self.pip = pip or []

    def _raise_if_invalid_image_name(self, image):
        if not IMAGE_REGEX.match(image):
            raise ValueError(
                "Image name must be of the form `REPOSITORY:TAG`."
                " Repository and tag can only contain alphanumeric letter, period, or dash."
            )

    @property
    def repository(self):
        return self.image.split(":")[0]

    @property
    def tag(self):
        return self.image.split(":")[1]

    def package(self, exist_ok=False):
        """Creates artifacts for building a Pinecone-compatible docker image.

        The following will be created:

        - The build directory :code:`build_path` where the artifacts reside in preparation for running :code:`docker build`.
        - The main model file will be copied from :code:`model_path` to the docker build path.
        - Ancillary data files and directories specified in :code:`data_paths` will be copied to the docker build path.
        - A `Dockerfile` template for building the docker image will be created in the docker build path.

        :param exist_ok: same as `pathlib.Path.mkdir`, defaults to False.
        :type exist_ok: bool, optional
        """
        self.build_path.mkdir(parents=True, exist_ok=exist_ok)

        # Pinecone base image
        base_image = Config.BASE_IMAGE

        # Pip packages to install
        pip_str = "" if not self.pip else "RUN pip3 install --quiet --no-cache-dir {0}".format(" ".join(self.pip))

        # Copy model file
        build_model_path = pathlib.Path(self.build_path.joinpath("model.py"))
        if build_model_path.exists():
            build_model_path.unlink()
        shutil.copy(self.model_path.resolve(), build_model_path)

        # Copy data files
        copy_str_list = []
        for pp in self.data_paths or []:
            basename = pp.name
            build_data_path = pathlib.Path(self.build_path.joinpath(basename))
            if build_data_path.exists():
                if build_data_path.is_dir():
                    build_data_path.rmdir()
                else:
                    build_data_path.unlink()
            if pp.is_dir():
                shutil.copytree(pp.resolve(), build_data_path)
                copy_str_list.append("COPY {basename} ./data/{basename}/".format(**locals()))
            else:
                shutil.copy(pp.resolve(), build_data_path)
                copy_str_list.append("COPY {basename} ./data/".format(**locals()))
        copy_str = "\n".join(copy_str_list)

        # Write Dockerfile
        dockerfile_path = self.build_path.joinpath("Dockerfile")
        with pathlib.Path(dockerfile_path).open("w") as outfile:
            logger.info("Writing Dockerfile to {dockerfile_path}".format(**locals()))
            template = """# This is a Pinecone Dockerfile template.
# Required: Pinecone base image
FROM {base_image}

RUN pip3 install --quiet --upgrade pip

# Optional: additional python packages
{pip_str}

# Optional: additional paths to copy
{copy_str}

# Required: model file
COPY model.py ./model.py
"""
            outfile.write(template.format(**locals()))

        logger.info("Docker build artifacts are saved to {0}".format(self.build_path))

    def get_build_cmd(self) -> str:
        """Returns the docker build command."""
        build_path = self.build_path.resolve()
        image = self.image
        template = " && \\\n".join(
            [
                "pushd {build_path}",
                "docker build -t {image} .",
                "popd",
            ]
        )
        return template.format(**locals())

    def get_push_cmd(self) -> str:
        """Returns command to push to docker hub."""

        # Creates the repository if it doesn't already exist.
        create_repository(self.repository)

        # The repository is immutable. Verify that the tag does not already exist.
        if self.tag in list_repository_tags(self.repository):
            raise RuntimeError(
                "The tag '{0}' already exists in the '{1}' repository. "
                "Please use a new image tag and rebuild the image.".format(self.tag, self.repository)
            )

        image = self.image
        repo_image = as_repo_image(image)
        template = " && \\\n".join(
            [
                "docker tag {image} {repo_image}",
                "docker push {repo_image}",
            ]
        )
        return template.format(**locals())


class ImageServer:
    """Creates a local server for testing a HubFunction."""

    def __init__(self, image: str, image_type: str):
        """

        :param image: name of the docker image
        :type image: str
        :param image_type: one of {"preprocessor", "postprocessor"}
        :type image_type: str
        """
        self.image = image
        self.image_type = image_type
        self.hub_fn = None

    def __enter__(self):
        if self.image_type == "preprocessor":
            self.hub_fn = HubPreprocessor(image=self.image)
        elif self.image_type == "postprocessor":
            self.hub_fn = HubPostprocessor(image=self.image)
        else:
            raise RuntimeError("Image type '{0}' is not supported.".format(self.image))

        self.hub_fn.start()
        return self.hub_fn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.hub_fn:
            self.hub_fn.stop()
            self.hub_fn.servlet.cleanup()
