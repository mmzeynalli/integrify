# LSIM

## Rəsmi Dokumentasiya (v2024.11.22) { #official-documentation }

[İngliscə](https://mmzeynalli.notion.site/LSIM-1974f14f727e8029a3f5f9e4e556afe3?pvs=74)

## Sorğular listi { #list-of-requests }

### Tək SMS sorğuları { #single-sms-requests }

| Sorğu metodu                                                                               | Məqsəd                                            |          LSIM API          |
| :----------------------------------------------------------------------------------------- | :------------------------------------------------ | :------------------------: |
| [`send_sms_get`][integrify.lsim.single.client.LSIMSingleSMSClientClass.send_sms_get]       | GET sorğusu ilə email göndərilmə                  |    `/quicksms/v1/send`     |
| [`send_sms_post`][integrify.lsim.single.client.LSIMSingleSMSClientClass.send_sms_post]     | POST sorğusu ilə email göndərilmə                 |  `/quicksms/v1/smssender`  |
| [`check_balance`][integrify.lsim.single.client.LSIMSingleSMSClientClass.check_balance]     | Balansı yoxlamaq                                  |   `/quicksms/v1/balance`   |
| [`get_report_get`][integrify.lsim.single.client.LSIMSingleSMSClientClass.get_report_get]   | GET sorğusu ilə göndərilmiş SMS haqqında məlumat  |   `/quicksms/v1/report`    |
| [`get_report_post`][integrify.lsim.single.client.LSIMSingleSMSClientClass.get_report_post] | POST sorğusu ilə göndərilmiş SMS haqqında məlumat | `/quicksms/v1/smsreporter` |

### Toplu SMS sorğuları { #bulk-sms-requests }

| Sorğu metodu                                                                                                         | Məqsəd                                              |   LSIM API   |
| :------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- | :----------: |
| [`bulk_send_one_message`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.bulk_send_one_message]                   | Toplu şəkildə hamıya eyni mesaj göndərilmə          | `/smxml/api` |
| [`bulk_send_different_messages`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.bulk_send_different_messages]     | Toplu şəkildə hərəyə fərqli mesaj göndərilmə        | `/smxml/api` |
| [`get_report`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.get_report]                                         | Toplu göndərilmiş SMS-in reportu                    | `/smxml/api` |
| [`get_detailed_report`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.get_detailed_report]                       | Toplu göndərilmiş SMS-in detallı reportu            | `/smxml/api` |
| [`get_detailed_report_with_dates`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.get_detailed_report_with_dates] | Toplu göndərilmiş SMS-in detallı və tarixli reportu | `/smxml/api` |
| [`check_balance`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.check_balance]                                   | Balansı yoxlamaq                                    | `/smxml/api` |
