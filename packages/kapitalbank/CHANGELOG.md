## v1.1.0 (2026-08-11)

### What's Changed

* Added full type hints and autocomplete for the async client (`KapitalAsyncRequest`) via sync/async overloads.
* Fixed `link_card_token` sending a double-encoded (stringified) JSON body; it now sends a proper JSON object.
* Response handling no longer crashes on non-JSON or empty response bodies.
* `KAPITAL_ENV` is now normalized and warns on unknown values instead of silently using the test gateway.
* Fixed `ImportError` against `integrify-core>=1.1` (removed `_UNSET`/`Unsettable` names).
* Migrated payload handlers to the class-attribute style.
* Requires `integrify-core>=1.2.0`.

## v1.0.0 (2025-07-19)

### What's Changed

* Refactored [old library](https://github.com/mmzeynalli/integrify) to new style.
