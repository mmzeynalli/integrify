# KapitalBank klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.kapital import KapitalAsyncRequest
    ```

::: integrify.kapital.client.KapitalRequest
    handler: python
    options:
      separate_signature: true

::: integrify.kapital.client.KapitalAsyncRequest
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `KapitalClientClass().save_card()` kimi istifadə etməlisiniz.

::: integrify.kapital.client.KapitalClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - create_order
        - get_order_information
        - get_detailed_order_info
        - refund_order
        - save_card
        - pay_and_save_card
        - full_reverse_order
        - clearing_order
        - partial_reverse_order
        - pay_with_saved_card
