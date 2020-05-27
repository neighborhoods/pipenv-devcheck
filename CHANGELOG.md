# v0.2.5 #
* Fixed bug that caused situations where equality (`==`) in the Pipfile combined
with a range operator would lead to detection of nonexistent discrepancies.

# v0.2.4 #
* Updated dependencies - specifically, addressed security concern with bleach v3.1.3

# v0.2.3 #
* Updated dependencies - specifically, addressed security concern with bleach v3.1.1

# v0.2.2 #
* Updated dependencies - specifically, addressed security concern with bleach v3.1.0

# v0.2.1 #
* Removed forgotten trace statement

# v0.2.0 #
* Parsing dependencies is not purely regexp-based now. More flexible and
less opportunity for blind spots
    * `Pipfile`s are read into dictionaries using the `pipfile` package
    * `setup.py` files are now parsed using the `ast` library
* Added support for `*` versioning

# v0.1.1 #
* Added open source licensing
* Added code for automating releases

# v0.1 #
* Dependency comparisons
* Capable of running via CLI and being used in CI checks
