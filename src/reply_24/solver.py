from typing import NamedTuple
from random import choice
from .map import GoldenPoint, Map, SilverPoint, Tile

Point = SilverPoint | GoldenPoint

def sign(x:int) -> int:
    return -1 if x < 0 else 1 if x > 0 else 0

class Position(NamedTuple):
    x: int
    y: int

def bird_distance(a: Point, b: Point) -> float:
    return abs(a.x - b.x) + abs(a.y - b.y)

DIRECTION_TO_TILES_SET: dict[Position, list[str]] = {
    Position(1, 1): ["6", "9", "7", "B", "D", "E", "F"],
    Position(1, 0): ["3", "7", "B", "F"],
    Position(1, -1): ["5", "7", "B", "A", "D", "E", "F"],
    Position(0, 1): ["C", "E", "D", "F"],
    Position(0, -1): ["C", "E", "D", "F"],
    Position(-1, 1): ["5", "7", "B", "A", "D", "E", "F"],
    Position(-1, 0): ["3", "7", "B", "F"],
    Position(-1, -1): ["6", "9", "7", "B", "D", "E", "F"],
}


class Solver:
    def __init__(self, map: Map):
        self.map = map

    def _get_golden_pairs(self, golden_points) -> list[tuple[GoldenPoint, GoldenPoint]]:
        points_pair_to_distance: dict[tuple[GoldenPoint, GoldenPoint], float] = {
            (point_a, point_b): bird_distance(point_a, point_b)
            for i, point_a in enumerate(golden_points)
            for j, point_b in enumerate(golden_points)
            if i < j
        }

        sorted_points_pair_and_distance = sorted(points_pair_to_distance.items(), key= lambda d: d[1])
        return [
            points_pair
            for points_pair, _ in sorted_points_pair_and_distance
        ]

    def solve(self) -> None:
        golden_points_pairs = self._get_golden_pairs(self.map.golden_points)
        for (start, next_golden) in golden_points_pairs:
            current = Position(start.x, start.y)
            direction = Position(sign(next_golden.x - start.x), sign(next_golden.y - start.y))

            target_x = Position( next_golden.x - direction.x, next_golden.y)
            target_y = Position( next_golden.x, next_golden.y - direction.y)
            target = target_x if direction.x == 0 else target_y

            tile_kind = DIRECTION_TO_TILES_SET[direction]
            kind = choice(tile_kind)

            tile = self.map.kind_to_tile[kind]
            self.map.kind_to_tile[kind] = Tile(tile.kind, tile.cost, tile.quantity-1)







        # Pour une paire (p1, p2):
        #   new_tile = Po
        #   cur update

        return
