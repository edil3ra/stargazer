from dataclasses import dataclass
from serde import serialize, deserialize
from serde.json import from_json, to_json
from typing import List

@deserialize
@serialize
@dataclass
class Stargazer:
    name: str
    count: int


@deserialize
@serialize
@dataclass
class RepoStargazer:
    repo: str
    stargazers: List[Stargazer]
