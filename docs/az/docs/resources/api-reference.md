# Daxili kod strukturunun API Reference-i

## API

::: integrify.api.APIClient
    handler: python
    options:
      members:
        - __init__
        - add_url
        - set_default_handler
        - add_handler

::: integrify.api.APIPayloadHandler
    handler: python
    options:
      members:
        - __init__
        - headers
        - pre_handle_payload
        - handle_payload
        - post_handle_payload
        - handle_request
        - handle_response

::: integrify.api.APIExecutor
    handler: python
    options:
      members:
        - __init__
        - request_function
        - sync_req
        - async_req

## Schema

::: integrify.schemas.APIResponse
    handler: python

::: integrify.schemas.PayloadBaseModel
    handler: python
    options:
      members:
        - from_args
