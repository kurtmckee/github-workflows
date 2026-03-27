# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pytest

from workflow_assets.create_pr import compute_branch_name


@pytest.mark.parametrize(
    "branch_name, default_branch_name, expected_branch_name",
    (
        ("updates", "default", "updates"),
        ("", "default", "default"),
        ("release/$VERSION", "default", "release/1.2.3"),
    ),
)
def test_compute_branch_name(
    monkeypatch, fs, branch_name, default_branch_name, expected_branch_name
):
    monkeypatch.setenv("BRANCH_NAME", branch_name)
    monkeypatch.setenv("DEFAULT_BRANCH_NAME", default_branch_name)
    monkeypatch.setenv("GITHUB_ENV", "output.txt")
    monkeypatch.setenv("VERSION", "1.2.3")

    assert compute_branch_name.main() == 0

    with open("output.txt") as file:
        assert file.read() == f"COMPUTED_BRANCH_NAME={expected_branch_name}\n"
