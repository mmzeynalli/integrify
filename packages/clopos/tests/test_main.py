# Main aspects of Clopos: Product, Sales, Order and Receipt
from typing import TYPE_CHECKING

from pytest_mock import MockerFixture

from integrify.clopos.schemas.common.response import ErrorResponse, ObjectResponse
from integrify.clopos.schemas.enums import OrderStatus, ProductType
from integrify.clopos.schemas.orders.object import Order
from integrify.clopos.schemas.price_lists.object import PriceList, PriceListPrice
from integrify.clopos.schemas.products.object import Product, StopList
from integrify.clopos.schemas.receipts.object import Receipt, ReceiptStockOperation
from integrify.schemas import APIResponse
from tests.client import CloposTestClientClass
from tests.conftest import requires_env

if TYPE_CHECKING:
    from tests.client import CloposTestClientClass


@requires_env()
def test_get_products(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_products()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Product)


@requires_env()
def test_get_products_filters(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_products(
        limit=100,
        filters={
            'type': [ProductType.GOODS, ProductType.DISH, ProductType.TIMER],
            'category_id': [1, 3],
            'station_id': [1, 2],
            'tags': [1, 2],
            'giftable': True,
            'discountable': True,
            'inventory_behavior': 3,
            'have_ingredients': True,
            'sold_by_portion': True,
            'has_variants': True,
            'has_modifiers': True,
            'has_barcode': True,
            'has_service_charge': True,
        },
    )

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Product)

    assert all(
        p.type in [ProductType.GOODS, ProductType.DISH, ProductType.TIMER]
        # and p.category_id in [1, 3]
        # and p.station_id in [1, 2]
        # and p.tags in [1, 2]
        # and p.giftable
        # and p.discountable
        # and p.inventory_behavior == 3
        # and p.modifications
        # and p.barcode
        for p in resp.body.data
    )


@requires_env()
def test_get_product_goods_with_variants(
    authed_client: 'CloposTestClientClass',
    mocker: MockerFixture,
    clopos_product_goods_with_variations_response,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=clopos_product_goods_with_variations_response,
    ):
        resp = authed_client.get_product_by_id(419)

        assert resp.ok
        assert resp.body.success
        assert isinstance(resp.body.data, Product)

        assert resp.body.data.id == 419

        assert resp.body.data.type == ProductType.GOODS
        assert resp.body.data.modifications
        assert not resp.body.data.setting
        assert not resp.body.data.modificator_groups


@requires_env()
def test_get_product_dish_without_variants(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_product_by_id(139)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Product)

    assert resp.body.data.id == 139

    assert resp.body.data.type == ProductType.DISH
    assert not resp.body.data.modificator_groups
    assert not resp.body.data.modifications
    assert not resp.body.data.setting


@requires_env()
def test_get_product_dish_with_variants(
    authed_client: 'CloposTestClientClass',
    mocker: MockerFixture,
    clopos_product_dish_with_modifiers,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=clopos_product_dish_with_modifiers,
    ):
        resp = authed_client.get_product_by_id(1)

        assert resp.ok
        assert resp.body.success
        assert isinstance(resp.body.data, Product)

        assert resp.body.data.id == 1

        assert resp.body.data.type == ProductType.DISH
        assert resp.body.data.modificator_groups
        assert not resp.body.data.setting
        assert not resp.body.data.modifications


@requires_env()
def test_get_product_timer(
    authed_client: 'CloposTestClientClass',
    mocker: MockerFixture,
    clopos_product_timer_response,
):
    with mocker.patch(
        'httpx.Client.request',
        return_value=clopos_product_timer_response,
    ):
        resp = authed_client.get_product_by_id(407)

        assert resp.ok
        assert resp.body.success
        assert isinstance(resp.body.data, Product)

        assert resp.body.data.id == 407

        assert resp.body.data.type == ProductType.TIMER
        assert resp.body.data.setting
        assert not resp.body.data.modificator_groups
        assert not resp.body.data.modifications


@requires_env()
def test_get_product_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_product_by_id(1000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert (
        resp.body.error[0].message
        == 'No query results for model [App\\Models\\Client\\Product] 1000'
    )
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_get_stop_list(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_stop_list()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)

    if len(resp.body.data) > 0:
        assert isinstance(resp.body.data[0], StopList)


@requires_env()
def test_get_orders(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_orders()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Order)


@requires_env()
def test_create_order(new_order_resp: APIResponse[ObjectResponse[Order]]):
    assert new_order_resp.ok
    assert isinstance(new_order_resp.body.data, Order)


@requires_env()
def test_get_orders_query_status(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_orders(status=OrderStatus.RECEIVED)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Order)

    # assert all(o.status == OrderStatus.RECEIVED for o in resp.body.data)


@requires_env()
def test_get_order_by_id(authed_client: 'CloposTestClientClass', new_order_object: Order):
    resp = authed_client.get_order_by_id(new_order_object.id)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Order)

    assert resp.body.data.id == new_order_object.id


@requires_env()
def test_get_order_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_order_by_id(1000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert (
        resp.body.error[0].message
        == 'No query results for model [App\\Models\\Client\\ServiceNotification] 1000'
    )
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_update_order(authed_client: 'CloposTestClientClass', new_order_object: Order):
    resp = authed_client.get_order_by_id(new_order_object.id)

    assert resp.ok

    resp = authed_client.update_order(id=new_order_object.id, status=OrderStatus.READY)

    assert resp.ok
    assert resp.body.data.status == OrderStatus.READY

    resp = authed_client.get_order_by_id(new_order_object.id)

    assert resp.ok
    assert resp.body.data.status == OrderStatus.READY


@requires_env()
def test_get_receipts(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_receipts()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)
    assert isinstance(resp.body.data[0], Receipt)


@requires_env()
def test_get_receipt_by_id_wrong_id(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_receipt_by_id(1_000_000_000)

    assert not resp.ok
    assert isinstance(resp.body, ErrorResponse)
    assert not resp.body.success

    assert (
        resp.body.error[0].message
        == 'No query results for model [App\\Models\\Client\\Receipt] 1000000000'
    )
    assert resp.body.error[0].http_code == 404
    assert resp.body.error[0].type == 'server_side'
    assert resp.body.error[0].exception == 'NotFoundHttpException'


@requires_env()
def test_get_receipt_by_id(authed_client: 'CloposTestClientClass', new_receipt_object: Receipt):
    resp = authed_client.get_receipt_by_id(new_receipt_object.id)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Receipt)

    assert resp.body.data.id == new_receipt_object.id


@requires_env()
def test_update_closed_receipt(authed_client: 'CloposTestClientClass', new_receipt_object: Receipt):
    resp = authed_client.get_receipt_by_id(new_receipt_object.id)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, Receipt)
    assert resp.body.data.status != OrderStatus.NEW

    resp = authed_client.update_closed_receipt(
        id=new_receipt_object.id,
        order_status=OrderStatus.NEW,
    )

    assert resp.ok
    assert isinstance(resp.body.data, Receipt)
    assert resp.body.data.order_status == OrderStatus.NEW


@requires_env()
def test_get_receipt_stock_operations(
    authed_client: 'CloposTestClientClass', new_receipt_object: Receipt
):
    resp = authed_client.get_receipt_stock_operations(new_receipt_object.id)

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)

    if len(resp.body.data) > 0:
        assert isinstance(resp.body.data[0], ReceiptStockOperation)


@requires_env()
def test_get_price_lists(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_price_lists()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)

    if len(resp.body.data) > 0:
        assert isinstance(resp.body.data[0], PriceList)


@requires_env()
def test_get_price_list_prices(authed_client: 'CloposTestClientClass'):
    resp = authed_client.get_price_list_prices()

    assert resp.ok
    assert resp.body.success
    assert isinstance(resp.body.data, list)

    if len(resp.body.data) > 0:
        assert isinstance(resp.body.data[0], PriceListPrice)
