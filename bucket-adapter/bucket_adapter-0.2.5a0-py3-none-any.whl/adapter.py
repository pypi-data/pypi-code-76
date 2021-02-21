"""adapter class."""
import import_string


class Adapter(object):
    """Adapter.

    Args:
        object ([type]): [description]
    """

    def __init__(self, settings_file):
        """__init__

        Args:
            settings_file ([type]): [description]
        """
        self.settings = settings_file
        adaptee_classname = self.settings['NAME']
        mod = import_string(adaptee_classname)
        self.adaptee_obj = mod()

    def upload(self, *args, **kwargs):
        """upload.

        Returns:
            [type]: [description]
        """
        return self.adaptee_obj.upload(*args, **kwargs, options=self.settings)

    def download(self, *args, **kwargs):
        """download.

        Returns:
            [type]: [description]
        """
        return self.adaptee_obj.download(*args, **kwargs, options=self.settings)
