# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Switched to standard NHDS CI pipeline

## [0.3.0] - 2020-06-15

### Added
- Support for private PyPi repositories

## [0.2.5] - 2020-05-28

### Changed
- Fixed bug that caused situations where equality (`==`) in the Pipfile combined
with a range operator would lead to detection of nonexistent discrepancies.

## [v0.2.4] - 2020-04-01

### Changed
- Updated dependencies - specifically, addressed security concern with bleach v3.1.3

## [0.2.3] - 2020-03-25

### Changed
- Updated dependencies - specifically, addressed security concern with bleach v3.1.1

## [0.2.2] - 2020-03-03

### Changed
- Updated dependencies - specifically, addressed security concern with bleach v3.1.0

## [0.2.1] - 2020-02-10

### Changed
- Removed forgotten trace statement

## [0.2.0] - 2020-02-10

### Added
- Support for `*` versioning

### Changed
- Parsing dependencies is not purely regexp-based now. More flexible and
less opportunity for blind spots
    - `Pipfile`s are read into dictionaries using the `pipfile` package
    - `setup.py` files are now parsed using the `ast` library

## [0.1.1] - 2020-02-04

### Added
- Open source licensing
- Code for automating releases

## [0.1] - 2020-01-29

### Added
- Dependency comparisons
- Capable of running via CLI and being used in CI checks
