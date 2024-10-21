# Kod arxitekturası

## Bünovrə

İlk öncə sorğunun hansı prosesdən keçdiyinə nəzər salaq. Nəzərə alaq ki, hal hazırda KapitalBank supportu olmasa da, əlavə edilib ki, iki fərqli sistem bir yerdə necə mövcud olacağı daha yaxşı göstərilsin.

```mermaid
graph TD;
    classDef classAPI  ;
    classDef classHandler  ;
    classDef classExecutor  ;

    subgraph API Support
        APIClient
        EPointClientClass
        KapitalAPISupport
    end

    subgraph API Handlers
        APIPayloadHandler
        epoint.PaymentPayloadHandler
        kapital.PaymentPayloadHandler
    end

    subgraph Request Execution
        APIExecutor
        httpx.Client
        httpx.AsyncClient
    end

    APIClient --> EPointClientClass
    APIClient --> KapitalAPISupport
    APIPayloadHandler --> epoint.PaymentPayloadHandler
    APIPayloadHandler --> kapital.PaymentPayloadHandler
    httpx.Client --> APIExecutor 
    httpx.AsyncClient --> APIExecutor

    EPointClientClass -->|add_url & add_handler| APIClient
    KapitalAPISupport -->|add_url & add_handler| APIClient
    epoint.PaymentPayloadHandler -->|handle_request & handle_response| APIPayloadHandler
    kapital.PaymentPayloadHandler -->|handle_request & handle_response| APIPayloadHandler
    APIExecutor -->|sync_req| httpx.Client
    APIExecutor -->|async_req| httpx.AsyncClient
```

Bu strukturu nəzərdən keçisəniz, sorğunun hazırlanıb, göndərilib, cavabın parse və
validate olunmasını bu diaqramdan anlaya bilərsiniz.
