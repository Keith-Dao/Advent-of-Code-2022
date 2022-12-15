"""
    Day 15 Solver Module
"""
from collections import defaultdict
from itertools import product
import sys
import re


class Map:
    """
    The map
    """

    def __init__(self) -> None:
        self.sensors = []
        self.beacons = []

    def add_sensor_and_beacon(self, line: str) -> None:
        """
        Add sensor and beacon.

        Args:
            line (str): One line of the input with the locations of the sensor and beacon
        """
        result = re.search(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line
        )
        if not result:
            raise ValueError("Invalid format.")
        sensor_x, sensor_y, beacon_x, beacon_y = [
            int(coord) for coord in result.groups()
        ]
        self.sensors.append((sensor_x, sensor_y))
        self.beacons.append((beacon_x, beacon_y))

    @staticmethod
    def manhattan_distance(point_1: tuple[int, int], point_2: tuple[int, int]) -> int:
        """
        Calculate the manhattan distance.

        Args:
            point_1 (tuple[int, int]): First point
            point_2 (tuple[int, int]): Second point
        Returns:
            The manhattan distance.
        """
        return sum(abs(a - b) for a, b in zip(point_1, point_2))

    def merge_intervals(self, intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Merge the given intervals.

        Args:
            intervals (list[tuple[int, int]]): Intervals to merge
        Returns:
            Merged intervals.
        """
        node_ranges = []
        for start, end in sorted(intervals):
            if not node_ranges or node_ranges[-1][1] < start:
                node_ranges.append((start, end))
            else:
                node_ranges[-1] = (
                    node_ranges[-1][0],
                    max(node_ranges[-1][1], end)
                )
        return node_ranges

    def find_coverage(self, target_y: int) -> int:
        """
        Find the number of spots that a sensor cannot be in.

        Args:
            target_y (int): The y value to the find the invalid spots in
        Returns:
            The number of invalid spots.
        """
        beacons = set()
        node_ranges = []

        # Find the ranges and beacons
        for sensor, beacon in zip(self.sensors, self.beacons):
            distance = Map.manhattan_distance(sensor, beacon)
            beacon_x, beacon_y = beacon
            if beacon_y == target_y:
                beacons.add(beacon_x)

            sensor_x, sensor_y = sensor
            sensor_reach = distance - abs(target_y - sensor_y)
            if sensor_reach < 0:
                continue
            node_ranges.append(
                (sensor_x - sensor_reach, sensor_x + sensor_reach)
            )

        # Merge the ranges
        node_ranges = self.merge_intervals(node_ranges)

        # Count the number of beacons that are in one of the ranges
        idx = num_beacons = 0
        for beacon_x in sorted(beacons):
            while idx < len(node_ranges) and beacon_x < node_ranges[idx][0]:
                idx += 1

            if idx == len(node_ranges):
                break
            num_beacons += node_ranges[idx][0] <= beacon_x <= node_ranges[idx][1]

        return sum((end - start + 1) for start, end in node_ranges) - num_beacons

    def get_possible_distress_beacon_locations(self) -> tuple[list[int], list[int]]:
        """
        Get the line where the distress beacon could be.

        Returns:
            The intercept of the negative and positive lines respectively.
        """
        lines = [defaultdict(lambda: [False, False])] * 2
        for sensor, beacon in zip(self.sensors, self.beacons):
            distance = Map.manhattan_distance(sensor, beacon) + 1
            sensor_x, sensor_y = sensor

            for gradient, y_shift in product([-1, 1], repeat=2):
                y_intercept = sensor_y - gradient * sensor_x + y_shift * distance
                lines[gradient > 0][y_intercept][y_shift > 0] = True

        return tuple([b for b, norm in lines[i].items() if all(norm)] for i in range(2))

    def get_distress_beacon_frequency(self, lower_bound: int, upper_bound: int) -> int:
        """
        Get the distress beacon frequency.

        Args:
            lower_bound (int): The lower bound of the distress beacon
            upper_bound (int): The upper bound of the distress beacon
        Returns:
            The distress beacon frequency
        """
        for b_0, b_1 in product(*self.get_possible_distress_beacon_locations()):
            beacon_x = (b_0 - b_1) // 2
            beacon_y = beacon_x + b_1
            if (
                lower_bound <= beacon_x <= upper_bound and
                lower_bound <= beacon_y <= upper_bound and
                all(
                    Map.manhattan_distance((beacon_x, beacon_y), sensor) >
                    Map.manhattan_distance(beacon, sensor)
                    for sensor, beacon in zip(self.sensors, self.beacons)
                )
            ):
                return beacon_x * 4000000 + beacon_y
        return -1


class Solver:
    """
    Day 15 Solver
    """

    def __init__(self) -> None:
        self.map = Map()
        self.parsed = ""

    def parse(self, filepath: str) -> None:
        """
        Parse the given file.

        Args:
            filepath (str): Path to the input file.
        """
        if self.parsed == filepath:
            return

        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            for line in file:
                self.map.add_sensor_and_beacon(line=line)
        self.parsed = filepath

    def part_1(self, filepath: str, is_sample: bool = False) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
            is_sample (bool): Is using the sample input
        Returns:
            Solution to part 1
        """
        self.parse(filepath=filepath)
        return self.map.find_coverage(target_y=2000000 if not is_sample else 10)

    def part_2(self, filepath: str, is_sample: bool = False) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
            is_sample (bool): Is using the sample input
        Returns:
            Solution to part 2
        """
        self.parse(filepath=filepath)
        return self.map.get_distress_beacon_frequency(
            lower_bound=0,
            upper_bound=4000000 if not is_sample else 20
        )

    def solve(self, filepath: str = "input.txt", is_sample: bool = False) -> None:
        """
        Perform full solve.
        """
        print("Day 15")
        print(f"Solving: {filepath}")
        print("Part 1")
        print(self.part_1(filepath=filepath, is_sample=is_sample))
        print("---")
        print("Part 2")
        print(self.part_2(filepath=filepath, is_sample=is_sample))


if __name__ == "__main__":
    solver = Solver()
    match sys.argv:
        case [_, "--path", path, "--sample"]:
            solver.solve(filepath=path, is_sample=True)
        case [_, "--path", path]:
            solver.solve(path)
        case [_]:
            solver.solve()
        case _:
            print("Usage: python solution.py --path <path>")
