.PHONY: test,main,watch

main:
	export PYTHONPATH=$$PYTHONPATH:$(PWD); \
    python3 find_todos.py
	
watch:
	export PYTHONPATH=$$PYTHONPATH:$(PWD); \
    python3 find_todos.py --watch

test:
	export PYTHONPATH=$$PYTHONPATH:$(PWD); \
    python3 -m unittest find_todos_test.py
