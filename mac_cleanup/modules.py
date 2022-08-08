from typing import Optional

from mac_cleanup.utils import _function
from inspect import getmembers, isfunction


def load_default(
) -> dict[str, _function]:
    """
    Loads the default modules

    Returns:
        Dict w/ the module name and the module function respectively
    """
    import mac_cleanup.default_modules as default_modules

    return dict(getmembers(default_modules, isfunction))


def load_custom(
        custom_path: Optional[str],
) -> dict[str, _function]:
    """
    Loads the custom modules from the given path

    Args:
        custom_path: Path to the custom module directory
    Returns:
        Dict w/ the module name and the module function respectively
    """
    if not custom_path:
        return dict()

    from importlib.machinery import SourceFileLoader
    from pathlib import Path

    custom_modules = dict()
    # Imports all modules from the given path
    for module in Path(custom_path).expanduser().rglob("*"):
        # Duplicates will be overwritten
        custom_modules.update(
            dict(
                getmembers(
                    SourceFileLoader(
                        module.name.split(".py")[0],
                        module.as_posix(),
                    ).load_module(),
                    isfunction
                )
            )
        )
    return custom_modules
