from typing import NamedTuple


# t = Tile(5, 4)
# t.x -> 5
class Tile(NamedTuple):
    x: int
    y: int
    # Add other state

class Map:
    # tiles (list[Tile])
    # gold_tiles (list[Tile])
    # silver_tiles (list[Tile])
    # solver (Solver)
    # Méthodes:
    # - A réfléchir: Methode pour faire optimiser la recherche de solution (cache, memoire, deplacement)
    # - get_score(self) -> int
    # - sort une solution dans un txt ouput(self) -> None
    def __init__(self, in_file: str) -> None:
        ...

    def output(self) -> None:
        ...
    ...