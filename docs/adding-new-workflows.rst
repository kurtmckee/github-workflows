..
    This file is a part of Kurt McKee's GitHub Workflows project.
    https://github.com/kurtmckee/github-workflows
    Copyright 2024-2026 Kurt McKee <contactme@kurtmckee.org>
    SPDX-License-Identifier: MIT


Adding new workflows
####################

Adding a new workflow requires some specific knowledge.


Workflow filename
=================

If the workflow has no need for templating, use a memorable name.

If templating is needed, use a filename that ends with ``.jinja.yaml``.


Permissions
===========

Permissions must be explicitly set, even if only defaults are needed.

These are the GitHub defaults:

..  code-block:: yaml

    permissions:
      contents: "read"


Jinja settings
==============

The default Jinja settings conflict with GitHub's ``${{ }}`` workflow syntax.

Therefore, these are the settings used when rendering workflow templates:

=============================== ===========================
Setting                         Value
=============================== ===========================
``block_start_string``          ``[%``
``block_end_string``            ``%]``
``variable_start_string``       ``[[``
``variable_end_string``         ``]]``
``comment_start_string``        ``#[#``
``comment_end_string``          ``#]#``
=============================== ===========================


Template variables
==================

Several template variables are available:

*   ``PYTHON_VERSION`` (read from ``pyproject.toml``)
*   ``UV_VERSION`` (read from ``requirements/uv/requirements.txt``)

These can be used to help lock dependencies and increase predictability.
For example, these can be used when using actions:

..  code-block:: yaml

    - name: "Setup Python"
      uses: "actions/setup-python@<SHA>" # <VERSION>
      with:
        python-version: "[[ PYTHON_VERSION ]]"

    - name: "Install uv"
      uses: "astral-sh/setup-uv@<SHA>" # <VERSION>
      with:
        version: "[[ UV_VERSION ]]"


Template functions
==================

Several template functions are available.


``include_requirements(directory: str)``
----------------------------------------

The ``directory`` given must exist in this repo's ``requirements/`` directory.
The constructed path to the ``requirements.txt`` file will be:

..  code-block:: text

    requirements/$DIRECTORY/requirements.txt

This is useful for locking dependencies to ensure consistent runtime behavior:

..  code-block:: yaml

    env:
      REQUIREMENTS: |
        [[ include_requirements("my_cool_package") | indent(4) ]]

    jobs:
      example:
        steps:

          # ...

          - run: |
              REQUIREMENTS_PATH="$(mktemp)"
              echo "${REQUIREMENTS}" > "${REQUIREMENTS_PATH}"

              uv run \
                --no-managed-python \
                --no-project \
                --with-requirements="${REQUIREMENTS_PATH}" \
                my_cool_package_cli


``include_file(file: str)``
---------------------------

The ``file`` must exist in a subdirectory in ``src/workflow_assets/``
that matches the normalized name of the workflow name.

For example, if the workflow filename is ``do-something.jinja.yaml``,
then the corresponding directory in ``src/workflow_assets/``
must be named ``do_something/``.

This is useful for keeping a file outside of the workflow itself
so that it can be linted and checked by standard tools.

Examples of JSON schemas and Python code exist in the ``tox.jinja.yaml``.


Block templates as runnable workflows
=====================================

Templates must be stored in the ``.github/workflows/`` directory
so that Dependabot can update the action versions authoritatively in the templates.

However, it's not desirable for the templates workflows to be runnable,
so use boilerplate like this to prevent execution of the workflows:

..  code-block:: yaml

    jobs:
      #[#-
      # Halt execution if an attempt is made to run the template directly.
      # This block is enclosed in a Jinja comment and will not be rendered.
      halt:
        name: "Halt"
        runs-on: "ubuntu-slim"
        steps:
          - name: "Halt"
            run: |
              echo "::error::⚠️ Do not run the workflow template directly."
              exit 1
      #]#

Then, add the boilerplate just after the key of the real job,
which will force the real job *in the template* to depend on the ``halt`` job:

..  code-block:: yaml

    real_job:
      #[#-
      # The `needs` key is in a Jinja comment and will not be rendered.
      needs: ["halt"]
      #]#

This ensures that the template workflow cannot be used by a calling workflow.


Disable template workflows
==========================

After the new workflow merges, disable the workflow in this repository.
This helps keeps focus on runnable actions in the Actions sidebar.

Go to the Actions tab in the repo, click on the workflow,
and then in the ``...`` menu on the right of the page,
select "Disable workflow".
