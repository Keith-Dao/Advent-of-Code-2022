"""
    Day 10 Solver Module
"""
import sys


class Solver:
    """
    Day 10 Solver
    """

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        reg_x = 1
        cycle = strength = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                tokens = line.rstrip().split()

                cycle += 1
                if cycle % 40 == 20:
                    strength += cycle * reg_x
                if tokens[0] == "noop":
                    continue

                cycle += 1
                if cycle % 40 == 20:
                    strength += cycle * reg_x
                reg_x += int(tokens[1])

        return strength

    def part_2(self, filepath: str) -> str:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            None
        """

        def print_pixel(cycle: int, reg_x: int) -> None:
            """
            Print the pixel if the sprite is in the correct position.

            Args:
                cycle (int): The cycle number
                reg_x (int): The value of register x
            """
            print(
                "#"
                if reg_x - 1 <= cycle % 40 <= reg_x + 1
                else ".",
                end=""
            )
            if (cycle + 1) % 40 == 0:
                print()

        reg_x = 1
        cycle = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                tokens = line.rstrip().split()

                print_pixel(cycle=cycle, reg_x=reg_x)
                cycle += 1
                if tokens[0] == "noop":
                    continue

                print_pixel(cycle=cycle, reg_x=reg_x)
                cycle += 1
                reg_x += int(tokens[1])

        return ""

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 10")
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
