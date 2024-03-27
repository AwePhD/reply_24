from reply_24.map import Map, Direction, SetTile, Tile
from reply_24.score import parse_output, explore_adjacent_tiles, follow_path
from reply_24.solver import Solver


def main():
    file_names = [
        "00-trailer.txt",
        "01-comedy.txt",
        "02-sentimental.txt",
        "03-adventure.txt",
        "04-drama.txt",
        "05-horror.txt",
    ]
    solver = Solver(Map(file_names[5]))
    solver.solve()


    map_00 = Map("00-trailer.txt")
    map_01 = Map("01-comedy.txt")
    map_02 = Map("02-sentimental.txt")
    map_03 = Map("03-adventure.txt")
    map_04 = Map("04-drama.txt")
    map_05 = Map("05-horror.txt")
    map_example = Map("example_input.txt")
    example_result = parse_output("example_output.txt", map_example)
    print(SetTile(Tile('F', 2, 1), 2, 2) == SetTile(Tile('F', 2, 1), 2, 2))
    print(explore_adjacent_tiles(example_result[2], map_example, Direction(0, 1), example_result))
    for k, v in follow_path(example_result, map_example).items():
        print(k, v)
    
if __name__ == "__main__":
    main()
