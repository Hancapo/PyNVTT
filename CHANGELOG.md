# Changelog

PyNVTT changes.

## [0.0.3] - TBD

## [0.0.2] - 2025-06-29

### New Features
- Added load from memory function.
- Color conversion, like sRGB, lineal, gamma related changes, etc.
- Added resize methods including resize to power-of-two methods, max extents, etc.
- Linux support.
- Added Pillow's `Image` support in Surface constructor.

### Changes
- CUDA acceleration is now disabled by default when using an `EasyDDS` object.
- The `convert_all` method now uses the `can_make_next_mipmap` method.
- Replaced almost all docstrings with their NVTT's headers counterparts.
- Surface's `is_null` method used are now used in most methods instead of doing a pointer check.

## [0.0.1] - Initial Release

- Initial release for pyNVTT