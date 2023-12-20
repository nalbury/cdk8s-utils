# Cdk8s Utils

This project contains helper utilities for using cdk8s in python.

## Usage

The utilities here build on top of the standard cdk8s workflow, but instead of using the npm installed cdk8s cli, everything is done with python tooling and a typed Config data class.

### Example
```python
from dataclasses import dataclass

from cdk8s import Chart, ApiObject, ApiObjectMetadata

from constructs import Construct

from cdk8s_utils import cli


@dataclass
## defaults can be overriden at runtime by providing a config.yaml file with the --config flag
# for example:
# --- !Config
# image: "nginx:notlatest"
#
class Config:
    image: str = "nginx:latest"

# our actual cdk8s Chart subclass, all Config class attribuates are available for templating the manifests as needed
class ExampleChart(Chart):
    def __init__(
        self,
        scope: Construct,
        id: str,
        config: Config,
    ):
        labels = {"app": id}
        super().__init__(scope, id, disable_resource_name_hashes=True, labels=labels)
        ApiObject(
            self,
            id="test-resource",
            api_version="v1alpha1",
            kind="TestResource",
            metadata=ApiObjectMetadata(name="test", labels={"image": config.image}),
        )
        self.config = config

# main script simply executes the cli.run() function to synthesize our manifests to both stdout and the default `dist/` path
# a --help flag is available for more info on cli usage options
if __name__ == "__main__":
    cli.run(Config, ExampleChart, cli_args=None)
```

It can be run as a standard python executable e.g. `python main.py --help`

```
usage: cdk8s-app [-h] [--config CONFIG] [--print | --no-print] name

positional arguments:
  name                 resource name

options:
  -h, --help           show this help message and exit
  --config CONFIG      path to config file with input values (default:
                       None)
  --print, --no-print  if true, the manifests will be printed to
                       stdout (default: True)
```

### Cookiecutter template

A complete cdk8s python framework can be generated for a new python project with the [cookiecutter template here.](https://github.com/nalbury/cookiecutter-cdk8s-python-app)

## Building and Pushing

The package is hosted on pypi for installation via pip etc. As a result a valid API token for a registered pypi.org user is required for pushing.

**NOTE: use the provided devcontainer for this.**

The package can be built and pushed using:

```
make push 
```

This will:
- create a venv in .venv
- run pip-compile (from [pip-tools](https://github.com/jazzband/pip-tools)) to generate a complete pinned set of requirements.txt files from the pyproject.toml
- build the python package artifacts
- prompt for user/token for pypi.org
- push the package artifacts to pypi.org

TODO: some CI here
