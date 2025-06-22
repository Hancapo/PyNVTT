from nvtt import NVTT
    
nvtt = NVTT()

print(f"NVTT Version: {nvtt.version}")
    
surface = nvtt.Surface(nvtt)
    
image = surface.load("texture_01.png")
print(f"Image loaded with dimensions: {surface.width}x{surface.height}, Has Alpha: {surface.has_alpha}, Depth: {surface.depth}")