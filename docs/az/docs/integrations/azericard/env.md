# Mühit dəyişənləri

## Haqqında

Aşağıdakı cədvəldə bütün mühit dəyişənləri ilə tanış ola bilərsiniz.

| Dəyişənin adı              | Məcburi?                  |                                     Mənası                                     | Default dəyəri |
| :------------------------- | :------------------------ | :----------------------------------------------------------------------------: | :------------: |
| `AZERICARD_KEY_FILE_PATH`  | :fontawesome-solid-check: |                    AzeriCard-dan alınmış açar faylının yeri                    |      `-`       |
| `AZERICARD_MERCHANT_ID`    | :fontawesome-solid-check: |                   Terminal ID (AzeriCard tərəfindən verilir)                   |      `-`       |
| `AZERICARD_MERCHANT_NAME`  | :fontawesome-solid-check: |   Satıcının (merchant) adı (kart istifadəçisinin anladığı formada olmalıdır)   |      `-`       |
| `AZERICARD_MERCHANT_URL`   | :fontawesome-solid-check: |                            Satıcının web site URL-ı                            |      `-`       |
| `AZERICARD_CALLBACK_URL`   | :fontawesome-solid-check: | Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL |      `-`       |
| `AZERICARD_INTERFACE_LANG` | :x:                       |                                   Dil seçimi                                   |      `az`      |

## .env template

```text
AZERICARD_KEY_FILE_PATH=
AZERICARD_MERCHANT_ID=
AZERICARD_MERCHANT_NAME=
AZERICARD_MERCHANT_URL=
AZERICARD_CALLBACK_URL=
AZERICARD_INTERFACE_LANG=
```
