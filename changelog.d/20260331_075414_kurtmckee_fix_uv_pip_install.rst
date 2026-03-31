Fixed
-----

-   Fix ``uv pip install`` invocations to use the ``--prefix`` option.

    Previously, the ``--directory`` option was used,
    which didn't result in e.g. ``.venv/bin/tox`` existing.
