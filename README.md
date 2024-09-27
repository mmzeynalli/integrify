<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır.</em>
</p>
<p align="center">
  <a href="https://app.netlify.com/sites/integrify-docs/deploys">
    <img src="https://api.netlify.com/api/v1/badges/d8931b6a-80c7-41cb-bdbb-bf6ef5789f80/deploy-status" alt="Netlify Status">
  </a>
</p>

# Integrify

Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır.

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev](https://integrify.mmzeynalli.dev)

**Kod**: [https://github.com/mmzeynalli/integrify](https://github.com/mmzeynalli/integrify)

---

## Kitabxananın yüklənməsi

<div class="termy">

```console
$ pip install integrify
```

</div>

## İstifadəsi

Məsələn, EPoint üçün sorğuları istifadə etmək istərsək:

### Sync

```python
from integrify.epoint import EPointRequest

resp = EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
print(resp.ok, resp.body)

```

### Async

```python
from integrify.epoint.asyncio import EPointRequest

# Async main loop artıq başlamışdır
resp = await EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
print(resp.ok, resp.body)

```

### Sorğu cavabı

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

## Dəstəklənən API inteqrasiyaları

| Servis  |                                             Əsas sorğular                                             |                                            Bütün sorğular                                             | Dokumentləşdirilmə | Link                                                                                                  |
| ------- | :---------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------: | ------------------ | ----------------------------------------------------------------------------------------------------- |
| EPoint  |                                          :heavy_check_mark:                                           | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/assets/spinner-solid.svg) | Tam                | [Docs](https://github.com/mmzeynalli/integrify/tree/main/integrify/epoint)                            |
| Payriff | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/assets/spinner-solid.svg) | Tam                | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/assets/spinner-solid.svg) |
