"""
    Day 9 Solver Module
"""
import sys


class Solver:
    """
    Day 9 Solver
    """

    def __init__(self) -> None:
        self.parsed = None
        self.trees = []

    def move_head(self, head: tuple[int, int], direction: str) -> tuple[int, int]:
        """
        Get the head's position after moving in a given direction.

        Args:
            head (tuple[int, int]): Position of the head
        Returns:
            The head's new position.
        """
        return {
            "U": lambda x, y: (x, y + 1),
            "D": lambda x, y: (x, y - 1),
            "L": lambda x, y: (x - 1, y),
            "R": lambda x, y: (x + 1, y)
        }[direction](*head)

    def move_tail(self, tail: tuple[int, int], head: tuple[int, int]) -> tuple[int, int]:
        """
        Get the tail's position given the head's current position.

        Args:
            tail (tuple[int, int]): Position of the tail
            head (tuple[int, int]): Position of the head
        Returns:
            The tail's new position.
        """
        def is_touching(tail: tuple[int, int], head: tuple[int, int]) -> int:
            return max(abs(a - b) for a, b in zip(tail, head)) <= 1

        if is_touching(tail=tail, head=head):
            return tail

        return tuple(
            h if abs(h - t) == 1 else (h + t) // 2
            for h, t in zip(head, tail)
        )

    def step(self, positions: list[tuple[int, int]], direction: str) -> None:
        """
        Perform on step of the simulation.

        Args:
            positions (list[tuple[int, int]]): The position of each knot
            direction (str): The head's direction
        """
        positions[0] = self.move_head(
            head=positions[0],
            direction=direction
        )
        for i in range(1, len(positions)):
            positions[i] = self.move_tail(
                tail=positions[i],
                head=positions[i - 1]
            )

    def simulate(self, filepath: str, num_knots: int) -> int:
        """
        Perform the complete simulation.

        Args:
            filepath (str): Path to the file with the instructions
            num_knots (int): Number of knots in the rope
        Returns:
            The number of unique positions for the last knot in the rope.
        """
        visited: set[tuple[int, int]] = {(0, 0)}
        positions: list[tuple[int, int]] = [(0, 0) for _ in range(num_knots)]
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                direction, steps = line.rstrip().split()
                for _ in range(int(steps)):
                    self.step(positions=positions, direction=direction)
                    visited.add(positions[-1])
        return len(visited)

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.simulate(filepath=filepath, num_knots=2)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.simulate(filepath=filepath, num_knots=10)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 9")
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
