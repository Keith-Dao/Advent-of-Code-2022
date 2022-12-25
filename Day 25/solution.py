"""
    Day 25 Solver Module
"""
import sys


class Solver:
    """
    Day 25 Solver
    """

    SNAFU_TO_DECIMAL = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2
    }

    DECIMAL_TO_SNAFU = ["0", "1", "2", "=", "-"]

    def snafu_to_decimal(self, snafu: str) -> int:
        """
        Convert from SNAFU to decimal.

        Args:
            snafu (str): A number in SNAFU
        Returns:
            The equivalent number in decimal.
        """
        place = 1
        total = 0
        for digit in reversed(snafu):
            total += place * Solver.SNAFU_TO_DECIMAL[digit]
            place *= 5
        return total

    def decimal_to_snafu(self, num: int) -> str:
        """
        Convert from decimal to SNAFU.

        Args:
            num (int): A number in binary
        Returns:
            The equivalent number in SNAFU
        """
        if num == 0:
            return "0"

        digits = []
        while num != 0:
            digit = ((num % 5) + 2) % 5 - 2
            if digit < 0:
                num -= digit
            digits.append(Solver.DECIMAL_TO_SNAFU[digit])
            num //= 5
        return "".join(reversed(digits))

    def part_1(self, filepath: str) -> str:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return self.decimal_to_snafu(
                sum(self.snafu_to_decimal(line.rstrip()) for line in file)
            )

    def part_2(self, _: str) -> str:
        """
        Solve part 2.

        Args:
            Ignores one arg
        Returns:
            Nothing
        """
        return ""

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 25")
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
