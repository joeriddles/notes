"""Find all pending and completed markdown task items and aggregate into one markdown file."""
import pathlib
import re
import sys
import time
from typing import Optional, Tuple


PENDING_TODO_PATTERN = re.compile(r"^\s*-\s+\[ \]\s+(?P<text>.*)$")
COMPLETED_TODO_PATTERN = re.compile(r"^\s*-\s+\[x\]\s+(?P<text>.*)$")


def save_todos(
    pending_todos: list[str],
    completed_todos: list[str],
    path: str = "TODO.md",
):
    with open(path, "w", encoding="utf-8") as todo_file:
        todo_file.write("# TODOs\n")
        todo_file.write("## Pending\n")
        [todo_file.write(f"- [ ] {todo}\n") for todo in pending_todos]
        todo_file.write("\n## Completed\n")
        [todo_file.write(f"- [x] {todo}\n") for todo in completed_todos]    


def find_todos(path: str = ".", exclude: Optional[str] = None) -> Tuple[list[str], list[str]]:
    """Recursively find all markdown task items for the given path.
    
    Args:
        path: The path to recursively search for markdown file in.
        exclude: A filename to exclude from the markdown file search.

    Returns:
        A tuple consisting of all found pending todo items and all completed todo items.
    """
    all_pending_todos: list = []
    all_completed_todos: list = []
    folder_path = pathlib.Path(path)
    for markdown_path in folder_path.rglob("**/*.md"):
        if markdown_path.name == exclude:
            continue
        with markdown_path.open("r", encoding="utf-8") as markdown_file:
            markdown_lines = markdown_file.readlines()
        if markdown_lines and "exclude TODO" in markdown_lines[0]:
            continue
        pending_todos, completed_todos = parse_todos(markdown_lines)
        all_pending_todos.extend(pending_todos)
        all_completed_todos.extend(completed_todos)
    return all_pending_todos, all_completed_todos


def parse_todos(lines) -> Tuple[list[str], list[str]]:
    """Parse all GitHub flavored markdown task lists"""
    pending_todos = [
        match.group("text")
        for line in lines
        if (match := PENDING_TODO_PATTERN.match(line))
    ]
    completed_todos = [
        match.group("text")
        for line in lines
        if (match := COMPLETED_TODO_PATTERN.match(line))
    ]
    return pending_todos, completed_todos



if __name__ == "__main__":
    watch = False
    if sys.argv[-1] == "--watch":
        watch = True

    if watch:
        while True:
            todos = find_todos("notes", exclude="TODO.md")
            save_todos(*todos, path="notes/TODO.md")
            time.sleep(1)
    else:
        todos = find_todos("notes", exclude="TODO.md")
        save_todos(*todos, path="notes/TODO.md")
