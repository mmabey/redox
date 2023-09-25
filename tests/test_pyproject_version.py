# -*- coding: utf-8 -*-
from pathlib import Path

from redox import __version__
from tomlkit import parse


def test_version():
    this_dir = Path(__file__).parent
    with open(this_dir / ".." / "pyproject.toml") as pyproject_file:
        pyproject = parse(pyproject_file.read())

    fail_msg = (
        "It looks like the version in the pyproject.toml file is not the same "
        "as the version in the code. This usually happens when the version was "
        "bumped manually or by running `poetry version patch` directly. The "
        "easiest way to correct this is to revert the change to the version "
        "number in pyproject.toml and then run `pull_request.py --version` "
        "from the gen_redox_lib tool."
    )

    assert pyproject["tool"]["poetry"]["version"] == __version__, fail_msg
