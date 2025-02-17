# LSIM

## Rəsmi Dokumentasiya (v2024.11.22) { #official-documentation }

[İngliscə](https://mmzeynalli.notion.site/LSIM-1974f14f727e8029a3f5f9e4e556afe3?pvs=74)

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                               | Məqsəd                              |          LSIM API          |
| :------------------------------------------------------------------------- | :---------------------------------- | :------------------------: |
| [`send_sms_get`][integrify.lsim.client.LSIMClientClass.send_sms_get]       | GET sorğusu ilə email göndərilmə    |    `/quicksms/v1/send`     |
| [`send_sms_post`][integrify.lsim.client.LSIMClientClass.send_sms_post]     | POST sorğusu ilə email göndərilmə   |  `/quicksms/v1/smssender`  |
| [`check_balance`][integrify.lsim.client.LSIMClientClass.check_balance]     | Ödəniş olmadan kartı yadda saxlamaq |   `/quicksms/v1/balance`   |
| [`get_report_get`][integrify.lsim.client.LSIMClientClass.get_report_get]   | Saxlanılan kartla ödəniş            |   `/quicksms/v1/report`    |
| [`get_report_post`][integrify.lsim.client.LSIMClientClass.get_report_post] | Ödəniş etmə və kartı yadda saxlamaq | `/quicksms/v1/smsreporter` |
