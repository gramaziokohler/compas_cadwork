********************************************************************************
Installation
********************************************************************************

.. NOTE::

    To install `compas_cadwork`, you need to have `cadwork <https://cadwork.swiss/>`_ and `Python3.10 <https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe>`_ installed on your system.


.. NOTE::

    There generally two ways one might use `compas_cadowrk` in cadwork.

    1. Use it in cadwork's Python Console for some quick scripting.
    2. Develop a plugin that uses `compas_cadwork`.

    Depending on your needs, you can choose one of the following two ways to install `compas_cadwork`.

Use in cadwork's Python Console
==========================================================

The simplest way to use `compas_cadwork` in cadwork's Python Console is to install it to the python environment that's integrated with cadwork.

One of these relevant paths is

``C:\Program Files\cadwork.dir\EXE_30\Pclib.x64\python310\site-packages``

To install `compas_cadwork` to this path, you can use the following command

.. code-block:: bash

    python -m pip install compas_cadwork --target "C:\Program Files\cadwork.dir\EXE_30\Pclib.x64\python310\site-packages" --upgrade


Develop a plugin using `compas_cadwork`
==========================================================

.. NOTE::

    `<my_plugin>` is used below as placeholder for the plugin's name. Make sure to replace it with the name of you plugin.


.. NOTE::

    There are two paths where python plugins can be stored in cadwork. Choose one of them depending on your needs.
    In the example below the chosen path is denoted as `<cadwork_plugin_path>`.

    - User plugin path: ``C:\Users\Public\Documents\cadwork\userprofil_30\3d\API.x64``
    - System plugin path: ``C:\ProgramData\cadwork\cadworkprofil_30\german\plugins``

To install `compas_cadwork` and use it in your own plugin development, it is recommended to create a virtual environment for your plugin and install `compas_cadwork` there.

To create a virtual environment first install `virtualenv`

.. code-block:: bash

    python -m pip install virtualenv

Then create a virtual environment named `<my_plugin>`

.. code-block:: bash

    python -m virtualenv <cadwork_plugin_path>\<my_plugin>


Activate the virtual environment

.. code-block:: bash

    <cadwork_plugin_path>\<my_plugin>\Scripts\activate


Install `compas_cadwork` to the virtual environment

.. code-block:: bash

    python -m pip install compas_cadwork --upgrade


The last step is to add the virtual environment to the python path in your main plugin module

.. code-block:: python

    # <cadwork_plugin_path>\<my_plugin>\<my_plugin>.py
    LIB = r"<cadwork_plugin_path>\<my_plugin>\Lib\site-packages"
    import sys
    if LIB not in sys.path:
        sys.path.append(LIB)

    # from here on you can import compas_cadwork
