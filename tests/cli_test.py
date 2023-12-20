from dataclasses import dataclass

from cdk8s import Chart, ApiObject, ApiObjectMetadata

from constructs import Construct

from cdk8s_utils import cli


@dataclass
class ExampleConfig:
    image: str = "nginx:latest"


class ExampleChart(Chart):
    def __init__(
        self,
        scope: Construct,
        id: str,
        config: ExampleConfig,
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


def test_cli(capsys):
    cli.run(ExampleConfig, ExampleChart, cli_args=["test"])
    captured = capsys.readouterr()
    assert (
        captured.out
        == """---
apiVersion: v1alpha1
kind: TestResource
metadata:
  labels:
    app: test
    image: nginx:latest
  name: test

"""
    )
