# :package: colcon_direnv

A colcon verb for initializing a `COLCON_DEFAULTS_FILE`, and optionally also configuring `direnv`.

# Key Features

- Build from anywhere in your colcon workspace. No more accidentally building in the wrong folder!
- Automatically source your workspace whenever your `cd` into it, or into any subfolder
- Use symlink install by default

# Installing from github

:construction: Once sufficiently tested, this package will be installable from standard `apt` repositories or from `conda-forge` repositories (for use with Pixi).

First, you should have `direnv` installed and configured

```bash
sudo apt install direnv
```

Add the following line at the end of the ~/.bashrc file:

```bash
eval "$(direnv hook bash)"
```

For now, we settle for a global python package install with pip

Go to the root of your workspace, e.g. `~/code/ws`
```bash
pip install --break-system-packages git@github.com:PeterMitrano/colcon-direnv.git
colcon direnv
direnv allow
```

# What it does

It creates a `.envrc` file, which the [direnv](https://direnv.net/) tool reads and executes when entering the directory or any subdirectory.
In this file, we set `COLCON_DEFAULTS_FILE` to point to a `defaults.json` file which we fill out with some sensible defaults.

# Credits

This repository is based off `colcon-clean`, by Ruffin White.
