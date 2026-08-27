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


def _walk_fn(owner: str, fn: ast.FunctionDef, filename: str) -> list[Observation]:
    loc = f"{filename}:{owner}.{fn.name}"
    out: list[Observation] = []
    for stmt in ast.walk(fn):
        if isinstance(stmt, ast.AugAssign):
            out.append(Observation("ast_code_match", f"AUG_ASSIGN {_expr(stmt.target)}", loc))
        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                out.append(Observation("ast_code_match", f"ASSIGN {_expr(target)}", loc))
        elif isinstance(stmt, ast.Return) and stmt.value is not None:
            out.append(Observation("ast_code_match", f"RETURN {_expr(stmt.value)}", loc))
        elif isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Name) and stmt.func.id == "setattr":
            if len(stmt.args) >= 2:
                out.append(
                    Observation(
                        "ast_code_match",
                        f"SETATTR {_expr(stmt.args[0])}.{_expr(stmt.args[1])}",
                        loc,
                    )
                )
        elif isinstance(stmt, ast.Subscript) and isinstance(stmt.ctx, ast.Store):
            out.append(Observation("ast_code_match", f"INDEX_WRITE {_expr(stmt)}", loc))
        elif isinstance(stmt, ast.Attribute) and isinstance(stmt.ctx, ast.Store):
            out.append(Observation("ast_code_match", f"ATTR_WRITE {_expr(stmt)}", loc))
    return out


def extract_access(source: str, filename: str = "module.py") -> list[Observation]:
    tree = ast.parse(source)
    out: list[Observation] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                out.extend(_walk_fn(node.name, item, filename))
    return out


def extract_file(path: Path) -> list[Observation]:
    return extract_access(path.read_text(), filename=path.name)


def kinds(obs: list[Observation]) -> set[str]:
    return {o.detail.split()[0] for o in obs if o.detail}
