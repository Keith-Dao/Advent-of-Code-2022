"""
    Day 21 Solver Module
"""
import sys
import re


class Solver:
    """
    Day 21 Solver
    """

    def get_monkeys(self, filepath: str) -> dict[str, str]:
        """
        Get the monkeys.

        Args:
            filepath (str): Path to the file
        Returns:
            The monkeys and what they will shout.
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return dict(
                line.rstrip().split(": ")
                for line in file
            )

    def calculate(self, operation: str, monkey_a: int, monkey_b: int) -> int:
        """
        Calculate the value for the given values and operation.

        Args:
            operation (str): The operation to perform
            monkey_a (int): Value of the the monkey in the left of the equation
            monkey_b (int): Value of the the monkey in the right of the equation
        Returns:
            The value of the operation.
        """
        return {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a // b
        }[operation](monkey_a, monkey_b)

    def reverse_calculate(self, operation: str, value: int, monkey: int) -> int:
        """
        Perform the inverse calculation. 
        Add an ! to the operation if the value to be calculated was originally on the right.

        Args:
            operation (str): The operation to perform
            monkey_a (int): Value of the the monkey in the left of the equation
            monkey_b (int): Value of the the monkey in the right of the equation
        Returns:
            The value of the operation.
        """
        return {
            "+": lambda a, b: a - b,
            "*": lambda a, b: a // b,
            "-": lambda a, b: -a + b,
            "/": lambda a, b: b // a,
            "+!": lambda a, b: a - b,
            "*!": lambda a, b: a // b,
            "-!": lambda a, b: a + b,
            "/!": lambda a, b: a * b
        }[operation](value, monkey)

    def get_monkey_value(self, monkey: str, monkeys: dict[str, str]) -> int:
        """
        The value for the given monkey.

        Args:
            monkey (str): The monkey to be calculated
            monkeys (dict[str, str]): Mapping of monkeys to their operations
        Returns:
            The resulting value for the monkey.
        """
        if monkey not in monkeys:
            raise ValueError(f"Monkey {monkey} does not exist.")

        if re.fullmatch(r"-?\d+", monkeys[monkey]):
            return int(monkeys[monkey])

        monkey_a, operation, monkey_b = monkeys[monkey].split()
        return self.calculate(
            operation,
            self.get_monkey_value(monkey=monkey_a, monkeys=monkeys),
            self.get_monkey_value(monkey=monkey_b, monkeys=monkeys)
        )

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        monkeys = self.get_monkeys(filepath=filepath)

        return self.get_monkey_value(monkey="root", monkeys=monkeys)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        monkeys = self.get_monkeys(filepath=filepath)

        # Find monkeys that lead to humn
        monkey_path = []

        def find_monkeys_to_humn(monkey: str) -> bool:
            if monkey not in monkeys:
                raise ValueError(f"Monkey {monkey} does not exist.")

            if monkey == "humn":
                monkey_path.append(monkey)
                return True

            if re.fullmatch(r"-?\d+", monkeys[monkey]):
                return False

            monkey_a, _, monkey_b = monkeys[monkey].split()
            if find_monkeys_to_humn(monkey_a) or find_monkeys_to_humn(monkey_b):
                monkey_path.append(monkey)
                return True
            return False

        find_monkeys_to_humn("root")

        # Get the value of the non-humn side
        monkey_path.pop()
        starting_monkey = [
            monkey
            for monkey in monkeys["root"].split()[::2]
            if monkey != monkey_path[-1]
        ][0]
        current_value = self.get_monkey_value(
            monkey=starting_monkey, monkeys=monkeys)

        def solve(current_value: int, monkey: str) -> int:
            if monkey not in monkeys:
                raise ValueError(f"Monkey {monkey} does not exist.")

            if monkey == "humn":
                return current_value

            value_monkey, operation, humn_monkey = monkeys[monkey].split()

            # Check if the first monkey actually leads to humn
            if value_monkey == monkey_path.pop():
                value_monkey, humn_monkey = humn_monkey, value_monkey
                operation += "!"

            current_value = self.reverse_calculate(
                operation=operation,
                value=current_value,
                monkey=self.get_monkey_value(
                    monkey=value_monkey,
                    monkeys=monkeys
                )
            )

            return solve(
                current_value=current_value,
                monkey=humn_monkey
            )

        return solve(current_value=current_value, monkey=monkey_path.pop())

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 21")
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
