import click

from energinetml.core.http import run_predict_api
from energinetml.cli.utils import discover_model, discover_trained_model


@click.command()
@discover_model()
@discover_trained_model()
@click.option('--host', default='127.0.0.1', type=str,
              help='Host to serve on (default: 127.0.0.1)')
@click.option('--port', default=8080, type=int,
              help='Port to serve on (default: 8080)')
def serve(host, port, model, trained_model):
    """
    Serve a HTTP web API for model prediction.
    \f

    :param str host:
    :param int port:
    :param Model model:
    :param TrainedModel trained_model:
    """
    run_predict_api(model, trained_model, host, port)
