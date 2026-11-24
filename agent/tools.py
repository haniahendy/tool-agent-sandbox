import ast
import operator

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg}


def calculator(expression: str) -> float:
    """Safely evaluate + - * / ** arithmetic (no eval)."""
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.operand))
        raise ValueError("unsupported expression")
    return ev(ast.parse(expression, mode="eval").body)


def word_count(text: str) -> int:
    return len(text.split())


def lookup(key: str) -> str:
    facts = {"capital_of_egypt": "Cairo", "python_creator": "Guido van Rossum"}
    if key not in facts:
        raise KeyError(f"unknown key: {key}")
    return facts[key]


REGISTRY = {
    "calculator": {"fn": calculator, "args": {"expression": str}},
    "word_count": {"fn": word_count, "args": {"text": str}},
    "lookup": {"fn": lookup, "args": {"key": str}},
}
