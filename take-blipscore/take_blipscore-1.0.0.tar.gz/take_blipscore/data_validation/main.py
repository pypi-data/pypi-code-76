import typing as tp

from .run_input_validation import input_type_validation


def data_validation(satisfaction_rate: tp.Union[int, float],
                    resolution_rate: tp.Union[int, float]) -> None:
    """Main function of validation layer.

    This method call all other validation that must exist on beginning of run.

    :param satisfaction_rate: A value between 0 and 1 that from satisfaction_rate package.
    :type  satisfaction_rate: ``tp.Union[int, float]``
    :param resolution_rate: A value between 0 and 1 that from resolution_rate package
    :type resolution_rate:  ``tp.Union[int, float]``
    """
    input_type_validation(satisfaction_rate=satisfaction_rate,
                          resolution_rate=resolution_rate)
