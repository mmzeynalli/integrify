# LSIM Bulk SMS klientinin API Reference-i

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.lsim import LSIMBulkSMSAsyncClient
    ```

::: integrify.lsim.bulk.client.LSIMBulkSMSClient
    handler: python
    options:
      separate_signature: true

::: integrify.lsim.bulk.client.LSIMBulkSMSAsyncClient
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `LSIMBulkSMSClientClass().check_balance()` kimi istifadə etməlisiniz.

::: integrify.lsim.bulk.client.LSIMBulkSMSClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - bulk_send_one_message
        - bulk_send_different_messages
        - get_report
        - get_detailed_report
        - get_detailed_report_with_dates
        - check_balance
