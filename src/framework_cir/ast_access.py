"""Extract access observations from Python source.

Facts are typed. AugAssign is not ASSIGN. setattr is not ASSIGN.
Binding is a later pass; this module only represents.
"""

from __future__ import annotations

import ast
from pathlib import Path

from framework_cir.models import Observation


def _expr(node: ast.AST) -> str:
    return ast.unparse(node).replace(" ", "")


def _from_stmt(stmt: ast.AST, loc: str) -> list[Observation]:
    out: list[Observation] = []
    if isinstance(stmt, ast.AugAssign):
        out.append(Observation("ast_code_match", f"AUG_ASSIGN {_expr(stmt.target)}", loc))
    elif isinstance(stmt, ast.Assign):
        for target in stmt.targets:
            out.append(Observation("ast_code_match", f"ASSIGN {_expr(target)}", loc))
    elif isinstance(stmt, ast.Return) and stmt.value is not None:
        out.append(Observation("ast_code_match", f"RETURN {_expr(stmt.value)}", loc))
    elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        call = stmt.value
        if isinstance(call.func, ast.Name) and call.func.id == "setattr" and len(call.args) >= 2:
            out.append(
                Observation(
                    "ast_code_match",
                    f"SETATTR {_expr(call.args[0])}.{_expr(call.args[1])}",
                    loc,
                )
            )
    return out


def extract_access(source: str, filename: str = "module.py") -> list[Observation]:
    tree = ast.parse(source)
    out: list[Observation] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            loc = f"{filename}:{node.name}.{item.name}"
            for stmt in item.body:
                out.extend(_from_stmt(stmt, loc))
    return out


def extract_file(path: Path) -> list[Observation]:
    return extract_access(path.read_text(), filename=path.name)


def kinds(obs: list[Observation]) -> set[str]:
    return {o.detail.split()[0] for o in obs if o.detail}
