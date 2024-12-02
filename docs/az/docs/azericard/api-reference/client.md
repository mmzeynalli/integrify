# EPoint klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.azericard import AzeriCardAsyncRequest
    ```

::: integrify.azericard.client.AzeriCardRequest
    handler: python
    options:
      separate_signature: true

::: integrify.azericard.client.AzeriCardAsyncRequest
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
        - pay
        - pay_and_save_card
        - pay_with_saved_card
        - block
        - block_and_save_card
        - block_with_saved_card
        - accept_blocked_payment
        - reverse_blocked_payment
        - cancel_blocked_payment
        - get_transaction_status
        - remit
        - auth
        - auth_response
