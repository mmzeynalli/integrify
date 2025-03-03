## v2.2.1 (2025-03-03)

[GitHub release](https://github.com/mmzeynalli/integrify/releases/tag/v2.2.1)

### What's Changed

#### New integrations

* Added LSIM integration
* Added PostaGuvercini integration ([kazimovzaman2](https://github.com/kazimovzaman2))

#### Additions

* Added _UNSET logic to distinguish between unset and `None` values
* Migrated from poetry to uv
* Switched Makefile to python duty library
* Now dry-run response is `TypedDict` instead of `dict`

#### Fixes

* Fixed GET requests sending data in body instead of query params
* Replaced all possible mock requests with live ones
* Fixed outdated Kapital documentation for test cards ([AlifaghaSalmanov](https://github.com/AlifaghaSalmanov))

## v2.1.1 (2025-01-27)

[GitHub release](https://github.com/mmzeynalli/integrify/releases/tag/v2.1.1)

### What's Changed

#### Additions

* Added dry-run functionality per request

#### Fixes

* Fixed API url generation for async requests

## v2.1.0 (2025-01-17)

[GitHub release](https://github.com/mmzeynalli/integrify/releases/tag/v2.1.0)

### What's Changed

#### New integrations

* Added KapitalBank integration  ([kazimovzaman2](https://github.com/kazimovzaman2))

#### Fixes

* Added dry-run functionality per request class

#### Support

* Dropped support for Python 3.8

## v2.0.1 (2024-10-28)

[GitHub release](https://github.com/mmzeynalli/integrify/releases/tag/v2.0.1)

### What's Changed

#### Fixes

* Changed the whole structure and released a new version with better handling of requests and responses.
* Increased test coverage
* Added more and detailed documentations

## v1.0.3 (2024-10-07)

[GitHub release](https://github.com/mmzeynalli/integrify/releases/tag/v1.0.3)

### What's Changed

#### Fixes

* Replaced `StrEnum` with `str, Enum` to be python <3.11 friendly.

## v1.0.1 (2024-09-28)

### What's Changed

#### Fixes

* Updated version for PyPI

## v1.0.0 (2024-09-27)

### What's Changed

#### New integrations

* Added EPoint intergration
* Added EPoint documentation
