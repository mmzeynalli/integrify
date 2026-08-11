## v1.2.0 (2026-08-11)

### What's Changed

* Added full type hints and autocomplete for the async client (`EPointAsyncRequest`) via sync/async overloads.
* Fixed response/callback parsing crashing on unknown bank response codes (`Code[...]` `KeyError`); unknown codes now fall back to the raw code.
* Migrated payload handlers to the class-attribute style.
* Requires `integrify-core>=1.2.0`.

## v1.1.0 (2025-24-11)

### What's Changed

* Added support to both old and new version of integrify-core.

## v1.0.0 (2025-07-19)

### What's Changed

* Refactored [old library](https://github.com/mmzeynalli/integrify) to new style.
