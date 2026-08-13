import ast
import importlib.util
import inspect
import os

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


def import_client_modules():
    current_dir = os.path.join(os.getcwd(), 'src', 'integrify')
    client_modules = {}
    for folder in os.listdir(current_dir):
        folder_path = os.path.join(current_dir, folder)
        if os.path.isdir(folder_path):
            client_file = os.path.join(folder_path, 'client.py')
            if os.path.exists(client_file):
                spec = importlib.util.spec_from_file_location(
                    f'integrify.{folder}.client',
                    client_file,
                )
                spec.loader.exec_module(importlib.util.module_from_spec(spec))
    return client_modules


def test_method_definitions():
    import_client_modules()
    for cls in APIClient.__subclasses__():
        if inspect.isclass(cls):
            add_url_calls, methods = get_client_attributes(cls)

            assert add_url_calls.issubset(
                methods
            ), f'Class {cls.__name__} has missing add_url calls'
