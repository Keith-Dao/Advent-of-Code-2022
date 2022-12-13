"""
    Day 11 Solver Module
"""
from __future__ import annotations
from collections.abc import Callable
import heapq
import math
import sys


class Monkey:
    """
    Monkey simulator.
    """

    def __init__(self, file) -> None:

        self.monkey_id = file.readline().split()[-1][:-1]

        self.items = [
            int(item)
            for item in file.readline().split(": ")[-1].split(", ")
        ]

        self.inspect: Callable[[int], int] = Monkey.get_inspection_method(
            file.readline().rstrip()
        )
        self.modulo = int(file.readline().split()[-1])
        self.true_monkey = int(file.readline().split()[-1])
        self.false_monkey = int(file.readline().split()[-1])

        self.inspections = 0

    @staticmethod
    def get_inspection_method(operation: str) -> Callable[[int], int]:
        """
        Get the inspection method for the given operation.

        Args:
            operation (str): The operation string
        Returns:
            Method to compute the inspection.
        """
        def get_value(token: str, value: int) -> int:
            return value if token == "old" else int(token)

        match operation.split(": ")[-1].split(" = ")[-1].split():
            case [first_val, "+", second_val]:
                return lambda old_value: (
                    get_value(first_val, old_value) +
                    get_value(second_val, old_value)
                )
            case [first_val, "*", second_val]:
                return lambda old_value: (
                    get_value(first_val, old_value) *
                    get_value(second_val, old_value)
                )
            case _:
                raise ValueError("Invalid format.")

    def simulate_round(
        self,
        monkeys: list[Monkey],
        post_inspection: Callable[[int], int],
        regulator: int
    ) -> None:
        """
        Simulate a round.

        Args:
            monkeys (list[Monkey]): All the monkeys
            post_inspection (callable): New value of the item after inspection and the item is safe
            regulator (int): The gcd of all monkey divisors to keep levels manageable
        """
        for old in self.items:
            new = post_inspection(
                self.inspect(old)  # pylint: disable=not-callable
            ) % regulator
            monkeys[
                self.false_monkey
                if new % self.modulo != 0
                else self.true_monkey
            ].items.append(new)

        self.inspections += len(self.items)
        self.items.clear()


class Solver:
    """
    Day 11 Solver
    """

    def solve_part(
        self,
        filepath: str,
        post_inspection: Callable[[int], int],
        num_rounds: int
    ) -> int:
        """
        Generic solve.

        Args:
            filepath (str): Path to the input file
            post_inspection (callable): New value of the item after inspection and the item is safe
            num_rounds (int): Number of rounds to simulate

        Returns:
            Solution
        """
        monkeys = []
        top_active_monkeys = 2
        heap = [0] * top_active_monkeys
        lcm = 1

        def get_gcd(x: int, y: int, /) -> int:
            """
            Find the greatest common divisor for x and y.

            Args:
                x (int): Some number
                y (int): Some other number
            Returns:
                The lowest common multiple of x and y.
            """
            while y:
                x, y = y, x % y
            return x

        def get_lcm(x: int, y: int, /) -> int:
            """
            Find the lowest common multiple for x and y.

            Args:
                x (int): Some number
                y (int): Some other number
            Returns:
                The lowest common multiple of x and y.
            """
            return (x * y) // get_gcd(x, y)

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            monkeys.append(Monkey(file=file))
            while file.readline() != "":
                monkeys.append(Monkey(file=file))

            for monkey in monkeys:
                lcm = get_lcm(lcm, monkey.modulo)

            for _ in range(num_rounds):
                for monkey in monkeys:
                    monkey.simulate_round(
                        monkeys=monkeys,
                        post_inspection=post_inspection,
                        regulator=lcm
                    )

            for monkey in monkeys:
                heapq.heappushpop(heap, monkey.inspections)

        return math.prod(heap)

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.solve_part(filepath=filepath, post_inspection=lambda x: x // 3, num_rounds=20)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.solve_part(filepath=filepath, post_inspection=lambda x: x, num_rounds=10000)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 11")
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
