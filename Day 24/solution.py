"""
    Day 24 Solver Module
"""
from functools import cache
import heapq
import sys


class Solver:
    """
    Day 24 Solver
    """

    DIRECTIONS = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0),
        ".": (0, 0)
    }

    @staticmethod
    def parse(
        filepath: str
    ) -> tuple[
        tuple[int, int],
        tuple[int, int],
        frozenset[tuple[int, int]],
        frozenset[tuple[tuple[int, int], tuple[int, int]]],
        int,
        int
    ]:
        """
        Parse the input file.

        Args:
            filepath (str): The path to the input file.
        Returns:
            The starting position, ending position, grid, blizzards,
            maximum row and maximum column respectively.
        """
        grid, blizzards = set(), set()
        starting_position = ending_position = -1, -1
        row_max = col_max = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for row_num, line in enumerate(file, start=-1):
                if row_num == -1:
                    starting_position = row_num, line.index(".") - 1
                    col_max = len(line.rstrip()) - 2
                    continue

                is_last_line = True
                for col_num, char in enumerate(line.rstrip()[1:-1]):
                    if char == "#":
                        continue

                    grid.add((row_num, col_num))
                    if char not in Solver.DIRECTIONS or char == ".":
                        continue
                    blizzards.add(
                        ((row_num, col_num), Solver.DIRECTIONS[char])
                    )
                    is_last_line = False

                if is_last_line:
                    ending_position = row_num, line.index(".") - 1
                row_max = row_num

        grid.add(starting_position)
        grid.add(ending_position)
        return (
            starting_position,
            ending_position,
            frozenset(grid),
            frozenset(blizzards),
            row_max,
            col_max
        )

    @staticmethod
    def distance(position_1: tuple[int, int], position_2: tuple[int, int]) -> int:
        """
        Return the manhattan distance between two points.

        Args:
            position_1 (tuple[int, int]): A position
            position_2 (tuple[int, int]): Another position
        Returns:
            The manhattan distance between the two points.
        """
        x_1, y_1 = position_1
        x_2, y_2 = position_2
        return abs(x_1 - x_2) + abs(y_1 - y_2)

    @staticmethod
    @cache
    def step(
        # self,
        blizzards: frozenset[tuple[tuple[int, int], tuple[int, int]]],
        grid: frozenset[tuple[int, int]],
        row_max: int,
        col_max: int
    ) -> tuple[
        frozenset[tuple[tuple[int, int], tuple[int, int]]],
        frozenset[tuple[int, int]]
    ]:
        """
        Move all the blizzards forward one minute.

        Args:
            blizzards (set[tuple[tuple[int, int], tuple[int, int]]]): All the blizzards
            grid (set[tuple[int, int]]): All the possible positions
            row_max (int): The maximum row number
            col_max (int): The maximum column number
        Returns:
            The blizzards and free positions after one minute.
        """
        blizzards = frozenset(
            (
                (
                    (row + d_row) % row_max,
                    (col + d_col) % col_max
                ),
                (
                    d_row,
                    d_col
                )
            )
            for (row, col), (d_row, d_col) in blizzards
        )
        free = grid - {blizzard for blizzard, _ in blizzards}
        return blizzards, free

    def __init__(self) -> None:
        self.seen = {}

    def map_to_string(
        self,
        starting_position: tuple[int, int],
        ending_position: tuple[int, int],
        row_max: int,
        col_max: int,
        blizzards: frozenset[tuple[tuple[int, int], tuple[int, int]]]
    ) -> str:
        """
        Convert the map to a string for visualisation.

        Args:
            starting_position (tuple[int, int]): The starting position
            ending_position (tuple[int, int]): The ending position
            row_max (int): The maximum number of rows
            col_max (int): The maximum number of columns
            blizzards (frozenset[tuple[tuple[int, int], tuple[int, int]]]): The blizzards
        Returns:
            A visual format of the map.
        """
        first_line = ["#"] * (col_max + 2)
        first_line[starting_position[1] + 1] = "."

        middle = []
        for row in range(row_max):
            line = ["#"]
            for col in range(col_max):
                chars = [
                    direction
                    for direction, change in Solver.DIRECTIONS.items()
                    if ((row, col), change) in blizzards
                ]
                if len(chars) == 0:
                    line.append(".")
                elif len(chars) == 1:
                    line.append(chars[0])
                else:
                    line.append(str(len(chars)))
            line.append("#")
            middle.append(line)

        last_line = ["#"] * (col_max + 2)
        last_line[ending_position[1] + 1] = "."

        return "\n".join("".join(line) for line in [first_line, *middle, last_line])

    def solve_part(self, filepath: str, rounds: int) -> int:
        """
        Generic solve.

        Args:
            filepath (str): Path to the input file
            rounds (int): The number of rounds that need to be taken
        Returns:
            The solution to the part.
        """
        starting_position, ending_position, grid, blizzards, row_max, col_max = self.parse(
            filepath
        )

        def search(
            starting_position: tuple[int, int],
            ending_position: tuple[int, int],
            blizzards: frozenset[tuple[tuple[int, int], tuple[int, int]]]
        ) -> tuple[int, frozenset[tuple[tuple[int, int], tuple[int, int]]]]:
            heap = [(0, starting_position, blizzards, 0)]
            seen = set()
            while heap:
                _, (row, col), blizzards, time = heapq.heappop(heap)

                blizzards, free = Solver.step(
                    blizzards, grid, row_max, col_max)
                for d_row, d_col in Solver.DIRECTIONS.values():
                    new_position = row + d_row, col + d_col
                    if new_position == ending_position:
                        return time + 1, blizzards
                    if new_position in free and (new_position, time) not in seen:
                        seen.add((new_position, time))
                        heapq.heappush(
                            heap,
                            (
                                time +
                                Solver.distance(new_position, ending_position),
                                new_position,
                                blizzards,
                                time + 1,
                            )
                        )
            return -1, frozenset()

        time_taken = 0
        for _ in range(rounds):
            time, blizzards = search(
                starting_position=starting_position,
                ending_position=ending_position,
                blizzards=blizzards
            )
            time_taken += time
            starting_position, ending_position = ending_position, starting_position
        return time_taken

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.solve_part(filepath=filepath, rounds=1)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.solve_part(filepath=filepath, rounds=3)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 24")
        print(f"Solving: {filepath}")
        print("Part 1")
        print(self.part_1(filepath))
        print("---")
        print("Part 2")
        print(self.part_2(filepath))


if __name__ == "__main__":
    solver = Solver()
    match sys.argv:
        case [_, "--path", path]:
            solver.solve(path)
        case [_]:
            solver.solve()
        case _:
            print("Usage: python solution.py --path <path>")
