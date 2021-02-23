# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

# --------------------------------------------------------------------


@dataclass
class Score(ABC):
    date_time: datetime
    set_used: str
    target: str

    @abstractmethod
    def __repr__(self):
        pass


# --------------------------------------------------------------------


@dataclass
class ClassificationScore(Score):
    """
    Dataclass that holds data of a scorig run for a classification pipeline.
    """

    accuracy: float
    auc: float
    cross_entropy: float

    def __repr__(self):
        return f"{self.date_time:%Y-%m-%d %H:%M:%S} {self.set_used} {self.target} {self.accuracy} {self.auc} {self.cross_entropy}"


# --------------------------------------------------------------------


@dataclass
class RegressionScore(Score):
    """
    Dataclass that holds data of a scorig run for a regression pipeline.
    """

    mae: float
    rmse: float
    rsquared: float

    def __repr__(self):
        return f"{self.date_time:%Y-%m-%d %H:%M:%S} {self.set_used} {self.target} {self.mae} {self.rmse} {self.rsquared}"
