# EPoint

Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `EPOINT_PUBLIC_KEY`, `EPOINT_PRIVATE_KEY`

EPoint interfeysinin dilini dəyişmək istəyirsinizsə, `EPOINT_INTERFACE_LANG` "environment variable"-na dəyər verin. Default olaraq, Azərbaycan dili olacaq.

Sorğular uğurlu və ya uğursuz olduqda, spesifik URL-ə yönləndirmək istəyirsinizsə, bu dəyişənlərə də mühit levelində dəyər verin: EPOINT_SUCCESS_REDIRECT_URL, EPOINT_FAILED_REDIRECT_URL

## Sorğular listi

| Sorğu class-ı                        | Məqsəd                                                               |                EPoint API                 | Callback-ə sorğu atılır |
| :----------------------------------- | :------------------------------------------------------------------- | :---------------------------------------: | :---------------------: |
| `EPointPaymentRequest`               | Ödəniş                                                               |             `/api/1/request`              |   :heavy_check_mark:    |
| `EPointGetTransactionStatusRequest`  | Ödəniş statusunun yoxlanılması                                       |            `/api/1/get-status`            |           :x:           |
| `EPointSaveCardRequest`              | Ödəniş olmadan kartı yadda saxlamaq                                  |        `/api/1/card-registration`         |   :heavy_check_mark:    |
| `EPointPayWithSavedCardRequest`      | Saxlanılan kartla ödəniş                                             |           `/api/1/execute-pay`            |           :x:           |
| `EPointPayAndSaveCardRequest`        | Ödəniş etmə və kartı yadda saxlamaq                                  |    `/api/1/card-registration-with-pay`    |   :heavy_check_mark:    |
| `EPointPayoutRequest`                | Vəsaitlərin köçürülməsi                                              |          `/api/1/refund-request`          |           :x:           |
| `EPointRefundRequest`                | Ödənişi tam və ya yarımçıq geri qaytarma                             |             `/api/1/reverse`              |           :x:           |
| `EPointSplitPaymentRequest`          | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə                    |          `/api/1/split-request`           |   :heavy_check_mark:    |
| `EPointSplitPayWithSavedCardRequest` | Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə |        `/api/1/split-execute-pay`         |           :x:           |
| `EPointSplitPayAndSaveCardRequest`   | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlamaq  | `/api/1/split-card-registration-with-pay` |   :heavy_check_mark:    |

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
