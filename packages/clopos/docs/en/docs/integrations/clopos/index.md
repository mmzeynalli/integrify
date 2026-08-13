# Clopos

???+ warning
    To use these requests you need to set correct environmental variables. Read more about them [here](./env.md).

## Official Documentation (v1.0.1) { #official-documentation }

[English](https://developer.clopos.com/)

## List of requests  { #list-of-requests }

| Request function      | Purpose                     |         Clopos API          |
| :-------------------- | :-------------------------- | :-------------------------: |
| `auth`                | Authenticate, get token     |      `/open-api/auth`       |
| `get_venues`          | Get list of venues/branches |     `/open-api/venues`      |
| `get_users`           | Get list of users           |      `/open-api/users`      |
| `get_user_by_id`      | Get user by id              |   `/open-api/users/{id}`    |
| `get_customers`       | Get list of customers       |    `/open-api/customers`    |
| `get_customer_by_id`  | Get customer by id          | `/open-api/customers/{id}`  |
| `get_customer_groups` | Get list of customer groups | `/open-api/customer-group`  |
| `get_categories`      | Get list of menu categories |   `/open-api/categories`    |
| `get_category_by_id`  | Get menu category by id     | `/open-api/categories/{id}` |
| `get_stations`        | Get list of stations        |    `/open-api/stations`     |
| `get_station_by_id`   | Get station by id           |  `/open-api/stations/{id}`  |
| `get_products`        | Get list of products        |    `/open-api/products`     |
| `get_product_by_id`   | Get product by id           |  `/open-api/products/{id}`  |
| `get_sale_types`      | Get list of sale types      |   `/open-api/sale-types`    |
| `get_payment_methods` | Get list of payment methods | `/open-api/payment-methods` |
| `get_orders`          | Get list of orders          |     `/open-api/orders`      |
| `get_order_by_id`     | Get order by id             |   `/open-api/orders/{id}`   |
| `create_order`        | Create new order            |     `/open-api/orders`      |
| `get_receipts`        | Get list of receipts        |    `/open-api/receipts`     |
| `get_receipt_by_id`   | Get receipt by id           |  `/open-api/receipts/{id}`  |
| `create_receipt`      | Create a new receipt        |    `/open-api/receipts`     |
| `delete_receipt`      | Delete a receipt            |  `/open-api/receipts/{id}`  |

## Usage

First of all, one should use `auth` method to acquire token. This token is used in all future API calls. Bear in mind that, these tokens are active for one hour. After one hour, token automatically expires, and you should again use `auth` to get a new one. This workflow responsibility falls on user.

After acquiring token, for any subsequent call, just use `headers={'token': token}` argument for any call. For other arguments that specific APIs might need, please check [API reference](api-reference/client.md).
