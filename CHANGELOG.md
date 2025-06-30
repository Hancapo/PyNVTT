# Changelog

PyNVTT changes.

## [0.0.3] - TBD

## [0.0.2] - 2025-06-29

### New Features
- More Surface methods mapped.
- Image from memory loading.
- Color conversion, like sRGB, lineal, gamma related changes, etc.
- resize methods including resize to power-of-two methods, max extents, etc.
- Linux support.
- Pillow's `Image` support in Surface constructor.
- Canvas resizing.
- Surface saving.

### Changes
- CUDA acceleration is now disabled by default when using an `EasyDDS` object.
- The `convert_all` method now uses the `can_make_next_mipmap` method.
- Replaced almost all docstrings with their NVTT's headers counterparts.
- Surface's `is_null` method used are now used in most methods instead of doing a pointer check.
- Filter enums merged in a single one called `Filters`.

## [0.0.1] - Initial Release

- Initial release for pyNVTT