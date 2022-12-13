"""
    Day 13 Solver Module
"""
from functools import cmp_to_key
from io import TextIOWrapper
import json
import sys


class Solver:
    """
    Day 13 Solver
    """

    def parse(self, file: TextIOWrapper) -> tuple[list, list]:
        """
        Parse the pairs.

        Args:
            file (TextIOWrapper): Opened file pointer
        Returns:
            Tuple with the parsed pairs.
        """
        return tuple(json.loads(file.readline().rstrip()) for _ in range(2))

    def compare(self, left: list | int, right: list | int) -> int:
        """
        Compare the left and right values.

        Args:
            left (list | int): The left value
            right (list | int): The right value
        Returns:
            A positive number if right > left.
            A negative number if right < left.
            Otherwise, 0
        """
        if isinstance(left, int) and isinstance(right, int):
            return right - left
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]

        if len(left) == 0 or len(right) == 0:
            return len(right) - len(left)

        left_first, *left_remaining = left
        right_first, *right_remaining = right
        return self.compare(left_first, right_first) or self.compare(left_remaining, right_remaining)

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        pair_number = 1
        result = 0
        line = " "
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            while line != "":
                if self.compare(*self.parse(file)) > 0:
                    result += pair_number
                pair_number += 1
                line = file.readline()
        return result

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        packets = [[[2]], [[6]]]
        line = " "
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            while line != "":
                packets.extend(self.parse(file))
                line = file.readline()

        packets.sort(key=cmp_to_key(self.compare), reverse=True)
        return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 13")
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
