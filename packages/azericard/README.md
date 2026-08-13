# Integrify Azericard

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana Azericard inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>
<p align="center">
<a href="https://github.com/Integrify-SDK/integrify-azericard-python/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-azericard-python/actions/workflows/test.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://github.com/Integrify-SDK/integrify-azericard-python/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-azericard-python/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/integrify-azericard" target="_blank">
  <img src="https://img.shields.io/pypi/v/integrify-azericard?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.netlify.com/sites/integrify-docs/deploys">
  <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
</a>
</p>
<p align="center">
<a href="https://pepy.tech/project/integrify-azericard" target="_blank">
  <img src="https://static.pepy.tech/badge/integrify-azericard" alt="Downloads">
</a>
<a href="https://pypi.org/project/integrify-azericard" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/integrify-azericard.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Integrify-SDK/integrify-azericard-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Integrify-SDK/integrify-azericard-python.svg" alt="Coverage">
</a>

</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/azericard/about/](https://integrify.mmzeynalli.dev/integrations/azericard/about/)

**Kod**: [https://github.com/Integrify-SDK/integrify-azericard-python](https://github.com/Integrify-SDK/integrify-azericard-python)

---

## Rəsmi Dokumentasiya (v2024.11.6)

[Azərbaycanca](https://developer.azericard.com/az)

[İngliscə](https://developer.azericard.com/en)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-azericard
```

</div>

## İstifadəsi

Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `AZERICARD_KEY_FILE_PATH`.

Bu sorğulardan rahat istifadə etmək üçün, qeyd olunan dəyərləri "environment variable"-larına əlavə etməyiniz məsləhət görülür: `AZERICARD_MERCHANT_ID` (Terminal ID), `AZERICARD_MERCHANT_NAME`, `AZERICARD_MERCHANT_URL`, `AZERICARD_CALLBACK_URL` (backref). Əks halda bu dəyərləri funksiyaları istifadə edərkən parametr kimi göndərməlisiniz.

AzeriCardClientClass interfeysinin dilini dəyişmək istəyirsinizsə, `AZERICARD_INTERFACE_LANG` "environment variable"-na dəyər verin, və ya hər sorğuda dil parametrini göndərin. Default olaraq, Azərbaycan dili olacaq.

### Sorğular listi

| Sorğu metodu             | Məqsəd                                               |                      Azericard API                       |
| :----------------------- | :--------------------------------------------------- | :------------------------------------------------------: |
| `authorization`          | Ödəniş/Bloklama                                      | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='1')`  |
| `auth_and_save_card`     | Ödəniş/Bloklama və kartı yadda saxlamaq              | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='1')`  |
| `auth_with_saved_card`   | Saxlanılan kartla ödəniş/bloklama                    | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='1')`  |
| `finalize`               | Blok olunmuş məbləği qəbul ETMƏMƏK (offline) sorğusu | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='24')` |
| `get_transaction_status` | Ödəniş statusunun yoxlanılması                       | `https://mpi.3dsecure.az/cgi-bin/cgi_link (TRTYPE='90')` |
| `transfer_start`         | Müştəriyə pul köçürülmə prosesinin başladılması      |         `https://mt.azericard.com/payment/view`          |
| `transfer_confirm`       | Müştəriyə pul köçürülmə prosesini təsdiqləmə         |          `https://mt.azericard.com/api/confirm`          |
| `transfer_decline`       | Müştəriyə pul köçürülmə prosesini imtina etmə        |          `https://mt.azericard.com/api/decline`          |

### Sorğu göndərmək axını

Nəzərə alsaq ki, Azericard form submission qəbul edərək, sizə redirectsiz səhifəni açır, form-u backend-dən submit etmık mümkün deyil, məhz front tərəfdən olmalıdır. Ona görə, başqa inteqrasiyalardan fərqli olaraq, Azericard-da kitabxana sorğu atmır, form-da göndərilməli olan data-nı qaytarır. Format JSON olsa da, köməkçi funksiyadan istifadə edərək, HTML formu alın, front-a response kimi göndərə bilərsiniz:

```python
from integrify.azericard.client import AzericardClient
from integrify.azericard.helpers import json_to_html_form

req = AzericardClient.pay(
    amount=1,
    currency='AZN',
    order='12345678',
    desc='test',
    country='AZ',
)

form = json_to_html_form(req)
print(form)  # <form action="https://testmpi.3dsecure.az/cgi-bin/cgi_link" method="POST">
             #   <input type="hidden" name="ORDER" value="12345678"> ...
```

### Callback Sorğusu

Bəzi sorğular müştəri məlumat daxil etdikdən və arxa fonda bank işləmləri bitdikdən sonra, tranzaksiya haqqında məlumat sizin mühit dəyişənində (və ya sorğuda) qeyd etdiyiniz callback URL-ə POST sorğusu göndərilir. Hər datada PSIGN field-i vardır ki, sizin server tərəfindən scamming-in qarşısını almaq üçün düzgün olub-olmadığını yoxlamalısınız.

> **Qeyd**
>
> FastAPI istifadəçiləri kiçik "shortcut"-dan istifadə edə bilərlər:
>
> ```python
> from fastapi import Fastapi, APIRouter, Depends
> from integrify.azericard.schemas.callback import AuthCallbackWithCardDataSchema
>
> router = APIRouter()
>
> @router.post('/azericard/callback')
> async def azericard_callback(data: AuthCallbackWithCardDataSchema):
>    ...
> ```

### Callback Data formatı

Nə sorğu göndərməyinizdən asılı olaraq, callback-ə gələn data biraz fərqlənə bilər. [`AuthCallbackWithCardDataSchema`][integrify.azericard.schemas.callback.AuthCallbackWithCardDataSchema] bütün bu dataları özündə cəmləsə də, hansı fieldlərin gəlməyəcəyini (yəni, decode-dan sonra `None` olacağını) bilmək yaxşı olar. Ümumilikdə, mümkün olacaq datalar bunlardır:

| Dəyişən adı | İzahı                                                                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `terminal`  | Sorğudan əks etdirilməsi Terminal ID                                                                                                           |
| `trtype`    | Sorğudan əks etdirilməsi Transaction Type                                                                                                      |
| `order`     | Sorğudan əks etdirilməsi order id                                                                                                              |
| `amount`    | İcazə verilən məbləğ. Adətən, orijinal məbləğə və alıcının haqqına bərabər olacaq.                                                             |
| `currency`  | Sorğudan əks etdirilməsi ödəniş məzənnəsi                                                                                                      |
| `action`    | EGateway fəaliyyət kodu                                                                                                                        |
| `rc`        | Əməliyyat cavab kodu (ISO-8583 Sahə 39)                                                                                                        |
| `approval`  | Müştəri bankının təsdiq kodu (ISO-8583 Sahə 38). Kart idarəetmə sistemi tərəfindən təmin edilmədikdə boş ola bilər.                            |
| `rrn`       | Müştəri bankının axtarış istinad nömrəsi (ISO-8583 Sahə 37)                                                                                    |
| `int_ref`   | Elektron ticarət şlüzünün daxili istinad nömrəsi                                                                                               |
| `timestamp` | GMT-də e-ticarət şlüzünün vaxt damğası:: YYYYMMDDHHMMSS                                                                                        |
| `nonce`     | E-Commerce Gateway qeyri-dəyərlidir. Hexadecimal formatda 8-32 gözlənilməz təsadüfi baytla doldurulacaq. MAC istifadə edildikdə mövcud olacaq. |
| `card`      | 123456******1234 formatında əks edilən kart maskası                                                                                            |
| `token`     | Saxlanılacaq kartın TOKEN parametri                                                                                                            |
| `p_sign`    | Onaltılıq formada E-Commerce Gateway MAC (Message Authentication Code). MAC istifadə edildikdə mövcud olacaq.                                  |

Sorğudan asılı olaraq, bu data-lar callback-də **GƏLMİR** (yəni, avtomatik `None` dəyəri alır):

| Sorğu metodu           | `None` field-lər |
| :--------------------- | :--------------- |
| `authorization`        | `card`, `token`  |
| `auth_and_save_card`   | -                |
| `auth_with_saved_card` | -                |
| `finalize`             | `card`, `token`  |

## Dəstəklənən başqa API inteqrasiyaları

<!-- AUTO-UPDATE SECTION -->
| Servis                                                                              |                                                        Əsas sorğular                                                         |                                                        Bütün sorğular                                                        | Dokumentləşdirilmə                                                                                                           | Real mühitdə test                                                                                                            | Əsas developer                                    |
| ----------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [EPoint](https://github.com/Integrify-SDK/integrify-epoint-python)                  |                                                              ✅                                                               | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Tam](https://integrify.mmzeynalli.dev/integrations/epoint/about/)                                                           | ✅                                                                                                                            | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [KapitalBank](https://github.com/Integrify-SDK/integrify-kapitalbank-python)        |                                                              ✅                                                               |                                                              ✅                                                               | [Tam](https://integrify.mmzeynalli.dev/integrations/kapital/about/)                                                          | ✅                                                                                                                            | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| [LSIM](https://github.com/Integrify-SDK/integrify-lsim-python)                      |                                                              ✅                                                               |                                                              ✅                                                               | [Tam](https://integrify.mmzeynalli.dev/integrations/lsim/about/)                                                             | ✅                                                                                                                            | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [Posta Guvercini](https://github.com/Integrify-SDK/integrify-postaguvercini-python) |                                                              ✅                                                               |                                                              ✅                                                               | [Tam](https://integrify.mmzeynalli.dev/integrations/posta-guvercini/about/)                                                  | ✅                                                                                                                            | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| [Azericard](https://github.com/Integrify-SDK/integrify-azericard-python)            |                                                              ✅                                                               | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Tam](https://integrify.mmzeynalli.dev/integrations/azericard/about)                                                         | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [Payriff](https://github.com/Integrify-SDK/integrify-payriff-python)                | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Vahid Həsənzadə](https://github.com/vahidzhe)    |
