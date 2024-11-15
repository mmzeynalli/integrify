import ast
import inspect

from integrify.api import APIClient


def get_client_attributes(cls):
    source = inspect.getsource(cls)
    tree = ast.parse(source)

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.add_url_calls = set()
            self.functions = set()

        def visit_FunctionDef(self, node: ast.FunctionDef):
            self.functions.add(node.name)
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call):
            if isinstance(node.func, ast.Attribute):
                if (
                    node.func.attr == 'add_url'
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == 'self'
                ):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        self.add_url_calls.add(node.args[0].value)

            self.generic_visit(node)

    visitor = Visitor()
    visitor.visit(tree)
    return visitor.add_url_calls, visitor.functions


def test_method_definitions():
    for cls in APIClient.__subclasses__():
        if inspect.isclass(cls):
            add_url_calls, methods = get_client_attributes(cls)

            assert add_url_calls.issubset(methods)
