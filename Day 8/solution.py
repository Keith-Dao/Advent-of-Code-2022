"""
    Day 8 Solver Module
"""
import sys


class Solver:
    """
    Day 8 Solver
    """

    def __init__(self) -> None:
        self.parsed = None
        self.trees = []

    def parse(self, filepath: str) -> list[list[int]]:
        """
        Parses the file.

        Args:
            filepath (str): Path of the file to parse
        """
        if self.parsed == filepath:
            return self.trees

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            self.trees = [
                [int(tree) for tree in line.rstrip()]
                for line in file
            ]
        self.parsed = filepath
        return self.trees

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        trees = self.parse(filepath)
        rows, cols = len(trees), len(trees[0])
        visible = [[False] * cols for _ in range(rows)]

        for i in [0, -1]:
            for j in [0, -1]:
                visible[i][j] = True

        # Check left
        for i in range(1, rows - 1):
            row = trees[i]
            prev_tallest = -1
            for j, tree in enumerate(row):
                if tree <= prev_tallest:
                    continue

                visible[i][j] = True
                prev_tallest = max(prev_tallest, tree)

        # Check right
        for i in range(1, rows - 1):
            row = trees[i]
            prev_tallest = -1
            for j, tree in enumerate(reversed(row)):
                if tree <= prev_tallest:
                    continue
                visible[i][cols - 1 - j] = True
                prev_tallest = max(prev_tallest, tree)

        # Check down
        for j in range(1, cols - 1):
            prev_tallest = -1
            for i in range(rows):
                tree = trees[i][j]
                if tree <= prev_tallest:
                    continue

                visible[i][j] = True
                prev_tallest = max(prev_tallest, tree)

        # Check up
        for j in range(1, cols - 1):
            prev_tallest = -1
            for i in range(rows - 1, -1, -1):
                tree = trees[i][j]
                if tree <= prev_tallest:
                    continue

                visible[i][j] = True
                prev_tallest = max(prev_tallest, tree)

        return sum(sum(row) for row in visible)

    def calculate_score(self, trees: list[list[int]], row: int, col: int) -> int:
        """
        Calculate the score of a tree for part 2.

        Args:
            trees (list[list[int]]): Grid of trees
            row (int): Row index of target tree
            col (int): Column index of target tree
        Returns:
            The score of the tree
        """
        score = 1
        tree = trees[row][col]
        rows, cols = len(trees), len(trees[0])

        # Look right
        visible_trees = 0
        while col + visible_trees + 1 < cols:
            visible_trees += 1
            if tree <= trees[row][col + visible_trees]:
                break
        if visible_trees == 0:
            return 0
        score *= visible_trees

        # Look down
        visible_trees = 0
        while row + visible_trees + 1 < rows:
            visible_trees += 1
            if tree <= trees[row + visible_trees][col]:
                break
        if visible_trees == 0:
            return 0
        score *= visible_trees

        # Look left
        visible_trees = 0
        while col - (visible_trees + 1) >= 0:
            visible_trees += 1
            if tree <= trees[row][col - visible_trees]:
                break
        if visible_trees == 0:
            return 0
        score *= visible_trees

        # Look up
        visible_trees = 0
        while row - (visible_trees + 1) >= 0:
            visible_trees += 1
            if tree <= trees[row - visible_trees][col]:
                break
        score *= visible_trees
        return score

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        trees = self.parse(filepath)

        return max(
            self.calculate_score(trees, row=i, col=j)
            for i, row in enumerate(trees)
            for j, tree in enumerate(row)
        )

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 8")
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
