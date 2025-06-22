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