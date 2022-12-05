"""
    Day 5 Solver Module
"""
import sys
from typing import Callable


class Solver:
    """
    Day 5 Solver
    """

    def get_instruction(self, line: str) -> tuple[int, int, int]:
        """
        Extracts the values from the instructions.

        Args:
            line (str): The instruction line
        Returns:
            The quantity to move, the source stack and the destination stack respectively
        """
        return tuple(int(num) for num in line.split()[1::2])

    def generic_solve(self, filepath: str, move_method: Callable) -> str:
        """
        The generic structure to solve each part.

        Args:
            filepath (str): The path of the input file
            move_method (Callable): The method that the crates are moved
        Returns:
            The crates on the top of the stack in order
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line: str = file.readline()
            stacks = [[] for _ in range(len(line) // 4)]

            # Strip the trailing spaces now that we know how many stacks there are
            line = line.rstrip()
            # Generate the stacks
            while line != "":
                for i in range(1, len(line), 4):
                    if line[i] != " ":
                        stacks[i // 4].append(line[i])
                line = file.readline().rstrip()

            # Reorganise the stacks
            for stack in stacks:
                stack.pop() # Remove the numbers
                stack.reverse()

            # Apply the instructions
            for line in file:
                quantity, source, destination = self.get_instruction(line)
                source -= 1
                destination -= 1
                move_method(stacks, quantity, source, destination)

            return "".join(stack[-1] for stack in stacks)

    def part_1(self, filepath: str) -> str:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """

        def move_boxes_sequentially(
            stacks: list[list[str]],
            quantity: int,
            source: int,
            destination: int,
        ) -> None:
            """
            Move one box from the top of the source stack to the destination stack
            and repeat till quantity number of boxes have been moved.

            Args:
                stacks (list[list[str]]): The boxes in each stack
                quantity (int): The number of boxes to move
                source (int): The base-1 indexed stack to move the boxes from
                destination (int): The base-1 indexed stack to move the boxes to
            """
            stacks[destination].extend(stacks[source][-quantity:][::-1])
            stacks[source] = stacks[source][:-quantity]

        return self.generic_solve(
            filepath=filepath, move_method=move_boxes_sequentially
        )

    def part_2(self, filepath: str) -> str:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        def move_boxes_together(
            stacks: list[list[str]],
            quantity: int,
            source: int,
            destination: int,
        ) -> None:
            """
            Move the top quantity boxes from the source stack to the destination stack.

            Args:
                stacks (list[list[str]]): The boxes in each stack
                quantity (int): The number of boxes to move
                source (int): The base-1 indexed stack to move the boxes from
                destination (int): The base-1 indexed stack to move the boxes to
            """
            stacks[destination].extend(stacks[source][-quantity:])
            stacks[source] = stacks[source][:-quantity]
        
        return self.generic_solve(
            filepath=filepath, move_method=move_boxes_together
        )

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 5")
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
