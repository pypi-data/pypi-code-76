from fiji_arnheim.registries.helper import BaseImageJHelper, set_running_helper


class ImageJHelper(BaseImageJHelper):

    def __init__(self, headless=False, bind=True, version="sc.fiji:fiji:2.1.1", plugins = []) -> None:
        if bind: set_running_helper(self)
        super().__init__(headless=headless, version=version, plugins= plugins)