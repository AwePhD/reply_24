from typing import NamedTuple


class GoldenPoint(NamedTuple):
    x: int
    y: int


class SilverPoint(NamedTuple):
    x: int
    y: int
    score: int


class Tile(NamedTuple):
    kind: str
    cost: int
    count: int


class SetTile(NamedTuple):
    tile: Tile
    x: int
    y: int


class Map:
    # Méthodes:
    # - A réfléchir: Methode pour faire optimiser la recherche de solution (cache, memoire, deplacement)
    # ok tile
    # - get_score(self) -> int
    # - sort une solution dans un txt ouput(self) -> None
    def __init__(self, in_file: str) -> None:
        with open(in_file, mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        width, height, n_golden_points, n_silver_points, n_tile_types = lines[0].split(
            " "
        )
        self.width = int(width)
        self.height = int(height)
        self.n_golden_points = int(n_golden_points)
        self.n_silver_points = int(n_silver_points)
        self.n_tile_types = int(n_tile_types)

        self.golden_points = [
            GoldenPoint(int(line.split(" ")[0]), int(line.split(" ")[1]))
            for line in lines[1 : 1 + self.n_golden_points]
        ]
        self.silver_points = [
            SilverPoint(
                int(line.split(" ")[0]),
                int(line.split(" ")[1]),
                int(line.split(" ")[2]),
            )
            for line in lines[
                1
                + self.n_golden_points : 1
                + self.n_golden_points
                + self.n_silver_points
            ]
        ]
        self.tiles = [
            Tile(line.split(" ")[0], int(line.split(" ")[1]), int(line.split(" ")[2]))
            for line in lines[
                 1
                + self.n_golden_points
                + self.n_silver_points:
            ]
        ]

    def tile_dict(self) -> dict[str, Tile]:
        return {tile.kind: tile for tile in self.tiles}

    def output(self) -> None: ...

    ...

