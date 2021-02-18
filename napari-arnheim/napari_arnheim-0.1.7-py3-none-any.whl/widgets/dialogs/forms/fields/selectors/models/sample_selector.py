
from napari_arnheim.widgets.dialogs.forms.fields.selectors.arnheim_model import ArnheimModelSelector
from grunnlag.schema import Sample
from napari_arnheim.widgets.dialogs.forms.models.new_sample import NewSampleForm

class SampleSelector(ArnheimModelSelector):
    list_query = """query {
            mysamples {
                id
                name
            }
        }"""
    model = Sample
    new_form = NewSampleForm