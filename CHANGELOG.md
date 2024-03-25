# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] 2024-03-25

### Added

### Changed

* Now getting dimension orientation from API.
* IFC export options are read from file defaults.
* `Text3dSceneObject` checks `Text3d.centered` attribute.

### Removed


## [0.2.1] 2024-03-21

### Added

### Changed

### Removed


## [0.2.0] 2024-03-21

### Added

* New `IFCExporter` class.
* Added setting to enable to disable translation to global coordinate system to `IFCExportSettings`.
* Added new methods and properties to `Element`.
* Added `ElementDelta` to support editing.

### Changed

* Fixed `RuntimeError` when calling `get_element_groups`.
* Fixed `IFCExportSettings` are ignored.
* Made all `Artist`s `SceneObjects` to support COMPAS 2.x.
* Added rendering of `Text3dObject` to type `raster`.

### Removed


## [0.1.2] 2024-01-24

### Added

### Changed

### Removed


## [0.1.1] 2024-01-24

### Added

### Changed

### Removed

