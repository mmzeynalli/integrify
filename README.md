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

```shell
$ pip install integrify
```

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

| Servis |   Əsas sorğular    | Bütün sorğular | Dokumentləşdirilmə | Link                                                                       |
| ------ | :----------------: | :------------: | ------------------ | -------------------------------------------------------------------------- |
| EPoint | :heavy_check_mark: |      :x:       | Tam                | [Docs](https://github.com/mmzeynalli/integrify/tree/main/integrify/epoint) |
