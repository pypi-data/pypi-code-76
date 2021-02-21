import ast
from pathlib import Path

FILE = Path("../tests/test_variables.py")


def find(tree, node_type):
    nodes = []
    if hasattr(tree, "body"):
        for node in tree.body:
            if type(node) == node_type:
                nodes.append(node)
            nodes += find(node, node_type)
    return nodes


def calls(tree):
    with_blocks = find(tree, ast.AsyncWith)

    for with_block in with_blocks:
        yield from find(with_block, ast.Expr)


def implicit_bind():
    tree = ast.parse(FILE.read_text())

    for exp in calls(tree):
        help(exp)
        print(exp.parent)
        print(exp.value.value.func.id)


implicit_bind()
