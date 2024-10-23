# Kod arxitekturası

## Bünovrə { #base }

İlk öncə sorğunun hansı prosesdən keçdiyinə nəzər salaq. Nəzərə alaq ki, hal hazırda KapitalBank supportu olmasa da, əlavə edilib ki, iki fərqli sistem bir yerdə necə mövcud olacağı daha yaxşı göstərilsin.

```mermaid
graph TD;
    classDef classAPI  ;
    classDef classHandler  ;
    classDef classExecutor  ;

    subgraph Request Execution
        APIExecutor
        httpx.Client
        httpx.AsyncClient
    end

    subgraph API Handlers
        APIPayloadHandler
        epoint.PaymentPayloadHandler
        kapital.PaymentPayloadHandler
    end

    subgraph API Support
        APIClient
        EPointClientClass
        KapitalAPISupport
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

## Axın { #code-flow }

Bu strukturu nəzərdən keçisəniz, sorğunun hazırlanıb, göndərilib, cavabın parse və
validate olunmasını bu diaqramdan anlaya bilərsiniz.

```mermaid
---
title: EPointClient `pay` sorğusunun axını
config:
  theme: forest
---
sequenceDiagram;

participant U as User
participant C as EPointClientClass
participant H as epoint.PaymentPayloadHandler
participant E as APIExecutor 

U ->> C: .pay(data)
Note over C: get_url

C <<->> H: get_handler
C <<->> E: get_request_function
C ->> E: execute_request
E <<->> H: handle_request (prepare data)
Note over E: send request
E <<->> H: handle_response
E ->> C: return
C ->> U: return
```

## Yeni inteqrasiya { #new-integration }

Yeni inteqrasiya əlavə etmək istəyirsinizsə, zəhmət olmazsa [bu mərhələləri](./contributing.md) icra etdiyinizdən əmin olun. Kod yazmaq hissəyə gəldikdə isə, növbəti mərhələləri izləyin:

### 0. File strukturu { #file-structure }

Mövcud fayl strukturunu mimikləyə və ya sadəcə `make new-integration name=new-integration` kommandını icra edə bilərsiniz. Gözlənilən struktur budur:

```text
integrify
├── epoint
└── new-integration
    ├── __init__.py
    ├── client.py
    ├── env.py
    ├── handlers.py
    └── schemas
        ├── __init__.py
        ├── request.py
        └── response.py
```

### 1. Hazırlıq və constant-lar { #preparation-and-constants }

İlk öncə istifadə edəcəyiniz API-ləri bir enum constantları kimi yığın.
