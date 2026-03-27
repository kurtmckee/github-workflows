# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import os
import sys

RC_SUCCESS = 0
RC_FAILURE = 1

mandatory_environment_variables = {
    "BRANCH_NAME",
    "DEFAULT_BRANCH_NAME",
    "GITHUB_ENV",
    "VERSION",
}


def main() -> int:
    # Ensure mandatory environment variables are present.
    if missing_keys := (mandatory_environment_variables - os.environ.keys()):
        for missing_key in missing_keys:
            print(f"`{missing_key}` is a mandatory environment variable.")
        return RC_FAILURE

    branch_name = os.environ["BRANCH_NAME"]
    if branch_name:
        version = os.environ["VERSION"]
        computed_branch_name = branch_name.replace("$VERSION", version)
    else:
        computed_branch_name = os.environ["DEFAULT_BRANCH_NAME"]

    with open(os.environ["GITHUB_ENV"], "a") as file:
        file.write(f"COMPUTED_BRANCH_NAME={computed_branch_name}\n")

    return RC_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
