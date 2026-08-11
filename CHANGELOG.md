## v1.2.0 (2026-08-11)

### What's Changed

* Payload handlers are now **stateless**: the request model is built per-call instead of being stored on the handler, so shared/singleton handlers are safe under concurrent (including async) requests.
* Handler `req_model`, `resp_model` and `dry` can now be declared as class attributes, in addition to `__init__` arguments (backward compatible).
* Added sync/async type markers `_Sync`, `_Async` and the `_Mode` `TypeVar`, enabling correctly-typed async clients through overloads.
* `APIClient` now dispatches requests via `__getattr__` instead of `__getattribute__` (faster; only triggered on an attribute miss).
* The `httpx` client is now created lazily and can be closed: added `close()`/`aclose()` and (async) context-manager support. Importing a client no longer opens connections.
* Request `timeout` is now configurable (default: 10s).
* Non-JSON or empty response bodies no longer raise `JSONDecodeError`; `APIResponse` now decodes defensively.
* `PayloadBaseModel.from_args` now raises on duplicate or excess positional arguments.


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
