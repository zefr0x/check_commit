"""Linter for git commit messages with the Conventional Commits standard."""

import logging
import re
import sys
from collections.abc import Generator, Sequence
from pathlib import Path

logging.basicConfig(level=logging.INFO)

log = logging.getLogger("check-commit")


def check_msg(max_line_width: int, commit_types: Sequence, footer_types: Sequence, msg: str) -> int:
    """Return 0 when the message is valid, and return 1 when it is not."""
    commit_pattern = re.compile(
        r"\A"
        rf"^(?P<type>{'|'.join(commit_types)})(?:\((?P<scope>[-\w/]+)\))?(?P<breaking>!)?: "
        r"(?P<description>.+)$"
        rf"(?P<body>\n(?:(?:\n^$\n|\n)^(?!{'|'.join(footer_types)}: ).+$)+)?"
        rf"(?P<footer>\n(?:(?:\n^$\n|\n)^(?:{'|'.join(footer_types)}): .+$)+)?"
        r"\Z",
        re.MULTILINE,
    )

    match = commit_pattern.match(msg)

    if match:
        log.info(match.groupdict())
        for i, line in enumerate(msg.splitlines(keepends=False)):
            if len(line) > max_line_width:
                log.error("Error: line %d is longer than %d characters", i, max_line_width)
                return 1

        return 0
    log.error("your commit message is broken, go read the docs and the Conventional Commits standard")
    return 1


def filter_lines(lines: Sequence[str]) -> Generator[str]:
    """Filter lines starting with # in a commit message."""
    for line in lines:
        if not line.startswith("#"):
            yield line


def main() -> int:
    """Entery point of the script."""
    max_line_width = int(sys.argv[1])
    commit_types = sys.argv[2].split(",")
    footer_types = sys.argv[3].split(",")

    try:
        commit_msg_file = sys.argv[4]
    except IndexError:
        commit_msg = sys.stdin.readlines()
    else:
        with Path.open(commit_msg_file) as f:
            commit_msg = f.readlines()

    return check_msg(max_line_width, commit_types, footer_types, "".join(filter_lines(commit_msg)).strip())
