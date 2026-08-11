## v1.1.0 (2026-08-11)

### What's Changed

* Added full type hints and autocomplete for the async client (`AzeriCardAsyncClient`) via sync/async overloads.
* HTML auto-submit form values are now HTML-escaped, preventing attribute/markup injection.
* The RSA signing key is now read and parsed once (cached) instead of on every request.
* `AZERICARD_ENV` is now normalized and warns on unknown values instead of silently using the test gateway.
* Fixed `ImportError` against `integrify-core>=1.1` (removed `_UNSET`/`Unsettable` names).
* Migrated payload handlers to the class-attribute style.
* Requires `integrify-core>=1.2.0`.

## v1.0.0 (2025-07-19)

### What's Changed

* Refactored [old library](https://github.com/mmzeynalli/integrify) to new style.
