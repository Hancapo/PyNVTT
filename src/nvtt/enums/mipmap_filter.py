from enum import IntEnum

class MipmapFilter(IntEnum):
    """Enum for mipmap filter modes used in mipmap generation."""
    BOX = 0
    TRIANGLE = 1
    KAISER = 2
    MITCHELL = 3
    MIN = 4
    MAX = 5