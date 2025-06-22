import ctypes
from pathlib import Path


class Surface:
        """High-level wrapper for nvttSurface."""
        def __init__(self, ctx):
            self._lib = ctx._lib
            self._ptr = ctx._lib.nvttCreateSurface()
            self._has_alpha = False
            if not self._ptr:
                raise RuntimeError("Failed to create nvttSurface.")
            
        def __del__(self):
            if getattr(self, '_ptr', None):
                self._lib.nvttDestroySurface(self._ptr)
                
        def load(self, filename: str, expect_signed: bool = False):
            if not Path.exists(Path(filename)):
                raise FileNotFoundError(f"File {filename} does not exist.")
            
            has_alpha = ctypes.c_bool(False)
            result = self._lib.nvttSurfaceLoad(
                self._ptr,
                filename.encode('utf-8'),
                ctypes.byref(has_alpha),
                expect_signed,
                None  # NvttTimingContext, not used here
            )
            if not result:
                raise RuntimeError(f"Failed to load texture from {filename}.")
            self._has_alpha = has_alpha.value
            return self._has_alpha
        
        @property
        def has_alpha(self) -> bool:
            """Check if the surface has an alpha channel."""
            return self._has_alpha
        
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