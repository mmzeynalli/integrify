# AzeriCard klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.azericard import AzeriCardAsyncClient
    ```

::: integrify.azericard.client.AzeriCardClient
    handler: python
    options:
      separate_signature: true

::: integrify.azericard.client.AzeriCardAsyncClient
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `AzeriCardClientClass().save_card()` kimi istifadə etməlisiniz.

::: integrify.azericard.client.AzeriCardClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - authorize
        - auth_and_save_card
        - auth_with_saved_card
        - finalize
        - get_transaction_status
        - transfer_start
        - transfer_confirm
        - transfer_decline
