import pytest

from compas_cadwork.utils.compatibility import _get_cadwork_version
from compas_cadwork.utils.compatibility import requires_cadwork


def make_gated_class():
    class GatedClass:
        @property
        def property_supported_always(self) -> int:
            return 123

        @property_supported_always.setter
        def property_supported_always(self, value: int) -> None: ...

        @property
        @requires_cadwork(2025)
        def property_supported_since_2025(self) -> int:
            return 123

        @property_supported_since_2025.setter
        @requires_cadwork(2025)
        def property_supported_since_2025(self, value: int) -> None: ...

        @property
        @requires_cadwork(2026)
        def property_supported_since_2026(self) -> int:
            return 123

        @property_supported_since_2026.setter
        @requires_cadwork(2026)
        def property_supported_since_2026(self, value: int) -> None: ...

        def method_supported_always(self) -> str:
            return "abc"

        @requires_cadwork(2025)
        def method_supported_since_2025(self) -> str:
            return "abc"

        @requires_cadwork(2026)
        def method_supported_since_2026(self) -> str:
            return "abc"

    return GatedClass()


def test_gets_cadwork_version(cadwork) -> None:
    cadwork.uc.get_3d_version.return_value = 30
    assert _get_cadwork_version() == 2024
    cadwork.uc.get_3d_version.return_value = 32
    assert _get_cadwork_version() == 2025
    cadwork.uc.get_3d_version.return_value = 33
    assert _get_cadwork_version() == 2026


def test_raises_on_unsupported_cadwork_version(cadwork) -> None:
    cadwork.uc.get_3d_version.return_value = 9999
    with pytest.raises(RuntimeError, match=r"Unsupported Cadwork version 9999"):
        _ = _get_cadwork_version()


def test_requires_cadwork_decorator_works_on_methods(set_cadwork_version) -> None:
    # Running on Cadwork 2026
    set_cadwork_version(2026)
    instance = make_gated_class()
    assert instance.method_supported_always() == "abc"
    assert instance.method_supported_since_2025() == "abc"
    assert instance.method_supported_since_2026() == "abc"

    # Running on Cadwork 2025
    set_cadwork_version(2025)
    instance = make_gated_class()
    assert instance.method_supported_always() == "abc"
    assert instance.method_supported_since_2025() == "abc"
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2026 or later"):
        _ = instance.method_supported_since_2026()

    # Running on Cadwork 2024
    set_cadwork_version(2024)
    instance = make_gated_class()
    assert instance.method_supported_always() == "abc"
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2025 or later"):
        _ = instance.method_supported_since_2025()
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2026 or later"):
        _ = instance.method_supported_since_2026()


def test_requires_cadwork_can_decorate_properties_with_functions(set_cadwork_version) -> None:
    # Running on Cadwork 2026
    set_cadwork_version(2026)
    instance = make_gated_class()
    assert instance.property_supported_always == 123
    assert instance.property_supported_since_2025 == 123
    assert instance.property_supported_since_2026 == 123
    instance.property_supported_always = 321
    instance.property_supported_since_2025 = 321
    instance.property_supported_since_2026 = 321

    # Running on Cadwork 2025
    set_cadwork_version(2025)
    instance = make_gated_class()
    assert instance.property_supported_always == 123
    assert instance.property_supported_since_2025 == 123
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2026 or later"):
        _ = instance.property_supported_since_2026
    instance.property_supported_always = 321
    instance.property_supported_since_2025 = 321
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2026 or later"):
        instance.property_supported_since_2026 = 321

    # Running on Cadwork 2024
    set_cadwork_version(2024)
    instance = make_gated_class()
    assert instance.property_supported_always == 123
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2025 or later"):
        _ = instance.property_supported_since_2025
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2026 or later"):
        _ = instance.property_supported_since_2026
    instance.property_supported_always = 321
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2025 or later"):
        instance.property_supported_since_2025 = 321
    with pytest.raises(RuntimeError, match=r"Requires Cadwork 2026 or later"):
        instance.property_supported_since_2026 = 321
