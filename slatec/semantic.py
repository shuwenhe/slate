from __future__ import annotations

from slatec.ast import FunctionDecl, PrintlnStmt, SourceFile


class SemanticError(Exception):
    pass


def check(source: SourceFile) -> None:
    if source.package != "main":
        raise SemanticError("hello-world MVP requires `package main`")

    mains = [fn for fn in source.functions if fn.name == "main"]
    if not mains:
        raise SemanticError("entry function `main` not found")
    if len(mains) > 1:
        raise SemanticError("multiple `main` functions found")

    for fn in source.functions:
        _check_function(fn)


def _check_function(fn: FunctionDecl) -> None:
    for stmt in fn.body:
        if not isinstance(stmt, PrintlnStmt):
            raise SemanticError(f"unsupported statement in {fn.name}")

