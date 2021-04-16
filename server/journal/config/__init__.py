import os
import sys
import server.journal.config.settings


APP_CONFIG = os.environ.get("APP_CONFIG", "Development")
_current = getattr(sys.modules["server.journal.config.settings"], f"{APP_CONFIG}Config")()

for atr in [f for f in dir(_current) if not "__" in f]:
    # environment can override anything
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)


def _as_dict():
    config_dict = {}
    module = getattr(sys.modules["server.journal.config"])
    for atr in [f for f in dir(module) if not "__" in f]:
        val = getattr(server.journal.config, atr)
        config_dict[atr] = val
    return config_dict