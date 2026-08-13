# Integrify PostaGuvercini

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana PostaGuvercini inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>
<p align="center">
<a href="https://github.com/Integrify-SDK/integrify-postaguvercini-python/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-postaguvercini-python/actions/workflows/test.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://github.com/Integrify-SDK/integrify-postaguvercini-python/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-postaguvercini-python/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/integrify-postaguvercini" target="_blank">
  <img src="https://img.shields.io/pypi/v/integrify-postaguvercini?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.netlify.com/sites/integrify-docs/deploys">
  <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
</a>
</p>
<p align="center">
<a href="https://pepy.tech/project/integrify-postaguvercini" target="_blank">
  <img src="https://static.pepy.tech/badge/integrify-postaguvercini" alt="Downloads">
</a>
<a href="https://pypi.org/project/integrify-postaguvercini" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/integrify-postaguvercini.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Integrify-SDK/integrify-postaguvercini-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Integrify-SDK/integrify-postaguvercini-python.svg" alt="Coverage">
</a>

</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/postaguvercini/about/](https://integrify.mmzeynalli.dev/integrations/postaguvercini/about/)

**Kod**: [https://github.com/Integrify-SDK/integrify-postaguvercini-python](https://github.com/Integrify-SDK/integrify-postaguvercini-python)

---

## Rəsmi Dokumentasiya (v1)

[İngliscə](https://www.poctgoyercini.com/api_json/swagger/ui/index#/)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-epoint
```

</div>

## İstifadəsi

Bu sorğulardan istifadə edə bilmək üçün, düzgün "environment variable"-ları quraşdırmalısınız. Daha ətraflı [burdan](https://integrify.mmzeynalli.dev/integrations/posta-guvercini/env.md) oxuya bilərsiniz.

### Sorğular listi

| Sorğu metodu        | Məqsəd                            |        PostaGuvercini API        |
| :------------------ | :-------------------------------- | :------------------------------: |
| `send_single_sms`   | Tək nömrəyə sms göndərilməsi      |   `/api_json/v1/Sms/Send_1_N`    |
| `send_multiple_sms` | Bir neçə nömrəyə sms göndərilməsi |   `/api_json/v1/Sms/Send_N_N`    |
| `get_status`        | SMS-in statusunu yoxlamaq         |    `/api_json/v1/Sms/Status`     |
| `credit_balance`    | Balansın yoxlanılması             | `/api_json/v1/Sms/CreditBalance` |

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
