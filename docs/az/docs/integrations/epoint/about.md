# EPoint

???+ warning
    Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `EPOINT_PUBLIC_KEY`, `EPOINT_PRIVATE_KEY`

???+ note
    EPoint interfeysinin dilini dəyişmək istəyirsinizsə, `EPOINT_INTERFACE_LANG` "environment variable"-na dəyər verin. Default olaraq, Azərbaycan dili olacaq.

    Sorğular uğurlu və ya uğursuz olduqda, spesifik URL-ə yönləndirmək istəyirsinizsə, bu dəyişənlərə də mühit levelində dəyər verin: `EPOINT_SUCCESS_REDIRECT_URL`, `EPOINT_FAILED_REDIRECT_URL`

## Rəsmi Dokumentasiya (v1.0.3) { #official-documentation }

[Azərbaycanca](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20az.pdf)

[İngliscə](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf)

[Rusca](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20ru.pdf)

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                                                       | Məqsəd                                                               |                EPoint API                 |  Callback-ə sorğu atılır  |
| :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :---------------------------------------: | :-----------------------: |
| [`pay`][integrify.epoint.client.EPointClientClass.pay]                                             | Ödəniş                                                               |             `/api/1/request`              | :fontawesome-solid-check: |
| [`get_transaction_status`][integrify.epoint.client.EPointClientClass.get_transaction_status]       | Ödəniş statusunun yoxlanılması                                       |            `/api/1/get-status`            |            :x:            |
| [`save_card`][integrify.epoint.client.EPointClientClass.save_card]                                 | Ödəniş olmadan kartı yadda saxlamaq                                  |        `/api/1/card-registration`         | :fontawesome-solid-check: |
| [`pay_with_saved_card`][integrify.epoint.client.EPointClientClass.pay_with_saved_card]             | Saxlanılan kartla ödəniş                                             |           `/api/1/execute-pay`            |            :x:            |
| [`pay_and_save_card`][integrify.epoint.client.EPointClientClass.pay_and_save_card]                 | Ödəniş etmə və kartı yadda saxlamaq                                  |    `/api/1/card-registration-with-pay`    | :fontawesome-solid-check: |
| [`payout`][integrify.epoint.client.EPointClientClass.payout]                                       | Vəsaitlərin köçürülməsi                                              |          `/api/1/refund-request`          |            :x:            |
| [`refund`][integrify.epoint.client.EPointClientClass.refund]                                       | Ödənişi tam və ya yarımçıq geri qaytarma                             |             `/api/1/reverse`              |            :x:            |
| [`split_pay`][integrify.epoint.client.EPointClientClass.split_pay]                                 | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə                    |          `/api/1/split-request`           | :fontawesome-solid-check: |
| [`split_pay_with_saved_card`][integrify.epoint.client.EPointClientClass.split_pay_with_saved_card] | Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə |        `/api/1/split-execute-pay`         |            :x:            |
| [`split_pay_and_save_card`][integrify.epoint.client.EPointClientClass.split_pay_and_save_card]     | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlamaq  | `/api/1/split-card-registration-with-pay` | :fontawesome-solid-check: |

## Callback Sorğusu { #callback-request }

Bəzi sorğular müştəri məlumat daxil etdikdən və arxa fonda bank işləmləri bitdikdən sonra, tranzaksiya haqqında məlumat sizin EPoint dashboard-da qeyd etdiyiniz `callback` URL-ə POST sorğusu göndərilir. Data siz adətən sorğu göndərdiyiniz formatda gəlir:

```python
{
    'data': 'base64data'
    'signature': 'sha1signature'
}
```

Bu data-nı `signature`-ni yoxladıqdan sonra, decode etmək lazımdır. Callback üçün API yazdıqda, datanı alıb, `helpers.py`-dakı [`decode_callback_data`][integrify.epoint.helpers.decode_callback_data] funksiyası ilə həm signature yoxlanması həm də datanın decode-unu edə bilərsiniz. Bu funksiya sizə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema] formatında decode olunmuş datanı qaytarır.

> **Qeyd**
>
> FastAPI istifadəçiləri kiçik "shortcut"-dan istifadə edə bilərlər:
>
> ```python
> from fastapi import Fastapi, APIRouter, Depends
> from integrify.epoint.schemas.callback import DecodedCallbackDataSchema
> from integrify.epoint.helpers import decode_callback_data
>
> router = APIRouter()
>
> @router.post('/epoint/callback')
> async def epoint_callback(data: DecodedCallbackDataSchema = Depends(decode_callback_data)):
>    ...
> ```
>
> Funksiyanı belə yazdıqda, data avtomatik signature-i yoxlanaraq decode edilir.

---

## Callback Data formatı { #callback-data-format }

Nə sorğu göndərməyinizdən asılı olaraq, callback-ə gələn data biraz fərqlənə bilər. [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema] bütün bu dataları özündə cəmləsə də, hansı fieldlərin gəlməyəcəyini (yəni, decode-dan sonra `None` olacağını) bilmək yaxşı olar. Ümumilikdə, mümkün olacaq datalar bunlardır:

| Dəyişən adı      | İzahı                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| status           | Success və ya failed əməliyyatının nəticəsi                                                             |
| message          | Ödənişin icra statusu haqqında mesaj                                                                    |
| code             | Bankın cavab kodu. 3 rəqəmli koddan, xəta/uğur mesajına çevrilir.                                       |
| transaction      | Epoint xidmətinin əməliyyat IDsi                                                                        |
| bank_transaction | Bank ödəniş əməliyyatı IDsi                                                                             |
| bank_response    | Ödəniş icrasının nəticəsi ilə bankın cavabı                                                             |
| operation_code   | 001-kart qeydiyyatı\n100- istifadəçi ödənişi                                                            |
| rrn              | Retrieval Reference Number - unikal əməliyyat identifikator. Yalnız uğurlu bir əməliyyat üçün mövcuddur |
| card_mask        | Ödəniş səhifəsində göstərilən istifadəçi adı                                                            |
| card_name        | 123456******1234 formatında əks edilən kart maskası                                                     |
| amount           | Ödəniş məbləği                                                                                          |
| order_id         | Tətbiqinizdə unikal əməliyyat ID                                                                        |
| card_id          | Ödənişləri yerinə yetirmək üçün istifadə edilm lazım olan unikal kart identifikatoru                    |
| split_amount     | İkinci istifadəçi üçün ödəniş məbləği                                                                   |
| other_attr       | Əlavə göndərdiyiniz seçimlər                                                                            |

Sorğudan asılı olaraq, bu data-lar callback-də **GƏLMİR** (yəni, avtomatik `None` dəyəri alır):

| Sorğu metodu              | Callback-də gəlməyəcək datalar                    |
| :------------------------ | :------------------------------------------------ |
| `pay`                     | `card_id`, `split_amount`                         |
| `save_card`               | `order_id`, `transaction`, `amount`, `other_attr` |
| `pay_and_save_card`       | `message`                                         |
| `split_pay`               | -                                                 |
| `split_pay_and_save_card` | `message`                                         |

> **Qeyd**
>
> Qalan bütün data-lar sorğu success olduqda gəlir, əks halda, onlar da `None` dəyəri alır.
