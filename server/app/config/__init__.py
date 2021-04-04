import os
import sys
import server.app.config.settings


APP_CONFIG = os.environ.get("APP_CONFIG")
_current = getattr(sys.modules["server.app.config.settings"], f"{APP_CONFIG}Config")

for attr in [f for f in dir(_current) if not "__" in f]:
    # environment can override anything
    val = os.environ.get(attr, getattr(_current, attr))
    setattr(sys.modules[__name__], attr, val)


def config_as_dict():
    config_dict = {}
    for attr in [f for f in dir(_current) if not "__" in f]:
        val = getattr(server.app.config, attr)
        config_dict[attr] = val
    return config_dict
