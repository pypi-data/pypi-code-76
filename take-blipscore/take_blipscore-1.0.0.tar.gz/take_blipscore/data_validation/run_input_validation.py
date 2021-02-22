import typing as tp


def input_type_validation(satisfaction_rate: tp.Union[int, float],
                          resolution_rate: tp.Union[int, float]) -> None:
    """Validate run input type.

    :param satisfaction_rate: A value between 0 and 1 that from satisfaction_rate package.
    :type  satisfaction_rate: ``tp.Union[int, float]``
    :param resolution_rate: A value between 0 and 1 that from resolution_rate package
    :type resolution_rate:  ``tp.Union[int, float]``
    :raise TypeError: if any input is not instance of expected type.
    """
    if not any([isinstance(satisfaction_rate, float),
                isinstance(satisfaction_rate, int)]):
        raise TypeError("`satisfaction_rate` input must be type `float` type")
    if not any([isinstance(resolution_rate, float),
                isinstance(resolution_rate, int)]):
        raise TypeError("`resolution_rate` input must be type `float` type")
