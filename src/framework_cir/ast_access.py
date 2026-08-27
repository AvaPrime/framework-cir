"""Extract ASSIGN/RETURN observations from Python source.

Separate from bind_structure. Method names are recorded in source_location
only; they are not role labels.
"""

from __future__ import annotations

import ast
from pathlib import Path

from framework_cir.models import Observation


def _expr(node: ast.AST) -> str:
    return ast.unparse(node).replace(" ", "")


def extract_access(source: str, filename: str = "module.py") -> list[Observation]:
    tree = ast.parse(source)
    out: list[Observation] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        owner = node.name
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            loc = f"{filename}:{owner}.{item.name}"
            for stmt in item.body:
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        out.append(
                            Observation("ast_code_match", f"ASSIGN {_expr(target)}", loc)
                        )
                elif isinstance(stmt, ast.Return) and stmt.value is not None:
                    out.append(
                        Observation("ast_code_match", f"RETURN {_expr(stmt.value)}", loc)
                    )
    return out


def extract_file(path: Path) -> list[Observation]:
    return extract_access(path.read_text(), filename=path.name)
