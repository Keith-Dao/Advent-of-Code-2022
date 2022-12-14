"""
    Day 14 Solver Module
"""
from collections import defaultdict
import sys
from typing import Callable


class Solver:
    """
    Day 14 Solver
    """
    ROCK = "#"
    AIR = "."
    SAND = "o"

    def __init__(self) -> None:
        self.cave_map = defaultdict(lambda: Solver.AIR)
        self.max_y = 0
        self.sand_count = 0
        self.parsed = ""

    def construct_cave_map(self, filepath: str) -> None:
        """
        Construct the cave map from the given file, if it has not already been parsed.

        Args:
            filepath (str): Path to the file
        """

        if self.parsed == filepath:
            return

        def parse_line(line: str):
            points = [
                tuple(int(num) for num in point.split(","))
                for point in line.rstrip().split(" -> ")
            ]

            for start, end in zip(points, points[1:]):
                x_nodes, y_nodes = zip(start, end)
                for x_position in range(min(x_nodes), max(x_nodes) + 1):
                    for y_position in range(min(y_nodes), max(y_nodes) + 1):
                        self.cave_map[(x_position, y_position)] = Solver.ROCK
                self.max_y = max(self.max_y, *y_nodes)

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                parse_line(line=line)
        self.parsed = filepath
        self.sand_count = 0

    def simulate_one_sand(self, x_position, y_position, invalid_y) -> bool:
        """
        Simulate dropping one grain of sand.

        Args:
            x_position (int): The initial x position
            y_position (int): The initial y position
            invalid_y (int): The y position that is invalid
        Returns:
            Whether or not the grain of sand will remain stationary
        """

        while y_position <= self.max_y:
            if self.cave_map[(x_position, y_position + 1)] == Solver.AIR:
                y_position += 1
            elif self.cave_map[(x_position - 1, y_position + 1)] == Solver.AIR:
                x_position -= 1
                y_position += 1
            elif self.cave_map[(x_position + 1, y_position + 1)] == Solver.AIR:
                x_position += 1
                y_position += 1
            else:
                break

        if y_position == invalid_y:
            return False
        self.cave_map[(x_position, y_position)] = Solver.SAND
        return True

    def part_solve(self, filepath: str, get_invalid_y: Callable[[int], int]) -> int:
        """
        Generic solve.

        Args:
            filepath (str): Path to the input file
            get_invalid_y (callable): Method to determine the invalid y position
        Returns:
            Solution to part
        """
        self.construct_cave_map(filepath=filepath)

        moving = True
        while moving:
            moving = self.simulate_one_sand(
                x_position=500,
                y_position=0,
                invalid_y=get_invalid_y(self.max_y)
            )
            self.sand_count += moving

        return self.sand_count

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.part_solve(filepath=filepath, get_invalid_y=lambda max_y: max_y + 1)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.part_solve(filepath=filepath, get_invalid_y=lambda _: 0) + 1

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 14")
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
