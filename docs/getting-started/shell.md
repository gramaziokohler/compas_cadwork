# Using COMPAS cadwork from the Python Shell

Cadwork 3d features a built-in Python shell plugin that lets you execute Python code directly within the running application.
To use COMPAS cadwork here, we need to install the library directly into Cadwork's integrated Python environment.

## Prerequisites

Before beginning, verify that you have the Python Shell available in your Cadwork environment.
If your Cadwork installation does not include the Python Shell, you can download and install it manually by following the instructions from the [official Cadwork Python documentation](https://docs.cadwork.com/projects/cwapi3dpython/en/latest/get_started/).

## Step 1: Locate your Cadwork "site-packages" Directory

Python libraries are stored in a specific folder called `site-packages`.
Because Cadwork uses its own self-contained Python instance, we must find the exact location of this folder on your computer.

The path follows this standard pattern:

```text
C:\Program Files\cadwork.dir\EXE_<Cadwork Version>\Pclib.x64\python<Python Version>\site-packages
```

Find your specific version of Cadwork in the list below and copy the path:

- **Cadwork 2024:** `C:\Program Files\cadwork.dir\EXE_30\Pclib.x64\python310\site-packages`
- **Cadwork 2025:** `C:\Program Files\cadwork.dir\EXE_2025\Pclib.x64\python312\site-packages`
- **Cadwork 2026:** `C:\Program Files\cadwork.dir\EXE_2026\Pclib.x64\python314\site-packages`

> [!WARNING]
> Older Cadwork versions may not support all the features offered by COMPAS cadwork.
> Check the page on [compatibility](../user-guide/compatibility.md) for more information.

## Step 2: Install the Library

To install the package, we use `pip` (Python's built-in package manager).
We will use the `--target` flag to tell `pip` to install the library directly into the Cadwork folder you identified before instead of your computer's global Python space.

1. Open a **PowerShell** terminal by pressing the Windows key, typing `powershell`, and hitting Enter.
2. Copy the command below, making sure to replace `<Path to Site Packages>` with the exact folder path from Step 1.
3. Press Enter to run the command.

```bash
pip install compas-cadwork --target "<Path to Site Packages>" --upgrade
```

## Step 3: Verify the installation

Double-check that the package was successfully installed and is accessible:

1. Launch **cadwork 3d**.
2. Open the **Python Shell** plugin.
3. Paste or type the following line into the console and press Enter.

```python
import compas_cadwork
```

If the console moves to the next line without throwing any error messages, the installation was a success!

> [!TIP]
> Whenever you need to upgrade COMPAS cadwork to its latest version, repeat the same steps from before.
