# Contributing

Thank you for your interest in contributing to COMPAS cadwork!
Here are some aspect that will help you get started with your first contribution to the project.

## Setting Up Your Developer Environment

1. Fork and clone the repository.

2. Make sure you have [Astral's uv](https://docs.astral.sh/uv/) installed, which we use as both the project and package manager.

3. Run this command to configure the project automatically on your machine:

    ```sh
    uv inv setup
    ```

4. Create a new branch.

    Depending on what you want to achieve with it, give it a name that follows this naming pattern:

    - `feat/<name-with-hyphens>` for new features.
    - `fix/<name-with-hyphens>` for bug fixes.
    - `chore/<name-with-hyphens>` for maintenance work.

Once that's done, you're ready to start coding.

## Other Commands

Here are a few other useful commands that you will most certainly need while working on the project:

- `uv run pytest` to run the test suite.
- `uv run inv lint` to check the code style and lint the project.
- `uv run inv docs` to regenerate the documentation.

## Use of LLMs and AI

> [!TIP]
> **TL;DR**: Any code generated with the help of LLMs should be carefully reviewed and verified by you.

We know that LLMs and agents can be helpful for writing code, and you're welcome to use them.

However, it's important to acknowledge that they can't take responsibility for what they produce: that part is on you.
Therefore, before pushing anything to this repository, please make sure the code is clean and does what it's supposed to do.
Also, you must have the legal right to contribute it.

If you'd like to use agents when contributing to COMPAS cadwork, we've included an [`AGENTS.md`](agents.md) file to help them follow our coding standards and best practices.
It's also a useful read for humans, so we recommend taking a look at it, too.

## Questions

If anything is unclear, if you find an issue in the documentation, or if you just want to ask a question, please reach out.
Open an issue on GitHub, or send us a private email if that feels better.
We'll be happy to help!
