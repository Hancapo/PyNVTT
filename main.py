from nvtt import NVTT
from surface import Surface
from compression_options import CompressionOptions
    
nvtt = NVTT()

print(f"NVTT Version: {nvtt.version}")
    
surface = Surface(nvtt)
co = CompressionOptions(nvtt)
    
image = surface.load("texture_01.png")
print(co)