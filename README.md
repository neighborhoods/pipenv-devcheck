# pipenv-devcheck
`pipenv-devcheck` is a command-line utility for helping python package developers
ensure that their development environments match what they are expecting of
their users' environments.

At Neighborhoods, some developers utilize Pipenv as a dependency management
system during development, allowing for assurance that an entire development
team is working with an identical environment. While Pipenv is an extremely
helpful development tool, it is not an all-in-one solution to development
challenges.

When a user installs a python package, for example, the dependencies they
need are specified not in Pipenv's `Pipfile`, but in `setup.py`. As a result,
it is possible for a developer to change the dependencies they are using
without reflecting those changes in the environment expected for package usage.

`pipenv-devcheck` is a lightweight command-line tool to check for such mistakes.
If a project is found to have discrepancies between the development and user
environments, an error is thrown, allowing for detection by CI tools. While
simple in nature, this check can prevent annoying issues such as revising a
package release to update requirements, or developers having difficulty
with helping users debug due to a hidden environment difference.

After installation, simply run `pipenv-devcheck` via the command line to use!
