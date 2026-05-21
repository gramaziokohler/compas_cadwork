from pathlib import Path

from compas_invocations2.console import chdir
from compas_invocations2.docs import docs
from compas_invocations2.tests import testdocs
from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


_UNRELEASED_CHANGELOG_TEMPLATE = "## Unreleased\n\n### Added\n\n### Changed\n\n### Removed\n\n## "


@task
def lint(ctx: Context) -> None:
    """Run all pre-commit hooks against the whole project."""
    ctx.run("pre-commit run --all-files")


@task
def prepare_changelog(ctx: Context) -> None:
    """Prepare changelog for next release."""
    with chdir(ctx.base_folder):
        with open("CHANGELOG.md", "r+", newline="") as changelog:
            content = changelog.read()
            changelog.seek(0)
            changelog.write(content.replace("## ", _UNRELEASED_CHANGELOG_TEMPLATE, 1))
        ctx.run('git add CHANGELOG.md && git commit -m "Prepare changelog for next release"')


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
