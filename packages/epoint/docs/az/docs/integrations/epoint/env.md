# EPoint mühit dəyişənləri

## Haqqında

Aşağıdakı cədvəldə bütün mühit dəyişənləri ilə tanış ola bilərsiniz.

| Dəyişənin adı               | Məcburi?                  |                           Mənası                           | Default dəyəri |
| :-------------------------- | :------------------------ | :--------------------------------------------------------: | :------------: |
| EPOINT_PUBLIC_KEY           | :fontawesome-solid-check: |           EPoint tərəfindən verilmiş public açar           |      `-`       |
| EPOINT_PRIVATE_KEY          | :fontawesome-solid-check: |          EPoint tərəfindən verilmiş private açar           |      `-`       |
| EPOINT_INTERFACE_LANG       | :x:                       |     İstifadəçilərin yönələcəyi EPoint səhifəsinin dili     |      `az`      |
| EPOINT_SUCCESS_REDIRECT_URL | :x:                       | İstifadəçilərin **uğurlu** ödənişdən sonra yönələcəyi url  |      `-`       |
| EPOINT_FAILED_REDIRECT_URL  | :x:                       | İstifadəçilərin **uğursuz** ödənişdən sonra yönələcəyi url |      `-`       |

## .env template

```text
EPOINT_PUBLIC_KEY=
EPOINT_PRIVATE_KEY=
EPOINT_INTERFACE_LANG=
EPOINT_SUCCESS_REDIRECT_URL=
EPOINT_FAILED_REDIRECT_URL=
```
