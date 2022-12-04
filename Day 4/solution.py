"""
    Day 4 Solver Module
"""
import sys
from typing import Callable


class Solver:
    """
    Day 4 Solver
    """

    def solve_part(
        self,
        filepath: str,
        pair_condition: Callable[[list[int], list[int]], int],
    ) -> int:
        """
        Generic solve structure for both parts.

        Args:
            filepath (str): Path to the input file
            pair_condition (Callable): The condition for the pair to be counted
        Returns:
            The total number of pairs that passes the check
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(
                # Compute the pair check for each pair
                pair_condition(
                    *[
                        # Get each elf's sections
                        [int(section) for section in elf_sections.split("-")]
                        for elf_sections in pair.rstrip().split(",")
                    ]
                )
                for pair in file
            )

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """

        def is_any_fully_contained(elf_1: list[int], elf_2: list[int]) -> bool:
            def is_fully_contained(elf_1: list[int], elf_2: list[int]) -> bool:
                return elf_1[0] <= elf_2[0] <= elf_2[1] <= elf_1[1]

            return (
                is_fully_contained(elf_1=elf_1, elf_2=elf_2) or
                is_fully_contained(elf_1=elf_2, elf_2=elf_1)
            )

        return self.solve_part(filepath, is_any_fully_contained)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """

        def is_any_overlapping(elf_1: list[int], elf_2: list[int]) -> bool:
            def is_overlapping(elf_1: list[int], elf_2: list[int]) -> bool:
                return (
                    elf_1[0] <= elf_2[0] <= elf_1[1] or
                    elf_1[0] <= elf_2[1] <= elf_1[1]
                )

            return (
                is_overlapping(elf_1=elf_1, elf_2=elf_2) or
                is_overlapping(elf_1=elf_2, elf_2=elf_1)
            )

        return self.solve_part(filepath, is_any_overlapping)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 4")
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
