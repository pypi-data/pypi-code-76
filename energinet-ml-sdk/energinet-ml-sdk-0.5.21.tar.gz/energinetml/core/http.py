import fastapi
import uvicorn

from energinetml.settings import PACKAGE_REQUIREMENT

from .predicting import PredictionController


def create_app(model, trained_model):
    """
    :param energinetml.Model model:
    :param energinetml.TrainedModel trained_model:
    :rtype: fastapi.FastAPI
    """
    controller = PredictionController(model, trained_model)

    async def predict_http_endpoint(
            request: controller.request_model,
            response: fastapi.Response):
        """
        TODO Write me!
        TODO /docs not working?
        """
        response.headers['X-sdk-version'] = str(PACKAGE_REQUIREMENT)

        return controller.predict(request)

    # -- Setup app -----------------------------------------------------------

    app = fastapi.FastAPI()
    app.router.add_api_route(
        path='/predict',
        methods=['POST'],
        endpoint=predict_http_endpoint,
        response_model=controller.response_model,

        # TODO:
        summary='',
        description='',
    )

    return app


def run_predict_api(model, trained_model, host, port):
    """
    :param energinetml.Model model:
    :param energinetml.TrainedModel trained_model:
    :param str host:
    :param int port:
    """
    uvicorn.run(create_app(model, trained_model), host=host, port=port)
