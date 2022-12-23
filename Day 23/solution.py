"""
    Day 23 Solver Module
"""
import itertools
import sys


class Solver:
    """
    Day 23 Solver
    """

    def parse(self, filepath: str) -> set[tuple[int, int]]:
        """
        Parse the input file for the elves' locations.

        Args:
            filepath (str): The filepath to the input file
        Returns:
            The locations of the elves.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return {
                (i, j)
                for i, row in enumerate(file)
                for j, x in enumerate(row)
                if x == "#"
            }

    def get_size(self, elves: set[tuple[int, int]]) -> tuple[int, int]:
        """
        Get the smallest rectangular region that encapsulates the elves.

        Args:
            elves (set[tuple[int, int]]): The elves' current positions
        Returns:
            The smallest rectangular region that encapsulates the elves.
        """
        min_row = min_height = float('inf')
        max_row = max_height = float('-inf')

        for row, height in elves:
            min_row = min(min_row, row)
            max_row = max(max_row, row)
            min_height = min(min_height, height)
            max_height = max(max_height, height)
        return int(max_row - min_row + 1), int(max_height - min_height + 1)

    def step(self, elves: set[tuple[int, int]], round_number: int) -> set[tuple[int, int]]:
        """
        Perform one round of steps.

        Args:
            elves (set[tuple[int, int]]): The elves' current positions
            round_number (int): The current round number
        Returns:
            The elves' new positions.
        """
        elf_to_new_location = {}
        proposed_location_to_original_elf = {}
        considerations = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def add_proposal(
            original_position: tuple[int, int],
            proposed_position: tuple[int, int]
        ) -> None:
            if proposed_position not in proposed_location_to_original_elf:
                proposed_location_to_original_elf[proposed_position] = original_position
                elf_to_new_location[original_position] = proposed_position
                return
            # Reset the contesting elf
            contested_elf = proposed_location_to_original_elf[proposed_position]
            elf_to_new_location[contested_elf] = contested_elf

            # Add the current elf to its original position
            elf_to_new_location[original_position] = original_position
            elf_to_new_location[original_position] = original_position

        def could_move_elf(row: int, col: int) -> bool:
            for num_considerations in range(4):
                row_diff, col_diff = considerations[
                    (num_considerations + round_number) % 4
                ]
                if all(
                    (
                        row + row_diff + (row_diff == 0) * diff,
                        col + col_diff + (col_diff == 0) * diff
                    ) not in elves
                    for diff in [-1, 0, 1]
                ):
                    add_proposal(
                        original_position=(row, col),
                        proposed_position=(row + row_diff, col + col_diff)
                    )
                    return True
            return False

        for row, col in elves:
            # Dont move
            if all(
                (row + row_diff, col + col_diff) not in elves
                for row_diff, col_diff in itertools.product([-1, 0, 1], repeat=2)
                if (row_diff, col_diff) != (0, 0)
            ):
                add_proposal(
                    original_position=(row, col),
                    proposed_position=(row, col)
                )
                continue

            # Try move
            if could_move_elf(row, col):
                continue

            # No valid moves
            add_proposal(
                original_position=(row, col),
                proposed_position=(row, col)
            )
        return set(elf_to_new_location.values())

    def print(
        self,
        elves: set[tuple[int, int]],
        row_range: tuple[int, int],
        col_range: tuple[int, int]
    ) -> None:
        """
        Print the board to the console.

        Args:
            elves (set[tuple[int, int]]): The elves' current positions
            row_range (tuple[int, int]): The range of rows to print
            col_range (tuple[int, int]): The range of cols to print
        """
        row_min, row_max = row_range
        col_min, col_max = col_range
        for row in range(row_min, row_max + 1):
            for col in range(col_min, col_max + 1):
                print("#" if (row, col) in elves else ".", end="")
            print()

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        elves = self.parse(filepath=filepath)
        for i in range(10):
            elves = self.step(elves, round_number=i)

        width, height = self.get_size(elves)
        return width * height - len(elves)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        elves = self.parse(filepath=filepath)

        round_number = 0
        next_elves = self.step(elves, round_number=round_number)

        while elves != next_elves:
            round_number += 1
            elves = next_elves
            next_elves = self.step(elves, round_number=round_number)

        return round_number + 1

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 23")
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
