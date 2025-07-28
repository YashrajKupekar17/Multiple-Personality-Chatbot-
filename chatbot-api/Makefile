# Simple Makefile for directory tree
.PHONY: tree

tree:
	@uv run --with directory-tree python -c "\
	from directory_tree import DisplayTree; \
	print(DisplayTree('.', stringRep=True, maxDepth=10, onlyFiles=False,onlyDirs=False, \
	ignoreList=['.venv', '__pycache__', '.git', '.pytest_cache', 'node_modules']))"

