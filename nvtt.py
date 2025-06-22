import ctypes
from pathlib import Path


LIBRARY_PATH = Path(Path(__file__).parent) / "libs"

NVTT_DLL_NAME: str = "nvtt30205.dll"

class NVTT:
    """Wrapper for the NVIDIA Texture Tools (nvtt) library."""
    def __init__(self, dll_path: str = str(Path.joinpath(LIBRARY_PATH, NVTT_DLL_NAME)) ):
        self._lib = ctypes.CDLL(dll_path)
        self._version: int = 0
        
        class NvttSurface(ctypes.Structure):
            pass
        class NvttContext(ctypes.Structure):
            pass
        class _NvttCompressionOptions(ctypes.Structure):
            pass
        class NvttOutputOptions(ctypes.Structure):
            pass
        
        self.NvttSurfacePtr = ctypes.POINTER(NvttSurface)
        
        self.NvttContextPtr = ctypes.POINTER(NvttContext)
        
        self.NvttCompressionOptionsPtr = ctypes.POINTER(_NvttCompressionOptions)
        
        self.NvttOutputOptionsPtr = ctypes.POINTER(NvttOutputOptions)
        
        self.map_comp_options_funcs()
        self.map_surface_funcs()
        self.map_nvtt_funcs()
        
    def map_nvtt_funcs(self):
        """Map NVTT functions."""
        self._lib.nvttVersion.restype = ctypes.c_uint
        self._lib.nvttVersion.argtypes = []
        
    def map_surface_funcs(self):
        """Map nvttSurface functions."""
        
        self._lib.nvttCreateSurface.restype = self.NvttSurfacePtr
        self._lib.nvttCreateSurface.argtypes = ()
        
        self._lib.nvttDestroySurface.restype = None
        self._lib.nvttDestroySurface.argtypes = [self.NvttSurfacePtr]
        
        self._lib.nvttSurfaceLoad.restype = ctypes.c_bool
        self._lib.nvttSurfaceLoad.argtypes = (
            self.NvttSurfacePtr, # Surface
            ctypes.c_char_p, # filename
            ctypes.POINTER(ctypes.c_bool), # hasAlpha
            ctypes.c_bool, # expectSigned
            ctypes.c_void_p, # NvttTimingContext
        )
        
        self._lib.nvttSurfaceWidth.restype  = ctypes.c_int
        self._lib.nvttSurfaceWidth.argtypes = [self.NvttSurfacePtr]
        self._lib.nvttSurfaceHeight.restype  = ctypes.c_int
        self._lib.nvttSurfaceHeight.argtypes = [self.NvttSurfacePtr]
        
        self._lib.nvttSurfaceDepth.restype  = ctypes.c_int
        self._lib.nvttSurfaceDepth.argtypes = [self.NvttSurfacePtr]
        
    def map_comp_options_funcs(self):
        """Map nvttCompressionOptions functions."""
        self._lib.nvttCreateCompressionOptions.restype = self.NvttCompressionOptionsPtr
        self._lib.nvttCreateCompressionOptions.argtypes = ()
        
        self._lib.nvttDestroyCompressionOptions.restype = None
        self._lib.nvttDestroyCompressionOptions.argtypes = [self.NvttCompressionOptionsPtr]
        
        self._lib.nvttResetCompressionOptions.restype = None
        self._lib.nvttResetCompressionOptions.argtypes = [self.NvttCompressionOptionsPtr]
        
        self._lib.nvttSetCompressionOptionsFormat.restype = None
        self._lib.nvttResetCompressionOptions.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_int]
        
        self._lib.nvttSetCompressionOptionsQuality.restype = None
        self._lib.nvttSetCompressionOptionsQuality.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_int]
        
        self._lib.nvttSetCompressionOptionsColorWeights.restype = None
        self._lib.nvttSetCompressionOptionsColorWeights.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
        
        self._lib.nvttSetCompressionOptionsPixelFormat.restype = None
        self._lib.nvttSetCompressionOptionsPixelFormat.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        
        self._lib.nvttSetCompressionOptionsPixelType.restype = None
        self._lib.nvttSetCompressionOptionsPixelType.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_int]
        
        self._lib.nvttSetCompressionOptionsPitchAlignment.restype = None
        self._lib.nvttSetCompressionOptionsPitchAlignment.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_int]
        
        self._lib.nvttSetCompressionOptionsQuantization.restype = None
        self._lib.nvttSetCompressionOptionsQuantization.argtypes = [self.NvttCompressionOptionsPtr, ctypes.c_bool, ctypes.c_bool, ctypes.c_bool, ctypes.c_int]
        
        self._lib.nvttGetCompressionOptionsD3D9Format.restype = ctypes.c_uint
        self._lib.nvttGetCompressionOptionsD3D9Format.argtypes = [self.NvttCompressionOptionsPtr]
     
    @property
    def version(self) -> int:
        """Get the version of the NVTT library."""
        if self._version == 0:
            self._version = self._lib.nvttVersion()
        return self._version
    
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
        
    class CompressionOptions:
        """High-level wrapper for nvttCompressionOptions."""
        def __init__(self, ctx):
            self._lib = ctx._lib
            self._ptr = ctx._lib.nvttCreateCompressionOptions()
            if not self._ptr:
                raise RuntimeError("Failed to create nvttCompressionOptions.")
        
        def __del__(self):
            if getattr(self, '_ptr', None):
                self._lib.nvttDestroyCompressionOptions(self._ptr)
                