# Clopos client API Reference

???+ note

    Below shown examples are for sync requests. To use async requests, just import async client,
    and call same-name functions with `await`:

    ```python
    from integrify.clopos import CloposAsyncRequest
    ```

::: integrify.clopos.client.CloposRequest
    handler: python
    options:
      separate_signature: true

::: integrify.clopos.client.CloposAsyncRequest
    handler: python
    options:
      separate_signature: true

???+ note

    These are already create class objects, considered for direct use. Otherwise, you should create
    instance at every call, such as: `CloposClientClass().auth()`

::: integrify.clopos.client.CloposClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - auth
        - get_venues
        - get_users
        - get_user_by_id
        - get_customers
        - get_customer_by_id
        - get_customer_groups
        - get_categories
        - get_category_by_id
        - get_stations
        - get_station_by_id
        - get_products
        - get_product_by_id
        - get_sale_types
        - get_payment_methods
        - get_stop_list
        - get_orders
        - get_order_by_id
        - create_order
        - update_order
        - get_receipts
        - get_receipt_by_id
        - create_receipt
        - update_closed_receipt
        - update_receipt
        - close_receipt
        - delete_receipt
