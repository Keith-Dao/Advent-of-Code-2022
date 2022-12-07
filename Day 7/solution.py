"""
    Day 7 Solver Module
"""
from __future__ import annotations
import sys


class Folder:
    """
    A folder in a file system.
    """

    def __init__(self, name: str, parent=None) -> None:
        self.name: str = name
        self.subfolders: dict[str, Folder] = {}
        self.files: dict[str, int] = {}
        self.parent: Folder | None = parent
        self.size: int = 0

    @staticmethod
    def change_directory(folder: Folder, root: Folder, token: str) -> Folder:
        """
        Change directories.

        Args:
            folder (Folder): The current folder
            root (Folder): The root folder
            token (str): The inputted change
        Returns:
            The resulting folder when applying the cd command.
        """
        if token == "/":
            return root
        if token == "..":
            return folder.get_parent()
        return folder.subfolders[token]

    def get_parent(self) -> Folder:
        """"
        Get the parent folder if it is not the root folder.

        Returns:
            The parent folder if this is not the root folder.
        Raises:
            ValueError: This was called on the root folder
        """
        if not self.parent:
            raise ValueError("The root folder does not have a parent.")
        return self.parent

    def get_size(self) -> int:
        """
        Get the total size of the folder.

        Returns:
            The total size of the folder.
        """
        return self.size

    def add_item(self, tokens: list[str]) -> None:
        """
        Add an item to the folder.

        Args:
            tokens (list[str]): The tokens of an output line.
        """
        if tokens[0] == "dir":
            self.add_subfolder(tokens[1])
        else:
            self.add_file(filename=tokens[1], size=tokens[0])

    def add_subfolder(self, folder_name: str) -> None:
        """
        Add a subfolder to the current folder.

        Args:
            folder_name (str): The name of the subfolder to add
        """
        if folder_name in self.subfolders:
            return
        self.subfolders[folder_name] = Folder(name=folder_name, parent=self)

    def add_file(self, filename: str, size: str) -> None:
        """
        Add a file to the folder.

        Args:
            filename (str): Name of the file to add
            size (str): The size of the file
        """
        if filename in self.files:
            return

        filesize = int(size)
        self.files[filename] = filesize
        self.add_size(size=filesize)

    def add_size(self, size: int) -> None:
        """
        Increase the total size of the folder.
        """
        self.size += size
        if self.parent:
            self.parent.add_size(size)

    def __str__(self, depth=0) -> str:
        indent = "  "
        newline = "\n"

        folder = f"{indent * depth}- {self.name} (dir){newline}"
        subfolders = ''.join(
            subfolder.__str__(depth=depth+1)
            for subfolder in self.subfolders.values()
        )
        items = "".join(
            f"{indent * (depth + 1)}- {filename} (file, size={size}){newline}"
            for filename, size in self.files.items()
        )

        return folder + subfolders + items


class Solver:
    """
    Day 7 Solver
    """

    def __init__(self) -> None:
        self.root: Folder = Folder("/")
        self.parsed: str = ""

    def parse_file_structure(self, filepath: str) -> None:
        """
        Parse the the file to determine the file structure.

        Args:
            filepath (str): Path to the file containing the data
        """
        if self.parsed == filepath:
            return

        self.root = Folder("/")
        current: Folder = self.root
        with open(filepath, "r", encoding=sys.getdefaultencoding()) as file:
            line = file.readline().rstrip()
            while line != "":
                # Read commands
                while line != "" and line[0] == "$":
                    tokens = line.split()
                    line = file.readline().rstrip()

                    if tokens[1] == "ls":
                        break
                    current = Folder.change_directory(
                        current,
                        self.root,
                        tokens[2]
                    )

                # Get the files
                while line != "" and line[0] != "$":
                    tokens = line.split()
                    line = file.readline().rstrip()
                    current.add_item(tokens)

        self.parsed = filepath

    def part_1(self, filepath: str) -> int:
        """
        Solve part 1.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 1
        """
        self.parse_file_structure(filepath)

        current = self.root
        stack = [current]
        total_size = 0
        max_directory_size = 100000
        while stack:
            folder = stack.pop()
            folder_size = folder.get_size()

            if folder_size <= max_directory_size:
                total_size += folder_size

            stack.extend(folder.subfolders.values())
        return total_size

    def part_2(self, filepath: str) -> int:
        """
        Solve part 2.

        Args:
            filepath (str): Path to the input file
        Returns:
            Solution to part 2
        """
        self.parse_file_structure(filepath)

        stack = [self.root]
        smallest_valid_folder_size = self.root.get_size()

        maximum_used_space = 70000000 - 30000000
        minimum_space_to_remove = smallest_valid_folder_size - maximum_used_space

        while stack:
            folder = stack.pop()
            folder_size = folder.get_size()

            if folder_size < minimum_space_to_remove:
                continue

            smallest_valid_folder_size = min(
                smallest_valid_folder_size,
                folder_size
            )

            stack.extend(folder.subfolders.values())
        return smallest_valid_folder_size

    def solve(self, filepath: str = "input.txt") -> None:
        """
        Perform full solve.
        """
        print("Day 7")
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
