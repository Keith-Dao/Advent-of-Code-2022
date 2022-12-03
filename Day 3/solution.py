"""
    Day 3 Solver Module
"""
import sys
from typing import Any, Callable, Iterable, Iterator


class Solver:
    """
    Day 3 Solver
    """

    def get_item_priority(self, item: str) -> int:
        """
        Get the priority value for a given item.

        Args:
            item (str): The item type
        Returns:
            The priority of the given item
        """
        if "a" <= item <= "z":
            return ord(item) - ord("a") + 1
        return ord(item) - ord("A") + 27

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.
        """

        def get_rucksack_priority(rucksack_items: str) -> int:
            """
            Get the priority of the common item in the first and second half of the rucksack.

            Args:
                rucksack_items (str): The items in the rucksack
            Returns:
                The priority of the common item
            """
            # Find the common item in the first and second half of the rucksack
            compartment_size = len(rucksack_items) // 2
            (common_item,) = set(rucksack_items[:compartment_size]) & set(
                rucksack_items[compartment_size:]
            )

            return self.get_item_priority(common_item)

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(
                get_rucksack_priority(rucksack_items) for rucksack_items in file
            )

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.
        """

        def batch_iterator(
            iterator: Iterable,
            size: int,
            item_processing: Callable[[Any], Any] = lambda a: a,
        ) -> Iterator:
            """
            Batch the iterator values into groups of the given size and perform any required
            processing.

            Args:
                iterator (Iterable): The iterator to batch results
                size (int): The number of results in each iteration
                item_processing (Callable): Function processing to apply to each item
            Yields:
                List of results in the given size
            """
            group = []
            for item in iterator:
                group.append(item_processing(item))

                if len(group) == size:
                    yield group
                    group.clear()

        def get_rucksack_priority(rucksacks: list[set[str]]) -> int:
            """
            Get the priority of the common item in the rucksacks.

            Args:
                rucksacks (set[str]): The unique items in each rucksack
            Returns:
                The priority of the common item
            """
            (common_item,) = set.intersection(*rucksacks)
            return self.get_item_priority(common_item)

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(
                get_rucksack_priority(rucksacks)
                for rucksacks in batch_iterator(
                    iterator=file,
                    size=3,
                    item_processing=lambda rucksack: set(rucksack.rstrip()),
                )
            )

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 3")
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
