# LSIM Single SMS klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.lsim import LSIMSingleSMSAsyncClient
    ```

::: integrify.lsim.single.client.LSIMSingleSMSClient
    handler: python
    options:
      separate_signature: true

::: integrify.lsim.single.client.LSIMSingleSMSAsyncClient
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `LSIMSingleSMSClientClass().send_sms_post()` kimi istifadə etməlisiniz.

::: integrify.lsim.single.client.LSIMSingleSMSClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - send_sms_get
        - send_sms_post
        - check_balance
        - get_report_get
        - get_report_post
