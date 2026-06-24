from functools import cached_property
from typing import ClassVar
from uuid import UUID


class IfcUUID(UUID):
    """A special UUID class that supports encoding to IFC Base64-compressed GUIDs.

    See https://technical.buildingsmart.org/resources/ifcimplementationguidance/ifc-guid/ for more information.
    """

    _ALPHABET: ClassVar[str] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$"

    @cached_property
    def base64(self) -> str:
        """Base64-compressed representation of the IFC GUID."""
        a = self._ALPHABET
        b = self.bytes
        v0 = b[0]
        chars = [a[(v0 >> 6) & 0x3F], a[v0 & 0x3F]]
        for i in range(1, 16, 3):
            v = (b[i] << 16) | (b[i + 1] << 8) | b[i + 2]
            chars.extend((a[(v >> 18) & 0x3F], a[(v >> 12) & 0x3F], a[(v >> 6) & 0x3F], a[v & 0x3F]))
        return "".join(chars)
