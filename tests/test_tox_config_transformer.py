import pathlib
import sys

src_path = pathlib.Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

import tox_config_transformer  # noqa: E402


def test_tox_pre_post_environments(monkeypatch):
    """Verify tox pre- and post- environment keys are transformed."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "cpython-beta": "3.13",
        "pypys": ["3.10"],
        "tox-pre-environments": ["spin-up"],
        "tox-post-environments": ["spin-down"],
        "cache-key-prefix": "lint",
        "cache-key-hash-files": ["mypy.ini", "requirements/*/requirements.txt"],
        "cache-key-paths": [".mypy_cache"],
    }

    tox_config_transformer.transform_config(config)
    assert "tox-pre-environments" not in config
    assert "tox-post-environments" not in config
    assert config["tox-environments"] == [
        "spin-up",
        "py3.12",
        "py3.13",
        "pypy3.10",
        "spin-down",
    ]


def test_tox_environments(monkeypatch):
    """Verify explicit tox environments are not transformed."""

    config = {
        "runner": "ubuntu-latest",
        "cpythons": ["3.12"],
        "cpython-beta": "3.13",
        "pypys": ["3.10"],
        "tox-environments": ["a", "c", "b"],
    }

    tox_config_transformer.transform_config(config)
    assert "tox-pre-environments" not in config
    assert "tox-post-environments" not in config
    assert config["tox-environments"] == [
        "a",
        "c",
        "b",
    ]
