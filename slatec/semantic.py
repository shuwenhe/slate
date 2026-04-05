from __future__ import annotations

from slatec.ast import (
    AssignStmt,
    BinaryExpr,
    ForStmt,
    FunctionDecl,
    IntLiteral,
    LetStmt,
    NameExpr,
    PrintlnStmt,
    RangeExpr,
    SourceFile,
    StringExpr,
)


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
    env: set[str] = set()
    for stmt in fn.body:
        _check_stmt(stmt, env)

def _check_stmt(stmt, env: set[str]) -> None:
    if isinstance(stmt, PrintlnStmt):
        _check_expr(stmt.value, env)
        return
    if isinstance(stmt, LetStmt):
        _check_expr(stmt.value, env)
        env.add(stmt.name)
        return
    if isinstance(stmt, AssignStmt):
        if stmt.name not in env:
            raise SemanticError(f"assignment to undefined name {stmt.name}")
        _check_expr(stmt.value, env)
        return
    if isinstance(stmt, ForStmt):
        _check_range(stmt.iterable, env)
        body_env = set(env)
        body_env.add(stmt.name)
        for item in stmt.body:
            _check_stmt(item, body_env)
        return
    raise SemanticError("unsupported statement")


def _check_expr(expr, env: set[str]) -> str:
    if isinstance(expr, IntLiteral):
        return "int"
    if isinstance(expr, StringExpr):
        return "string"
    if isinstance(expr, NameExpr):
        if expr.name not in env:
            raise SemanticError(f"undefined name {expr.name}")
        return "int"
    if isinstance(expr, BinaryExpr):
        left = _check_expr(expr.left, env)
        right = _check_expr(expr.right, env)
        if expr.op != "+":
            raise SemanticError(f"unsupported operator {expr.op}")
        if left != "int" or right != "int":
            raise SemanticError("only integer addition is supported in MVP")
        return "int"
    raise SemanticError("unsupported expression")


def _check_range(expr: RangeExpr, env: set[str]) -> None:
    left = _check_expr(expr.start, env)
    right = _check_expr(expr.end, env)
    if left != "int" or right != "int":
        raise SemanticError("for range must use integer bounds")
