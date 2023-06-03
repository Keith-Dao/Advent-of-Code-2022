"""
    Day 19 Solver Module
"""
import math
import sys
import re


class Solver:
    """
    Day 19 Solver
    """
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3

    def get_robot_costs(self, robot_values: list[int]) -> list[list[int]]:
        """
        Parse the robot costs.

        Args:
            robot_values (list[int]): Unparsed values of the robot cost
        Returns:
            The robot costs.
        """
        return [
            [robot_values[0], 0, 0, 0],  # Ore Robot
            [robot_values[1], 0, 0, 0],  # Clay Robot
            [robot_values[2], robot_values[3], 0, 0],  # Obsidian robot
            [robot_values[4], 0, robot_values[5], 0]  # Geode robot
        ]

    def get_maximum_geode(self, line: str, time: int) -> tuple[int, int]:
        """
        Get the maximum number of geode for a given blueprint.

        Args:
            line (str): The blueprint
            time (int): The maximum amount of time
        Returns:
            The blueprint id and the maximum number of geode for a blueprint
        """
        if line == "":
            return 0, 1

        blueprint_id, *robot_values = (
            int(num)
            for num in re.findall(r"\d+", line)
        )
        robot_costs = self.get_robot_costs(robot_values=robot_values)
        max_costs = [
            max(resource) for resource in zip(*robot_costs)
        ]
        geode_max: int = 0

        def can_build(
            resources: list[int],
            target_robot: int
        ) -> bool:
            return all(
                resource >= cost
                for resource, cost in zip(resources, robot_costs[target_robot])
            )

        def solve(
            time: int,
            resources: list[int],
            robots: list[int],
            can_build_robots: list[bool]
        ) -> None:
            nonlocal geode_max

            if time <= 0:
                geode_max = max(geode_max, resources[Solver.GEODE])
                return

            if (
                resources[Solver.GEODE] + robots[Solver.GEODE] *
                    time + time * (time - 1) // 2
                    <= geode_max
            ):
                return

            if can_build(resources, Solver.GEODE):
                new_resources = [
                    resource + robot - cost
                    for resource, robot, cost
                    in zip(resources, robots, robot_costs[Solver.GEODE])
                ]
                new_robots = list(robots)
                new_robots[Solver.GEODE] += 1
                solve(time - 1, new_resources, new_robots, [True] * 3)
                return

            new_can_build_robots = [True] * 3
            for resource in [Solver.OBSIDIAN, Solver.CLAY, Solver.ORE]:
                if can_build(resources, resource):
                    new_can_build_robots[resource] = False
                    if can_build_robots[resource] and robots[resource] < max_costs[resource]:
                        new_resources = [
                            resource + robot - cost
                            for resource, robot, cost
                            in zip(resources, robots, robot_costs[resource])
                        ]
                        new_robots = list(robots)
                        new_robots[resource] += 1
                        solve(time - 1, new_resources, new_robots, [True] * 3)

            new_resources = [
                resource + robot
                for resource, robot
                in zip(resources, robots)
            ]
            solve(time - 1, new_resources, robots, new_can_build_robots)

            # return current_geode_max

        solve(time, [0, 0, 0, 0], [1, 0, 0, 0], [True] * 3)
        return blueprint_id, geode_max

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return sum(math.prod(self.get_maximum_geode(line=line, time=24)) for line in file)

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            return math.prod(
                self.get_maximum_geode(line=file.readline(), time=32)[1]
                for _ in range(3)
            )

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 19")
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
