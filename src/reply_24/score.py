import itertools
from reply_24.map import (
    Coordinate,
    Node,
    Map,
    PathCost,
    SetTile,
    Direction,
    SilverPoint,
    TILE_KIND_TO_DIR,
    GoldenPoint,
    Tile,
)


def parse_output(file: str, map: Map) -> list[SetTile]:
    with open(file, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    return [
        SetTile(
            map.kind_to_tile[line.split(" ")[0]],
            int(line.split(" ")[1]),
            int(line.split(" ")[2]),
        )
        for line in lines
    ]


def get_neighbours(node: Node, map: Map, result: list[SetTile]) -> list[Node]:
    adjacent_tiles = []
    get_tile_result = node.get_tile(map, result)
    current_tile: SetTile
    connections: list[tuple[Direction | None, Direction]]
    if get_tile_result is None:
        raise Exception("no tile on node", node)
    if isinstance(get_tile_result, GoldenPoint):
        current_tile = SetTile(
            Tile(kind="Golden", cost=0, quantity=0),
            get_tile_result.x,
            get_tile_result.y,
        )
        connections = [
            (node.direction, Direction(0, 1)),
            (node.direction, Direction(1, 0)),
            (node.direction, Direction(0, -1)),
            (node.direction, Direction(-1, 0)),
        ]
    else:
        current_tile = get_tile_result
        connections = TILE_KIND_TO_DIR[current_tile.tile.kind]
    for connection in connections:
        if node.direction in connection:
            i = connection.index(node.direction)
            to_direction = connection[1 - i]  # 0 if i == 1, 1 if i == 0
            new_node = Node(
                coordinate=Coordinate(
                    x=current_tile.x + to_direction.dx,
                    y=current_tile.y + to_direction.dy,
                ),
                direction=Direction(
                    dx=-to_direction[0],
                    dy=-to_direction[1],
                ),
            )
            # print(node)
            # On a un chemin possible
            #  vérifions si une tuile est présente dans cette direction
            new_tile_if_present = new_node.get_tile(map, result)
            if new_tile_if_present is not None:
                adjacent_tiles.append(new_node)

    # print(adjacent_tiles)
    return adjacent_tiles


def find_path_dijkstra(
    map: Map, starting_point: Node, result: list[SetTile]
) -> dict[Node, tuple[PathCost, Node]]:
    dijkstra_output: dict[Node, tuple[PathCost, Node]] = dict()
    visited: set[Node] = set()
    to_visit: list[tuple[PathCost, Node]] = [
        (PathCost.from_node(starting_point, map, result), starting_point)
    ]
    while len(to_visit) != 0:
        to_visit.sort()
        # print()
        # for e in to_visit:
        # print(e)
        current_cost, current_node = to_visit.pop(0)
        visited.add(current_node)
        # print(current_node)
        if current_node not in dijkstra_output:
            dijkstra_output[current_node] = (current_cost, current_node)
        for neighbour in get_neighbours(current_node, map, result):
            if neighbour not in visited:
                if isinstance(neighbour.get_tile(map, result), GoldenPoint):
                    neighbour = Node(
                        neighbour.coordinate, None
                    )  # Direction is irrelevant for GoldenPoints
                to_visit.append(
                    (
                        current_cost + PathCost.from_node(neighbour, map, result),
                        neighbour,
                    )
                )
        # map.print([v.get_tile(map, result) for v in visited])
        # print(current_cost)
        # print(current_node)
    return dijkstra_output


def calculate_score(solution: list[SetTile], map: Map):
    score = 0
    for i in range(len(map.golden_points) - 1):
        gpA = map.golden_points[i]
        nodeA = Node(coordinate=Coordinate(x=gpA.x, y=gpA.y), direction=None)
        path_dijkstra = find_path_dijkstra(map, nodeA, solution)
        for j in range(i + 1, len(map.golden_points)):
            gpB = map.golden_points[j]
            nodeB = Node(coordinate=Coordinate(x=gpB.x, y=gpB.y), direction=None)
            # print(f"from ({gpA.x}, {gpA.y}) to ({gpB.x}, {gpB.y}) : ")
            # print(f"   costs {path_dijkstra[nodeB][0].cost}, earns {path_dijkstra[nodeB][0].earning}")
            score += path_dijkstra[nodeB][0].earning
    for tile in solution:
        score -= tile.tile.cost
    return score

# def path_score(path: list[SetTile], map: Map):
#     cost = 0
#     earning = 0
#     for set_tile in path:
#         assert set_tile.tile.kind in map.tile_dict().keys()
#         cost += set_tile.tile.cost
#         for silver_point in map.silver_points:
#             if silver_point.x == set_tile.x and silver_point.y == set_tile.y:
#                 earning += silver_point.score
#     return cost, earning


# def follow_path(
#     output: list[SetTile], map: Map
# ) -> dict[frozenset, list[list[SetTile]]]:
#     paths: dict[frozenset, list[list[SetTile]]] = {
#         frozenset({golden_point_A, golden_point_B}): []
#         for golden_point_B in map.golden_points
#         for golden_point_A in map.golden_points
#         if golden_point_A != golden_point_B
#     }
#     start_golden: GoldenPoint = map.golden_points[0]
#     path: list[SetTile] = []

#     queue: list[tuple[GoldenPoint | SetTile, Direction, GoldenPoint]] = []
#     current_tile: GoldenPoint | SetTile = map.golden_points[0]
#     visited: list[SetTile] = []
#     all_tiles_visited: bool = False
#     arriving_dir: Direction = Direction(0, 0)
#     while not all_tiles_visited:
#         visited.append(current_tile)
#         if isinstance(current_tile, GoldenPoint) and current_tile != start_golden:
#             paths[frozenset({start_golden, current_tile})].append(path)
#             start_golden = current_tile.copy()
#             path = []
#             print(f"Golden     {current_tile.x}, {current_tile.y}")
#         else:
#             path.append(current_tile.copy())
#             print(current_tile)

#         next_tiles_and_dir = explore_adjacent_tiles(
#             current_tile, map, arriving_dir, output
#         )
#         current_tile, arriving_dir = next_tiles_and_dir.pop(0)
#         while current_tile in visited:
#             if isinstance(current_tile, SetTile):
#                 for source_target in paths:
#                     if current_tile in paths[source_target]:
#                         i = paths[source_target].index(current_tile)
#                         paths[frozenset({start_golden, source_target[1]})] = (
#                             path.extend(paths[source_target][:i])
#                         )
#                         paths[frozenset({start_golden, source_target[0]})] = paths[
#                             source_target
#                         ][i + 1 :: -1].extend(path)

#                 # paths[frozenset({start_golden, current_tile})].append(path)

#             print(f"{current_tile} in visited")
#             if len(next_tiles_and_dir) != 0:
#                 current_tile, arriving_dir = next_tiles_and_dir.pop(0)
#             else:
#                 if len(queue) == 0:
#                     assert len(visited) - len(map.golden_points) == len(output)
#                     all_tiles_visited = True
#                     break
#                 else:
#                     current_tile, arriving_dir, start_golden = queue.pop(0)
#                     print("Backtracking to ", current_tile)
#         if next_tiles_and_dir:
#             print(
#                 "Adding to queue",
#                 [
#                     next_tile
#                     for next_tile in next_tiles_and_dir
#                     if next_tile[0] not in visited
#                 ],
#             )
#         queue.extend(
#             [
#                 (*next_tile, start_golden)
#                 for next_tile in next_tiles_and_dir
#                 if next_tile[0] not in visited
#             ]
#         )

#     return paths


# def explore_adjacent_tiles(
#     current_tile: SetTile | GoldenPoint,
#     map: Map,
#     from_direction: Direction,
#     output: list[SetTile],
# ) -> list[(SetTile | GoldenPoint, Direction)]:
#     adjacent_tiles = []
#     if isinstance(current_tile, GoldenPoint):
#         current_tile = SetTile(Tile("Golden", 0, None), current_tile.x, current_tile.y)
#         connections = [
#             (from_direction, Direction(0, 1)),
#             (from_direction, Direction(1, 0)),
#             (from_direction, Direction(0, -1)),
#             (from_direction, Direction(-1, 0)),
#         ]
#     else:
#         connections = TILE_KIND_TO_DIR[current_tile.tile.kind]
#     for connection in connections:
#         if from_direction in connection:
#             i = connection.index(from_direction)
#             to_direction = connection[1 - i]  # 0 if i == 1, 1 if i == 0
#             # On a un chemin possible
#             y = current_tile.y + to_direction.dy
#             #  vérifions si une tuile est présente dans cette direction
#             x = current_tile.x + to_direction.dx
#             for available_set_tile in output:
#                 if x == available_set_tile.x and y == available_set_tile.y:
#                     adjacent_tiles.append(
#                         (available_set_tile, (-to_direction[0], -to_direction[1]))
#                     )
#             # vérifions si un golden point est présent dans cette direction
#             # print(f"({x}, {y})")
#             for golden_point in map.golden_points:
#                 # print(f"Golden point({golden_point.x}, {golden_point.y})")
#                 if x == golden_point.x and y == golden_point.y:
#                     adjacent_tiles.append(
#                         (golden_point, (-to_direction[0], -to_direction[1]))
#                     )

#     # print(adjacent_tiles)
#     return adjacent_tiles
