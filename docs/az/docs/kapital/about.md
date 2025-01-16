# Kapital

???+ warning
    Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `KAPITAL_USERNAME`, `KAPITAL_PASSWORD`
    Əlave olaraq `KAPITAL_ENV` dəyişənini də təyin etməlisiniz. Əgər default olaraq saxlasaz test mühitindən istifadə edəcəksiniz. Əks halda, `prod` dəyərini təyin etməlisiniz.

    | **Environment Variable**  | **Description**                               | **Default**                             |
    |---------------------------|-----------------------------------------------|-----------------------------------------|
    | `KAPITAL_USERNAME`        | Kapital API autentifikasiyası üçün Username   | `TerminalSys/kapital`                   |
    | `KAPITAL_PASSWORD`        | Kapital API autentifikasiyası üçün Password   | `kapital123`                            |
    | `KAPITAL_ENV`             | Environment mode (`test` və ya `prod`)        | `test` (default)                        |


???+ note
    Kapital interfeysinin dilini dəyişmək istəyirsinizsə, `KAPITAL_INTERFACE_LANG` "environment variable"-na dəyər verin. Default olaraq, Azərbaycan dili olacaq.

    Sorğular uğurlu və ya uğursuz olduqda, spesifik URL-ə yönləndirmək istəyirsinizsə, bu dəyişənlərə də mühit levelində dəyər verin: `KAPITAL_REDIRECT_URL`

???+ info
    ### Test Card Məlumatları
    | **PAN**            | **ExpDate** | **CVV/CVV2** |
    |--------------------|-------------|--------------|
    | 4169741330151778   | 11/26       | 119          |
    | 5239151747183468   | 11/24       | 292          |

## Rəsmi Dokumentasiya { #official-documentation }

[Notion](https://brawny-airport-7ca.notion.site/Kapital-bank-E-commerce-API-Documentation-6dd6a228c40644e3bef034bca7845e3c)

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                                                           | Məqsəd                                             |            Kapital API            |  Callback-ə sorğu atılır  |
| :----------------------------------------------------------------------------------------------------- | :------------------------------------------------- | :-------------------------------: | :-----------------------: |
| [`create_order`][integrify.kapital.client.KapitalClientClass.create_order]                             | Ödəniş                                             |           `/api/order`            | :fontawesome-solid-check: |
| [`get_order_information`][integrify.kapital.client.KapitalClientClass.get_order_information]                   | Ödəniş haqda qısa məlumat                          |      `/api/order/{order_id}`      |            :x:            |
| [`get_detailed_order_info`][integrify.kapital.client.KapitalClientClass.get_detailed_order_info] | Ödəniş haqda detallı məlumat                       |      `/api/order/{order_id}`      |            :x:            |
| [`refund_order`][integrify.kapital.client.KapitalClientClass.refund_order]                             | Geri ödəniş sorğusu                                | `/api/order/{order_id}/exec-tran` |            :x:            |
| [`save_card`][integrify.kapital.client.KapitalClientClass.save_card]                                   | Kartı saxlamaq üçün ödəniş sorğusu                 |           `/api/order`            |            :fontawesome-solid-check:            |
| [`pay_and_save_card`][integrify.kapital.client.KapitalClientClass.pay_and_save_card] | Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu |           `/api/order`            |            :fontawesome-solid-check:            |
| [`full_reverse_order`][integrify.kapital.client.KapitalClientClass.full_reverse_order]                 | Ödənişi ləğv etmək üçün sorğu                      | `/api/order/{order_id}/exec-tran` |            :x:            |
| [`clearing_order`][integrify.kapital.client.KapitalClientClass.clearing_order]                         | Ödənişin təsdiq edilməsi üçün sorğu                | `/api/order/{order_id}/exec-tran` |            :x:            |
| [`pay_with_saved_card`][integrify.kapital.client.KapitalClientClass.pay_with_saved_card]               | Ödənişin hissəsini ləğv etmək üçün sorğu           | `/api/order/{order_id}/exec-tran` |            :x:            |
