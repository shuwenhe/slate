from __future__ import annotations

from slatec.ast import BinaryExpr, FunctionDecl, IntLiteral, PrintlnStmt, SourceFile, StringExpr


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
        _check_expr(stmt.value)


def _check_expr(expr) -> str:
    if isinstance(expr, IntLiteral):
        return "int"
    if isinstance(expr, StringExpr):
        return "string"
    if isinstance(expr, BinaryExpr):
        left = _check_expr(expr.left)
        right = _check_expr(expr.right)
        if expr.op != "+":
            raise SemanticError(f"unsupported operator {expr.op}")
        if left != "int" or right != "int":
            raise SemanticError("only integer addition is supported in MVP")
        return "int"
    raise SemanticError("unsupported expression")
