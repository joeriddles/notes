"""Find all pending and completed markdown task items and aggregate into one markdown file."""
from __future__ import annotations

import dataclasses
import pathlib
import re
import sys
import time
from collections import defaultdict
from typing import Optional


TODO_PATTERN = re.compile(r"^\s*-\s?\[([x ])\]\s+(?P<text>.*)$")


@dataclasses.dataclass
class Todo:
    value: str
    filename: str = ""
    is_completed: bool = False

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_str(cls, value: str) -> Todo:
        rmatch = TODO_PATTERN.match(value)
        if rmatch is None:
            raise ValueError(f"{value} did not match {TODO_PATTERN.pattern}")

        return cls.from_match(rmatch)
    
    @classmethod
    def from_match(cls, rmatch: re.Match) -> Todo:
        value = rmatch.group("text")
        is_completed = rmatch.groups()[0].casefold() == "x"
        return Todo(value, "", is_completed)
    
    def to_markdown(self, exclude_links: bool = False) -> str:
        result = str(self)

        if self.filename and not exclude_links:
            result = f"[[{self.filename}]] {result}"
        
        result = f"- [x] {result}" if self.is_completed else f"- [ ] {result}"
        return result


def save_todos(
    todos: list[Todo],
    path: str = "TODO.md",
    include_done: bool = False,
    exclude_links: bool = False,
):
    pending_todos = [_ for _ in todos if not _.is_completed]
    completed_todos = [_ for _ in todos if _.is_completed]
    
    with open(path, "w", encoding="utf-8") as todo_file:
        if pending_todos:
            todos_by_filename: dict[str, list[Todo]] = defaultdict(list)
            for todo in pending_todos:
                todos_by_filename[todo.filename].append(todo)

            if include_done:
                # only include level 2 headers if multiple of them
                todo_file.write("## Pending\n")
            
            for filename, todos_for_filename in todos_by_filename.items():
                todo_file.write(f"- [[{filename}]]")
                for todo in todos_for_filename:
                    line = "    " + todo.to_markdown(exclude_links=True) + "\n"
                    todo_file.write(line)
        
        if include_done and any(completed_todos):
            todos_by_filename: dict[str, list[Todo]] = defaultdict(list)
            for todo in completed_todos:
                todos_by_filename[todo.filename].append(todo)

            todo_file.write("\n## Completed\n")
            for todo in completed_todos:
                todo_file.write(todo.to_markdown(exclude_links) + "\n")


def find_todos(path: str = ".", exclude: Optional[str] = None) -> list[Todo]:
    """Recursively find all markdown task items for the given path.
    
    Args:
        path: The path to recursively search for markdown file in.
        exclude: A filename to exclude from the markdown file search.
        exclude_done: Exclude completed TODOs

    Returns:
        A tuple consisting of all found pending todo items and all completed todo items.
    """
    all_todos: list[Todo] = []

    folder_path = pathlib.Path(path)
    for markdown_path in folder_path.rglob("**/*.md"):
        dir_contains_excludes_file = (markdown_path.parent / ".exclude_todos").exists()
        if dir_contains_excludes_file:
            continue

        filename = markdown_path.name
        if filename == exclude:
            continue

        with markdown_path.open("r", encoding="utf-8") as markdown_file:
            markdown_lines = markdown_file.readlines()

        contains_exclude_comment = any(["<!-- exclude TODO -->" in line for line in markdown_lines])
        if contains_exclude_comment:
            continue

        todos = parse_todos(markdown_lines)
        for todo in todos:
            todo.filename = filename

        all_todos.extend(todos)

    return all_todos


def parse_todos(lines) -> list[Todo]:
    """Parse all GitHub flavored markdown task lists"""
    todos = [
        Todo.from_match(match)
        for line in lines
        if (match := TODO_PATTERN.match(line))
    ]
    return todos


if __name__ == "__main__":
    watch = "--watch" in sys.argv
    include_done = "--include-done" in sys.argv
    exclude_links = "--exclude-links" in sys.argv

    def main():
        todos = find_todos("notes", exclude="TODO.md",)
        save_todos(
            todos,
            path="notes/TODO.md",
            include_done=include_done,
            exclude_links=exclude_links,
        )

    if watch:
        while True:
            main()
            time.sleep(1)
    else:
        main()
