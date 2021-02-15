# -*- coding: utf-8 -*-

"""The `ConceptNet <https://conceptnet.io/>`_ dataset.

Get a summary with ``python -m pykeen.datasets.conceptnet``
"""

import click
from more_click import verbose_option

from .base import SingleTabbedDataset
from ..typing import TorchRandomHint

URL = 'https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz'


class ConceptNet(SingleTabbedDataset):
    """The ConceptNet dataset from [speer2017]_.

    The dataset is structured into 5 columns (see https://github.com/commonsense/conceptnet5/wiki/Downloads#assertions):
    edge URL, relation, head, tail, metadata.

    .. [speer2017] Robyn Speer, Joshua Chin, and Catherine Havasi. (2017)
       `ConceptNet 5.5: An Open Multilingual Graph of General Knowledge <https://arxiv.org/abs/1612.03975>`_.
       *In proceedings of AAAI 31*.
    """

    def __init__(
        self,
        create_inverse_triples: bool = False,
        random_state: TorchRandomHint = 0,
        **kwargs,
    ):
        """Initialize the `ConceptNet <https://github.com/commonsense/conceptnet5>`_ dataset from [speer2017]_.

        :param create_inverse_triples: Should inverse triples be created? Defaults to false.
        :param random_state: The random seed to use in splitting the dataset. Defaults to 0.
        :param kwargs: keyword arguments passed to :class:`pykeen.datasets.base.SingleTabbedDataset`.
        """
        super().__init__(
            url=URL,
            create_inverse_triples=create_inverse_triples,
            random_state=random_state,
            read_csv_kwargs=dict(
                usecols=[2, 1, 3],
                header=None,
            ),
            **kwargs,
        )


@click.command()
@verbose_option
def _main():
    ds = ConceptNet()
    ds.summarize()


if __name__ == '__main__':
    _main()
