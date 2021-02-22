import pytest

from dkist_processing_common._util.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common._util.graphql import RecipeRunStatusResponse


class FakeGQLClient:
    @staticmethod
    def execute_gql_mutation(**kwargs):
        mutation_base = kwargs["mutation_base"]

        if mutation_base == "updateRecipeRun":
            return
        if mutation_base == "createRecipeRunStatus":
            return CreateRecipeRunStatusResponse(
                recipeRunStatus=RecipeRunStatusResponse(recipeRunStatusId=1)
            )


def test_add_new_recipe_run_status(mocker):
    from dkist_processing_common._util.graphql import add_new_recipe_run_status

    mocker.patch("dkist_processing_common._util.graphql.graph_ql_client", new=FakeGQLClient)
    with pytest.raises(TypeError):
        add_new_recipe_run_status(status=4, is_complete=True)
    with pytest.raises(TypeError):
        add_new_recipe_run_status(status="INPROGRESS", is_complete="true")
    with pytest.raises(KeyError):
        add_new_recipe_run_status(status="READY", is_complete=True)
    assert isinstance(add_new_recipe_run_status(status="INPROGRESS", is_complete=True), int)
