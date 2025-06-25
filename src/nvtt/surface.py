import ctypes
from pathlib import Path
from .enums import MipmapFilter, WrapMode, AlphaMode
from .core import nvtt


class Surface:
    """High-level wrapper for nvttSurface."""

    def __init__(self, filepath: str = None):
        self._lib = nvtt._lib
        self._ptr = nvtt._lib.nvttCreateSurface()
        self._has_alpha = None
        if not self._ptr:
            raise RuntimeError("Failed to create nvttSurface.")
        self.load(filepath) if filepath else None

    def __del__(self):
        if getattr(self, "_ptr", None):
            self._lib.nvttDestroySurface(self._ptr)

    def clone(self) -> "Surface":
        "Clone the current surface to a new one."
        new_ptr = self._lib.nvttSurfaceClone(self._ptr)
        if not new_ptr:
            raise RuntimeError("nvttSurfaceClone error")
        surf: Surface = Surface()
        surf._ptr = new_ptr
        return surf

    @property
    def width(self) -> int:
        """Get the width of the surface."""
        return self._lib.nvttSurfaceWidth(self._ptr)

    @property
    def height(self) -> int:
        """Get the height of the surface."""
        return self._lib.nvttSurfaceHeight(self._ptr)

    @property
    def depth(self) -> int:
        """Get the depth of the surface."""
        return self._lib.nvttSurfaceDepth(self._ptr)
    
    @property
    def wrap_mode(self) -> WrapMode:
        """Get the wrap mode of the surface."""
        return WrapMode(self._lib.nvttSurfaceWrapMode(self._ptr))
    
    @wrap_mode.setter
    def wrap_mode(self, value: WrapMode) -> None:
        """Set the wrap mode of the surface."""
        if not isinstance(value, WrapMode):
            raise TypeError("value must be WrapMode")
        self._lib.nvttSetSurfaceWrapMode(self._ptr, int(value))
        
    @property
    def alpha_mode(self) -> AlphaMode:
        """Get the alpha mode of the surface."""
        return AlphaMode(self._lib.nvttSurfaceAlphaMode(self._ptr))
    
    @property
    def normal_map(self) -> bool:
        """Check if the surface is a normal map."""
        return bool(self._lib.nvttSurfaceIsNormalMap(self._ptr))
    
    @normal_map.setter
    def normal_map(self, value: bool) -> None:
        """Set the surface as a normal map."""
        if not isinstance(value, bool):
            raise TypeError("value must be bool")
        self._lib.nvttSetSurfaceNormalMap(self._ptr, value)
    
    @alpha_mode.setter
    def alpha_mode(self, value: AlphaMode) -> None:
        """Set the alpha mode of the surface."""
        if not isinstance(value, AlphaMode):
            raise TypeError("value must be AlphaMode")
        self._lib.nvttSetSurfaceAlphaMode(self._ptr, int(value))

    def count_mipmaps(self, min_size: int = 1) -> int:
        """Count the number of mipmaps in the surface."""
        return self._lib.nvttSurfaceCountMipmaps(self._ptr, min_size)

    def load(self, filename: str, expect_signed: bool = False) -> bool:
        if not Path.exists(Path(filename)):
            raise FileNotFoundError(f"File {filename} does not exist.")

        has_alpha = ctypes.c_bool(False)
        result = self._lib.nvttSurfaceLoad(
            self._ptr,
            filename.encode("utf-8"),
            ctypes.byref(has_alpha),
            expect_signed,
            None,
        )
        if not result:
            raise RuntimeError(f"Failed to load texture from {filename}.")
        self._has_alpha = has_alpha.value
        return self._has_alpha

    def build_next_mipmap(self, filter: MipmapFilter, min_size: int = 1) -> bool:
        """Build the next mipmap level."""
        if not self._ptr:
            raise RuntimeError("Surface has already been destroyed or not initialized.")
        return self._lib.nvttSurfaceBuildNextMipmapDefaults(
            self._ptr, int(filter), min_size, None
        )

    @property
    def has_alpha(self) -> bool:
        """Check if the surface has an alpha channel."""
        if self._has_alpha is None:
            raise RuntimeError("Surface has not been loaded or has been destroyed.")
        return self._has_alpha
