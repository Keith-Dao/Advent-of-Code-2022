"""
    Day 12 Solver Module
"""
from collections import deque
import sys


class Solver:
    """
    Day 12 Solver
    """
    START = "S"
    EXIT = "E"

    def find_locations(
        self,
        height_map: list[list[str]],
        chars: list[str]
    ) -> list[tuple[int, int]]:
        """
        Find all the locations of the given characters in the map.

        Args:
            height_map (list[list[str]]): The height map
            chars (list[str]): The list of characters to search for
        Returns:
            List of all the locations of the given characters.
        """
        return [
            (i, j)
            for i, row in enumerate(height_map)
            for j, x in enumerate(row)
            if x in chars
        ]

    def get_height_map(self, filepath: str) -> list[list[str]]:
        """
        Parse the input file and get the height map.

        Args:
            filepath (str): The path to the input file
        Returns:
            The height map parsed from the input file.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return [list(line.rstrip()) for line in file]

    def solve_part(self, filepath: str, starting_letters: list[str]) -> int:
        """
        Generic solve.

        Args:
            filepath (str): The path to the input file
            starting_letters (list[str]): The symbols to start searching from
        Returns:
            Solution.
        """
        height_map = self.get_height_map(filepath=filepath)
        rows, cols = len(height_map), len(height_map[0])

        queue = deque(
            self.find_locations(
                height_map=height_map,
                chars=starting_letters
            )
        )
        visited = set(queue)
        steps = 0

        while queue:
            for _ in range(len(queue)):
                i, j = queue.popleft()

                current_height = height_map[i][j]
                if current_height == Solver.EXIT:
                    return steps
                if current_height == Solver.START:
                    current_height = "a"

                for n_i, n_j in [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]:
                    if not 0 <= n_i < rows or not 0 <= n_j < cols or (n_i, n_j) in visited:
                        continue

                    next_height = height_map[n_i][n_j]
                    if next_height == Solver.EXIT:
                        next_height = "z"

                    if ord(next_height) - ord(current_height) <= 1:
                        queue.append((n_i, n_j))
                        visited.add((n_i, n_j))
            steps += 1

        return -1

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.solve_part(filepath=filepath, starting_letters=[Solver.START])

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            None
        """
        return self.solve_part(filepath=filepath, starting_letters=[Solver.START, "a"])

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 12")
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
