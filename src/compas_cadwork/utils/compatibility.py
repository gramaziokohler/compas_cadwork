from collections.abc import Callable
from typing import Any
from typing import Final
from typing import Literal
from typing import TypeAlias
from typing import TypeVar
from typing import cast

import utility_controller as uc
from typing_extensions import Never


_CadworkVersion: TypeAlias = Literal[2024] | Literal[2025] | Literal[2026]


def _get_cadwork_version() -> _CadworkVersion:
    raw_version = uc.get_3d_version()
    match raw_version:
        case 30:
            return 2024
        case 32:
            return 2025
        case 33:
            return 2026
        case _:
            raise RuntimeError(f"Unsupported Cadwork version {raw_version!r}")


CADWORK_VERSION: Final[_CadworkVersion] = _get_cadwork_version()
"""Version of the Cadwork 3d program in which the library is currently running."""


_T = TypeVar("_T", bound=Callable[..., Any] | property)


def requires_cadwork(min_version: _CadworkVersion) -> Callable[[_T], _T]:
    """Requires minimum Cadwork version.

    Parameters
    ----------
    min_version : _CadworkVersion
        Minimum Cadwork 3d version.

    Returns
    -------
    Callable[[_T], _T]
        Decorator for functions/methods and properties.
    """

    def decorator(target: _T) -> _T:
        if CADWORK_VERSION >= min_version:
            return target

        def wrapper(*args: Any, **kwargs: Any) -> Never:
            raise RuntimeError(f"Requires Cadwork {min_version} or later")

        # Handle properties
        if isinstance(target, property):
            return cast(
                _T,
                property(
                    fget=wrapper if target.fget else None,
                    fset=wrapper if target.fset else None,
                    fdel=wrapper if target.fdel else None,
                ),
            )

        # Handle functions/methods
        return cast(_T, wrapper)

    return decorator
