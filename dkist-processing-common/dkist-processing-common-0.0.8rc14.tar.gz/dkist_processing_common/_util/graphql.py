import json
from collections import defaultdict
from dataclasses import dataclass
from os import environ

from gqlclient import GraphQLClient

from dkist_processing_common._util.config import get_mesh_config


@dataclass
class RecipeRunMutation:
    recipeRunId: int
    recipeRunStatusId: int
    authToken: str = environ.get("GQL_AUTH_TOKEN")


@dataclass
class RecipeRunStatusResponse:
    recipeRunStatusId: int


@dataclass
class RecipeRunStatusQuery:
    recipeRunStatusName: str


@dataclass
class CreateRecipeRunStatusResponse:
    recipeRunStatus: RecipeRunStatusResponse


@dataclass
class RecipeRunStatusMutation:
    recipeRunStatusName: str
    isComplete: bool
    recipeRunStatusDescription: str = "To add a description, use the processing-preparation-worker"
    authToken: str = environ.get("GQL_AUTH_TOKEN")


@dataclass
class InputDatasetResponse:
    inputDatasetDocument: str


@dataclass
class ProcessingCandidateResponse:
    observingProgramExecutionId: str
    proposalId: str


@dataclass
class RecipeInstanceResponse:
    inputDataset: InputDatasetResponse
    processingCandidate: ProcessingCandidateResponse


@dataclass
class RecipeRunResponse:
    recipeInstance: RecipeInstanceResponse


@dataclass
class RecipeRunInputDatasetQuery:
    recipeRunId: int


@dataclass
class DatasetCatalogReceiptAccountMutation:
    """
    Dataclass used to write the dataset_catalog_receipt_account record for the run.
    It sets an expected object count for a dataset so that dataset inventory creation
    doesn't happen until all objects are transferred and inventoried.
    """

    datasetId: str
    expectedObjectCount: int
    authToken: str = environ.get("GQL_AUTH_TOKEN")


recipe_run_statuses = {
    "INPROGRESS": "Recipe run is currently undergoing processing",
    "COMPLETEDSUCCESSFULLY": "Recipe run processing completed with no errors",
}


# Environment variable indicating how to connect to dependencies on the service mesh
MESH_CONFIG = get_mesh_config()

graph_ql_client = GraphQLClient(
    f'http://{MESH_CONFIG["internal-api-gateway"]["mesh_address"]}:{MESH_CONFIG["internal-api-gateway"]["mesh_port"]}/graphql'
)


def get_message_status_query(status: str):
    """
    Find the id of a recipe run status
    """
    return graph_ql_client.execute_gql_query(
        query_base="recipeRunStatuses",
        query_response_cls=RecipeRunStatusResponse,
        query_parameters=RecipeRunStatusQuery(recipeRunStatusName=status),
    )


def add_new_recipe_run_status(status: str, is_complete: bool) -> int:
    """
    Add a new recipe run status to the db
    :param status: name of the status to add
    :param is_complete: does the new status correspond to an accepted completion state
    """
    if not isinstance(status, str):
        raise TypeError(f"status must be of type str: {status}")
    if not isinstance(is_complete, bool):
        raise TypeError(f"is_complete must be of type bool: {is_complete}")
    recipe_run_status_response = graph_ql_client.execute_gql_mutation(
        mutation_base="createRecipeRunStatus",
        mutation_response_cls=CreateRecipeRunStatusResponse,
        mutation_parameters=RecipeRunStatusMutation(
            recipeRunStatusName=status,
            isComplete=is_complete,
            recipeRunStatusDescription=recipe_run_statuses[status],
        ),
    )
    return recipe_run_status_response.recipeRunStatus.recipeRunStatusId


def apply_status_id_to_recipe_run(recipe_run_status_id: int, recipe_run_id: int):
    """
    Change the status of a given recipe run id
    :param recipe_run_status_id: the new status to use
    :param recipe_run_id: id of the recipe run to have the status changed
    """
    graph_ql_client.execute_gql_mutation(
        mutation_base="updateRecipeRun",
        mutation_parameters=RecipeRunMutation(
            recipeRunId=recipe_run_id, recipeRunStatusId=recipe_run_status_id
        ),
    )
