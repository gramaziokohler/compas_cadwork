from pathlib import Path

from compas_invocations2.build import prepare_changelog
from compas_invocations2.docs import docs
from compas_invocations2.style import lint
from compas_invocations2.tests import test
from compas_invocations2.tests import testdocs
from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


@task
def precommit(ctx: Context) -> None:
    """Run all pre-commit hooks against the whole project."""
    ctx.run("pre-commit run --all-files")


@task
def setup(ctx: Context) -> None:
    """Register the pre-commit hooks for this project."""
    ctx.run("pre-commit install")


ns = Collection(
    docs,
    lint,
    precommit,
    prepare_changelog,
    setup,
    test,
    testdocs,
)

ns.configure(
    {
        "base_folder": Path(__file__).parent,
        "run": {
            "encoding": "utf-8",
        },
    }
)
