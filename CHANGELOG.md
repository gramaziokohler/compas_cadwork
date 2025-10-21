# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Removed

* Removed obsolete module `compas_cadwork.utilities.dimensions.py`.
* Removed obsolete class `CameraView`, replaced by `compas_cadwork.scene.Camera`.
* Removed obsolete function `set_camera_view`, replaced by `compas_cadwork.scene.Camera`.

## [0.9.0] 2024-11-28

### Added

### Changed

### Removed

* Removed `ElementType` class.
* Removed `Element.from_id` method.
* Removed `Element.type` property. Use `Element.is_*` properties instead.
* Removed `Dimension.from_element` method. Use `Dimension(element_id)` instead.
* Removed `Dimension.from_id` method. Use `Dimension(element_id)` instead.

## [0.8.0] 2024-11-15

### Added
- Added utility function to query wall_frame elements from selection

### Changed

### Removed


## [0.7.0] 2024-10-29

### Added

### Changed

### Removed


## [0.6.0] 2024-10-15

### Added

* Added new file storage manager `FileStorage` to `compas_cadwork.storage`.
* Added new project storage manager `ProjectStorage` to `compas_cadwork.storage`.

### Changed

### Removed


## [0.5.0] 2024-09-16

### Added

### Changed

* Made changes to instruction scene objects to support recent COMPAS2.x versions.

### Removed

* Removed the unused `Model3dSceneObject`.

## [0.4.4] 2024-09-03

### Added

### Changed

* Added additional default LoD settings on IFC export.

### Removed


## [0.4.3] 2024-08-08

### Added

### Changed

### Removed


## [0.4.2] 2024-07-22

### Added

### Changed

* Number of anchor points is taken into account when comparing `Dimension` instances.

### Removed


## [0.4.1] 2024-07-12

### Added

* Added method `translate` to `Element`.

### Changed

* Fixed centered text instructions are sometimes shifted the worng direction.

### Removed


## [0.4.0] 2024-06-27

### Added

* Added new types `Dimension` and `AnchorPoint` in `compas_cadwork.datamodel`.
* Added `from_element` and `from_id` to `Dimension`. 
* Added `compas_cadwork.scene.Camera` to read and manipulate the camera.
* Added `compas_cadwork.datamodel.Element.centerline`.
* Added `compas_cadwork.datamodel.Element.midpoint`.

### Changed

* Exporting now with ifc4 and bimwood property set (true).

### Removed


## [0.3.1] 2024-05-16

### Added

### Changed

### Removed


## [0.3.0] 2024-05-15

### Added

### Changed

### Removed


## [0.2.3] 2024-03-27

### Added

### Changed

* Fixed added linear dimension pushed up every time it shows.

### Removed


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

