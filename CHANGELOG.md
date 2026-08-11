## v0.1.0 (2026-08-11)

### What's Changed

- Added full type hints and autocomplete for the async client (`CloposAsyncRequest`) via sync/async overloads.
- Updated handlers for the stateless handler API in integrify-core 1.2.0; requires `integrify-core>=1.2.0`.
- Migrated to Clopos Open API **v2** (base URL `https://integrations.clopos.com/open-api/v2/`).
- Authentication now uses `integrator_id` (env var `CLOPOS_INTEGRATOR_ID`) instead of `venue_id`.
- v2 requests send only the `x-token` header; `x-brand` is no longer sent and `x-venue` is now optional (overrides the venue encoded in the JWT).
- `AuthResponse` now includes the `expires_at` field.
- **Receipts**: removed `create_receipt`, `update_receipt` and `delete_receipt` — these are no longer part of Open API v2. Added `close_receipt` (`POST receipts/{id}/close`) and `get_receipt_stock_operations` (`GET receipts/{id}/stock-operations`, returns `ReceiptStockOperation`).
- **Price lists**: added `get_price_lists` (`GET price-lists`, returns `PriceList`) and `get_price_list_prices` (`GET price-lists/prices`, returns `PriceListPrice`).
- Note: nested relation objects on the new schemas (`PriceList.prices` product/list relations, `ReceiptStockOperation.product`/`stock`) are typed as `dict` where the exact nested shapes were not verifiable from the API docs.

## v0.0.1 (2025-12-01)

### What's Changed

- Added new integration with full API support, but not production tested.
