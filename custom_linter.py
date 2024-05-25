import ast
import sys

class CustomLinter(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_FunctionDef(self, node):
        # Example check: Ensure functions have docstrings
        if not ast.get_docstring(node):
            self.errors.append(f"Function '{node.name}' is missing a docstring at line {node.lineno}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Example check: Ensure classes have docstrings
        if not ast.get_docstring(node):
            self.errors.append(f"Class '{node.name}' is missing a docstring at line {node.lineno}")
        self.generic_visit(node)

    def visit_ListComp(self, node):
        # Example check: Custom syntax for list comprehensions
        for gen in node.generators:
            if isinstance(gen, ast.comprehension) and len(gen.ifs) > 0:
                for if_clause in gen.ifs:
                    if isinstance(if_clause, ast.Compare) and len(if_clause.ops) == 1 and isinstance(if_clause.ops[0], ast.Mod):
                        # This is a custom check for your specific list comprehension syntax
                        continue
                    else:
                        self.errors.append(f"Invalid list comprehension syntax at line {node.lineno}")
        self.generic_visit(node)

    def check(self, code):
        try:
            tree = ast.parse(code)
            self.visit(tree)
        except SyntaxError as e:
            self.errors.append(f"SyntaxError: {e.msg} at line {e.lineno}")

def lint_file(file_path):
    with open(file_path, "r") as file:
        code = file.read()
        linter = CustomLinter()
        linter.check(code)
        for error in linter.errors:
            print(error)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python custom_linter.py <file.py>")
    else:
        for file_path in sys.argv[1:]:
            lint_file(file_path)

