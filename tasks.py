from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


@task
def setup(ctx: Context):
    """Register the pre-commit hooks for this project."""
    ctx.run("pre-commit install")


@task
def lint(ctx: Context):
    """Run all pre-commit hooks against the whole project."""
    ctx.run("pre-commit run --all-files")


ns = Collection(
    setup,
    lint,
)

ns.configure(
    {
        "run": {
            "encoding": "utf-8",
        },
    }
)
