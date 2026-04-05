from __future__ import annotations

from dataclasses import dataclass

from slatec.ast import FunctionDecl, PrintlnStmt, SourceFile, StringLiteral
from slatec.lexer import Token


class ParseError(Exception):
    pass


@dataclass
class Parser:
    tokens: list[Token]

    def __post_init__(self) -> None:
        self.index = 0

    def parse(self) -> SourceFile:
        self._expect_keyword("package")
        package = self._expect("ident").value
        functions: list[FunctionDecl] = []
        while not self._at("eof"):
            functions.append(self._parse_function())
        return SourceFile(package=package, functions=functions)

    def _parse_function(self) -> FunctionDecl:
        self._expect_keyword("func")
        name = self._expect("ident").value
        self._expect_symbol("(")
        self._expect_symbol(")")
        self._expect_symbol("{")
        body: list[PrintlnStmt] = []
        while not self._eat_symbol("}"):
            body.append(self._parse_stmt())
        return FunctionDecl(name=name, body=body)

    def _parse_stmt(self) -> PrintlnStmt:
        callee = self._expect("ident").value
        if callee != "println":
            raise self._error("only println(...) is supported in MVP")
        self._expect_symbol("(")
        value = self._expect("string").value
        self._expect_symbol(")")
        return PrintlnStmt(StringLiteral(value))

    def _at(self, kind: str) -> bool:
        return self.tokens[self.index].kind == kind

    def _eat_symbol(self, value: str) -> bool:
        token = self.tokens[self.index]
        if token.kind == "symbol" and token.value == value:
            self.index += 1
            return True
        return False

    def _expect_symbol(self, value: str) -> Token:
        token = self.tokens[self.index]
        if token.kind == "symbol" and token.value == value:
            self.index += 1
            return token
        raise self._error(f"expected symbol {value!r}")

    def _expect_keyword(self, value: str) -> Token:
        token = self.tokens[self.index]
        if token.kind == "keyword" and token.value == value:
            self.index += 1
            return token
        raise self._error(f"expected keyword {value!r}")

    def _expect(self, kind: str) -> Token:
        token = self.tokens[self.index]
        if token.kind == kind:
            self.index += 1
            return token
        raise self._error(f"expected {kind}")

    def _error(self, message: str) -> ParseError:
        token = self.tokens[self.index]
        return ParseError(f"{message} at {token.line}:{token.column}")

