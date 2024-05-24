import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import ast
from syntax_transformer import SyntaxTransformer, preprocess_code, custom_unparse, EnhancedSyntaxError
from debugging_tool import DebuggingTool

class TestSyntaxTransformer(unittest.TestCase):
    def test_list_comp(self) -> None:
        code = "[x | for x in range(10) | if x % 2 == 0]"
        expected_code = "[x for x in range(10) if x % 2 == 0]"

        with DebuggingTool():
            try:
                # Preprocess the code
                preprocessed_code = preprocess_code(code)

                # Parse the code into an AST
                tree = ast.parse(preprocessed_code)

                # Transform the AST
                transformer = SyntaxTransformer()
                new_tree = transformer.visit(tree)

                # Convert the transformed AST back to code
                new_code = custom_unparse(new_tree)

                # Assert the transformed code is as expected
                self.assertEqual(new_code.strip(), expected_code)
            except EnhancedSyntaxError as e:
                self.fail(f"EnhancedSyntaxError: {e}")

if __name__ == '__main__':
    unittest.main()

