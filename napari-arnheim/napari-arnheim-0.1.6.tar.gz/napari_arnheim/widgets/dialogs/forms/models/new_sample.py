


from grunnlag.schema import Sample
from napari_arnheim.widgets.dialogs.forms.fields.text_field import TextField
from napari_arnheim.widgets.dialogs.forms.arnheim_model import ArnheimModelForm
from napari_arnheim.widgets.dialogs.forms.fields.selectors.models.experiment_selector import ExperimentSelector
import namegenerator

class NewSampleForm(ArnheimModelForm):
    create_mutation = """
            mutation ($experiment: ID, $name: String!) {
                createSample(experiment: $experiment, name: $name){
                    id
                    name
                
                }
            }
        
    """
    model =  Sample
    fields = {
        "name": TextField,
        "experiment": ExperimentSelector
    }

