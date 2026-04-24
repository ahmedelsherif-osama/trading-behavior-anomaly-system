from abc import ABC, abstractmethod
import pandas as pd


class BaseValidator(ABC):
    """
    Abstract base class for all validators.
    """

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> None:
        pass
