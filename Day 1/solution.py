"""
Day 1 Solver Module
"""
import heapq
import sys


class Solver:
    """
    Solver
    """

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1

        Args:
            filepath (str): Path to the input file
        """
        max_sum = current_sum = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                if line == "\n":
                    current_sum = 0
                else:
                    current_sum += int(line)
                    max_sum = max(max_sum, current_sum)
        return max_sum

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2

        Args:
            filepath (str): Path to the input file
        """

        def heap_insert(heap: list[int], value: int) -> None:
            if len(heap) == 3:
                heapq.heappushpop(heap, value)
            else:
                heapq.heappush(heap, value)

        heap: list[int] = []
        current_sum: int = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                if line == "\n":
                    heap_insert(heap, current_sum)
                    current_sum = 0
                else:
                    current_sum += int(line)
        heap_insert(heap, current_sum)
        return sum(heap)

    def solve(self, filepath: str = "input.txt"):
        """
        Perform full solve

        Args:
            filepath (str): Path to the input file
        """
        print("Day 1")
        print(f"Solving: {filepath}")
        print("Part 1:")
        print(self.part_1(filepath))
        print("---")
        print("Part 2:")
        print(self.part_2(filepath))


if __name__ == "__main__":
    solver = Solver()
    match sys.argv:
        case [_]:
            solver.solve()
        case [_, "--path", path]:
            solver.solve(path)
        case other:
            print("Usage: python solution.py --path <path>")
