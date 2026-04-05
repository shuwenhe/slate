from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StringLiteral:
    value: str


@dataclass(frozen=True)
class PrintlnStmt:
    value: StringLiteral


@dataclass(frozen=True)
class FunctionDecl:
    name: str
    body: list[PrintlnStmt]


@dataclass(frozen=True)
class SourceFile:
    package: str
    functions: list[FunctionDecl]

