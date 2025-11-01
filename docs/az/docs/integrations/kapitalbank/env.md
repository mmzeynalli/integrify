# Mühit dəyişənləri

## Haqqında

Aşağıdakı cədvəldə bütün mühit dəyişənləri ilə tanış ola bilərsiniz.

| Dəyişənin adı            | Məcburi?                  | Mənası                                                       | Default dəyəri |
| ------------------------ | ------------------------- | ------------------------------------------------------------ | -------------- |
| `KAPITAL_USERNAME`       | :fontawesome-solid-check: | KapitalBank API autentifikasiyası üçün Username              | `-`            |
| `KAPITAL_PASSWORD`       | :fontawesome-solid-check: | KapitalBank API autentifikasiyası üçün Password              | `-`            |
| `KAPITAL_ENV`            | :fontawesome-solid-check: | Environment mode (`test` və ya `prod`)                       | `test`         |
| `KAPITAL_INTERFACE_LANG` | :x:                       | KapitalBank ödəniş interfeysinin dili                        | `az`           |
| `KAPITAL_REDIRECT_URL`   | :x:                       | Sorğular uğurlu/uğursuz olduqda, spesifik URL-ə yönləndirmək | `-`            |

## .env template

```text
KAPITAL_USERNAME=
KAPITAL_PASSWORD=
KAPITAL_ENV=
KAPITAL_INTERFACE_LANG=
KAPITAL_REDIRECT_URL=
```
