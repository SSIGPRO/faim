# faim

## Setup

### Windows

1. Install Git for Windows from [git-scm.com/download/win](https://git-scm.com/download/win), then run the installer (default options are fine).
2. Install Visual Studio Code from [code.visualstudio.com/download](https://code.visualstudio.com/download), then run the installer.
3. Open VS Code, open its integrated terminal (Terminal > New Terminal), and follow the command line instructions below to clone the repository, create the virtual environment, and install the packages.

To create and activate the virtual environment on Windows, use:

```bash
python -m venv faim-venv
faim-venv\Scripts\activate
```

### Clone the repository

```bash
git clone git@github.com:SSIGPRO/faim.git
cd faim
```

### Create a virtual environment (Linux)

```bash
python3 -m venv faim-venv
source faim-venv/bin/activate
```

### Install the required packages

```bash
pip install scipy matplotlib pandas seaborn folium scikit-learn ipykernel ipympl PyQt5
```

`PyQt5` gives matplotlib a GUI backend so plot windows can open from a plain script (not just inside a notebook). Without it, matplotlib may fall back to a non-interactive backend and warn that it "cannot be shown".
