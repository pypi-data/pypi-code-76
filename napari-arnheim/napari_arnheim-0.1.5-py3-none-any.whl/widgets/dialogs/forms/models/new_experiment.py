


from grunnlag.schema import Experiment
from napari_arnheim.widgets.dialogs.forms.fields.text_field import TextField
from napari_arnheim.widgets.dialogs.forms.arnheim_model import ArnheimModelForm
import namegenerator

class NewExperimentForm(ArnheimModelForm):
    create_mutation = """
            mutation CreateExperiment($name: String!){
                createExperiment(name: $name){
                    id
                    name
                    creator {
                    id
                    }
                    description
                }
            } 
    """
    model =  Experiment
    fields = {
        "name": TextField,
    }



