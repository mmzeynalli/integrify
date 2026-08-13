# Integrify KapitalBank

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/Integrify-SDK/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana KapitalBank inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>
<p align="center">
<a href="https://github.com/Integrify-SDK/integrify-kapitalbank-python/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-kapitalbank-python/actions/workflows/test.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://github.com/Integrify-SDK/integrify-kapitalbank-python/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/Integrify-SDK/integrify-kapitalbank-python/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/integrify-kapitalbank" target="_blank">
  <img src="https://img.shields.io/pypi/v/integrify-kapitalbank?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.netlify.com/sites/integrify-docs/deploys">
  <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
</a>
</p>
<p align="center">
<a href="https://pepy.tech/project/integrify-kapitalbank" target="_blank">
  <img src="https://static.pepy.tech/badge/integrify-kapitalbank" alt="Downloads">
</a>
<a href="https://pypi.org/project/integrify-kapitalbank" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/integrify-kapitalbank.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Integrify-SDK/integrify-kapitalbank-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Integrify-SDK/integrify-kapitalbank-python.svg" alt="Coverage">
</a>

</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/kapitalbank/about/](https://integrify.mmzeynalli.dev/integrations/kapitalbank/about/)

**Kod**: [https://github.com/Integrify-SDK/integrify-kapitalbank-python](https://github.com/Integrify-SDK/integrify-kapitalbank-python)

---

## Rəsmi Dokumentasiya (v1.0.3)

[Azərbaycanca, İngliscə, Rusca](https://pg.kapitalbank.az/docs)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-kapitalbank
```

</div>

## İstifadəsi

Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `KAPITAL_USERNAME`, `KAPITAL_PASSWORD`

Əlavə olaraq `KAPITAL_ENV` dəyişənini də təyin etməlisiniz. Default olaraq saxlasaz test mühitindən istifadə edəcəksiniz. Əks halda, `prod` dəyərini təyin etməlisiniz.

Kapital interfeysinin dilini dəyişmək istəyirsinizsə, `KAPITAL_INTERFACE_LANG` "environment variable"-na dəyər verin. Default olaraq, Azərbaycan dili olacaq.

Sorğular uğurlu və ya uğursuz olduqda, spesifik URL-ə yönləndirmək istəyirsinizsə, bu dəyişənlərə də mühit levelində dəyər verin: `KAPITAL_REDIRECT_URL`

### Sorğular listi

| Sorğu metodu              | Məqsəd                                             |            Kapital API            | Callback-ə sorğu atılır |
| :------------------------ | :------------------------------------------------- | :-------------------------------: | :---------------------: |
| `create_order`            | Ödəniş                                             |           `/api/order`            |            ✅            |
| `get_order_information`   | Ödəniş haqda qısa məlumat                          |      `/api/order/{order_id}`      |            ❌            |
| `get_detailed_order_info` | Ödəniş haqda detallı məlumat                       |      `/api/order/{order_id}`      |            ❌            |
| `refund_order`            | Geri ödəniş sorğusu                                | `/api/order/{order_id}/exec-tran` |            ❌            |
| `save_card`               | Kartı saxlamaq üçün ödəniş sorğusu                 |           `/api/order`            |            ✅            |
| `pay_and_save_card`       | Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu |           `/api/order`            |            ✅            |
| `full_reverse_order`      | Ödənişi ləğv etmək üçün sorğu                      | `/api/order/{order_id}/exec-tran` |            ❌            |
| `clearing_order`          | Ödənişin təsdiq edilməsi üçün sorğu                | `/api/order/{order_id}/exec-tran` |            ❌            |
| `pay_with_saved_card`     | Ödənişin hissəsini ləğv etmək üçün sorğu           | `/api/order/{order_id}/exec-tran` |            ❌            |

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
