
from napari_arnheim.widgets.dialogs.forms.fields.selectors.arnheim_model import ArnheimModelSelector
from grunnlag.schema import Experiment
from napari_arnheim.widgets.dialogs.forms.models.new_experiment import NewExperimentForm

class ExperimentSelector(ArnheimModelSelector):
    list_query = """query {
            myexperiments {
                id
                name
            }
        }"""
    model = Experiment
    new_form = NewExperimentForm