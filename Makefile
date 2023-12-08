.PHONY: test

test:
	export PYTHONPATH=$$PYTHONPATH:$(PWD); \
    python3 -m unittest find_todos_test.py
