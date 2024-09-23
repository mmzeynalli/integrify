# Integrify

Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır.

## Əsas özəlliklər { #esas-ozellikler }

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev](https://integrify.mmzeynalli.dev)

**Kod**: [https://github.com/mmzeynalli/integrify](https://github.com/mmzeynalli/integrify)

---

## Kitabxananın yüklənməsi { #kitabxananin-yuklenmesi }

<div class="termy">

```console
$ pip install integrify

---> 100%
```

</div>

## İstifadəsi { #istifadesi }

Məsələn, EPoint üçün sorğuları istifadə etmək istərsək:

### Sync

```python
from integrify.epoint.payment import EPointPaymentRequest

resp = EPointPaymentRequest(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')()
print(resp.ok, resp.body)

```

### Async

```python
from integrify.epoint.asyncio.payment import EPointPaymentRequest

# Async main loop artıq başlamışdır
resp = await EPointPaymentRequest(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')()
print(resp.ok, resp.body)

```

### Sorğu cavabı { #sorgu-cavabi }

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

## Dəstəklənən API inteqrasiyaları { #desteklenen-api-inteqrasiyalari }

| Servis |   Əsas sorğular    | Bütün sorğular | Dokumentləşdirilmə | Link                                                                       |
| ------ | :----------------: | :------------: | ------------------ | -------------------------------------------------------------------------- |
| EPoint | :fontawesome-solid-check:  |      :x:       | Tam                | [Docs](api_reference/epoint.md) |
