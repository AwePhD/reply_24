from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int


class Direction(NamedTuple):
    dx: int
    dy: int


TILE_KIND_TO_DIR: dict[str, list[tuple[Direction, Direction]]] = {
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
}

TILE_KIND_TO_CHAR = {
    "3": "\u2500",
    "5": "\u256d",
    "6": "\u256e",
    "7": "\u252c",
    "9": "\u2570",
    # "96": "\u2534",
    "A": "\u256f",
    # "A5": "\u251c",
    "B": "\u2534",
    "C": "\u2502",
    # "C3": "\u2551",
    "D": "\u251c",
    "E": "\u2524",
    "F": "\u253c",

}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    cost: int
    quantity: int
    kind: str


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
            lines = [line.strip() for line in file.readlines()]

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
            Tile(
                kind=line.split(" ")[0],
                cost=int(line.split(" ")[1]),
                quantity=int(line.split(" ")[2]),
            )
            for line in lines[1 + self.n_golden_points + self.n_silver_points :]
        ]
        self.kind_to_tile = {tile.kind: tile for tile in tiles}

    # def tile_dict(self) -> dict[str, Tile]:
    #     return {tile.kind: tile for tile in self.tiles}

    def _get_char_of_coord(self, x: int, y: int, set_tiles: list[SetTile]):
        for gold in self.golden_points:
            if x == gold.x and y == gold.y:
                return "G"
        for silv in self.silver_points:
            if x == silv.x and y == silv.y:
                return "S"
        for tile in set_tiles:
            if x == tile.x and y == tile.y:
                return TILE_KIND_TO_CHAR[tile.tile.kind]
            
        return "."

    def print(self, set_tiles: list[SetTile]):
        output = []
        for y in range(self.height):
            for x in range(self.width):
                output.append(self._get_char_of_coord(x, y, set_tiles))
            output.append('\n')
        print("".join(output))


    def output(self) -> None: ...

    ...


class Node(NamedTuple):
    coordinate: Coordinate
    direction: Direction | None

    @staticmethod
    def from_tile(tile: SetTile, direction: Direction | None = None):
        return Node(coordinate=Coordinate(x=tile.x, y=tile.y), direction=direction)

    def get_tile(self, map: Map, result: list[SetTile]) -> SetTile | GoldenPoint | None:
        for golden in map.golden_points:
            if golden.x == self.coordinate.x and golden.y == self.coordinate.y:
                return golden
        for tile in result:
            if tile.x == self.coordinate.x and tile.y == self.coordinate.y:
                return tile
        return None


class PathCost(NamedTuple):
    cost: int
    earning: int

    @staticmethod
    def from_node(node: Node, map: Map, result: list[SetTile]) -> "PathCost":
        earning: int = 0
        for silver_point in map.silver_points:
            if (
                silver_point.x == node.coordinate.x
                and silver_point.y == node.coordinate.y
            ):
                earning = silver_point.score
        tile_or_none = node.get_tile(map, result)
        if tile_or_none is None or isinstance(tile_or_none, GoldenPoint):
            return PathCost(0, 0)
        else:
            return PathCost(cost=tile_or_none.tile.cost, earning=earning)

    def __add__(self, other: tuple):
        return PathCost(self.cost + other[0], self.earning + other[1])
