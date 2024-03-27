from typing import NamedTuple


# Tile 3:
# From left to right (*)
# Tile 5:
# From down to right (*)
# Tile 6:
# From left to down (*)
# Tile 7:
# • From left to right (*)
# • From left to down (*)
# • From down to right (*)
# Tile 9:
# From up to right (*)
# Tile 96:
# • From left to down (*)
# • From up to right (*)
# Tile A:
# From left to up (*)
# Tile A5:
# • From left to up (*)
# • From down to right (*)
# Tile B:
# • From left to right (*)
# • From left to up (*)
# • From up to right (*)
# Tile C:
# From up to down (*)
# Tile C3:
# • From left to right (*)
# • From up to down (*)
# Tile D:
# • From up to down (*)
# • From up to right (*)
# • From down to right (*)
# Tile E:
# • From left to up (*)
# • From left to down (*)
# • From up to down (*)
# Tile F:
# • From left to right (*)
# • From left to down (*)
# • From left to up (*)
# • From up to down (*)
# • From down to right (*)
# • From up to right (*)
# TILE_KIND_TO_DIR = {
#     "3": [((-1, 0), (1, 0))],
#     "5": [((0, 1), (1, 0))],
#     "6": [((-1, 0), (0, 1))],
#     "7": [((-1, 0), (1, 0)), ((-1, 0), (0, 1)), ((0, 1), (1, 0))],
#     "9": [((0, -1), (1, 0))],
#     "96": [((-1, 0), (0, 1)), ((0, -1), (1, 0))],
#     "A": [((-1, 0), (0, -1))],
#     "A5": [((-1, 0), (0, -1)), ((0, 1), (1, 0))],
#     "B": [((-1, 0), (1, 0)), ((-1, 0), (0, -1)), ((0, -1), (1, 0))],
#     "C": [((0, -1), (0, 1))],
#     "C3": [((-1, 0), (1, 0)), ((0, -1), (0, 1))],
#     "D": [((0, -1), (0, 1)), ((0, -1), (1, 0)), ((0, 1), (1, 0))],
#     "E": [((-1, 0), (0, -1)), ((-1, 0), (0, 1)), ((0, -1), (0, 1))],
#     "F": [
#         ((-1, 0), (1, 0)),
#         ((-1, 0), (0, 1)),
#         ((-1, 0), (0, -1)),
#         ((0, -1), (0, 1)),
#         ((0, 1), (1, 0)),
#         ((0, -1), (1, 0)),
#     ],
# }


class Direction(NamedTuple):
    x: int
    y: int


TILE_KIND_TO_DIR = {
    "3": [(Direction(-1, 0), Direction(1, 0))],
    "5": [(Direction(0, 1), Direction(1, 0))],
    "6": [(Direction(-1, 0), Direction(0, 1))],
    "7": [
        (Direction(-1, 0), Direction(1, 0)),
        (Direction(-1, 0), Direction(0, 1)),
        (Direction(0, 1), Direction(1, 0)),
    ],
    "9": [(Direction(0, -1), Direction(1, 0))],
    "96": [(Direction(-1, 0), Direction(0, 1)), (Direction(0, -1), Direction(1, 0))],
    "A": [(Direction(-1, 0), Direction(0, -1))],
    "A5": [(Direction(-1, 0), Direction(0, -1)), (Direction(0, 1), Direction(1, 0))],
    "B": [
        (Direction(-1, 0), Direction(1, 0)),
        (Direction(-1, 0), Direction(0, -1)),
        (Direction(0, -1), Direction(1, 0)),
    ],
    "C": [(Direction(0, -1), Direction(0, 1))],
    "C3": [(Direction(-1, 0), Direction(1, 0)), (Direction(0, -1), Direction(0, 1))],
    "D": [
        (Direction(0, -1), Direction(0, 1)),
        (Direction(0, -1), Direction(1, 0)),
        (Direction(0, 1), Direction(1, 0)),
    ],
    "E": [
        (Direction(-1, 0), Direction(0, -1)),
        (Direction(-1, 0), Direction(0, 1)),
        (Direction(0, -1), Direction(0, 1)),
    ],
    "F": [
        (Direction(-1, 0), Direction(1, 0)),
        (Direction(-1, 0), Direction(0, 1)),
        (Direction(-1, 0), Direction(0, -1)),
        (Direction(0, -1), Direction(0, 1)),
        (Direction(0, 1), Direction(1, 0)),
        (Direction(0, -1), Direction(1, 0)),
    ],
    # "Golden": [
    #     (Direction(0, 0), Direction(0, 1)),
    #     (Direction(0, 0), Direction(1, 0)),
    #     (Direction(0, 0), Direction(0, -1)),
    #     (Direction(0, 0), Direction(-1, 0)),
    # ]
}


class GoldenPoint(NamedTuple):
    x: int
    y: int

    def copy(self):
        return GoldenPoint(self.x, self.y)


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

    def copy(self):
        return SetTile(self.tile, self.x, self.y)

    def __str__(self) -> str:
        return f"{self.tile.kind}   ({self.x}, {self.y})"


class Map:
    # Méthodes:
    # - A réfléchir: Methode pour faire optimiser la recherche de solution (cache, memoire, deplacement)
    # ok tile
    # - get_score(self) -> int
    # - sort une solution dans un txt ouput(self) -> None
    def __init__(self, in_file: str) -> None:
        with open(in_file, mode="r", encoding="utf-8") as file:
            lines = [ line.strip() for line in file.readlines()]

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
        tiles = [
            Tile(line.split(" ")[0], int(line.split(" ")[1]), int(line.split(" ")[2]))
            for line in lines[1 + self.n_golden_points + self.n_silver_points :]
        ]
        self.kind_to_tile = {
            tile.kind: tile
            for tile in tiles
        }

    # def tile_dict(self) -> dict[str, Tile]:
    #     return {tile.kind: tile for tile in self.tiles}

    def output(self) -> None: ...

    ...
