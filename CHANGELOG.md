## v1.1.1 (2026-08-08)

### What's Changed

* Bumped maximal httpx version from 0.28.0 to 1.
* Added dependabot

## v1.1.0 (2025-10-28)

### What's Changed

* Bumped minimal pydantic version from 2.8 to 2.11.
* Added new constant: `UNSET`. Used for differentiating None from missing (or unset) values. `UnsetField`/`UnsetOrNoneField` were also added as annotated pydantic fields.
* Now all requests can also pass request header as argument (see Clopos).
* Added function `_build_request_lambda` to enable subclasses to override without overriding whole `__getattribute__`. Can be used to enforce some arguments.

## v1.0.5 (2025-10-20)

### What's Changed

* Fixed and made integrify-core a namespace package.

## v1.0.3 (2025-07-19)

### What's Changed

* Refactored [old library](https://github.com/mmzeynalli/integrify) to new style.
