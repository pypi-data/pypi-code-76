from logger import logger
from ...file_utils import file_exists, dir_exists
from ...path_utils import get_newest_filepath
from ...prompt_utils import weights_scratch_prompt, weights_newest_prompt

class ResumeWeightsChecker:
    def __init__(self, resume: bool, resume_path: str=None, weights_save_dir: str=None, weights_extension: str='pth'):
        self.resume = resume
        self.resume_path = resume_path
        self.weights_save_dir = weights_save_dir
        self.weights_extension = weights_extension

    def _scratch_prompt(self):
        start_from_scratch = weights_scratch_prompt()
        if start_from_scratch:
            self.resume = False
            self.resume_path = None
        else:
            raise Exception

    def prompt_if_invalid(self):
        if self.resume:
            if self.resume_path is None:
                if self.weights_save_dir is not None:
                    if dir_exists(self.weights_save_dir):
                        self.resume_path = get_newest_filepath(dir_path=self.weights_save_dir, extension=self.weights_extension)
                        if self.resume_path is None:
                            logger.warning(f"Couldn't find a .{self.weights_extension} weights file in:\n{self.weights_save_dir}")
                            self._scratch_prompt()
                    else:
                        logger.warning(f"Couldn't find weights dir:\n{self.weights_save_dir}")
                        self._scratch_prompt()
                else:
                    logger.warning(f"weights_save_dir hasn't been provided for detecting the newest weights path.")
                    self._scratch_prompt()
            else:
                if not file_exists(self.resume_path):
                    logger.warning(f"Couldn't find resume_path:\n{self.resume_path}")
                    if dir_exists(self.weights_save_dir):
                        newest_weights_path = get_newest_filepath(dir_path=self.weights_save_dir, extension=self.weights_extension)
                        if newest_weights_path is not None:
                            use_newest_weights = weights_newest_prompt(newest_weights_path)
                            if use_newest_weights:
                                self.resume_path = newest_weights_path
                            else:
                                self._scratch_prompt()
                        else:
                            logger.warning(f"Couldn't find newest weights.")
                            self._scratch_prompt()
                    else:
                        self._scratch_prompt()
        else:
            self.resume_path = None

    def get_updated(self) -> (bool, str):
        return self.resume, self.resume_path