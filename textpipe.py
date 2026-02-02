from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Addr:
    """An ed-like line address."""

    number: int | None = None
    regex: str | None = None
    last: bool = False
    delta: int = 0

    @classmethod
    def parse(cls, expr: str) -> tuple[Addr, str]:
        m = re.match(
            r"""(?x)
            ^
            (?:
                (?P<number>\d+)         # line number
                |
                (?P<regex>/[^/]+?/)     # regex
                |
                (?P<last>\$)            # last line
            )?
            (?:
                (?P<delta>[+-]?\d+)     # optional numeric delta
                |
                (?P<plus>[+-]+)         # optional plus/minus delta
            )?
            """,
            expr,
        )
        assert m is not None  # the pattern can match nothing, so it always matches
        addr = cls()
        if m["number"] is not None:
            addr.number = int(m["number"])
        elif m["regex"] is not None:
            addr.regex = m["regex"].strip("/")
        elif m["last"] is not None:
            addr.last = True
        if m["delta"] is not None:
            addr.delta = int(m["delta"])
        elif m["plus"] is not None:
            if len(set(m["plus"])) != 1:
                raise ValueError(f"Invalid address delta: {expr!r}")
            addr.delta = len(m["plus"]) * (1 if m["plus"][0] == "+" else -1)
        return addr, expr[m.end() :]


@dataclass
class Range:
    """A range of lines specified by one or two addresses."""

    start: Addr
    end: Addr | None = None
    from0: bool = True

    @classmethod
    def parse(cls, expr: str) -> Range:
        start, rest = Addr.parse(expr)
        r = Range(start=start)
        if not rest:
            return r
        if rest[0] not in ",;":
            raise ValueError(f"Invalid range: {expr!r}")
        r.from0 = rest[0] == ","
        r.end, rest = Addr.parse(rest[1:])
        if rest:
            raise ValueError(f"Invalid range tail: {rest!r}")
        return r


class TextPipe:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def __str__(self) -> str:
        return "".join(self.lines)

    @classmethod
    def text(cls, text: str) -> TextPipe:
        return cls(text.splitlines(keepends=True))

    @classmethod
    def file(cls, filename: str) -> TextPipe:
        with open(filename) as f:
            return cls(list(f))

    @classmethod
    def cmd(cls, command: str, cwd: str | None = None) -> TextPipe:
        import subprocess

        output = f"$ {command}\n"
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        output += result.stdout
        if result.returncode != 0:
            output += f"(exit code: {result.returncode})\n"
        return cls.text(output)

    def _resolve_addr(self, addr: Addr, start: int) -> int:
        """Return the one-based line index for the given address.
        `start` is the one-based index of the current line, except 0 means
        start from the beginning.
        """
        if addr.number is not None:
            res = addr.number + addr.delta
        elif addr.regex is not None:
            for num, line in enumerate(self.lines[start:], start=start + 1):
                if re.search(addr.regex, line):
                    res = num + addr.delta
                    break
            else:
                raise ValueError(f"Pattern not found: /{addr.regex}/")
        elif addr.last:
            res = len(self.lines) + addr.delta
        else:
            if start == 0:
                start = 1
            res = start + addr.delta
        return res

    def ranges(self, *range_exprs: str) -> TextPipe:
        lines = []
        start = 0
        for range_expr in range_exprs:
            r = Range.parse(range_expr)
            start_idx = self._resolve_addr(r.start, start=start)
            if r.end is None:
                end_idx = start_idx
            else:
                start = 1 if r.from0 else start_idx
                if r.end.number is None and r.end.regex is None and not r.end.last:
                    if r.from0 is True:
                        raise ValueError(f"Invalid range: {range_expr!r}")
                end_idx = self._resolve_addr(r.end, start=start)
            if start_idx > end_idx:
                raise ValueError(f"Invalid range: start {start_idx} > end {end_idx}")
            lines.extend(self.lines[start_idx - 1 : end_idx])
            start = end_idx
        return TextPipe(lines)

    range = ranges

    def __getitem__(self, key: str | tuple[str, ...]) -> TextPipe:
        if isinstance(key, str):
            return self.range(key)
        else:
            return self.ranges(*key)
