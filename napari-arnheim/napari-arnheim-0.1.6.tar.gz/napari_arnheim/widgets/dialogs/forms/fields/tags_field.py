from napari_arnheim.widgets.dialogs.forms.fields.text_field import TextField

class TagsField(TextField):

    def getValue(self):
        return [ tag.strip() for tag in self.text().split(",")]