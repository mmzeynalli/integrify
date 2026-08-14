from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any, Generic, overload
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse, _Async, _Mode, _Sync
from integrify.kapitalbank import env
from integrify.kapitalbank.handlers import (
    ClearingOrderPayloadHandler,
    CreateOrderPayloadHandler,
    DetailedOrderInformationPayloadHandler,
    FullReverseOrderPayloadHandler,
    LinkCardTokenPayloadHandler,
    OrderInformationPayloadHandler,
    OrderWithSavedCardPayloadHandler,
    PartialReverseOrderPayloadHandler,
    PayAndSaveCardPayloadHandler,
    ProcessPaymentWithSavedCardPayloadHandler,
    RefundOrderPayloadHandler,
    SaveCardPayloadHandler,
)
from integrify.kapitalbank.schemas.response import (
    BaseResponseSchema,
    ClearingOrderResponseSchema,
    CreateOrderResponseSchema,
    DetailedOrderInformationResponseSchema,
    FullReverseOrderResponseSchema,
    LinkCardTokenResponseSchema,
    OrderInformationResponseSchema,
    PartialReverseOrderResponseSchema,
    ProcessPaymentWithSavedCardResponseSchema,
    RefundOrderResponseSchema,
)
from integrify.utils import UNSET as _UNSET
from integrify.utils import Unset as Unsettable

__all__ = ['KapitalClientClass']


class KapitalClientClass(APIClient, Generic[_Mode]):
    def __init__(
        self,
        name='Kapital',
        base_url=env.API.BASE_URL,
        default_handler=None,
        sync=True,
        dry=False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url('create_order', env.API.ORDER, verb='POST')
        self.add_handler('create_order', CreateOrderPayloadHandler)

        self.add_url('get_order_information', env.API.GET_ORDER, verb='GET')
        self.add_handler('get_order_information', OrderInformationPayloadHandler)

        self.add_url('get_detailed_order_info', env.API.GET_DETAILED_ORDER, verb='GET')
        self.add_handler('get_detailed_order_info', DetailedOrderInformationPayloadHandler)

        self.add_url('refund_order', env.API.ORDER_EXECUTION, verb='POST')
        self.add_handler('refund_order', RefundOrderPayloadHandler)

        self.add_url('save_card', env.API.ORDER, verb='POST')
        self.add_handler('save_card', SaveCardPayloadHandler)

        self.add_url('pay_and_save_card', env.API.ORDER, verb='POST')
        self.add_handler('pay_and_save_card', PayAndSaveCardPayloadHandler)

        self.add_url('full_reverse_order', env.API.ORDER_EXECUTION, verb='POST')
        self.add_handler('full_reverse_order', FullReverseOrderPayloadHandler)

        self.add_url('clearing_order', env.API.ORDER_EXECUTION, verb='POST')
        self.add_handler('clearing_order', ClearingOrderPayloadHandler)

        self.add_url('partial_reverse_order', env.API.ORDER_EXECUTION, verb='POST')
        self.add_handler('partial_reverse_order', PartialReverseOrderPayloadHandler)

        self.add_url('order_with_saved_card', env.API.ORDER, verb='POST')
        self.add_handler(
            'order_with_saved_card',
            OrderWithSavedCardPayloadHandler,
        )

        self.add_url('link_card_token', env.API.ORDER_LINK_CARD_TOKEN, verb='POST')
        self.add_handler('link_card_token', LinkCardTokenPayloadHandler)

        self.add_url(
            'process_payment_with_saved_card',
            env.API.PROCESS_PAYMENT_WITH_SAVED_CARD,
            verb='POST',
        )
        self.add_handler(
            'process_payment_with_saved_card',
            ProcessPaymentWithSavedCardPayloadHandler,
        )

    # All other endpoints were tested separately
    def pay_with_saved_card(  # pragma: no cover
        self,
        token: int,
        amount: Numeric,
        currency: str,
        description: Unsettable[str] = _UNSET,
    ) -> APIResponse[BaseResponseSchema[ProcessPaymentWithSavedCardResponseSchema]]:
        """
        Yadda saxlanmış kartdan ödəniş etmək üçün sorğu

        **Endpoint** /api/order

        Example:
        ```python
        from integrify.kapitalbank import KapitalRequest

        KapitalRequest.pay_with_saved_card(123456, 1.0, "AZN", "Test payment")
        ```

        **Cavab formatı: [`BaseResponseSchema[ProcessPaymentWithSavedCardResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

        Bu sorğunu göndərdikdə, cavab olaraq ödənişin təsdiq edilməsi haqda məlumat əldə edə bilərsiniz.

        Args:
            token: Kart tokeni.
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """  # noqa: E501
        # Bu köməkçi metod nəticələri sinxron istifadə edir (`.body.data`), ona görə
        # yalnız sync klient üçün mənalıdır. Alt-metodların overload-ları `self`-in
        # `KapitalClientClass[_Sync]` olmasını tələb etdiyi üçün `self`-i sync kimi cast edirik.
        sync_self: KapitalClientClass[_Sync] = self

        order_response = sync_self.order_with_saved_card(  # pylint: disable=assignment-from-no-return
            amount=amount,
            currency=currency,
            description=description,
        )

        assert order_response.body and order_response.body.data

        order_id = order_response.body.data.id
        password = order_response.body.data.password

        sync_self.link_card_token(
            token=token,
            order_id=order_id,
            password=password,
        )

        return sync_self.process_payment_with_saved_card(
            amount=amount,
            order_id=order_id,
            password=password,
        )

    if TYPE_CHECKING:
        # pylint: disable=missing-function-docstring,unused-argument

        @overload
        def create_order(
            self: 'KapitalClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Ödəniş sorğusu

            **Endpoint** /api/order

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.create_order(
                amount=10.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını get_detailed_order_info() funksiyandan istifadə edərək əldə edə bilərsiz.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def create_order(
            self: 'KapitalClientClass[_Async]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]]: ...
        def create_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_order_information(
            self: 'KapitalClientClass[_Sync]', order_id: int
        ) -> APIResponse[BaseResponseSchema[OrderInformationResponseSchema]]:
            """Ödəniş haqda qısa məlumat əldə etmək üçün sorğu

            **Endpoint** /api/order/{order_id}

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.get_order_information(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[OrderInformationResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödəniş haqda qısa məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        @overload
        def get_order_information(
            self: 'KapitalClientClass[_Async]', order_id: int
        ) -> Coroutine[
            Any, Any, APIResponse[BaseResponseSchema[OrderInformationResponseSchema]]
        ]: ...
        def get_order_information(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_detailed_order_info(
            self: 'KapitalClientClass[_Sync]', order_id: int
        ) -> APIResponse[BaseResponseSchema[DetailedOrderInformationResponseSchema]]:
            """Ödəniş haqda detallı məlumat əldə etmək üçün sorğu

            **Endpoint** /api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.get_detailed_order_info(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[DetailedOrderInformationResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin detallı məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        @overload
        def get_detailed_order_info(
            self: 'KapitalClientClass[_Async]', order_id: int
        ) -> Coroutine[
            Any, Any, APIResponse[BaseResponseSchema[DetailedOrderInformationResponseSchema]]
        ]: ...
        def get_detailed_order_info(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def refund_order(
            self: 'KapitalClientClass[_Sync]',
            order_id: int,
            amount: Numeric,
        ) -> APIResponse[BaseResponseSchema[RefundOrderResponseSchema]]:
            """Geri ödəniş sorğusu

            **Endpoint** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.refund_order(
                order_id=123456,
                amount=10.0,
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[RefundOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğu ilə əvvəlki ödənişi geri ödəmək üçün istifadə edə bilərsiniz.
            Cavab olaraq ödənişin detallarını əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
                amount: Geri ödəniş miqdarı. Numerik dəyər.
            """  # noqa: E501

        @overload
        def refund_order(
            self: 'KapitalClientClass[_Async]',
            order_id: int,
            amount: Numeric,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[RefundOrderResponseSchema]]]: ...
        def refund_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def save_card(
            self: 'KapitalClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Kartı saxlamaq üçün ödəniş sorğusu

            **Endpoint** /api/order

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.save_card(
                amount=1.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını get_detailed_order_info() funksiyandan istifadə edərək əldə edə bilərsiz.
            Həmin detallarda storedTokens key-i altındaki tokenləri saxlayaraq, sonrakı ödənişlərdə bu tokenləri
            istifadə edə bilərsiniz.

            `response.body.data.stored_tokens[0].id` ilə tokeni əldə edə bilərsiniz.
            """  # noqa: E501

        @overload
        def save_card(
            self: 'KapitalClientClass[_Async]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]]: ...
        def save_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def pay_and_save_card(
            self: 'KapitalClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu

            **Endpoint** /api/order

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.pay_and_save_card(
                amount=1.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını get_detailed_order_info() funksiyandan istifadə edərək əldə edə bilərsiz.
            Həmin detallarda storedTokens key-i altındaki tokenləri saxlayaraq, sonrakı ödənişlərdə bu tokenləri
            istifadə edə bilərsiniz.

            `response.body.data.stored_tokens[0].id` ilə tokeni əldə edə bilərsiniz.
            """  # noqa: E501

        @overload
        def pay_and_save_card(
            self: 'KapitalClientClass[_Async]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]]: ...
        def pay_and_save_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def full_reverse_order(
            self: 'KapitalClientClass[_Sync]',
            order_id: int,
        ) -> APIResponse[BaseResponseSchema[FullReverseOrderResponseSchema]]:
            """Ödənişi ləğv etmək üçün sorğu

            **Endpoint** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.full_reverse_order(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[FullReverseOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin ləğv edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani save_card() funksiyası ilə yaradılan ödənişlər üçün istifadə edə bilərsiniz.
            Kartın token-i saxladıqdan sonra həmin ödənişi qaytarmaq üçün istifade etmək olar.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        @overload
        def full_reverse_order(
            self: 'KapitalClientClass[_Async]',
            order_id: int,
        ) -> Coroutine[
            Any, Any, APIResponse[BaseResponseSchema[FullReverseOrderResponseSchema]]
        ]: ...
        def full_reverse_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def clearing_order(
            self: 'KapitalClientClass[_Sync]',
            order_id: int,
            amount: Numeric,
        ) -> APIResponse[BaseResponseSchema[ClearingOrderResponseSchema]]:
            """Ödənişin təsdiq edilməsi üçün sorğu

            **Endpoint** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.clearing_order(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[ClearingOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin təsdiq edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani save_card() funksiyası ilə yaradılan ödənişlər üçün istifadə edə bilərsiniz.
            Preauthorization əməliyyatının ikinci mərhələsi üçün.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        @overload
        def clearing_order(
            self: 'KapitalClientClass[_Async]',
            order_id: int,
            amount: Numeric,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[ClearingOrderResponseSchema]]]: ...
        def clearing_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def partial_reverse_order(
            self: 'KapitalClientClass[_Sync]',
            order_id: int,
            amount: Numeric,
        ) -> APIResponse[BaseResponseSchema[PartialReverseOrderResponseSchema]]:
            """Ödənişin hissəsini ləğv etmək üçün sorğu

            **Endpoint** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapitalbank import KapitalRequest

            KapitalRequest.partial_reverse_order(order_id=123456, amount=5.0)
            ```

            **Cavab formatı: [`BaseResponseSchema[PartialReverseOrderResponseSchema]`][integrify.kapitalbank.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin ləğv edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani clearing_order() funksiyası ilə təsdiq edilmiş ödənişlər üçün istifadə edə bilərsiniz.
            İlkin məbləğdən az olan vəsaitləri qaytarmaq üçün istifadə olunur. Bir dəfə istifadə etmək olar.

            Args:
                order_id: Ödənişin ID-si.
                amount: Ləğv olunacaq miqdar. Numerik dəyər.
            """  # noqa: E501

        @overload
        def partial_reverse_order(
            self: 'KapitalClientClass[_Async]',
            order_id: int,
            amount: Numeric,
        ) -> Coroutine[
            Any, Any, APIResponse[BaseResponseSchema[PartialReverseOrderResponseSchema]]
        ]: ...
        def partial_reverse_order(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def order_with_saved_card(
            self: 'KapitalClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """
            Bu funksiya sadece KapitalClientClass daxilinde istifade olunur!

            **Endpoint** /api/order

            Bu funksiya pay_with_saved_card() funksiyasında istifadə olunur.
            Əsas məqsədi order_id və password dəyərlərini əldə etməkdir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def order_with_saved_card(
            self: 'KapitalClientClass[_Async]',
            amount: Numeric,
            currency: str,
            description: Unsettable[str] = _UNSET,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]]: ...
        def order_with_saved_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def link_card_token(
            self: 'KapitalClientClass[_Sync]',
            token: int,
            order_id: int,
            password: str,
        ) -> APIResponse[BaseResponseSchema[LinkCardTokenResponseSchema]]:
            """
            Bu funksiya sadece KapitalClientClass daxilinde istifade olunur!

            **Endpoint** /api/order/{order_id}/set-src-token?password={password}

            Bu funksiya pay_with_saved_card() funksiyasında istifadə olunur.
            Əsas məqsədi token-i həmin order üçün set etməkdir.

            Args:
                token: Kart tokeni.
                order_id: Ödənişin ID-si.
                password: Ödənişin passwordu.
            """  # noqa: E501

        @overload
        def link_card_token(
            self: 'KapitalClientClass[_Async]',
            token: int,
            order_id: int,
            password: str,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema[LinkCardTokenResponseSchema]]]: ...
        def link_card_token(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def process_payment_with_saved_card(
            self: 'KapitalClientClass[_Sync]',
            amount: Numeric,
            order_id: int,
            password: str,
        ) -> APIResponse[BaseResponseSchema[ProcessPaymentWithSavedCardResponseSchema]]:
            """
            Bu funksiya sadece KapitalClientClass daxilinde istifade olunur!

            **Endpoint** /api/order/{order_id}/exec-tran?password={password}

            Bu funksiya pay_with_saved_card() funksiyasında istifadə olunur.
            Əsas məqsədi ödənişi təsdiq etməkdir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                order_id: Ödənişin ID-si.
                password: Ödənişin password
            """  # noqa: E501

        @overload
        def process_payment_with_saved_card(
            self: 'KapitalClientClass[_Async]',
            amount: Numeric,
            order_id: int,
            password: str,
        ) -> Coroutine[
            Any, Any, APIResponse[BaseResponseSchema[ProcessPaymentWithSavedCardResponseSchema]]
        ]: ...
        def process_payment_with_saved_card(self, *args: Any, **kwds: Any) -> Any: ...


KapitalRequest: 'KapitalClientClass[_Sync]' = KapitalClientClass(sync=True)
KapitalAsyncRequest: 'KapitalClientClass[_Async]' = KapitalClientClass(sync=False)
