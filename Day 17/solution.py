"""
    Day 17 Solver Module
"""
import sys


class Simulator:
    """
    Simulator
    """
    ROCKS = [
        ["####"],
        [".#.", "###", ".#."],
        ["###", "..#", "..#"],
        ["#", "#", "#", "#"],
        ["##", "##"]
    ]
    EMPTY = "."
    ROCK = "#"
    COLUMNS = 7

    def __init__(self, jet_pattern: str) -> None:
        self.chamber = []
        self.highest = [-1] * Simulator.COLUMNS

        self.current_rock = 0

        self.jet_pattern = jet_pattern
        self.jet_idx = 0

    def push(self, rock: list[str], row_num: int, col_num: int) -> tuple[int, int]:
        """
        Find the position of the rock when it is being pushed by the vents.

        Args:
            rock (list[str]): Rock in character form
            row_num (int): Current row of the bottom left corner of the rock
            col_num (int): Current column of the bottom left corner of the rock
        Returns:
            Tuple with the new row, column and whether the rock can continue moving
        """
        direction = self.jet_pattern[self.jet_idx]
        self.jet_idx = (self.jet_idx + 1) % len(self.jet_pattern)
        new_j = col_num + (1 if direction == ">" else -1)

        # Check if the walls are hit
        if new_j < 0 or new_j + len(rock[0]) > Simulator.COLUMNS:
            return row_num, col_num

        for d_i, row in enumerate(rock):
            if row_num + d_i >= len(self.chamber):
                break

            if any(
                space ==
                self.chamber[row_num + d_i][new_j + d_j] ==
                Simulator.ROCK
                for d_j, space in enumerate(row)
            ):
                return row_num, col_num
        return row_num, new_j

    def fall(self, rock: list[str], row_num: int, col_num: int) -> tuple[int, int, bool]:
        """
        Find the position of the rock when it is falling.

        Args:
            rock (list[str]): Rock in character form
            row_num (int): Current row of the bottom left corner of the rock
            col_num (int): Current column of the bottom left corner of the rock
        Returns:
            Tuple with the new row, column and whether the rock can continue moving
        """
        row_num -= 1
        for d_i, row in enumerate(rock):
            if row_num + d_i >= len(self.chamber):
                break

            if any(
                space ==
                self.chamber[row_num + d_i][col_num + d_j] ==
                Simulator.ROCK
                for d_j, space in enumerate(row)
            ):
                return row_num + 1, col_num, False
        return row_num, col_num, row_num != 0

    def add_rock(self, rock: list[str], row_num: int, col_num: int) -> None:
        """
        Add a rock to the room.

        Args:
            rock (list[str]): Rock in character form
            row_num (int): Row of the bottom left corner of the rock
            col_num (int): Column of the bottom left corner of the rock
        """
        for d_i, row in enumerate(rock):
            if row_num + d_i == len(self.chamber):
                self.chamber.append([Simulator.EMPTY] * Simulator.COLUMNS)

            for d_j, space in enumerate(row):
                if space == Simulator.EMPTY:
                    continue

                self.chamber[row_num + d_i][col_num + d_j] = space
                self.highest[col_num + d_j] = max(
                    self.highest[col_num + d_j],
                    row_num + d_i
                )

    def step(self) -> None:
        """
        Simulate one step in the room.
        """
        rock = Simulator.ROCKS[self.current_rock]
        self.current_rock = (self.current_rock + 1) % len(Simulator.ROCKS)
        row_num, col_num = len(self.chamber) + 3, 2

        moving = True
        while moving:
            row_num, col_num = self.push(
                rock=rock,
                row_num=row_num,
                col_num=col_num
            )
            row_num, col_num, moving = self.fall(
                rock=rock,
                row_num=row_num,
                col_num=col_num
            )
        if row_num == 0:
            row_num, col_num = self.push(
                rock=rock,
                row_num=row_num,
                col_num=col_num
            )

        self.add_rock(
            rock=rock,
            row_num=row_num,
            col_num=col_num
        )

    def hash(self) -> tuple[int, int, tuple[int]]:
        """
        Create a hash of the current simulator state.

        Returns:
            Hash of the current simulator state.
        """
        height_differences = tuple(
            next(
                (
                    len(self.chamber) - height
                    for height in range(len(self.chamber) - 1, -1, -1)
                    if self.chamber[height][j] == Simulator.ROCK
                ),
                -1
            )
            for j in range(Simulator.COLUMNS)
        )
        return self.jet_idx, self.current_rock, height_differences


class Solver:
    """
    Day 17 Solver
    """

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            simulator = Simulator(jet_pattern=file.readline().rstrip())
        for _ in range(2022):
            simulator.step()
        return len(simulator.chamber)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            simulator = Simulator(jet_pattern=file.readline().rstrip())

        # Find cycle
        hashes = {}
        rocks_landed = 0
        while True:
            simulator_hash = simulator.hash()
            if simulator_hash in hashes:
                break
            hashes[simulator_hash] = (rocks_landed, len(simulator.chamber))
            simulator.step()
            rocks_landed += 1

        # Cycle info
        rocks_per_cycle = rocks_landed - hashes[simulator_hash][0]
        height_per_cycle = len(simulator.chamber) - hashes[simulator_hash][1]
        target_rocks = 1000000000000
        complete_cycles = (target_rocks - rocks_landed) // rocks_per_cycle

        # Remaining steps not in the cycle
        remaining_rocks = target_rocks - complete_cycles * rocks_per_cycle - rocks_landed
        for _ in range(remaining_rocks):
            simulator.step()

        return len(simulator.chamber) + height_per_cycle * complete_cycles

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 17")
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
