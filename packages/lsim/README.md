# Integrify LSIM

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana LSIM inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>
<p align="center">
<a href="https://github.com/Integrify-SDK/integrify-lsim-python/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-lsim-python/actions/workflows/test.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://github.com/Integrify-SDK/integrify-lsim-python/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-lsim-python/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/integrify-lsim" target="_blank">
  <img src="https://img.shields.io/pypi/v/integrify-lsim?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.netlify.com/sites/integrify-docs/deploys">
  <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
</a>
</p>
<p align="center">
<a href="https://pepy.tech/project/integrify-lsim" target="_blank">
  <img src="https://static.pepy.tech/badge/integrify-lsim" alt="Downloads">
</a>
<a href="https://pypi.org/project/integrify-lsim" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/integrify-lsim.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Integrify-SDK/integrify-lsim-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Integrify-SDK/integrify-lsim-python.svg" alt="Coverage">
</a>

</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/lsim/about/](https://integrify.mmzeynalli.dev/integrations/lsim/about/)

**Kod**: [https://github.com/Integrify-SDK/integrify-lsim-python](https://github.com/Integrify-SDK/integrify-lsim-python)

---

## Rəsmi Dokumentasiya (v2024.11.22)

[İngliscə](https://mmzeynalli.notion.site/LSIM-1974f14f727e8029a3f5f9e4e556afe3?pvs=74)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-lsim
```

</div>

## İstifadəsi

Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `LSIM_LOGIN`, `LSIM_PASSWORD`, `LSIM_SENDER_NAME`

### Sorğular listi

### Tək SMS sorğuları

| Sorğu metodu      | Məqsəd                                            |          LSIM API          |
| :---------------- | :------------------------------------------------ | :------------------------: |
| `send_sms_get`    | GET sorğusu ilə SMS göndərilmə                    |    `/quicksms/v1/send`     |
| `send_sms_post`   | POST sorğusu ilə SMS göndərilmə                   |  `/quicksms/v1/smssender`  |
| `check_balance`   | Balansı yoxlamaq                                  |   `/quicksms/v1/balance`   |
| `get_report_get`  | GET sorğusu ilə göndərilmiş SMS haqqında məlumat  |   `/quicksms/v1/report`    |
| `get_report_post` | POST sorğusu ilə göndərilmiş SMS haqqında məlumat | `/quicksms/v1/smsreporter` |

### Toplu SMS sorğuları

| Sorğu metodu                     | Məqsəd                                              |   LSIM API   |
| :------------------------------- | :-------------------------------------------------- | :----------: |
| `bulk_send_one_message`          | Toplu şəkildə hamıya eyni SMS göndərilmə            | `/smxml/api` |
| `bulk_send_different_messages`   | Toplu şəkildə hərəyə fərqli SMS göndərilmə          | `/smxml/api` |
| `get_report`                     | Toplu göndərilmiş SMS-in reportu                    | `/smxml/api` |
| `get_detailed_report`            | Toplu göndərilmiş SMS-in detallı reportu            | `/smxml/api` |
| `get_detailed_report_with_dates` | Toplu göndərilmiş SMS-in detallı və tarixli reportu | `/smxml/api` |
| `check_balance`                  | Balansı yoxlamaq                                    | `/smxml/api` |

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

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
