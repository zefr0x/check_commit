"""Tests for `check_msg` fucntion."""

import pytest  # noqa: F401

from check_commit import check_msg

TYPES = ["feat", "fix", "refac"]
FOTTER_TYPES = ["Closes", "Fixes", "Refs"]


def test_header() -> None:
    """Test for header with commit type, scope, and description."""
    assert check_msg(74, TYPES, FOTTER_TYPES, "feat(ui): add new button") == 0
    assert check_msg(74, TYPES, FOTTER_TYPES, "refac(api)!: deprecate `get_name`") == 0
    assert check_msg(74, TYPES, FOTTER_TYPES, "refac(core/api)!: deprecate `get_name`") == 0
    assert check_msg(74, TYPES, FOTTER_TYPES, "refac(`ui`)!: remove button") == 1  # Invalid "`" char in the scope
    assert check_msg(74, TYPES, FOTTER_TYPES, "refac: clean old files") == 0
    assert check_msg(74, TYPES, FOTTER_TYPES, "chore: clean old files") == 1  # Invalid type
    assert check_msg(74, TYPES, FOTTER_TYPES, "clean old files") == 1  # No type


def test_commit_with_body() -> None:
    """Test for commit message with body when expected."""
    assert check_msg(74, TYPES, FOTTER_TYPES, "feat: add new button\n\nThis is the body of the commit.") == 0

    # Multi part body
    assert (
        check_msg(
            74,
            TYPES,
            FOTTER_TYPES,
            "fix(ui): correct button color"
            "\n\nThis fixes the issue with the button color,\nbut jsut for the Linux platform."
            "\n\nThe color was broken in dark theme.",
        )
        == 0
    )

    assert check_msg(74, TYPES, FOTTER_TYPES, "feat(ui): add new button\n\n") == 1  # Missing body
    assert check_msg(74, TYPES, FOTTER_TYPES, "fix(ui): correct button color\n\n\n") == 1  # Missing body


def test_commit_with_body_and_footer() -> None:
    """Test for valid commit message with body and footer."""
    assert (
        check_msg(
            74,
            TYPES,
            FOTTER_TYPES,
            "feat: add new button\n\nThis is the body of the commit.\n\nFixes: #83,#59",
        )
        == 0
    )
    assert (
        check_msg(
            74,
            TYPES,
            FOTTER_TYPES,
            "fix(ui): correct button color in dark theme"
            "\n\nThis fixes the issue with the button color."
            "\n\nRefs: 8cbe59a,746c3d7",
        )
        == 0
    )

    # Multi part body with footer
    assert (
        check_msg(
            74,
            TYPES,
            FOTTER_TYPES,
            "fix(ui): correct button color"
            "\n\nThis fixes the issue with the button color,\nbut jsut for the Linux platform."
            "\n\nThe color was broken in dark theme."
            "\n\nRefs: 8cbe59a,746c3d7",
        )
        == 0
    )


def test_commit_with_only_footer() -> None:
    """Test for commit message with footer but no body."""
    assert check_msg(74, TYPES, FOTTER_TYPES, "feat(ui): add new button\n\nFixes: #83,#59\nRefs: #123") == 0
    assert check_msg(74, TYPES, FOTTER_TYPES, "fix(api): correct button color\n\nRefs: #123\nFixes: #83,#59") == 0

    # Invalid footer type, but parsed greedily without issues as a body
    assert check_msg(74, TYPES, FOTTER_TYPES, "fix(api): correct button color\n\nFix: #123") == 0

    # Invalid footer type after a valid one is not parsed as a body
    assert check_msg(74, TYPES, FOTTER_TYPES, "fix(api): correct button color\n\nFixes: #83,#59\nRelated: #123") == 1


def test_valid_commit_with_long_line() -> None:
    """Test for valid commit message with a long line."""
    long_line = "This is a long body of the commit message with details about the changes made in this commit."
    assert check_msg(74, TYPES, FOTTER_TYPES, f"feat: add new button\n\n{long_line}") == 1
    assert check_msg(74, TYPES, FOTTER_TYPES, f"feat: add new button\n\n{long_line[:74]}\n{long_line[74:]}") == 0

    assert check_msg(98, TYPES, FOTTER_TYPES, f"feat: {long_line}") == 1
    assert check_msg(99, TYPES, FOTTER_TYPES, f"feat: {long_line}") == 0


def test_empty_commit_message() -> None:
    """Test for completely empty commit message."""
    assert check_msg(74, TYPES, FOTTER_TYPES, "") == 1
    assert check_msg(74, TYPES, FOTTER_TYPES, "\n") == 1
    assert check_msg(74, TYPES, FOTTER_TYPES, "\n\n") == 1
    assert check_msg(74, TYPES, FOTTER_TYPES, "\n\n\n") == 1
