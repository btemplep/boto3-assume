# Changelog

Changelog for `boto3-assume`.
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [Unreleased] - YYYY-MM-DD

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security 
-->

## [0.2.1] - 2026-01-14

### Fixed

- type hints and docstrings on `assume_role`
- README formatting


## [0.2.0] - 2026-01-13

### Added

- `assume_role` 
    - replaces `assume_role_session`
    - Allowed to pass parameters for the created session
    - simplifies assume role APIs

### Deprecated

- `assume_role_session` - Deprecated in favor of the new `assume_role` function
- `assume_role_aio_session` - Deprecated and moved to a new python package `aioboto3-assume` to simplify dependencies and split boto3 and aioboto3 functionality.


## [0.1.3] - 2025-11-28

### Added

- Tags for support of python 3.13 and 3.14

### Removed

- Support for python 3.7-3.9


## [0.1.2] - 2024-05-18

### Removed
    - `boto3` and `aioboto3` package extras.  They didn't work and weren't documented correctly. 

### Fixed
    - `datetime.datetime.utcnow()` deprecation in tests for python 3.12


## [0.1.1] - 2023-06-28

### Fixed
    - Formatting for Changelog, README


## [0.1.0] - 2023-06-28

Initial Release.

