## v1.1.0 (2026-08-11)

### What's Changed

* Added full type hints and autocomplete for the async clients (single & bulk) via sync/async overloads.
* Fixed the single-SMS report handler crashing on empty or non-numeric report bodies; the response is now built safely.
* Migrated single-SMS payload handlers to the class-attribute style.
* Requires `integrify-core>=1.2.0`.

## v1.0.0 (2025-07-19)

### What's Changed

* Refactored [old library](https://github.com/mmzeynalli/integrify) to new style.
