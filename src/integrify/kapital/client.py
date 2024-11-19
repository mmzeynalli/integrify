from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.kapital import env
from integrify.kapital.handlers import (
    ClearingOrderPayloadHandler,
    CreateOrderAndSaveCardPayloadHandler,
    CreateOrderForPayWithSavedCardPayloadHandler,
    CreateOrderPayloadHandler,
    DetailedOrderInformationPayloadHandler,
    ExecPayWithSavedCardPayloadHandler,
    FullReverseOrderPayloadHandler,
    OrderInformationPayloadHandler,
    PartialReverseOrderPayloadHandler,
    RefundOrderPayloadHandler,
    SaveCardPayloadHandler,
    SetSrcTokenPayloadHandler,
)
from integrify.kapital.schemas.response import (
    BaseResponseSchema,
    ClearingOrderResponseSchema,
    CreateOrderResponseSchema,
    DetailedOrderInformationResponseSchema,
    ExecPayWithSavedCardResponseSchema,
    FullReverseOrderResponseSchema,
    OrderInformationResponseSchema,
    PartialReverseOrderResponseSchema,
    RefundOrderResponseSchema,
    SetSrcTokenResponseSchema,
)

__all__ = ['KapitalClientClass']


class KapitalClientClass(APIClient):
    def __init__(self, sync: bool = True):
        super().__init__(name='Kapital', sync=sync)

        self.add_url(
            'create_order',
            env.API.CREATE_ORDER,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('create_order', CreateOrderPayloadHandler)

        self.add_url(
            'order_information',
            env.API.ORDER_INFORMATION,
            verb='GET',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('order_information', OrderInformationPayloadHandler)

        self.add_url(
            'detailed_order_information',
            env.API.DETAILED_ORDER_INFORMATION,
            verb='GET',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('detailed_order_information', DetailedOrderInformationPayloadHandler)

        self.add_url(
            'refund_order',
            env.API.REFUND_ORDER,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('refund_order', RefundOrderPayloadHandler)

        self.add_url(
            'save_card',
            env.API.SAVE_CARD,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('save_card', SaveCardPayloadHandler)

        self.add_url(
            'create_order_and_save_card',
            env.API.CREATE_ORDER_AND_SAVE_CARD,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('create_order_and_save_card', CreateOrderAndSaveCardPayloadHandler)

        self.add_url(
            'full_reverse_order',
            env.API.FULL_REVERSE_ORDER,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('full_reverse_order', FullReverseOrderPayloadHandler)

        self.add_url(
            'clearing_order',
            env.API.CLEARING_ORDER,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('clearing_order', ClearingOrderPayloadHandler)

        self.add_url(
            'partial_reverse_order',
            env.API.PARTIAL_REVERSE_ORDER,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('partial_reverse_order', PartialReverseOrderPayloadHandler)

        self.add_url(
            'create_order_for_pay_with_saved_card',
            env.API.CREATE_ORDER_FOR_PAY_WITH_SAVED_CARD,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler(
            'create_order_for_pay_with_saved_card',
            CreateOrderForPayWithSavedCardPayloadHandler,
        )

        self.add_url(
            'set_src_token',
            env.API.SET_SRC_TOKEN,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('set_src_token', SetSrcTokenPayloadHandler)

        self.add_url(
            'exec_pay_with_saved_card',
            env.API.EXEC_PAY_WITH_SAVED_CARD,
            verb='POST',
            base_url=env.API.get_base_url(env.KAPITAL_ENV),
        )
        self.add_handler('exec_pay_with_saved_card', ExecPayWithSavedCardPayloadHandler)

    def pay_with_saved_card(
        self,
        token: int,
        amount: Numeric,
        currency: str,
        description: Optional[str] = None,
        **extra: Any,
    ) -> APIResponse[BaseResponseSchema[ExecPayWithSavedCardResponseSchema]]:
        """
        Yadda saxlanmış kartdan ödəniş etmək üçün sorğu

        **Kapital** /api/order

        Example:
        ```python
        from integrify.kapital import KapitalRequest

        KapitalRequest.pay_with_saved_card(123456, 1.0, "AZN", "Test payment")
        ```

        **Cavab formatı: [`BaseResponseSchema[ExecPayWithSavedCardResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

        Bu sorğunu göndərdikdə, cavab olaraq ödənişin təsdiq edilməsi haqda məlumat əldə edə bilərsiniz.

        Args:
            token: Kart tokeni.
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """  # noqa: E501
        create_order_response = self.create_order_for_pay_with_saved_card(
            amount=amount, currency=currency, description=description, **extra
        )

        assert create_order_response.body and create_order_response.body.data

        order_id = create_order_response.body.data.id
        password = create_order_response.body.data.password

        self.set_src_token(token=token, order_id=order_id, password=password, **extra)

        return self.exec_pay_with_saved_card(
            amount=amount, order_id=order_id, password=password, **extra
        )

    if TYPE_CHECKING:

        def create_order(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Ödəniş sorğusu

            **Kapital** /api/order

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.create_order(
                amount=10.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını detailed_order_information() funksiyandan istifadə edərək əldə edə bilərsiz.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def order_information(
            self, order_id: int
        ) -> APIResponse[BaseResponseSchema[OrderInformationResponseSchema]]:
            """Ödəniş haqda qısa məlumat əldə etmək üçün sorğu

            **Kapital** /api/order/{order_id}

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.order_information(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[OrderInformationResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödəniş haqda qısa məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def detailed_order_information(
            self, order_id: int
        ) -> APIResponse[BaseResponseSchema[DetailedOrderInformationResponseSchema]]:
            """Ödəniş haqda detallı məlumat əldə etmək üçün sorğu

            **Kapital** /api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.detailed_order_information(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[DetailedOrderInformationResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin detallı məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def refund_order(
            self,
            order_id: int,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[RefundOrderResponseSchema]]:
            """Geri ödəniş sorğusu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.refund_order(
                order_id=123456,
                amount=10.0,
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[RefundOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğu ilə əvvəlki ödənişi geri ödəmək üçün istifadə edə bilərsiniz.
            Cavab olaraq ödənişin detallarını əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
                amount: Geri ödəniş miqdarı. Numerik dəyər.
            """  # noqa: E501

        def save_card(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Kartı saxlamaq üçün ödəniş sorğusu

            **Kapital** /api/order

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.save_card(
                amount=1.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını detailed_order_information() funksiyandan istifadə edərək əldə edə bilərsiz.
            Həmin detallarda storedTokens key-i altındaki tokenləri saxlayaraq, sonrakı ödənişlərdə bu tokenləri
            istifadə edə bilərsiniz.

            `response.body.data.stored_tokens[0].id` ilə tokeni əldə edə bilərsiniz.
            """  # noqa: E501

        def create_order_and_save_card(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu

            **Kapital** /api/order

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.pay_and_save_card(
                amount=1.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını detailed_order_information() funksiyandan istifadə edərək əldə edə bilərsiz.
            Həmin detallarda storedTokens key-i altındaki tokenləri saxlayaraq, sonrakı ödənişlərdə bu tokenləri
            istifadə edə bilərsiniz.

            `response.body.data.stored_tokens[0].id` ilə tokeni əldə edə bilərsiniz.
            """  # noqa: E501

        def full_reverse_order(
            self,
            order_id: int,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[FullReverseOrderResponseSchema]]:
            """Ödənişi ləğv etmək üçün sorğu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.full_reverse_order(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[FullReverseOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin ləğv edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani save_card() funksiyası ilə yaradılan ödənişlər üçün istifadə edə bilərsiniz.
            Kartın token-i saxladıqdan sonra həmin ödənişi qaytarmaq üçün istifade etmək olar.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def clearing_order(
            self,
            order_id: int,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[ClearingOrderResponseSchema]]:
            """Ödənişin təsdiq edilməsi üçün sorğu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.clearing_order(order_id=123456)
            ```

            **Cavab formatı: [`BaseResponseSchema[ClearingOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin təsdiq edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani save_card() funksiyası ilə yaradılan ödənişlər üçün istifadə edə bilərsiniz.
            Preauthorization əməliyyatının ikinci mərhələsi üçün.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def partial_reverse_order(
            self,
            order_id: int,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[PartialReverseOrderResponseSchema]]:
            """Ödənişin hissəsini ləğv etmək üçün sorğu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.partial_reverse_order(order_id=123456, amount=5.0)
            ```

            **Cavab formatı: [`BaseResponseSchema[PartialReverseOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin ləğv edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani clearing_order() funksiyası ilə təsdiq edilmiş ödənişlər üçün istifadə edə bilərsiniz.
            İlkin məbləğdən az olan vəsaitləri qaytarmaq üçün istifadə olunur. Bir dəfə istifadə etmək olar.

            Args:
                order_id: Ödənişin ID-si.
                amount: Ləğv olunacaq miqdar. Numerik dəyər.
            """  # noqa: E501

        def create_order_for_pay_with_saved_card(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """
            Bu funksiya sadece KapitalClientClass daxilinde istifade olunur!

            **Kapital** /api/order

            Bu funksiya pay_with_saved_card() funksiyasında istifadə olunur.
            Əsas məqsədi order_id və password dəyərlərini əldə etməkdir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def set_src_token(
            self, token: int, order_id: int, password: str, **extra: Any
        ) -> APIResponse[BaseResponseSchema[SetSrcTokenResponseSchema]]:
            """
            Bu funksiya sadece KapitalClientClass daxilinde istifade olunur!

            **Kapital** /api/order/{order_id}/set-src-token?password={password}

            Bu funksiya pay_with_saved_card() funksiyasında istifadə olunur.
            Əsas məqsədi token-i həmin order üçün set etməkdir.

            Args:
                token: Kart tokeni.
                order_id: Ödənişin ID-si.
                password: Ödənişin passwordu.
            """  # noqa: E501

        def exec_pay_with_saved_card(
            self, amount: Numeric, order_id: int, password: str, **extra: Any
        ) -> APIResponse[BaseResponseSchema[ExecPayWithSavedCardResponseSchema]]:
            """
            Bu funksiya sadece KapitalClientClass daxilinde istifade olunur!

            **Kapital** /api/order/{order_id}/exec-tran?password={password}

            Bu funksiya pay_with_saved_card() funksiyasında istifadə olunur.
            Əsas məqsədi ödənişi təsdiq etməkdir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                order_id: Ödənişin ID-si.
                password: Ödənişin password
            """  # noqa: E501


KapitalRequest = KapitalClientClass(sync=True)
KapitalAsyncRequest = KapitalClientClass(sync=False)
