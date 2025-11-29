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

