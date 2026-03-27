..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Kurt McKee's GitHub Workflows
#############################

*Reusable workflows that reduce maintenance effort.*

---------------------------------------------------------------------------

This repo centralizes many of my CI workflows.

In many cases, workflows in my other repositories can be minimized
to a set of configuration values and a reference to the workflows here.


Table of contents
=================

*   Workflows

    *   `tox`_
    *   `create-pr`_
    *   `create-tag-and-release`_
    *   `build-python-package`_

*   `Adding new workflows`_


tox
===

`Workflow documentation <docs/tox.rst>`__

The ``tox.yaml`` workflow captures best practices I have found over the years
that optimize test suite execution, including tools, plugins, and caching.

It has the following features:

*   Configurable runners
*   Multiple CPython/PyPy interpreter versions per runner
*   Selectable tox environments
*   Schema validation of the inputs passed to the workflow
*   Fast tox environment creation using the ``tox-uv`` plugin
*   Built-in caching of tox and virtual environments with strong cache-busting


create-pr
=========

`Workflow documentation <docs/create-pr.rst>`__

The ``create-pr.yaml`` workflow cuts release PRs
and automates regular update PRs as needed.

It has the following features:

*   A ``version`` workflow input, suitable for cutting new releases
*   Settings for customizing branches, commits, and PRs
*   Verified commits via the GitHub Actions bot account
*   Schema validation of the inputs passed to the workflow


create-tag-and-release
======================

`Workflow documentation <docs/create-tag-and-release.rst>`__

The ``create-tag-and-release.yaml`` workflow creates a git tag and a GitHub release.

It has the following features:

*   The project version is extracted from ``pyproject.toml``.
*   The version's CHANGELOG entry is extracted using scriv.
*   An annotated git tag named ``v$VERSION`` is created.
    The tag body contains the CHANGELOG entry in GitHub-formatted Markdown.
*   A GitHub release, also named ``v$VERSION``, is created.


build-python-package
====================

`Workflow documentation <docs/build-python-package.rst>`__

The ``build-python-package.yaml`` workflow builds a Python sdist and wheel,
and uploads an artifact containing these.

It has the following features:

*   The project is built using the ``build`` module.
*   An artifact is uploaded to GitHub, suitable for download and publication to PyPI.


Adding new workflows
====================

See the `Adding new workflows <docs/adding-new-workflows.rst>`__ documentation.
