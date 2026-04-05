from __future__ import annotations

from pathlib import Path
import subprocess

from slatec.ast import PrintlnStmt, SourceFile


class BackendError(Exception):
    pass


def build_executable(source: SourceFile, output_path: Path, workdir: Path) -> None:
    main_fn = next(fn for fn in source.functions if fn.name == "main")
    parts: list[str] = []
    for stmt in main_fn.body:
        if not isinstance(stmt, PrintlnStmt):
            raise BackendError("only println statements are supported")
        parts.append(stmt.value.value)
    message = "\n".join(parts) + ("\n" if parts else "")
    asm = _emit_asm(message)

    asm_path = workdir / "out.s"
    obj_path = workdir / "out.o"
    asm_path.write_text(asm)

    try:
        subprocess.run(["as", "-o", str(obj_path), str(asm_path)], check=True)
        subprocess.run(["ld", "-o", str(output_path), str(obj_path)], check=True)
    except subprocess.CalledProcessError as exc:
        raise BackendError(f"toolchain failed with exit code {exc.returncode}") from exc


def _emit_asm(message: str) -> str:
    encoded = message.encode("utf-8")
    payload = ", ".join(str(byte) for byte in encoded) if encoded else "0"
    size = len(encoded)
    return f""".global _start

.section .data
message:
    .byte {payload}

.section .text
_start:
    mov $1, %rax
    mov $1, %rdi
    lea message(%rip), %rsi
    mov ${size}, %rdx
    syscall

    mov $60, %rax
    xor %rdi, %rdi
    syscall
"""

