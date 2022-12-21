"""
    Day 20 Solver Module
"""
from __future__ import annotations
import sys


class Number:
    """
    Represents a number in the input. 
    Allows the the index method to differentiate between two of the same numbers.
    """

    def __init__(self, val: int) -> None:
        self.val = val

    def __repr__(self) -> str:
        return f"{self.val}"

    def get_index_changes(self, numbers: list[Number]) -> tuple[int, int]:
        """
        Get the original index and the new index.

        Args:
            numbers (list[Number]): The list of numbers
        Returns:
            Tuple with the original index and the new index.
        """
        index = numbers.index(self)
        offset = abs(self.val) % (len(numbers) - 1)
        offset = -offset if self.val < 0 else offset
        new_index = index + offset
        if new_index >= len(numbers):
            new_index = new_index % len(numbers) + 1
        elif new_index == 0:
            new_index = 0 if offset > 0 else len(numbers)
        return index, new_index


class Solver:
    """
    Day 20 Solver
    """

    def mix(self, numbers: list[Number], target_number: Number) -> None:
        """
        Perform a mix.

        Args:
            numbers (list[Number]): The list of numbers
            target_number (Number): The number to move
        """
        index, new_index = target_number.get_index_changes(numbers=numbers)
        numbers.pop(index)
        numbers.insert(new_index, target_number)

    def part_solve(
        self,
        filepath: str,
        decryption_key: int = 1,
        mixing_rounds: int = 1
    ) -> int:
        """
        Generic solve.

        Args:
            filepath (str): Path to the input file
            decryption_key (int): The decryption key to use
            mixing_rounds (int): The number of rounds to mix
        Returns:
            The solution to the part.
        """
        numbers = []
        zero = None
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                numbers.append(Number(val=int(line) * decryption_key))
                if line.strip() == "0":
                    zero = numbers[-1]

        # Mix the nodes
        original_numbers = list(numbers)
        for _ in range(mixing_rounds):
            for number in original_numbers:
                self.mix(numbers=numbers, target_number=number)

        # Find the 1000th, 2000th and 3000th node
        zero_index = numbers.index(zero)
        return sum(numbers[(zero_index + 1000 * i) % len(numbers)].val for i in range(1, 4))

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.part_solve(filepath=filepath)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.part_solve(filepath=filepath, decryption_key=811589153, mixing_rounds=10)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 20")
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
