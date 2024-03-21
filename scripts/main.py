from reply_24.map import Map
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


if __name__ == "__main__":
    main()
