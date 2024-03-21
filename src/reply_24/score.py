from reply_24.map import Map, SetTile, Direction, SilverPoint, TILE_KIND_TO_DIR, GoldenPoint, Tile


def parse_output(file: str, map: Map) -> list[SetTile]:
    with open(file, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    return [
        SetTile(
            map.tile_dict()[line.split(" ")[0]],
            int(line.split(" ")[1]),
            int(line.split(" ")[2]),
        )
        for line in lines
    ]


def path_score(path: list[SetTile], map: Map):
    cost = 0
    earning = 0
    for set_tile in path:
        assert set_tile.tile.kind in map.tile_dict().keys()
        cost += set_tile.tile.cost
        for silver_point in map.silver_points:
            if silver_point.x == set_tile.x and silver_point.y == set_tile.y:
                earning += silver_point.score
    return cost, earning


def follow_path(path: list[SetTile], map: Map) -> list[list[SetTile]]:
    # to fix
    start = map.golden_points[0]
    queue = [start]
    visited = [start]
    all_tiles_visited = False
    arriving_dir = Direction(0, 0)
    while not all_tiles_visited:
        next_tiles = explore_adjacent_tiles(queue[0], map, arriving_dir, path)
        if len(next_tiles) != 0:
            print(f'{next_tiles[0].tile.kind}     {next_tiles[0].x}, {next_tiles[0].y}')
        queue.extend(next_tiles)
        visited.append(queue.pop(0))
        if len(queue) == 0:
            all_tiles_visited = True

    return visited
    

def explore_adjacent_tiles(current_tile: SetTile|GoldenPoint, map: Map, arriving_dir: Direction, output: list[SetTile]) -> list[SetTile|GoldenPoint]:
    adjacent_tiles = []
    if isinstance(current_tile, GoldenPoint):
        current_tile = SetTile(Tile('Golden', 0, None), current_tile.x, current_tile.y)
    for connection in TILE_KIND_TO_DIR[current_tile.tile.kind]:
        if arriving_dir in connection:
            i = connection.index(arriving_dir)
            to_dir = connection[1 - i]
            # On a un chemin possible
            y = current_tile.y + to_dir.y
            #  vérifions si une tuile est présente dans cette direction
            x = current_tile.x + to_dir.x
            for available_set_tile in output:
                if x == available_set_tile.x and y == available_set_tile.y:
                    adjacent_tiles.append(available_set_tile)
            # vérifions si un golden point est présent dans cette direction
            for golden_point in map.golden_points:
                if x == golden_point.x and y == golden_point.y:
                    adjacent_tiles.append(golden_point)
            
    return adjacent_tiles


