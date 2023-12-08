import unittest

from find_todos import Todo

class TodoTests(unittest.TestCase):

    def test_from_str(self):
        SUB_TESTS = [
            ("- [ ] hello", Todo("hello", "", False)),
            ("- [x] hello", Todo("hello", "", True)),
            ("-[ ] hello",  Todo("hello", "", False)),
            ("-[x] hello",  Todo("hello", "", True)),
        ]

        for line, expected in SUB_TESTS:
            with self.subTest(line=line):
                actual = Todo.from_str(line)
                self.assertEqual(actual, expected)
