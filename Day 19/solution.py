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
        max_ore, max_clay, max_obsidian, _ = [
            max(resource) for resource in zip(*robot_costs)
        ]

        def can_get_resource_in_time(
            time: int,
            resources: list[int],
            target_resource: int,
            robots: list[int],
            target_robot: int
        ) -> bool:
            return (
                resources[target_resource] + (time - 1) * robots[target_resource] >=
                robot_costs[target_robot][target_resource]
            )

        def can_build_in_time(
            time: int,
            resources: list[int],
            robots: list[int],
            target_robot: int
        ) -> bool:
            if not can_get_resource_in_time(time, resources, Solver.ORE, robots, target_robot):
                return False
            if target_robot == Solver.OBSIDIAN:
                return can_get_resource_in_time(time, resources, Solver.CLAY, robots, target_robot)
            if target_robot == Solver.GEODE:
                return can_get_resource_in_time(
                    time, resources, Solver.OBSIDIAN, robots, target_robot)
            return True

        def should_not_build(
            time: int,
            resources: list[int],
            robots: list[int],
            target_robot: int,
            current_geode_max: int
        ) -> bool:
            # Not enough time
            if time <= 0:
                return True

            # No need for more ore robots
            if target_robot == Solver.ORE and robots[Solver.ORE] >= max_ore:
                return True

            # No need for more clay robots
            if target_robot == Solver.CLAY and robots[Solver.CLAY] >= max_clay:
                return True

            # No need for more obsidian robots or they are impossible to build
            if (
                target_robot == Solver.OBSIDIAN and
                (
                    robots[Solver.OBSIDIAN] >= max_obsidian or
                    robots[Solver.CLAY] == 0
                )
            ):
                return True

            # Impossible to build geode robots
            if target_robot == Solver.GEODE and robots[Solver.OBSIDIAN] == 0:
                return True

            max_possible_geode = resources[Solver.GEODE] + \
                robots[Solver.GEODE] * time + (time - 1) * time // 2
            return max_possible_geode <= current_geode_max

        def solve(
            time: int,
            resources: list[int],
            robots: list[int],
            target_robot: int,
            current_geode_max: int
        ) -> int:
            if should_not_build(
                time=time,
                resources=resources,
                robots=robots,
                target_robot=target_robot,
                current_geode_max=current_geode_max
            ):
                return resources[Solver.GEODE]

            if not can_build_in_time(
                time=time,
                resources=resources,
                robots=robots,
                target_robot=target_robot
            ):
                return resources[Solver.GEODE] + time * robots[Solver.GEODE]

            time_taken = math.ceil(max(
                0, *(
                    (cost - resource) / robot if robot > 0 else 0
                    for cost, resource, robot
                    in zip(robot_costs[target_robot], resources, robots)
                )
            ))

            time -= time_taken + 1
            new_resources = [
                resource + robot * (time_taken + 1) - cost
                for resource, robot, cost
                in zip(resources, robots, robot_costs[target_robot])
            ]

            robots[target_robot] += 1
            for next_robot in range(4):
                current_geode_max = max(
                    current_geode_max,
                    solve(
                        time=time,
                        resources=new_resources,
                        robots=robots,
                        target_robot=next_robot,
                        current_geode_max=current_geode_max
                    )
                )
            robots[target_robot] -= 1

            return current_geode_max

        result = 0
        for target_robot in range(4):
            result = max(
                result,
                solve(
                    time=time,
                    resources=[0, 0, 0, 0],
                    robots=[1, 0, 0, 0],
                    target_robot=target_robot,
                    current_geode_max=result
                )
            )

        return blueprint_id, result

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
