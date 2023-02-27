# hypermodern-python

## Setup

First create a conda environment

```
mamba create -n py310 python=3.10 -c conda-forge
```

Then activate it 
```
mamba activate py310
```

Install poetry
```
mamba install poetry
```

Initialize your Python project:
```
poetry init --no-interaction
```

Install some packages
```
poetry add click
poetry add requests
```

## Test

Install some more packages
```
poetry add --dev pytest
poetry add --dev coverage[toml] pytest-cov
poetry add --dev nox
```

Run end-to-end test
```
nox -r -- -m e2e
```