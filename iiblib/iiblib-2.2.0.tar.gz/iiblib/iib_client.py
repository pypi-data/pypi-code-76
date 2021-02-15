import time

from .iib_build_details_pager import IIBBuildDetailsPager
from .iib_build_details_model import (
    IIBBuildDetailsModel,
    RmModel,
    AddModel,
    RegenerateBundleModel,
)
from .iib_authentication import IIBAuth
from .iib_session import IIBSession


class IIBException(Exception):
    """ General IIB exception"""

    pass


# pylint: disable=bad-option-value,useless-object-inheritance
class IIBClient(object):
    """IIB requests wrapper"""

    def __init__(
        self,
        hostname,
        retries=3,
        auth=None,
        poll_interval=30,
        ssl_verify=True,
        backoff_factor=2,
        wait_for_build_timeout=7200,
    ):
        """
        Args:
            hostname (str)
                IIB service hostname
            retries (int)
                number of http retries for IIB requests
            auth (IIBAuth)
                IIBAuth subclass instance
            poll_interval (int)
                number of seconds to wait before fetching new status of task in wait_for_task
            ssl_verify (bool)
                enable/disable SSL verification
            backoff_factor (int)
                backoff factor to apply between attempts after the second try
            wait_for_build_timeout (int)
                maximum time which we should wait for build to be completed
        """
        self.iib_session = IIBSession(
            hostname, retries=retries, verify=ssl_verify, backoff_factor=backoff_factor
        )
        self.wait_for_build_timeout = wait_for_build_timeout
        self.poll_interval = poll_interval
        if auth:
            auth.make_auth(self.iib_session)

    @staticmethod
    def _check_response(response):
        """
        Checks response for status and raises IIBException in case of error

        Args:
            response (requests.Response) response which will be checked for status

        Raises:
            IIBException when any error occurs
        """
        if response.status_code >= 400:
            try:
                resp_error = response.json().get("error")
                if resp_error:
                    # raise exception only if error is specified
                    raise IIBException(resp_error)

            except ValueError:
                pass

            # check status in case no error is specified or response
            # does not contain valid json
            response.raise_for_status()

    def add_bundles(
        self,
        index_image,
        bundles,
        arches,
        binary_image=None,
        cnr_token=None,
        organization=None,
        overwrite_from_index=False,
        overwrite_from_index_token=None,
        raw=False,
    ):
        """Rebuild index image with new bundles to be added.

        Args:
            index_image (str)
                Index image ref used as source to rebuild
            bundles (list)
                List of references to bundle images to be added to index image
            arches (list)
                List of architectures supported in new index image
            binary_image (str)
                optional. Image with binary used to rebuild existing index image
            cnr_token (srt)
                optional. CNR token.
            organization (str)
                optional. Name of the organization in the legacy app registry.
            overwrite_from_index (bool)
                optional. Indicates if resulting index_image needs to be
                overwritten at the location of from_index. If this is provided,
                overwrite_from_index_token needs to be specified too.
            overwrite_from_index_token (str)
                optional. Token of the destination registry repo where the
                resulting index image built by IIB has to be overwritten. If
                this is provided, overwrite_from_index must be set to True.
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            IIBBuildDetailsModel or dict
              if raw == True return dict with json response otherwise
              return IIBBuildDetailsModel instance.
        """

        post_data = {
            "from_index": index_image,
            "add_arches": arches,
        }

        if binary_image:
            post_data["binary_image"] = binary_image

        if bundles:
            post_data["bundles"] = bundles

        if cnr_token:
            post_data["cnr_token"] = cnr_token

        if organization:
            post_data["organization"] = organization

        if overwrite_from_index:
            if overwrite_from_index_token:
                post_data["overwrite_from_index"] = overwrite_from_index
                post_data["overwrite_from_index_token"] = overwrite_from_index_token
            else:
                raise ValueError(
                    "Either both or neither of overwrite-from-index and "
                    "overwrite-from-index-token should be specified."
                )
        elif overwrite_from_index_token:
            raise ValueError(
                "Either both or neither of overwrite-from-index and "
                "overwrite-from-index-token should be specified."
            )

        resp = self.iib_session.post("builds/add", json=post_data)
        self._check_response(resp)

        if raw:
            return resp.json()
        return AddModel.from_dict(resp.json())

    def remove_operators(
        self,
        index_image,
        operators,
        arches,
        binary_image=None,
        overwrite_from_index=False,
        overwrite_from_index_token=None,
        raw=False,
    ):
        """Rebuild index image with existing operators to be removed.

        Args:
            index_image (str)
                Index image ref used as source to rebuild
            operators (list)
                List of operators to be removed from existing index image
            arches (list)
                List of architectures supported in new index image
            binary_image (str)
                optional. Image with binary used to rebuild existing index image
            overwrite_from_index (bool)
                optional. Indicates if resulting index_image needs to be
                overwritten at the location of from_index. If this is provided,
                overwrite_from_index_token needs to be specified too.
            overwrite_from_index_token (str)
                optional. Token of the destination registry repo where the
                resulting index image built by IIB has to be overwritten. If
                this is provided, overwrite_from_index must be set to True.
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            IIBBuildDetailsModel or dict
              if raw == True return dict with json response otherwise
              return IIBBuildDetailsModel instance.
        """
        post_data = {
            "from_index": index_image,
            "operators": operators,
            "add_arches": arches,
        }

        if binary_image:
            post_data["binary_image"] = binary_image

        if overwrite_from_index:
            if overwrite_from_index_token:
                post_data["overwrite_from_index"] = overwrite_from_index
                post_data["overwrite_from_index_token"] = overwrite_from_index_token
            else:
                raise ValueError(
                    "Either both or neither of overwrite-from-index and "
                    "overwrite-from-index-token should be specified."
                )
        elif overwrite_from_index_token:
            raise ValueError(
                "Either both or neither of overwrite-from-index and "
                "overwrite-from-index-token should be specified."
            )

        resp = self.iib_session.post("builds/rm", json=post_data)
        self._check_response(resp)

        if raw:
            return resp.json()
        return RmModel.from_dict(resp.json())

    def get_builds(self, page=1, raw=False):
        """Get all historical builds of index image.

        Args:
            page (int)
                Offset page to start listing results
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            IIBBuildDetailsPager or dict
              if raw == True return dict with json response otherwise
              return IIBBuildDetailsPager instance.
        """

        resp = self.iib_session.get("builds", params={"page": page})
        self._check_response(resp)

        if raw:
            return resp.json()
        return IIBBuildDetailsPager.from_dict(self, resp.json())

    def get_build(self, bid, raw=False):
        """Get specific index image build

        Args:
            bid (int)
                Build id of requested build
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            `IIBBuildDetailsModel` or dict
              if raw == True return dict with json response otherwise
              return `IIBBuildDetailsModel` instance.
        """

        resp = self.iib_session.get("builds/%s" % bid)
        self._check_response(resp)

        if raw:
            return resp.json()
        return IIBBuildDetailsModel.from_dict(resp.json())

    def wait_for_build(self, build):
        """Wait until specific build is finished

        Args:
            build (IIBBuildDetailsModel)
                Instance of `IIBBuildDetailsModel` class
        Raises:
            IIBException when timeout for get build from IIB was reached
        """
        timeout = time.time() + self.wait_for_build_timeout
        while True:
            build_details = self.get_build(build.id)
            if build_details.state in ("complete", "failed"):
                return build_details
            if time.time() >= timeout:
                raise IIBException(
                    "Timeout reached. Build request %s was not processed in %d seconds."
                    % (build.id, self.wait_for_build_timeout),
                )
            time.sleep(self.poll_interval)

    def regenerate_bundle(
        self,
        bundle_image,
        organization=None,
        raw=False,
    ):
        """Regenerate bundle image.

        Args:
            bundle_image (str)
                The pull specification of the original bundle image
                that will be modified.
            organization (str)
                The name of the organization the bundle should be
                regenerated for.
            raw (bool)
                Return raw json response instead of model instance

        Returns:
            `RegenerateBundleModel` or dict
              if raw == True return dict with json response otherwise
              return `RegenerateBundleModel` instance.
        """

        post_data = {
            "from_bundle_image": bundle_image,
        }
        if organization:
            post_data["organization"] = organization

        resp = self.iib_session.post("builds/regenerate-bundle", json=post_data)
        self._check_response(resp)

        if raw:
            return resp.json()
        return RegenerateBundleModel.from_dict(resp.json())

    def rebuild_index(self, index_image):
        raise NotImplementedError

    def health(self):
        raise NotImplementedError
