import ast
import importlib
import inspect
import os
import textwrap

from integrify.api import APIClient


def get_client_attributes(cls):
    """Return (add_url endpoint names, function names defined under `if TYPE_CHECKING`).

    Client endpoints are registered dynamically via ``self.add_url('<name>')`` and
    only get a real ``def <name>`` as typed ``@overload`` stubs inside the class's
    ``if TYPE_CHECKING:`` block (so editors still autocomplete them). This lets the
    test assert that every registered endpoint has such a stub.
    """
    source = textwrap.dedent(inspect.getsource(cls))
    tree = ast.parse(source)

    add_url_calls: set[str] = set()
    type_checking_funcs: set[str] = set()

    def _is_type_checking(test: ast.expr) -> bool:
        # matches `if TYPE_CHECKING:` and `if typing.TYPE_CHECKING:`
        return (isinstance(test, ast.Name) and test.id == 'TYPE_CHECKING') or (
            isinstance(test, ast.Attribute) and test.attr == 'TYPE_CHECKING'
        )

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call):
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == 'add_url'
                and isinstance(func.value, ast.Name)
                and func.value.id == 'self'
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                add_url_calls.add(node.args[0].value)
            self.generic_visit(node)

        def visit_If(self, node: ast.If):
            if _is_type_checking(node.test):
                for sub in ast.walk(node):
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        type_checking_funcs.add(sub.name)
            self.generic_visit(node)

    Visitor().visit(tree)
    return add_url_calls, type_checking_funcs


def _all_subclasses(cls):
    subs = set()
    for sub in cls.__subclasses__():
        subs.add(sub)
        subs |= _all_subclasses(sub)
    return subs


def import_client_modules():
    """Import every ``integrify.*.client`` module across all installed packages so
    their client classes register as ``APIClient`` subclasses."""
    import integrify

    for base in list(integrify.__path__):
        for root, _dirs, files in os.walk(base):
            if 'client.py' in files:
                rel = os.path.relpath(root, base).replace(os.sep, '.')
                module = 'integrify' + (('.' + rel) if rel != '.' else '') + '.client'
                importlib.import_module(module)


def test_method_definitions():
    import_client_modules()

    clients = _all_subclasses(APIClient)
    assert clients, 'No APIClient subclasses discovered — client modules failed to import.'

    for cls in clients:
        try:
            add_url_calls, type_checking_funcs = get_client_attributes(cls)
        except (OSError, TypeError):
            continue  # no source available (e.g. a dynamically generated class)

        missing = add_url_calls - type_checking_funcs
        assert not missing, (
            f'{cls.__module__}.{cls.__name__}: add_url endpoint(s) without a '
            f'TYPE_CHECKING def stub: {sorted(missing)}'
        )
