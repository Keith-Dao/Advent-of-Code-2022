"""
    Day 16 Solver Module

    Needed to look at solutions for this one.
"""
from collections import deque
from itertools import product
import sys
import re


class Solver:
    """
    Day 16 Solver
    """

    def parse_line(self, line: str) -> tuple[str, int, list[str]]:
        """
        Parse the given line.

        Args:
            line (str): The line to parse
        Returns the extracted info.
        """
        result = re.search(
            r"Valve ([a-zA-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line
        )

        if not result:
            raise ValueError("Invalid format.")
        name, flow_rate, neighbours = result.groups()
        return name, int(flow_rate), neighbours.split(", ")

    def solve_part(self, filepath: str, starting_time: int, include_elephant: bool) -> int:
        """
        Generic solve.

        Args:
            filepath (str): Path to the input file
            starting_time (int): The amount of time to start with
            include_elephant (bool): Include an elephant to help
        Returns:
            Solution to part
        """
        pipes = {}
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                name, flow_rate, neighbours = self.parse_line(line)
                pipes[name] = {
                    "flow_rate": flow_rate,
                    "neighbours": neighbours,
                    "paths": {}
                }

        def bfs(source: str, destination: str) -> int:
            queue = deque([source])
            visited = set(queue)
            steps = 1

            while queue:
                for _ in range(len(queue)):
                    node = queue.popleft()

                    for neighbour in pipes[node]["neighbours"]:
                        if neighbour in visited:
                            continue
                        if neighbour == destination:
                            return steps
                        visited.add(neighbour)
                        queue.append(neighbour)
                steps += 1
            return -1

        for destination in pipes:
            if destination == "AA":
                continue
            pipes["AA"]["paths"][destination] = bfs("AA", destination)

        for source, destination in product(
            (
                pipe_name for pipe_name, pipe in pipes.items()
                if pipe["flow_rate"] != 0
            ),
            repeat=2
        ):
            if destination == source:
                continue
            pipes[source]["paths"][destination] = bfs(source, destination)

        def dfs(
            time_remaining: int,
            current_pipe: str,
            opened_pipes: set[str],
            include_elephant: bool
        ) -> int:
            if time_remaining <= 0:
                return 0

            # Open current valve
            if current_pipe not in opened_pipes:
                return time_remaining * pipes[current_pipe]["flow_rate"] + max(
                    dfs(
                        time_remaining=time_remaining - 1,
                        current_pipe=current_pipe,
                        opened_pipes=opened_pipes | {current_pipe},
                        include_elephant=include_elephant
                    ),
                    include_elephant and dfs(
                        time_remaining=starting_time - 1,
                        current_pipe="AA",
                        opened_pipes=opened_pipes | {current_pipe},
                        include_elephant=False
                    )
                )

            # Move to a neighbouring pipe
            return max(
                0, 0,
                *(
                    dfs(
                        time_remaining=time_remaining - time_taken,
                        current_pipe=destination_pipe,
                        opened_pipes=opened_pipes,
                        include_elephant=include_elephant
                    )
                    for destination_pipe, time_taken in pipes[current_pipe]["paths"].items()
                    if destination_pipe not in opened_pipes
                )
            )

        return dfs(
            time_remaining=starting_time,
            current_pipe="AA",
            opened_pipes=set("AA"),
            include_elephant=include_elephant
        )

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        return self.solve_part(filepath=filepath, starting_time=30, include_elephant=False)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        return self.solve_part(filepath=filepath, starting_time=26, include_elephant=True)

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 16")
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
