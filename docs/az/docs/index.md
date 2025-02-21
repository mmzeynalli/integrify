<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır.</em>
</p>
<p  style='display:flex;flex-wrap:wrap;gap:5px;width:70%;justify-content:flex-start;margin: 0 auto;'>
<a href="https://github.com/mmzeynalli/integrify/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/mmzeynalli/integrify/actions/workflows/test.yml/badge.svg?branch=main" alt="Test">
</a>
<a href="https://github.com/mmzeynalli/integrify/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/mmzeynalli/integrify/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/integrify" target="_blank">
  <img src="https://img.shields.io/pypi/v/integrify?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://app.netlify.com/sites/integrify-docs/deploys">
  <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
</a>
<a href="https://pepy.tech/project/integrify" target="_blank">
  <img src="https://static.pepy.tech/badge/integrify" alt="Downloads">
</a>
<a href="https://pypi.org/project/integrify" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/integrify.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/mmzeynalli/integrify" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/mmzeynalli/integrify.svg" alt="Coverage">
</a>

</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev](https://integrify.mmzeynalli.dev)

**Kod**: [https://github.com/mmzeynalli/integrify](https://github.com/mmzeynalli/integrify)

---

## Əsas özəlliklər { #main-features }

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

---

## Kitabxananın yüklənməsi { #installation }

<div class="termy">

```console
$ pip install integrify
```

</div>

## İstifadəsi { #usage }

Məsələn, EPoint üçün sorğuları istifadə etmək istərsək:

### Sync

```python
from integrify.epoint import EPointRequest

resp = EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
print(resp.ok, resp.body)

```

### Async

```python
from integrify.epoint import EPointAsyncRequest

# Async main loop artıq başlamışdır
resp = await EPointAsyncRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
print(resp.ok, resp.body)

```

### Sorğu cavabı { #request-response }

Yuxarıdakı sorğuların (və ya istənilən sorğunun) cavab formatı `ApiResponse` class-ıdır:

```python
class ApiResponse:
    ok: bool
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: Dəyişkən
    """Cavab sorğusunun body-si"""
```

???+ warning
    Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.'

## Dəstəklənən API inteqrasiyaları

| Servis      |                                                 Əsas sorğular                                                 |                                                Bütün sorğular                                                 | Dokumentləşdirilmə                                                                                            | Real mühitdə test                                                                                             | Əsas developer                                    |
| ----------- | :-----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| EPoint      |                                              :white_check_mark:                                               | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Tam](https://integrify.mmzeynalli.dev/epoint/about/)                                                         | :white_check_mark:                                                                                            | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| KapitalBank |                                              :white_check_mark:                                               |                                              :white_check_mark:                                               | [Tam](https://integrify.mmzeynalli.dev/kapital/about/)                                                        | :white_check_mark:                                                                                            | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| LSIM        |                                              :white_check_mark:                                               |                                              :white_check_mark:                                               | [Tam](https://integrify.mmzeynalli.dev/lsim/about/)                                                           | :white_check_mark:                                                                                            | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| Azericard   | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| Payriff     | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg) | [Vahid Həsənzadə](https://github.com/vahidzhe)    |
