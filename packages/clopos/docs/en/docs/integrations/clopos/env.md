# Env Variables

## About

To use these requests you need to set these environmental variables:

| Variable Name          | Purpose                                            | Header equivalent | Default Value |
| :--------------------- | :------------------------------------------------- | ----------------- | :-----------: |
| `CLOPOS_CLIENT_ID`     | Client ID given by Clopos (used only for auth)     | `-`               |      `-`      |
| `CLOPOS_CLIENT_SECRET` | Client Secret given by Clopos (used only for auth) | `-`               |      `-`      |
| `CLOPOS_BRAND`         | Brand that you want to request                     | `x-brand`         |      `-`      |
| `CLOPOS_VENUE_ID`      | Venue/Branch id that you want to request           | `x-venue`         |      `-`      |

Note that, these values **MIGHT** be unset. In this case, you should send it in header of each request. Let's say you want to request menu categories of two venues separately:

```python
# CLOPOS_CLIENT_ID, CLOPOS_CLIENT_SECRET and CLOPOS_BRAND have been set as env variables
from integrify.clopos.client import CloposClient

venue1_id=1
venue2_id=2

token1 = CloposClient.auth(venue_id=venue1_id).body.token
categories1 = CloposClient.get_categories(headers={'x-token': token1, 'x-venue': venue1_id}).body.data

token2 = CloposClient.auth(venue_id=venue2_id).body.token
categories2 = CloposClient.get_categories(headers={'x-token': token1, 'x-venue': venue2_id}).body.data
```

If you want to fetch categories from different brand, just manually add `x-brand` to the header.

For auth, instead of headers, you will just send these as params.

```python
# No env was set
from integrify.clopos.client import CloposClient

client_id='eNUKI04aYJRU6TBhh5bwUrvmEORgQoxM'
client_secret='dqYkWUpDjzvKOgbP3ar8tSNKJbwMyYe1V5R7DHClfSNYkap5C5XxRA6PmzoPv1I2'
brand='openapitest'
venue_id='1'

token = CloposClient.auth(client_id=client_id, client_secret=client_secret, brand=brand, venue_id=venue_id).body.token
```

## Test Credentials

| **Variable**    | **Value**                                       |
| --------------- | ----------------------------------------------- |
| `client_id`     | `6553676e0d265ac837e8f79fc`                     |
| `client_secret` | `seCyF_4vja6yddQxE2PlerET0Uhy8ASbJ36hO68PD3JM=` |
| `brand`         | `openapitest`                                   |
| `venue_id`      | `1`                                             |

## .env template

```text
CLOPOS_CLIENT_ID=
CLOPOS_CLIENT_SECRET=
CLOPOS_BRAND=
CLOPOS_VENUE_ID=
```
