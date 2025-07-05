from dataclasses import dataclass


@dataclass(frozen=True)
class RSSUrl:
    url: str
    name: str
    description: str = ""
    active: bool = True
