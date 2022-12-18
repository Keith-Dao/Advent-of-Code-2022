"""
    Day 18 Solver Module
"""
import sys
from typing import Generator


class Solver:
    """
    Day 18 Solver
    """

    @staticmethod
    def neighbours(x: int, y: int, z: int, /) -> Generator[tuple[int, int, int], None, None]:
        """
        Get the neighbours of a coordinate.

        Args:
            x (int): The x coordinate
            y (int): The y coordinate
            z (int): The z coordinate
        Returns:
            Generator for the neighbouring coordinates.
        """
        for change in [-1, 1]:
            yield x + change, y, z
            yield x, y + change, z
            yield x, y, z + change

    def parse(self, filepath: str) -> set[tuple[int, int, int]]:
        """
        Parse the given input file.

        Args:
            filepath (str): The filepath to the input file
        Returns:
            Set of all the cubes.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return {
                tuple(
                    int(coord)
                    for coord in line.rstrip().split(",")
                )
                for line in file
            }

    def solve_part(self, filepath: str, exclude_inside: bool) -> int:
        """
        Generic solve.

        Args:
            filepath (str): The filepath to the input file
            exclude_inside (int): Whether to exclude the air on the inside
        Returns:
            Solution to the part
        """
        cubes = self.parse(filepath=filepath)
        visible_faces = 0
        x_range = y_range = z_range = float("inf"), float("-inf")
        for cube in cubes:
            visible_faces += (
                6 -
                sum(
                    1
                    for neighbour in Solver.neighbours(*cube)
                    if neighbour in cubes
                )
            )

            x_range = (
                min(x_range[0], cube[0]),
                max(x_range[1], cube[0])
            )
            y_range = (
                min(y_range[0], cube[1]),
                max(y_range[1], cube[1])
            )
            z_range = (
                min(z_range[0], cube[2]),
                max(z_range[1], cube[2])
            )

        def is_inside(
            position: tuple[int, int, int],
            visited: set[tuple[int, int, int]],
            is_initial: bool = False
        ) -> bool:
            """
            Check if the given position is an air gap inside.

            Args:
                position (tuple[int, int, int]): The x, y, z coordinates to check
                visited (set[tuple[int, int, int]]): Visited coordinates
                is_initial (bool): If the current position was initial position
            Returns:
                Whether the position is inside.
            """
            if position in cubes:
                return False

            if position in memo:
                return memo[position]

            # Check if it is is outside
            if (
                not x_range[0] <= position[0] <= x_range[1] or
                not y_range[0] <= position[1] <= y_range[1] or
                not z_range[0] <= position[2] <= z_range[1]
            ):
                memo[position] = False
                return False

            # Check neighbours
            for neighbour in Solver.neighbours(*position):
                if neighbour in cubes or neighbour in visited:
                    continue

                visited.add(neighbour)
                if not is_inside(neighbour, visited=visited):
                    memo[position] = False
                    return False

            # The visited neighbours are inside
            if is_initial:
                memo[position] = True
            return True

        memo = {}
        if exclude_inside:
            visible_faces -= sum(
                is_inside(
                    position=neighbour,
                    visited={neighbour},
                    is_initial=True
                )
                for position in cubes
                for neighbour in Solver.neighbours(*position)
            )

        return visible_faces

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.solve_part(filepath=filepath, exclude_inside=False)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.solve_part(filepath=filepath, exclude_inside=True)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 18")
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
