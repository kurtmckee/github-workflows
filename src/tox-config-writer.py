# This file is a part of Kurt McKee's GitHub Workflows project.
# https://github.com/kurtmckee/github-workflows
# Copyright 2024 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import json
import os
import sys

try:
    config_string = os.environ["inputs_config"]  # KeyError
    config = json.loads(config_string)  # json.JSONDecodeError
    if not isinstance(config, dict):
        raise TypeError
except KeyError:
    print("The 'inputs_config' key wasn't found in the environment")
except json.JSONDecodeError:
    print("The config input couldn't be decoded as valid JSON")
except TypeError:
    print("The config isn't a JSON object")
else:
    with open("config.json", "w") as file:
        file.write(json.dumps(config, sort_keys=True, separators=(",", ":")))
    sys.exit(0)

sys.exit(1)
