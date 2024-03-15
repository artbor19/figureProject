from dataclasses import dataclass
from DTO import ReleaseDTO


@dataclass
class FigureDTO:
    title: str = None
    origin: str = None
    character: list[str] = None
    company: list[str] = None
    version: str = None
    releases: list[ReleaseDTO] = None
    url: str = None

    def get_string(self):
        figureString = (f"title={self.title}; "
                        f"origin={self.origin}; "
                        f"character={self.character}; "
                        f"company={self.company}; "
                        f"version={self.version};"
                        f"url={self.url}\n")

        for release in self.releases:
            figureString += release.get_string()

        return (
            figureString
        )
