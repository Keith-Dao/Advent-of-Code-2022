"""
    Day 2 Solver Module
"""
import sys
from typing import Callable


class Solver:
    """
    Day 2 Solver
    """

    rock = 0
    paper = 1
    scissors = 2
    opponent_moves: dict[str, int] = {
        "A": rock,
        "B": paper,
        "C": scissors,
    }

    def part_1(self, opponent_choice: str, player_choice: str) -> int:
        """
        Calculate the player score for part 1.
        """
        opponent: int = Solver.opponent_moves[opponent_choice]
        player: int = {
            "X": Solver.rock,
            "Y": Solver.paper,
            "Z": Solver.scissors,
        }[player_choice]

        return player + 1 + ((player - opponent + 1) % 3) * 3

    def part_2(self, opponent_choice: str, round_result: str) -> int:
        """
        Calculate the player score for part 2.
        """
        opponent: int = Solver.opponent_moves[opponent_choice]
        round_diff: int = {"X": -1, "Y": 0, "Z": 1}[round_result]

        return (opponent + round_diff) % 3 + 1 + (round_diff + 1) * 3

    def solve_part(
        self, filepath: str, get_score: Callable[[str, str], int]
    ) -> int:
        """
        Solve for one of the parts.
        """
        score = 0
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                opponent, player = line.rstrip().split()
                score += get_score(opponent, player)
        return score

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 2")
        print(f"Solving: {filepath}")
        print("Part 1")
        print(self.solve_part(filepath, self.part_1))
        print("---")
        print("Part 2")
        print(self.solve_part(filepath, self.part_2))


if __name__ == "__main__":
    solver = Solver()
    match sys.argv:
        case [_, "--path", path]:
            solver.solve(path)
        case [_]:
            solver.solve()
        case other:
            print("Usage: python solution.py --path <path>")
