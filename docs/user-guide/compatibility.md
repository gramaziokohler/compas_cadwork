# Compatibility

Cadwork officially only supports the latest version of cadwork 3d.
In COMPAS cadwork, we try to maintain backward compatibility with older cadwork 3d releases wherever possible.
However, backward compatibility is not always feasible when a feature requires API bindings that are unavailable in older versions (for example, in Cadwork 2024).

If you plan to use COMPAS cadwork on an older cadwork 3d build, the library will install successfully but unsupported methods or unavailable properties will raise a `RuntimeError`.
You can find which features are available in which cadwork 3d versions in the [API Reference](../api/compas_cadwork.md).

> [!TIP]
> We strongly recommend always using COMPAS cadwork with the latest version of cadwork 3d.

## Summary of Version-Specific Features

For your convenience, below is a summary of features that are only available in some cadwork 3d versions:

| Module                     | Method / Property          | Cadwork 2024 | Cadwork 2025 | Cadwork 2026 |
| :------------------------- | :------------------------- | :----------: | :----------: | :----------: |
| `compas_cadwork.materials` | `FloorLayerStack.create()` |      ❌      |      ✅      |      ✅      |
| `compas_cadwork.materials` | `RoofLayerStack.create()`  |      ❌      |      ✅      |      ✅      |
