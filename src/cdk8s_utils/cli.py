import argparse
import sys
import ruamel.yaml
from typing import Any, Sequence

from cdk8s import App


def run(config_class: Any, chart_class: Any, cli_args: Sequence[str] | None) -> None:
    """Run the provided cdk8s application.
    Keyword arguments:
    
    config_class -- a python data class defining the expected user inputs, an instance of the class will be created with any overrides set in the user provided config.yaml file applied, it's then passed to the provided chart class for use in rendering the cdk8s manfiests

    chart class -- a valid subclass of the cdk8s.Chart class which also accepts a config argument in its init function, an example can be found in cli_test.py (ExampleChart)

    cli_args -- this is an optional override for the argparse args sequence, if not set, it default to sys.argv[1:] i.e. all cmd line args minus the executable name
    """
    yaml = ruamel.yaml.YAML()
    yaml.register_class(config_class)

    parser = argparse.ArgumentParser(
        prog="cdk8s-app", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("name", help="resource name")
    parser.add_argument("--config", help="path to config file with input values")
    parser.add_argument(
        "--print",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="if true, the manifests will be printed to stdout",
    )

    if not cli_args:
        cli_args = sys.argv[1:]
    args = parser.parse_args(cli_args)

    c = config_class()
    if args.config:
        with open(args.config, "r") as y:
            c = yaml.load(y)

    app = App()
    chart_class(app, args.name, c)

    app.synth()

    if args.print:
        with open(f"./dist/{args.name}.k8s.yaml", "r") as f:
            print("---")
            print(f.read())
