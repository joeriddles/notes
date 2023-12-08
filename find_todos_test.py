import unittest

from find_todos import Todo


class TodoTests(unittest.TestCase):
    def test_from_str(self):
        SUB_TESTS: list[tuple[str, Todo]] = [
            ("- [ ] hello", Todo("hello", "", False)),
            ("- [x] hello", Todo("hello", "", True)),
            ("-[ ] hello", Todo("hello", "", False)),
            ("-[x] hello", Todo("hello", "", True)),
        ]

        for line, expected in SUB_TESTS:
            with self.subTest(line=line):
                actual = Todo.from_str(line)
                self.assertEqual(actual, expected)

    def test_to_markdown(self):
        SUB_TESTS: list[tuple[Todo, str]] = [
            (Todo("hello", "", False), "- [ ] hello"),
            (Todo("hello", "", True), "- [x] hello"),
            (Todo("hello", "file.md", False), "- [ ] [[file.md]] hello"),
            (Todo("hello", "file.md", True), "- [x] [[file.md]] hello"),
        ]

        for todo, expected in SUB_TESTS:
            with self.subTest(todo=todo):
                actual = todo.to_markdown()
                self.assertEqual(actual, expected)
