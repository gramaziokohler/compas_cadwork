from pathlib import Path

from compas_invocations2.docs import docs
from compas_invocations2.tests import testdocs
from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


@task
def lint(ctx: Context) -> None:
    """Run all pre-commit hooks against the whole project."""
    ctx.run("pre-commit run --all-files")


@task
def setup(ctx: Context) -> None:
    """Register the pre-commit hooks for this project."""
    ctx.run("pre-commit install")


@task
def test(ctx: Context) -> None:
    """Run the entire test suite."""
    ctx.run("pytest")


ns = Collection(
    docs,
    lint,
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
