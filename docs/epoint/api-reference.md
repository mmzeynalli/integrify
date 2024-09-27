???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:
    
    ```python
    from integrify.epoint.asyncio import EPointRequest
    ```

::: integrify.epoint.sync.EPointRequest

???+ note

    Bu artıq hazır yaradılmış klass obyektidir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `_EPointRequest().save_card()` kimi istifadə etməlisiniz.

::: integrify.epoint.sync._EPointRequest
    handler: python
    options:
      members:
        - pay
        - get_transaction_status
        - save_card
        - pay_with_saved_card
        - pay_and_save_card
        - payout
        - refund
        - split_pay
        - split_pay_with_saved_card
        - split_pay_and_save_card
