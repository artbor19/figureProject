from dataclasses import dataclass
from decimal import Decimal
import datetime


@dataclass
class ReleaseDTO:
    releaseDate: datetime = None
    releasePrice: Decimal = None
    releaseCurrency: str = None
    releaseJanCode: str = None

    def get_string(self):
        return (
            f"releaseDate={self.releaseDate}; "
            f"releasePrice={self.releasePrice}; "
            f"releaseCurrency={self.releaseCurrency}; "
            f"releaseJanCode={self.releaseJanCode};\n"
        )
