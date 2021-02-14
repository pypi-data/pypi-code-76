from plomberie.progress_bar.abstract_progress_bar import AbstractProgressBar


class DisabledProgressBar(AbstractProgressBar):
    def set_total(self, total: int) -> None:
        pass

    def increment(self) -> None:
        pass

    def close(self) -> None:
        pass

    @staticmethod
    def get_instance(label: str) -> 'AbstractProgressBar':
        return DisabledProgressBar()
