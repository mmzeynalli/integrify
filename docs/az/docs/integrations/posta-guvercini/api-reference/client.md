# Posta Guvercini klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.postaguvercini import PostaGuverciniAsyncClient
    ```

::: integrify.postaguvercini.client.PostaGuverciniClient
    handler: python
    options:
      separate_signature: true

::: integrify.postaguvercini.client.PostaGuverciniAsyncClient
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `PostaGuverciniClientClass().send_single_sms()` kimi istifadə etməlisiniz.

::: integrify.postaguvercini.client.PostaGuverciniClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - send_single_sms
        - send_multiple_sms
        - get_status
        - credit_balance
