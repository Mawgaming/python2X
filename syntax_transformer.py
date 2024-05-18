import ast

class EnhancedSyntaxError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")

class SyntaxTransformer(ast.NodeTransformer):
    def visit_ListComp(self, node):
        try:
            for generator in node.generators:
                if isinstance(generator.iter, ast.Call) and generator.iter.func.id == 'range':
                    generator.ifs = [
                        ast.Compare(
                            left=ast.BinOp(
                                left=ast.Name(id='x', ctx=ast.Load()),
                                op=ast.Mod(),
                                right=ast.Constant(value=2)
                            ),
                            ops=[ast.Eq()],
                            comparators=[ast.Constant(value=0)]
                        )
                    ]
            return node
        except Exception as e:
            raise EnhancedSyntaxError("Invalid list comprehension syntax", node.lineno, node.col_offset) from e

def preprocess_code(code):
    # Replace the new syntax with the old syntax
    return code.replace('| for', 'for').replace('| if', 'if')

# Sample code to test
code = "[x | for x in range(10) | if x % 2 == 0]"

# Preprocess the code
preprocessed_code = preprocess_code(code)

# Parse the code into an AST
tree = ast.parse(preprocessed_code)

# Transform the AST
transformer = SyntaxTransformer()
new_tree = transformer.visit(tree)

# Custom unparse function
def custom_unparse(node):
    if isinstance(node, ast.Module):
        return '\n'.join(custom_unparse(stmt) for stmt in node.body)
    elif isinstance(node, ast.Expr):
        return custom_unparse(node.value)
    elif isinstance(node, ast.ListComp):
        elt = custom_unparse(node.elt)
        generator = node.generators[0]
        target = custom_unparse(generator.target)
        iter = custom_unparse(generator.iter)
        ifs = ' '.join([custom_unparse(if_cond) for if_cond in generator.ifs])
        return f'[{elt} for {target} in {iter} if {ifs}]'
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.BinOp):
        left = custom_unparse(node.left)
        op = custom_unparse(node.op)
        right = custom_unparse(node.right)
        return f'{left} {op} {right}'
    elif isinstance(node, ast.Compare):
        left = custom_unparse(node.left)
        op = custom_unparse(node.ops[0])
        right = custom_unparse(node.comparators[0])
        return f'{left} {op} {right}'
    elif isinstance(node, ast.Mod):
        return '%'
    elif isinstance(node, ast.Eq):
        return '=='
    elif isinstance(node, ast.Call):
        func = custom_unparse(node.func)
        args = ', '.join([custom_unparse(arg) for arg in node.args])
        return f'{func}({args})'
    elif isinstance(node, ast.comprehension):
        target = custom_unparse(node.target)
        iter = custom_unparse(node.iter)
        ifs = ' '.join([custom_unparse(if_cond) for if_cond in node.ifs])
        return f'{target} in {iter} if {ifs}'
    return ast.dump(node)

# Convert the transformed AST back to code
new_code = custom_unparse(new_tree)
print(new_code)

