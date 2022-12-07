import y2022.shared as shared
from dataclasses import dataclass
from typing import List, Dict

## Data
raw = shared.read_file("day07.txt")
test = shared.read_file("day07-test.txt")

## Functions
@dataclass
class Directory:
    name: str
    parent: dict
    dirs: Dict[str, "Directory"] = None
    files: Dict[str, "File"] = None
    size: int = 0


@dataclass
class File:
    name: str
    size: int = 0
    ext: str = None


@dataclass
class FileSystem:
    commands: List[str]
    root: Directory = None
    cwd: Directory = None
    dirs: list = None

    def __post_init__(self):
        self.cwd = Directory(
            name="root",
            files={},
            dirs={},
            parent=None,
        )
        self.root = self.cwd
        self.dirs = []
        self.process_lines()

    def is_command(self, line: str):
        return line.startswith("$")

    def split_command(self, line: str):
        command = line[2:]
        if " " in command:
            command, arg = command.split()
        else:
            arg = None
        return command, arg

    def mkdir(self, dirname: str):
        if dirname == "/":
            dirname = "root"
        if dirname not in self.cwd.dirs:
            new_dir = Directory(
                name=dirname,
                parent=self.cwd,
                dirs={},
                files={},
            )
            self.cwd.dirs[dirname] = new_dir

    def stat_file(self, filename: str, size: int):
        if filename not in self.cwd.files:
            new_file = File(
                name=filename,
                # parent = self.cwd,
                size=int(size),
                ext=filename.split(".")[1] if "." in filename else None,
            )
            self.cwd.files[filename] = new_file

    def cd(self, arg: str):
        if arg == "..":
            self.cwd = self.cwd.parent
        else:
            if arg not in self.cwd.dirs:
                print(f"Creating directory {arg}...")
                new_dir = Directory(
                    name=arg,
                    parent=self.cwd,
                    dirs={},
                    files={},
                )
                self.cwd.dirs[arg] = new_dir
            self.cwd = self.cwd.dirs[arg]

    def process_line(self, line: str):
        if line.startswith("dir"):
            dirname = line.split()[1]
            self.mkdir(dirname)
        elif line[0].isdigit():
            size, filename = line.split()
            self.stat_file(filename, size)
        elif self.is_command(line):
            command, arg = self.split_command(line)
            if command == "cd" and arg != "/":
                self.cd(arg)
            elif command == "ls":
                pass

    def process_lines(self):
        for line in self.commands:
            self.process_line(line)

    def du(self, directory: Directory = None) -> int:
        if directory is None:
            directory = self.root
        size = 0
        size += sum([file.size for file in directory.files.values()])
        size += sum([self.du(subdir) for subdir in directory.dirs.values()])
        directory.size = size
        self.dirs.append(directory)
        return size

    def get_total_size(self, max_size=100000) -> int:
        return sum([d.size for d in self.dirs if d.size <= max_size])

    def find_dir_to_delete(
        self,
        fs_max_size=70000000,
        update_size=30000000,
    ) -> Directory:
        _ = self.get_total_size()
        remaining_size = fs_max_size - self.root.size
        free_up_size = update_size - remaining_size
        if free_up_size <= 0:
            return 0
        else:
            sizes = [(d.size, d) for d in self.dirs if d.size >= free_up_size]
            sizes.sort()
            return sizes[0][1]


def solve(raw):
    fs = FileSystem(raw)
    fs.du()
    return fs.get_total_size()


def solve2(raw):
    fs = FileSystem(raw)
    fs.du()
    return fs.find_dir_to_delete().size


## Testing
assert solve(test) == 95437
assert solve2(test) == 24933642

## Solutions
print(f"Solution to part 1: {solve(raw)}")
print(f"Solution to part 2: {solve2(raw)}")
