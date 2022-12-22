"""
    Day 22 Solver Module
"""
from collections import defaultdict
import sys
from typing import Generator, Iterable


class Solver:
    """
    Day 22 Solver
    """
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    DIRECTION = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def instructions_generator(self, instructions: Iterable) -> Generator[str | int, None, None]:
        """
        Generator for the instructions.

        Args:
            instructions (Iterable): The instructions
        Yields:
            The number of spaces to move forward or the direction to rotate.
        """
        num = 0
        for value in instructions:
            if value.isdigit():
                num = num * 10 + int(value)
            else:
                yield num
                num = 0
                yield value
        yield num

    def parse_file(
        self,
        filepath: str
    ) -> tuple[dict[tuple[int, int], str], Generator[str | int, None, None]]:
        """
        Parse the file and get the board and instructions.

        Args:
            filepath (str): The path to the file
        Returns:
            The board and the instructions generator.
        """
        board: dict[tuple[int, int], str] = defaultdict(str)
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for i, row in enumerate(file):
                row = row.rstrip()
                if row == "":
                    break
                for j, col in enumerate(row):
                    if col != " ":
                        board[i, j] = col

            return board, self.instructions_generator(file.readline())

    def get_starting_position(self, board: dict[tuple[int, int], str]) -> tuple[int, int]:
        """
        Find the the starting position

        Args:
            board (dict[tuple[int, int], str]): The board
        Returns:
            The starting position.
        """
        row = col = 0
        while board[row, col] == "":
            col += 1
        return 0, col

    def get_next_position(
        self,
        board: dict[tuple[int, int], str],
        row: int,
        col: int,
        direction: int
    ) -> tuple[int, int]:
        """
        Find the next valid position.

        Args:
            board (dict[tuple[int, int], int]): The board
            row (int): The row of the position
            col (int): The column of the position
            direction (int): The current direction
        Returns:
            The next valid position.
        """
        row_diff, col_diff = Solver.DIRECTION[direction]

        row += row_diff
        col += col_diff
        if board[row, col] != "":
            return row, col

        # Position is off the board
        # Find where the column wraps to
        row -= row_diff
        col -= col_diff
        while board[row, col] != "":
            row -= row_diff
            col -= col_diff
        return row + row_diff, col + col_diff

    def perform_move(
        self,
        board: dict[tuple[int, int], str],
        position: tuple[int, int],
        direction: int,
        steps: int
    ) -> tuple[int, int]:
        """
        Move the number of steps forward.

        Args:
            board (dict[tuple[int, int], int]): The board
            position (tuple[int, int]): The current position
            direction (int): The current direction
            steps (int): The number of steps to go forward
        Returns:
            The position after moving the given number of steps forward.
        """
        for _ in range(steps):
            next_position = self.get_next_position(
                board, *position, direction
            )
            if board[next_position] == "#":
                break
            position = next_position
        return position

    def get_region(self, row: int, col: int, region_size: int) -> int:
        """
        Get the region for the current row and column.

        Args:
            row (int): The current row
            col (int): The current column
            region_size (int): The size of the regions
        Returns:
            The region of the position.
        """
        row_region = row // region_size
        col_region = col // region_size

        return [[-1, 5, 6], [-1, 4,], [2, 3], [1]][row_region][col_region]

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        board, instructions = self.parse_file(filepath=filepath)

        position = self.get_starting_position(board)
        direction = Solver.RIGHT

        for instruction in instructions:
            if isinstance(instruction, str):
                direction = (direction + (1 if instruction == "R" else -1)) % 4
                continue

            position = self.perform_move(
                board,
                position,
                direction,
                steps=instruction
            )

        row, col = position
        return 1000 * (row + 1) + 4 * (col + 1) + direction

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        board, instructions = self.parse_file(filepath=filepath)

        def step(
            position: tuple[int, int],
            direction: int
        ) -> tuple[tuple[int, int], int, int]:
            region_size = 50
            new_position = tuple(
                x + d_x for x, d_x in zip(position, Solver.DIRECTION[direction])
            )
            region = self.get_region(*position, region_size=region_size)
            invalid_region = board[new_position] == ""

            def step_right() -> tuple[tuple[int, int], int, int]:
                if not invalid_region or region in [2, 5]:
                    return new_position, direction, -1

                if region == 1:
                    return (
                        (
                            region_size * 3 - 1,
                            region_size + position[0] % region_size
                        ),
                        Solver.UP,
                        3
                    )
                if region == 3:
                    return (
                        (
                            region_size - 1 - position[0] % region_size,
                            region_size * 3 - 1,
                        ),
                        Solver.LEFT,
                        6
                    )
                if region == 4:
                    return (
                        (
                            region_size - 1,
                            region_size * 2 + position[0] % region_size
                        ),
                        Solver.UP,
                        6
                    )
                if region == 6:
                    return (
                        (
                            region_size * 3 - 1 - position[0] % region_size,
                            region_size * 2 - 1
                        ),
                        Solver.LEFT,
                        3
                    )
                raise Exception("Unreachable")

            def step_down() -> tuple[tuple[int, int], int, int]:
                if not invalid_region or region in [2, 4, 5]:
                    return new_position, direction, -1

                if region == 1:
                    return (
                        (
                            0,
                            region_size * 2 + position[1] % region_size
                        ),
                        Solver.DOWN,
                        6
                    )
                if region == 3:
                    return (
                        (
                            region_size * 3 + position[1] % region_size,
                            region_size - 1
                        ),
                        Solver.LEFT,
                        1
                    )
                if region == 6:
                    return (
                        (
                            region_size + position[1] % region_size,
                            region_size * 2 - 1
                        ),
                        Solver.LEFT,
                        4
                    )
                raise Exception("Unreachable")

            def step_left() -> tuple[tuple[int, int], int, int]:
                if not invalid_region or region in [3, 6]:
                    return new_position, direction, -1

                if region == 1:
                    return (
                        (
                            0,
                            region_size + position[0] % region_size
                        ),
                        Solver.DOWN,
                        5
                    )
                if region == 2:
                    return (
                        (
                            region_size - 1 - position[0] % region_size,
                            region_size
                        ),
                        Solver.RIGHT,
                        5
                    )
                if region == 4:
                    return (
                        (
                            region_size * 2,
                            position[0] % region_size
                        ),
                        Solver.DOWN,
                        2
                    )
                if region == 5:
                    return (
                        (
                            region_size * 3 - 1 - position[0] % region_size,
                            0
                        ),
                        Solver.RIGHT,
                        2
                    )

                raise Exception("Unreachable")

            def step_up() -> tuple[tuple[int, int], int, int]:
                if not invalid_region or region in [1, 3, 4]:
                    return new_position, direction, -1

                if region == 2:
                    return (
                        (
                            region_size + position[1] % region_size,
                            region_size
                        ),
                        Solver.RIGHT,
                        4
                    )
                if region == 5:
                    return (
                        (
                            region_size * 3 + position[1] % region_size,
                            0
                        ),
                        Solver.RIGHT,
                        1
                    )
                if region == 6:
                    return (
                        (
                            region_size * 4 - 1,
                            position[1] % region_size
                        ),
                        Solver.UP,
                        1
                    )
                print(position, direction)
                raise Exception("Unreachable")

            return [step_right, step_down, step_left, step_up][direction]()

        def perform_move(
            position: tuple[int, int],
            direction: int,
            steps: int
        ) -> tuple[tuple[int, int], int]:
            for _ in range(steps):
                new_position, new_direction, _ = step(
                    position, direction)
                if board[new_position] == "#":
                    break
                position, direction = new_position, new_direction
            return position, direction

        position = self.get_starting_position(board)
        direction = Solver.RIGHT

        for instruction in instructions:
            if isinstance(instruction, str):
                direction = (direction + (1 if instruction == "R" else -1)) % 4
                continue

            position, direction = perform_move(
                position, direction, instruction
            )

        row, col = position
        return 1000 * (row + 1) + 4 * (col + 1) + direction

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 22")
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
