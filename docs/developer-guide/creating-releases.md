# Creating Releases

> [!IMPORTANT]
> Only users that can push to `main` can create releases.

This library is distributed through the Python Package Index (PyPi).
You can create a new release by following these steps:

1. Checkout the `main` branch.

    ```sh
    git checkout main
    ```

2. Bump the library version.

    ```sh
    uv run bump-my-version bump (patch|minor|major)
    ```

3. Prepare the changelog file for next release.

    ```sh
    uv run inv prepare-changelog
    ```

4. Push the new commits to the remote repository.

    ```sh
    git push
    ```

5. [Create a new release](https://github.com/gramaziokohler/compas_cadwork/releases/new) on GitHub targeting `main`.

    It will automatically trigger a workflow and publish the release to PyPi.
