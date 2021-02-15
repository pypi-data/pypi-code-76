from django.core.exceptions import ObjectDoesNotExist

from papyru.logger import LogSequence, log_root
from papyru.problem import Problem

# defined in RFC 7231
HTTP_METHODS = set(['get', 'head', 'post', 'put', 'delete', 'connect',
                    'options', 'trace'])


class Resource:
    @log_root()
    def __call__(self, request, *args):
        try:
            with LogSequence('%s %s' % (
                    request.method, request.get_full_path())) as log:

                request_id = request.headers.get('pap-request-id', None)

                if request_id is not None:
                    log.info('Request-ID: %s' % request_id)

                try:
                    method = getattr(self.__class__, request.method.lower())
                except AttributeError:
                    allowed = set(dir(self.__class__)) & HTTP_METHODS
                    raise Problem.method_not_allowed(allowed)

                return method(self, request, *args)

        except Problem as problem:
            return problem.to_response()

        except ObjectDoesNotExist:
            return Problem.not_found().to_response()

        except NotImplementedError:
            return Problem.not_implemented().to_response()

        except Exception as exc:
            return Problem.internal_error(
                'unexpected error: %s' % exc).to_response()
