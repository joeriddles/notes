"""Find all pending and completed markdown task items and aggregate into one markdown file."""
from __future__ import annotations

import dataclasses
import pathlib
import re
import sys
import time
from typing import Optional


TODO_PATTERN = re.compile(r"^\s*-\s?\[([x ])\]\s+(?P<text>.*)$")


@dataclasses.dataclass
class Todo:
    value: str
    filename: str = ""
    is_completed: bool = False

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
    
    def to_string(self, exclude_links: bool) -> str:
        result = self.value
        if not exclude_links:
            result = f"[[{self.filename}]]" + result
        return result


def save_todos(
    todos: list[Todo],
    path: str = "TODO.md",
    exclude_done: bool = False,
    exclude_links: bool = False,
):
    pending_todos = [_ for _ in todos if not _.is_completed]
    completed_todos = [_ for _ in todos if _.is_completed]
    
    with open(path, "w", encoding="utf-8") as todo_file:
        todo_file.write("# TODOs\n")
        
        if pending_todos:
            todo_file.write("## Pending\n")
            [todo_file.write(f"- [ ] {todo.to_string(exclude_links)}\n") for todo in pending_todos]
        
        if not exclude_done and completed_todos:
            todo_file.write("\n## Completed\n")
            [todo_file.write(f"- [x] {todo.to_string(exclude_links)}\n") for todo in completed_todos]    


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

        if markdown_lines and "exclude TODO" in markdown_lines[0]:
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
    exclude_done = "--exclude-done" in sys.argv
    exclude_links = "--exclude-links" in sys.argv

    def main():
        todos = find_todos("notes", exclude="TODO.md",)
        save_todos(
            todos,
            path="notes/TODO.md",
            exclude_done=exclude_done,
            exclude_links=exclude_links,
        )

    if watch:
        while True:
            main()
            time.sleep(1)
    else:
        main()
