# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import pytest

from workflow_assets.create_pr import compute_versioned_variables

DEFAULT_BRANCH_NAME = "DEFAULT_BRANCH"
DEFAULT_PR_TITLE = "DEFAULT_TITLE"
VERSION = "1.2.3"


@pytest.fixture(scope="module", autouse=True)
def default_variables():
    m = pytest.MonkeyPatch()
    m.setenv("GITHUB_ENV", "output.txt")
    m.setenv("VERSION", VERSION)
    m.setenv("DEFAULT_BRANCH_NAME", DEFAULT_BRANCH_NAME)
    m.setenv("DEFAULT_PR_TITLE", DEFAULT_PR_TITLE)
    # These will be replaced by the specific tests.
    m.setenv("BRANCH_NAME", "bogus")
    m.setenv("PR_TITLE", "bogus")


@pytest.mark.parametrize(
    "branch_name, expected_branch_name",
    (
        ("updates", "updates"),
        ("release/$VERSION", f"release/{VERSION}"),
        ("", DEFAULT_BRANCH_NAME),
    ),
)
def test_compute_branch_name(monkeypatch, fs, branch_name, expected_branch_name):
    monkeypatch.setenv("BRANCH_NAME", branch_name)

    assert compute_versioned_variables.main() == 0

    with open("output.txt") as file:
        lines = file.readlines()

    assert f"COMPUTED_BRANCH_NAME={expected_branch_name}\n" in lines


@pytest.mark.parametrize(
    "pr_title, expected_pr_title",
    (
        ("Updates", "Updates"),
        ("Update metadata for $VERSION", f"Update metadata for {VERSION}"),
        ("", DEFAULT_PR_TITLE),
    ),
)
def test_compute_pr_title(monkeypatch, fs, pr_title, expected_pr_title):
    monkeypatch.setenv("PR_TITLE", pr_title)

    assert compute_versioned_variables.main() == 0

    with open("output.txt") as file:
        lines = file.readlines()

    assert f"COMPUTED_PR_TITLE={expected_pr_title}\n" in lines
