import math
from reply_24.map import Map, Direction, Node, SetTile, Tile
from reply_24.score import calculate_score, find_path_dijkstra, get_neighbours, parse_output
from reply_24.solver import Solver
import time

def main():
    file_names = [
        "00-trailer.txt",
        "01-comedy.txt",
        "02-sentimental.txt",
        "03-adventure.txt",
        "04-drama.txt",
        "05-horror.txt",
    ]
    # solver = Solver(Map(file_names[5]))
    # solver.solve()
    # print(Tile('kind', 5, 6) == ('kind', 5, 6))  # True


    map_00 = Map("00-trailer.txt")
    map_01 = Map("01-comedy.txt")
    map_02 = Map("02-sentimental.txt")
    map_03 = Map("03-adventure.txt")
    map_04 = Map("04-drama.txt")
    map_05 = Map("05-horror.txt")
    map_example = Map("example_input.txt")
    example_result = parse_output("example_output.txt", map_example)
    map_example.print(example_result)
    start_time = time.perf_counter()
    print("Score =", calculate_score(example_result, map_example))
    
    stop_time = time.perf_counter()
    execution_time = stop_time - start_time
    units = {0: 's', -3: 'ms', -6: 'µs', -9: 'ns'}
    execution_time_power_of_ten = int(math.log10(execution_time))
    execution_time_power_of_ten -= execution_time_power_of_ten % 3
    execution_time = execution_time * 10**(-execution_time_power_of_ten)
    print(f"[Done] Execution time: {execution_time:.2f} {units[execution_time_power_of_ten]}")
if __name__ == "__main__":
    main()
