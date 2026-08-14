# Using COMPAS cadwork in a Plugin

If you are developing a standalone Python plugin for Cadwork, it is highly recommended to keep your plugin's dependencies isolated in a **virtual environment**.

## Step 1: Set up the plugin project

Before adding COMPAS cadwork, initialize your standard plugin structure.
You can read how to create a basic plugin by following the steps in the [official Cadwork documentation](https://docs.cadwork.com/projects/cwapi3dpython/en/latest/get_started/).

There are two primary ways to create and manage virtual environments.
Choose the approach that best fits your workflow.

### Option A. Using a Project Manager (Recommended)

Modern Python tools like [uv](https://docs.astral.sh/uv/) or [poetry](https://python-poetry.org) handle virtual environments cleanly.

If you use **uv**, open your terminal, navigate to your plugin's root folder, and run:

```bash
uv add compas-cadwork
```

This single command automatically initializes a virtual environment and installs the latest version of `compas-cadwork` into it.

### Option B. Manual setup

If you prefer to use standard built-in Python utilities without installing extra tools, you can create the environment manually.
Open your terminal, navigate to your plugin directory, and execute these commands sequentially:

```ps1
# 1. Create a virtual environment folder named '.venv' inside your plugin folder
python -m virtualenv .venv

# 2. Activate the virtual environment
.venv\Scripts\activate

# 3. Install (or upgrade) the library inside this local environment
pip install compas-cadwork --upgrade
```

## Step 2: Import COMPAS cadwork in your code

Because Cadwork runs plugins from its own internal environment, you must explicitly point it to your plugin's local packages.
Add this snippet at the very top of your plugin's entrypoint Python file:

```python
import sys
from pathlib import Path

# Add your local virtual environment to Python's search path
deps_path = str(Path(__file__).parent / ".venv" / "Lib" / "site-packages")
if deps_path not in sys.path:
    sys.path.append(deps_path)

# Now you can safely import the library
import compas_cadwork
```
