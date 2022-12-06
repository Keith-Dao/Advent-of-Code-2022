"""
    Day 6 Solver Module
"""
from collections import defaultdict, deque
import sys

class Solver:
    """
    Day 6 Solver
    """

    def solve_part(self, filepath: str, length: int) -> int:
        """
        Generic solve for a given part.

        Args:
            filepath (str): Path to the input file
            length (str): Length of the window
        Returns:
            Solution
        """
        window = deque()
        seen = defaultdict(int)
        counter = 1
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            c = file.read(1)
            while c:
                while window and (seen[c] > 0 or len(window) > length):
                    seen[window.popleft()] -= 1
                window.append(c)
                seen[c] += 1

                if len(window) == length:
                    return counter
                
                c = file.read(1)
                counter += 1
        return -1

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.solve_part(filepath=filepath, length=4)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.solve_part(filepath=filepath, length=14)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 6")
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
