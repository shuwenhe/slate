from __future__ import annotations

from dataclasses import dataclass


class Expr:
    pass


@dataclass(frozen=True)
class StringLiteral:
    value: str


@dataclass(frozen=True)
class IntLiteral(Expr):
    value: int


@dataclass(frozen=True)
class StringExpr(Expr):
    value: str


@dataclass(frozen=True)
class BinaryExpr(Expr):
    left: Expr
    op: str
    right: Expr


@dataclass(frozen=True)
class PrintlnStmt:
    value: Expr


@dataclass(frozen=True)
class FunctionDecl:
    name: str
    body: list[PrintlnStmt]


@dataclass(frozen=True)
class SourceFile:
    package: str
    functions: list[FunctionDecl]
