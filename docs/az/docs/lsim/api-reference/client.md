# LSIM klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:
    
    ```python
    from integrify.lsim import LSIMAsyncClient
    ```

::: integrify.lsim.client.LSIMClient
    handler: python
    options:
      separate_signature: true

::: integrify.lsim.client.LSIMAsyncClient
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `LSIMClientClass().get_request_get()` kimi istifadə etməlisiniz.

::: integrify.lsim.client.LSIMClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - get_report_get
