# EPoint Callback Məntiqi

## Sorğular listi

| Sorğu class-ı                        | Məqsəd                                                               |                EPoint API                 | Callback-ə sorğu atılır |
| :----------------------------------- | :------------------------------------------------------------------- | :---------------------------------------: | :---------------------: |
| `EPointPaymentRequest`               | Ödəniş                                                               |             `/api/1/request`              |      <li>[x]</li>       |
| `EPointGetTransactionStatusRequest`  | Ödəniş statusunun yoxlanılması                                       |            `/api/1/get-status`            |      <li>[ ]</li>       |
| `EPointSaveCardRequest`              | Ödəniş olmadan kartı yadda saxlamaq                                  |        `/api/1/card-registration`         |      <li>[x]</li>       |
| `EPointPayWithSavedCardRequest`      | Saxlanılan kartla ödəniş                                             |           `/api/1/execute-pay`            |      <li>[ ]</li>       |
| `EPointPayAndSaveCardRequest`        | Ödəniş etmə və kartı yadda saxlamaq                                  |    `/api/1/card-registration-with-pay`    |      <li>[x]</li>       |
| `EPointPayoutRequest`                | Vəsaitlərin köçürülməsi                                              |          `/api/1/refund-request`          |      <li>[ ]</li>       |
| `EPointRefundRequest`                | Ödənişi tam və ya yarımçıq geri qaytarma                             |             `/api/1/reverse`              |      <li>[ ]</li>       |
| `EPointSplitPaymentRequest`          | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə                    |          `/api/1/split-request`           |      <li>[x]</li>       |
| `EPointSplitPayWithSavedCardRequest` | Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə |        `/api/1/split-execute-pay`         |      <li>[ ]</li>       |
| `EPointSplitPayAndSaveCardRequest`   | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlamaq  | `/api/1/split-card-registration-with-pay` |      <li>[x]</li>       |

## Callback Sorğusu

Bəzi sorğular müştəri məlumat daxil etdikdən və arxa fonda bank işləmləri bitdikdən sonra, tranzaksiya haqqında məlumat sizin EPoint dashboard-da qeyd etdiyiniz `callback` URL-ə POST sorğusu göndərilir. Data siz adətən sorğu göndərdiyiniz formatda gəlir:

```python
{
    'data': 'base64data'
    'signature': 'sha1signature'
}
```

Bu data-nı `signature`-ni yoxladıqdan sonra, decode etmək lazımdır. Callback üçün API yazdıqda, datanı alıb, `helper.py`-dakı `decode_callback_data` funksiyası ilə həm signature yoxlanması həm də datanın decode-unu edə bilərsiniz. Bu funksiya sizə `EPointDecodedCallbackDataSchema` formatında decode olunmuş datanı qaytarır.

> **Qeyd**
>
> FastAPI istifadəçiləri kiçik "shortcut"-dan istifadə edə bilərlər:
>
> ```python
> @router.post('/epoint/callback')
> async def epoint_callback(data: EPointDecodedCallbackDataSchema = Depends(decode_callback_data)):
> ```
>
> Funksiyanı belə yazdıqda, data avtomatik signature-i yoxlanaraq decode edilir.

---

## Callback Data formatı

Nə sorğu göndərməyinizdən asılı olaraq, callback-ə gələn data biraz fərqlənə bilər. `EPointDecodedCallbackDataSchema` bütün bu dataları özündə cəmləsə də, hansı fieldlərin gəlməyəcəyini (yəni, decode-dan sonra `None` olacağını) bilmək yaxşı olar. Ümumilikdə, mümkün olacaq datalar bunlardır:

```text
status -> Success və ya failed əməliyyatının nəticəsi
message -> Ödənişin icra statusu haqqında mesaj
code -> Bankın cavab kodu. 3 rəqəmli koddan, xəta/uğur mesajına çevrilir.
transaction -> Epoint xidmətinin əməliyyat IDsi
bank_transaction -> Bank ödəniş əməliyyatı IDsi
bank_response -> Ödəniş icrasının nəticəsi ilə bankın cavabı
operation_code -> 001-kart qeydiyyatı\n100- istifadəçi ödənişi
rrn -> Retrieval Reference Number - unikal əməliyyat identifikator. Yalnız uğurlu bir əməliyyat üçün mövcuddur
card_mask -> Ödəniş səhifəsində göstərilən istifadəçi adı
card_name -> 123456******1234 formatında əks edilən kart maskası
amount -> Ödəniş məbləği
order_id -> Tətbiqinizdə unikal əməliyyat ID
card_id -> Ödənişləri yerinə yetirmək üçün istifadə edilm lazım olan unikal kart identifikatoru
split_amount -> İkinci istifadəçi üçün ödəniş məbləği
other_attr -> Əlavə göndərdiyiniz seçimlər
```

Sorğudan asılı olaraq, bu data-lar callback-də **GƏLMİR** (yəni, avtomatik `None` dəyəri alır):

| Sorğu class-ı                      | Callback-də gəlməyəcək datalar                    |
| :--------------------------------- | :------------------------------------------------ |
| `EPointPaymentRequest`             | `card_id`, `split_amount`                         |
| `EPointSaveCardRequest`            | `order_id`, `transaction`, `amount`, `other_attr` |
| `EPointPayAndSaveCardRequest`      | `message`                                         |
| `EPointSplitPaymentRequest`        | -                                                 |
| `EPointSplitPayAndSaveCardRequest` | `message`                                         |

> **Qeyd**
>
> Qalan bütün data-lar sorğu success olduqda gəlir, əks halda, onlar da `None` dəyəri alır.
