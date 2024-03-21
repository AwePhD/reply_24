from reply_24.map import Map, Direction
from reply_24.score import parse_output, explore_adjacent_tiles, follow_path


def main():
    map_00 = Map("00-trailer.txt")
    map_01 = Map("01-comedy.txt")
    map_02 = Map("02-sentimental.txt")
    map_03 = Map("03-adventure.txt")
    map_04 = Map("04-drama.txt")
    map_05 = Map("05-horror.txt")
    example_result = parse_output("example_output.txt", map_00)
    print(explore_adjacent_tiles(example_result[0], map_00, Direction(-1, 0), example_result))
    print(follow_path(example_result, map_00))

    
if __name__ == "__main__":
    main()